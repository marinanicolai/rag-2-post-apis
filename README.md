```
  Get-Content $env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl -Tail 10 |
  ForEach-Object { $_ | ConvertFrom-Json } |
  Where-Object { $_.cwd -like '*local-agent-mode-sessions*' } |
  Select-Object ts, hook_event, tool_name, action, deny_rule_id | Format-Table -AutoSize
```
