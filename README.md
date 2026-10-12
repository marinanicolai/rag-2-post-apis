```
psql "$DATABASE_URL" -c "SELECT 'skills' kind, status::text, count(*) FROM ai_marketplace_dev.skills GROUP BY 2 UNION ALL SELECT 'hooks', status::text, count(*) FROM ai_marketplace_dev.hooks GROUP BY 2 UNION ALL SELECT 'plugin_versions', status::text, count(*) FROM ai_marketplace_dev.plugin_versions GROUP BY 2 ORDER BY 1,2;"
```
