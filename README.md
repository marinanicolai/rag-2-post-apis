```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
Get-ChildItem -Recurse -Filter hooks.json | ForEach-Object { $_.FullName; Select-String $_.FullName -Pattern '"command"' | ForEach-Object { "  " + $_.Line.Trim() } }
```
