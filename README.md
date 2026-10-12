```
git switch -c tmp/compare-sql origin/main
git add -f tmp/compare_dev_prod.sql
git commit -m "tmp: dev/prod diff query (do not merge)"
git push -u origin tmp/compare-sql
git switch -
```
```
git fetch origin tmp/compare-sql
git show origin/tmp/compare-sql:tmp/compare_dev_prod.sql > ~/compare_dev_prod.sql
head -5 ~/compare_dev_prod.sql
export PGOPTIONS='-c default_transaction_read_only=on'
psql "$DATABASE_URL" -f ~/compare_dev_prod.sql > ~/compare_dev_prod.out 2>&1
wc -l ~/compare_dev_prod.out
```
