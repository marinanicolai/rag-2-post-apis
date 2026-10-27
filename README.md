```
Get-ChildItem "$env:LOCALAPPDATA\inference-hook-dlp" -Recurse -File | Sort-Object LastWriteTime -Descending | Select-Object -First 5 FullName, LastWriteTime
```
