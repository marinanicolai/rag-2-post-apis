```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
Select-String -Path .\restrictions\*.md, .\client\*.py, .\app\*.py -Pattern "This content is marked" | Select-Object Filename, LineNumber, Line
```
