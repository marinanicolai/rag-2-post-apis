```
$hook = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\hook.py"
$cmd = @'
PASTE THE COMMAND HERE
'@
$in = @{hook_event_name="PreToolUse"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo\dlp-demo-files"; tool_name="Bash"; tool_input=@{command=$cmd.Trim()}} | ConvertTo-Json -Compress
$in | python $hook PreToolUse
$LASTEXITCODE
```
```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
Select-String -Path .\client\*.py, .\app\*.py -Pattern "Bash|tool_input|command" | Select-Object Filename, LineNumber, Line -First 40
```

