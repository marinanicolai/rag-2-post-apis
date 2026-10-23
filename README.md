```
Get-Content $log -Tail 12 | ConvertFrom-Json | Select-Object @{n='time';e={([datetime]$_.ts).ToString('HH:mm:ss')}}, hook_event, action, deny_rule_id, tool_name | Format-Table -AutoSize
```
```
$hook = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\hook.py"
$in = @{hook_event_name="PreToolUse"; session_id="manual-test"; cwd="C:\Users\M3MXN08\repo\dlp-demo-files"; tool_name="Read"; tool_input=@{file_path="C:\Users\M3MXN08\Documents\confidential-test.docx"}} | ConvertTo-Json -Compress
$in | python $hook PreToolUse
$LASTEXITCODE
```
