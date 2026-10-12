```
git status                       # check nothing uncommitted you care about
Get-Content tmp\compare_dev_prod.sql -TotalCount 5   # should start with BEGIN TRANSACTION READ ONLY;
git switch -c tmp/compare-sql origin/main
git add -f tmp/compare_dev_prod.sql
git commit -m "tmp: dev/prod diff query (do not merge)"
git push -u origin tmp/compare-sql
git switch -                     # back to the branch you were on
```
