```
function Last { Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail 1 | ConvertFrom-Json | Format-List }
```
