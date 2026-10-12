```
git push origin --delete tmp/compare-sql
git branch -D tmp/compare-sql
```
```
Get-ChildItem -Path . -Recurse -Filter compare_dev_prod.sql -ErrorAction SilentlyContinue | Select-Object FullName
Get-ChildItem -Path $env:TEMP, C:\tmp -Recurse -Filter compare_dev_prod.sql -ErrorAction SilentlyContinue | Select-Object FullName
```
