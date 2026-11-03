```
psql "$DATABASE_URL" -c "SELECT p.slug, pv.version, pv.status, left(pv.content_hash, 12) AS hash FROM ai_marketplace.plugin_versions pv JOIN ai_marketplace.plugins p ON p.id = pv.plugin_id WHERE p.slug ILIKE '%testnicolai%';"
```
