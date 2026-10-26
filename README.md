```
   Select-String -Path $env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl -Pattern 'local-agent-mode-sessions' | Select-Object -Last 5
```
