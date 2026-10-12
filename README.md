```
git -C /tmp/$USER-cmp/repo pull
cp /tmp/$USER-cmp/repo/tmp/sync_precheck.sql /tmp/$USER-cmp/
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
export PGOPTIONS='-c default_transaction_read_only=on'
psql "$DATABASE_URL" -f /tmp/$USER-cmp/sync_precheck.sql > /tmp/$USER-cmp/precheck.out 2>&1
less /tmp/$USER-cmp/precheck.out
```
