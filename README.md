```
PGOPTIONS="-c default_transaction_read_only=on" psql "$DATABASE_URL" -c "SELECT 'dev' AS env, count(1) FROM ai_marketplace_dev.users WHERE division = 'unknown' UNION ALL SELECT 'prod', count(1) FROM ai_marketplace.users WHERE division = 'unknown';"
```
