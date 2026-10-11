```
Hello, sorry for the late response. I can’t package the release as-is: both the exe and the marketplace install fail on our laptops. AppLocker blocks the exe because it’s unsigned (Jitesh notes this in the repo), and our endpoint DLP blocks Claude from copying the plugin files during the marketplace install (this one is new; I found it while testing).

What does work: clone the repo with git and register the hooks in the user’s Claude settings, pointing at the Python hook in the clone. Nothing gets copied by Claude and no exe runs. I tested it today in the desktop app (Code tab) and the CLI, and SSN test prompts are blocked by the hook as expected.

So the package for the small group is: the repo link, the install steps below (clone, run one PowerShell snippet, restart, 1-minute check), and the may test the hook.

```
```
DLP Hooks — Tester Install Guide
Oct 10, 2026 · @Marina
These steps turn on the DLP hooks for the Code tab of the Claude desktop app. They take about 5 minutes. Chat and Cowork are not covered.
Before you start
• You need Python 3.11 or newer and access to the C4G DLP Hooks repo on GitLab.
• Step 3 replaces any hooks you already have in your Claude settings, and saves a backup first.
• Auto-labeling is on: when you ask Claude about an unlabeled Office file, the hook writes a sensitivity label and header into that file.
1. Check Python
In PowerShell:
python --version
It should show 3.11 or newer.
2. Clone the repo
New-Item -ItemType Directory -Force $env:USERPROFILE\source\repos | Out-Null
cd $env:USERPROFILE\source\repos
git clone https://gitlab.frb.gov/ai-program/platforms/tech-enablement/coding-tools/c4g-dlp-hooks-repo.git
3. Add the hooks to your Claude settings
Copy and paste the whole block. It backs up your settings to settings.json.bak first.
$repo = ("$env:USERPROFILE\source\repos\c4g-dlp-hooks-repo") -replace '\\','/'
$s = "$env:USERPROFILE\.claude\settings.json"
if (Test-Path $s) { Copy-Item $s "$s.bak" -Force; $cfg = Get-Content $s -Raw | ConvertFrom-Json } else { New-Item -ItemType Directory -Force (Split-Path $s) | Out-Null; $cfg = [pscustomobject]@{} }
$h = ((Get-Content "$repo/hooks/hooks.json" -Raw) -replace '\$\{CLAUDE_PLUGIN_ROOT\}', $repo) | ConvertFrom-Json
$cfg | Add-Member -NotePropertyName hooks -NotePropertyValue $h.hooks -Force
[IO.File]::WriteAllText($s, ($cfg | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding $false))
"hooks added: " + ((Get-Content $s -Raw | ConvertFrom-Json).hooks.PSObject.Properties.Name -join ", ")
It should print:
hooks added: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse
4. Restart the Claude desktop app
1. Fully quit the app: right-click the Claude icon in the system tray and choose Quit. Closing the window is not enough.
2. Reopen it, go to the Code tab, and start a new session in any folder.
5. One-minute check
Send this prompt:
check this record: employee 123-45-6789, start date Monday
You should see "A hook blocked your prompt". If Claude answers instead, the hooks are not running: stop and tell us.
Updates and uninstall
• Update: in PowerShell, run git pull in %USERPROFILE%\source\repos\c4g-dlp-hooks-repo. Updates are not automatic.
• Uninstall: copy the backup back, then fully restart the app:
Copy-Item "$env:USERPROFILE\.claude\settings.json.bak" "$env:USERPROFILE\.claude\settings.json" -Force
What to expect
See the known-gaps document for current limitations. The ones you are most likely to notice:
• The first check in a new session can time out and block your action. Retry and it works.
• Office files you ask Claude about get an "INTERNAL FR" header added.
• Report anything that is blocked when it should not be, or allowed when it should not be, with the dlp_... reference from the message.
```
