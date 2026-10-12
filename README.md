```
Write a SQL script that copies selected content from the dev schema (ai_marketplace_dev) into the prod schema (ai_marketplace). Both schemas are in the same Postgres database, both at alembic revision 057_add_plugin_fork_lineage. Read the models in libs/db/skillhub_db/models and migrations 047-057 for exact table/column names, constraints, and FKs. Don't guess names.

RULES: Write files only. Don't connect to any database, run Python, commit, or edit existing files. Never print credentials. Schema-qualify every table (ai_marketplace. / ai_marketplace_dev.).

WHAT TO COPY (and nothing else):
1. Skills: dev skills with status='published' whose slug does NOT exist in prod (expected: 23). Do NOT modify any existing prod skill (prod's 7 skills, including 508 and grill-me, stay exactly as they are).
   - Copy each skill's current/published version row(s) only, plus its skill_categories, skill_tags, and skill_divisions links.
   - Reset on insert: install_count, fork_count, favorite_count, view_count, review_count, avg rating = 0; featured = false, featured_order = NULL; reviewer fields NULL; parent_skill_id NULL if the parent isn't in prod.
   - Keep id, slug, content, and content_hash verbatim so hashes stay valid. Regenerate display_id only if it collides with prod.
2. Hooks: dev hooks with status='published' (expected: 5), slug not in prod. Reset featured_order and reviewer fields; regenerate display_id only on collision.
3. Plugin: dev plugin slug 'onboarding-context-pack' and ONLY its plugin_version with status='published', plus that version's plugin_version_skills and plugin_version_hooks links. Map linked skills/hooks to prod rows by slug (e.g. if it links 508 or grill-me, use prod's existing ids). If any linked skill/hook is not published in dev and not already in prod, RAISE EXCEPTION naming it. Copy content_hash verbatim. Reset favorite_count, avg_rating, featured_order.
4. Dependencies: categories needed by copied skills. Match by name/slug to existing prod categories first; insert only truly missing ones. Same for tags if they're a table.
5. Authors (author_id, submitted_by, created_by, etc.): create a temp mapping table author_map(dev_user_id, prod_user_id) at the TOP of the script, prefilled by matching dev users to prod users by email, then username/Kerberos principal. If any copied row's author has no prod match, RAISE EXCEPTION listing them (dev user id, username, email) so I can decide. Don't create users automatically.
6. Do NOT copy user activity: reviews, favorites, installs, hook_installs, plugin_installs, follows, forks, comments, audit_log, notifications, submissions, submission_state_transitions.
7. After inserts, bump mcp_cache_version (or equivalent) if such a setting/table exists. Insert one audit_log row describing the sync if audit_log allows it without breaking constraints; otherwise skip.

STRUCTURE of tmp/sync_prod_from_dev.sql:
- BEGIN; then SET LOCAL statement_timeout = '5min';
- Pre-checks that RAISE EXCEPTION on: alembic version not 057 in either schema; slug collisions; unmapped authors; plugin links to non-copyable items.
- Inserts in FK order, each using INSERT ... SELECT ... WHERE NOT EXISTS (idempotent).
- Verification SELECTs: published counts in prod (expect skills 29, hooks 5, plugins 1 with 1 published version), no orphan FKs for copied rows, and the list of copied slugs.
- LAST LINE: ROLLBACK;  with a comment directly above it: "-- DRY RUN. Change to COMMIT only after a clean dry run AND a pg_dump backup."

Also write tmp/sync_precheck.sql: BEGIN TRANSACTION READ ONLY; ... ROLLBACK; with SELECTs only, showing the 23 skills / 5 hooks / plugin version to be copied, the authors and their prod matches (or missing), categories/tags to be matched vs inserted, and the plugin version's linked skills/hooks with their status in dev and existence in prod.

When done, summarize: tables touched in order, anything you couldn't determine from the models, and the psql commands to run each file.
```
