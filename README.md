```
Get-ChildItem -Recurse -Force -Filter *.ps1 | Sort-Object LastWriteTime -Descending | Select-Object -First 5 FullName, LastWriteTime
```
