```
BEGIN READ ONLY;

SELECT table_schema FROM information_schema.tables
WHERE table_name = 'plugin_versions' ORDER BY 1;

SELECT 'ai_marketplace' AS schema, p.division_slug, p.slug, p.name, pv.version, pv.status, pv.id
FROM ai_marketplace.plugin_versions pv
JOIN ai_marketplace.plugins p ON p.id = pv.plugin_id
WHERE pv.content_hash LIKE '45d25cbf1e0a%'
UNION ALL
SELECT 'ai_marketplace_dev', p.division_slug, p.slug, p.name, pv.version, pv.status, pv.id
FROM ai_marketplace_dev.plugin_versions pv
JOIN ai_marketplace_dev.plugins p ON p.id = pv.plugin_id
WHERE pv.content_hash LIKE '45d25cbf1e0a%';
```
