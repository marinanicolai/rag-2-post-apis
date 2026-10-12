```
psql "$DATABASE_URL" -c "SELECT p.slug, pv.status, pv.created_at FROM ai_marketplace_dev.plugins p JOIN ai_marketplace_dev.plugin_versions pv ON pv.plugin_id = p.id ORDER BY p.slug, pv.created_at;"
```
