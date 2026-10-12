```
grep -E '^(DEV_)?DATABASE_URL' /ai/www/cgi-bin/ai-marketplace-dev/.env | sed -E 's#://[^@]*@#://***@#'
grep -E '^(DEV_)?DATABASE_URL' /ai/www/cgi-bin/ai-marketplace/.env     | sed -E 's#://[^@]*@#://***@#'
```
```
set -a && source /ai/www/cgi-bin/ai-marketplace-dev/.env && set +a
PGOPTIONS='-c default_transaction_read_only=on' psql "$DATABASE_URL" -c "SELECT table_schema FROM information_schema.tables WHERE table_name='alembic_version';"
```
