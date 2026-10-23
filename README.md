```
$evid = "C:\Users\M3MXN08\repo\dlp-evidence\2026-10-23"
New-Item -ItemType Directory -Force $evid | Out-Null
$log = "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl"
```
```
Get-Content $log | ConvertFrom-Json | Where-Object { $_.ts -like "2026-10-23*" } | Select-Object @{n='local_time';e={([datetime]$_.ts).ToString('yyyy-MM-dd HH:mm:ss')}}, event, hook_event, action, deny_rule_id, reference_id, tool_name, latency_ms | Export-Csv "$evid\dlp-decisions.csv" -NoTypeInformation
```
```
Get-Content $log | Where-Object { $_ -like '*"ts":"2026-10-23*' } | Set-Content "$evid\dlp-decisions-raw.jsonl"
```
