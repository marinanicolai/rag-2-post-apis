```
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
PGOPTIONS='-c default_transaction_read_only=on' psql "$DATABASE_URL" -c "SELECT tgname FROM pg_trigger WHERE tgrelid = 'ai_marketplace_dev.review_events'::regclass AND NOT tgisinternal;" -c "SELECT indexname FROM pg_indexes WHERE schemaname='ai_marketplace_dev' AND tablename IN ('jobs','scan_results','plugin_versions') ORDER BY 1;"

```

