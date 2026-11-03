```
SELECT pv.id, pv.version, count(h.hook_id) AS pinned_hooks
FROM ai_marketplace_dev.plugin_versions pv
LEFT JOIN ai_marketplace_dev.plugin_version_hooks h ON h.plugin_version_id = pv.id
WHERE pv.content_hash LIKE '45d25cbf1e0a%'
GROUP BY pv.id, pv.version;

ROLLBACK;
```
