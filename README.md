```
   which pg_dump
   mkdir -p ~/backups && chmod 700 ~/backups
   pg_dump "$DATABASE_URL" -n ai_marketplace -f ~/backups/ai_marketplace_before_sync_$(date +%F).sql
```

```
   psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sync_prod_content_from_dev.sql 2>&1 | tee ~/backups/sync_$(date +%F).log
```
