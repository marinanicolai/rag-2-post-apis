```
Get-Content $log -Tail 8 | ConvertFrom-Json | Select-Object ts, hook_event, action, deny_rule_id, reference_id | Format-Table
```
