```
set -a; source /ai/www/cgi-bin/ai-marketplace-dev/.env; set +a
pg_dump --version; psql "$DATABASE_URL" -tc "SHOW server_version;"
pg_dump "$DATABASE_URL" -n ai_marketplace -Fc -f /tmp/$USER-cmp/prod_before_sync_$(date +%F_%H%M).dump
ls -lh /tmp/$USER-cmp/*.dump
pg_restore --list /tmp/$USER-cmp/prod_before_sync_*.dump | head
```
