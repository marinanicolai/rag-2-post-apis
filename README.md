```
env | grep -i database | cut -d= -f1
grep -o '^[A-Z_]*DATABASE[A-Z_]*' /ai/www/cgi-bin/ai-marketplace/.env
```
```
export PGOPTIONS="-c default_transaction_read_only=on"
psql "$DATABASE_URL" -c "SELECT current_database();" -c "SHOW search_path;"
```
```
psql "$DATABASE_URL" -c "SET search_path TO ai_marketplace;" -c "SELECT count(*) AS pinned_hooks FROM plugin_version_hooks WHERE plugin_version_id = (SELECT pv.id FROM plugin_versions pv JOIN plugins p ON p.id = pv.plugin_id WHERE p.slug = 'testnicolai' AND pv.version = '1.0.0');"
```
