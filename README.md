```
git -C /tmp/$USER-cmp/repo pull
cp /tmp/$USER-cmp/repo/tmp/sync_precheck.sql /tmp/$USER-cmp/
cp /tmp/$USER-cmp/repo/tmp/sync_prod_from_dev.sql /tmp/$USER-cmp/
tail -2 /tmp/$USER-cmp/sync_prod_from_dev.sql
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
export PGOPTIONS='-c default_transaction_read_only=on'
psql "$DATABASE_URL" -f /tmp/$USER-cmp/sync_precheck.sql > /tmp/$USER-cmp/precheck.out 2>&1
grep -c ERROR /tmp/$USER-cmp/precheck.out
less /tmp/$USER-cmp/precheck.out
```
