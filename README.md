```
psql "$DATABASE_URL" -c "\copy (SELECT 'skill' kind, slug, name, status, created_at FROM ai_marketplace_dev.skills UNION ALL SELECT 'hook', slug, name, status, created_at FROM ai_marketplace_dev.hooks UNION ALL SELECT 'plugin', slug, name, status, created_at FROM ai_marketplace_dev.plugins ORDER BY 1,2) TO '/tmp/$USER-cmp/dev_content.csv' CSV HEADER"
wc -l /tmp/$USER-cmp/dev_content.csv
```
