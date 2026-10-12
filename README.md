```
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
export PGOPTIONS='-c default_transaction_read_only=on'
psql "$DATABASE_URL" -f /tmp/$USER-cmp/compare_dev_prod.sql > /tmp/$USER-cmp/compare.out 2>&1
wc -l /tmp/$USER-cmp/compare.out
less /tmp/$USER-cmp/compare.out
```
