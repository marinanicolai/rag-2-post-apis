```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern "no recent block", "overridable", "override" | Select-Object Path, LineNumber, Line
```
