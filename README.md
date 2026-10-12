```
Get-Content tmp\compare_dev_prod.sql -TotalCount 5
git switch -c tmp/compare-sql origin/main
git add -f tmp/compare_dev_prod.sql
git commit -m "tmp: dev/prod diff query (do not merge)"
git push -u origin tmp/compare-sql
git switch -
```
