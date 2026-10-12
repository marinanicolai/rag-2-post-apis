```
cd C:\Users\M3MXN08\repo\ai-marketplace
git switch tmp/compare-sql
git add -f tmp/sync_precheck.sql tmp/sync_prod_from_dev.sql
git commit -m "tmp: prod sync precheck + dry-run script (do not merge)"
git push
git switch -
```
