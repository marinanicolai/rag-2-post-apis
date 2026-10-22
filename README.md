```
$in = '{"hook_event_name":"PreToolUse","session_id":"manual-test","cwd":"C:\\Users\\M3MXN08\\repo\\dlp-demo-files","tool_name":"Read","tool_input":{"file_path":"C:\\Users\\M3MXN08\\repo\\dlp-demo-files\\employee.txt"}}'
```
```
$in | python $hook PreToolUse
```
```
$LASTEXITCODE
```
Get-Content $log -Tail 1 | ConvertFrom-Json | Select-Object hook_event, action, deny_rule_id, tool_name
```
