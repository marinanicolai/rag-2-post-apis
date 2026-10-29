```
function LastCowork($n = 5) {
  Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" |
    ConvertFrom-Json |
    Where-Object { $_.cwd -like "*Claude-3p*" } |
    Select-Object -Last $n @{n='local_time';e={([datetime]$_.ts).ToLocalTime()}}, hook_event, tool_name, action, deny_rule_id, reference_id, pack_hash
}
LastCowork
```
