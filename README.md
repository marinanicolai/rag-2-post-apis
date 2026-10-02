```
Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail 30 | Select-String '"tool_name":"Bash"'
```
