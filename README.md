```
Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail 0 -Wait |
  ConvertFrom-Json | Select-Object ts, cwd, hook_event, tool_name, action, deny_rule_id, reference_id
```
