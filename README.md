```
function Last($n = 1) { Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail $n | ConvertFrom-Json | Format-List }
```
