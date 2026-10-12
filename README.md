```
Investigate how to copy selected skills, hooks, and plugins from the dev schema (ai_marketplace_dev) to the prod schema (ai_marketplace) in ai-marketplace. Both schemas are in the same Postgres database and both are at alembic revision 057_add_plugin_fork_lineage.

READ-ONLY / PLANNING ONLY:
- Do NOT connect to any database, run Python, write migrations, edit existing files, or commit.
- You may create ONE new file: tmp/compare_dev_prod.sql (SELECT statements only).
- Never print credential values. If a file contains secrets, skip those lines and tell me the file name.

1. Data model: from libs/db/skillhub_db/models (and migrations 047-057), list every table involved in skills, skill versions, hooks (and hook versions/curation), plugins, plugin_versions, plugin_version_skills, plugin_version_hooks, plus anything they reference by foreign key (users, divisions, categories, tags, etc.). Give me the FK dependency order for inserts. Mark which tables are user activity (installs, reviews, review votes, favorites, notifications, audit log, downloads) that should NOT be copied.

2. Existing process: read scripts/transform_prod_data.py, scripts/*production*.sql, scripts/validate_production_*.sql, and anything that references prod_data_transformed_20260528.sql. Explain what process they implement (how prod data was produced and loaded before), and whether any of it can be reused for a selective copy. Flag anything destructive (TRUNCATE, DROP, DELETE).

3. Write tmp/compare_dev_prod.sql that I will run with psql on the server in a READ ONLY transaction (start with BEGIN TRANSACTION READ ONLY; end with ROLLBACK;). Use only SELECTs, each statement on one line where practical. It should show:
   a. Row counts per relevant table in both schemas.
   b. Skills, hooks, and plugins in dev but not in prod (match by id AND separately by slug), with name, slug, status, author, created_at.
   c. Conflicts: same slug in both schemas with different ids, or same id with different slug/content.
   d. Authors (users) referenced by dev content that don't exist in prod.
   e. Any other FK target (division, category, tag, etc.) referenced by dev content that's missing in prod.
   f. min/max created_at for skills in each schema.

4. Copy plan (do not implement): steps for a selective copy of an agreed list of slugs: pre-copy pg_dump of the ai_marketplace schema, one transaction, insert order, how to handle each conflict type and missing authors, which columns to reset (e.g. counts, install stats, reviewer fields), how to keep bundle/content hashes valid, a rehearsal on a scratch schema, and post-copy verification queries. Note any reason this should instead go through the app's submit → review → approve flow.

Report the findings for 1, 2, and 4, and tell me the exact psql command to run tmp/compare_dev_prod.sql on the server.
```
