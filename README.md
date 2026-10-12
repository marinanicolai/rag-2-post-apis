```
bash
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
export PGOPTIONS='-c default_transaction_read_only=on'
psql "$DATABASE_URL" -f ~/compare_dev_prod.sql > ~/compare_dev_prod.out 2>&1
```
