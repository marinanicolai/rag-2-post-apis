```
bash
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
export PGOPTIONS='-c default_transaction_read_only=on'
psql "$DATABASE_URL" -c "SELECT table_schema FROM information_schema.tables WHERE table_name='alembic_version';"
psql "$DATABASE_URL" -c "SELECT version_num FROM ai_marketplace_dev.alembic_version;"
psql "$DATABASE_URL" -c "SELECT table_schema, table_name FROM information_schema.tables WHERE table_name ILIKE '%plugin%' ORDER BY 1,2;"
exit
```
