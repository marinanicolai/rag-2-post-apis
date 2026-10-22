```
$log = "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl"
Test-Path $log
```
```
Get-Content $log -Tail 15 | ConvertFrom-Json | Select-Object @{n='time';e={([datetime]$_.ts).ToString('HH:mm:ss')}}, event, hook_event, action, deny_rule_id, tool_name, @{n='rules_hit';e={$_.matched_rule_ids -join ','}}, latency_ms | Format-Table -AutoSize
```
