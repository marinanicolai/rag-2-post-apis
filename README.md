```
Select-String -Path tmp\sync_precheck.sql -Pattern "name_differs" | Select-Object -First 1
Get-Content tmp\sync_precheck.sql -TotalCount 3
```
```
git switch tmp/compare-sql
git add -f tmp/sync_precheck.sql
git commit -m "tmp: prod sync precheck (do not merge)"
git push
git switch -
```
