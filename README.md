
```powershell
$dir = "C:\Users\M3MXN08\repo\dlp-demo-files"
Test-Path "$dir\marked-memo.txt"
```

It should say **True**. If it says False, create the file again:

```powershell
Set-Content "$dir\marked-memo.txt" "RESTRICTED FR`r`nTest memo for DLP. Fake content only."
```

```powershell
Get-Content "$dir\marked-memo.txt"
```

The first line should show the marking.

**Control first** (should block on any version):

```powershell
$in2 = @{hook_event_name="PreToolUse"; session_id="mr-test"; cwd=$dir; tool_name="Bash"; tool_input=@{command="type $dir\marked-memo.txt"}} | ConvertTo-Json -Compress
$in2 | python .\client\hook.py PreToolUse
$LASTEXITCODE
```

You should see **"Blocked Bash..."** and **2**. **If this gives 0, stop and send me a photo**, because then something else is off.

**The one-liner test:**

```powershell
$cmd = "python -c `"print(open(r'$dir\marked-memo.txt').read())`""
$in = @{hook_event_name="PreToolUse"; session_id="mr-test"; cwd=$dir; tool_name="Bash"; tool_input=@{command=$cmd}} | ConvertTo-Json -Compress
```

```powershell
git switch --detach origin/main
```

```powershell
$in | python .\client\hook.py PreToolUse
$LASTEXITCODE
```

Expected: **0** (the bug).

```powershell
git switch fix/bash-embedded-paths
```

```powershell
$in | python .\client\hook.py PreToolUse
$LASTEXITCODE
```

Expected: **"Blocked Bash..."** and **2** (fixed).

For the merge request description, change the setup in step 1 to use a folder that exists, like `dlp-demo-files`, and note that the file must contain a real marking.
