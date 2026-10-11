```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
Get-ChildItem -Recurse -Include FRB_SERVER_HANDOFF.md, DEPLOYMENT_RUNBOOK.md | ForEach-Object { "== $($_.FullName)"; Select-String $_.FullName -Pattern "^#" | ForEach-Object { "$($_.LineNumber): $($_.Line)" } }
```
