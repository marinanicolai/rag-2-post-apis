
The cleanest repro is the **dummy plugin test** from last Saturday. It takes about 2 minutes, uses no real or sensitive data, and shows blocked versus allowed side by side. The Zscaler team can then match the exact timestamp in their logs.

**Before the meeting**, open PowerShell and make sure you're not running Claude with the DLP hooks active in that folder (they don't affect this test, but it keeps things clean).

**1. Create the dummy plugin** (one harmless file, one with "RESTRICTED FR"):

```powershell
$m = "C:\temp\mp-test"
New-Item -ItemType Directory -Force "$m\.claude-plugin", "$m\copytest\.claude-plugin", C:\temp\c4g-test | Out-Null
Set-Content "$m\.claude-plugin\marketplace.json" '{"name":"mp-test","owner":{"name":"test"},"plugins":[{"name":"copytest","source":"./copytest"}]}'
Set-Content "$m\copytest\.claude-plugin\plugin.json" '{"name":"copytest","version":"0.0.1"}'
Set-Content "$m\copytest\a.md" "hello"
Set-Content "$m\copytest\b.md" "Anything above RESTRICTED FR is denied."
cd C:\temp\c4g-test
claude plugin marketplace add C:\temp\mp-test
```

**2. Show the block** (note the time for their logs):

```powershell
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
claude plugin install copytest@mp-test --scope project
```

Expected: `EPERM: operation not permitted, copyfile 'C:\temp\mp-test\copytest\b.md' -> 'C:\Users\M3MXN08\.claude\plugins\cache\temp_local_…\b.md'`

**3. Show that the same copy works for PowerShell**, into the same folder Claude was writing to:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\plugins\cache\pstest" | Out-Null
Copy-Item C:\temp\mp-test\copytest\b.md "$env:USERPROFILE\.claude\plugins\cache\pstest\b.md"; "PowerShell copy ok: $(Test-Path $env:USERPROFILE\.claude\plugins\cache\pstest\b.md)"
```

**4. Show that it's the content, not the plugin:**

```powershell
Set-Content C:\temp\mp-test\copytest\b.md "Nothing special here."
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
claude plugin install copytest@mp-test --scope project
```

Expected: `Successfully installed plugin: copytest@mp-test`

**What to ask them:**

1. **Is it Zscaler that blocks this** (Zscaler endpoint DLP), or another agent such as Microsoft Purview? Give them the two timestamps from steps 2 and 4.
2. **Which policy or rule** fires: the dictionary or pattern that matches "RESTRICTED FR", and the process it targets (`claude.exe`).
3. **Can the exception be narrow:** only Claude, only the `inference-hook-dlp` plugin folder under `%USERPROFILE%\.claude\plugins\`, ideally tied to the approved release (0.2.1)?
4. **Do other level names trigger it too** (CONFIDENTIAL FR, RESTRICTED-CONTROLLED FR), and **does SSN-style test data** in files trigger it?
5. **The network side:** your desktop tests showed Zscaler blocking some SSN prompts ("Access denied") but not others. Is that expected?

**Cleanup after the meeting:**

```powershell
cd C:\temp\c4g-test
claude plugin uninstall copytest@mp-test --scope project
claude plugin marketplace remove mp-test
Remove-Item C:\temp\mp-test, "$env:USERPROFILE\.claude\plugins\cache\pstest" -Recurse -Force
```

If they want to see the **real plugin** fail too, add the GitLab marketplace and install `inference-hook-dlp@frb-infosec`, as you did Saturday. It fails the same way on `SECURITY_AND_DATA_HANDLING.md`. The dummy version is clearer to show, because it isolates the cause in one line.

