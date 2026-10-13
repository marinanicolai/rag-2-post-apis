```
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
PGOPTIONS='-c default_transaction_read_only=on' psql "$DATABASE_URL" -c "SELECT version_num FROM ai_marketplace_dev.alembic_version;"

```

