```
SELECT current_user;
SELECT tablename, tableowner
FROM pg_tables
WHERE schemaname = 'ai_marketplace'
  AND tablename IN ('jobs', 'plugin_versions', 'review_events');
```
