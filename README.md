```
Get-Content $log -Tail 20 | ConvertFrom-Json | Select-Object @{n='time';e={([datetime]$_.ts).ToString('HH:mm:ss')}}, hook_event, action, deny_rule_id, tool_name | Format-Table -AutoSize
```
