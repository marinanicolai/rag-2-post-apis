```
Prod was deployed just now from main (2fbf857 or later) WITHOUT the manual
059 pre-apply; the deploy job's alembic step should have applied it.
Re-read docs/script-support/PROGRESS.md on main. Then:
1. Give me the read-only checks for the salt1 Claude to run on ai_marketplace.
2. Create branch docs/progress-after-deploy from main and update PROGRESS.md:
   merged as 2fbf857, deployed to prod on 2026-11-03 via the pipeline (no pre-apply).
   Leave the verification results blank until I send them. Don't commit.
```
```
Prod ai-marketplace was just deployed from main, which includes migration 059.
Verify prod, READ-ONLY ONLY (BEGIN READ ONLY ... ROLLBACK, schema ai_marketplace,
DATABASE_URL with search_path swapped to ai_marketplace). No writes, no alembic upgrade.
1. SELECT version_num FROM ai_marketplace.alembic_version;  expect 059_add_plugin_version_skill_md_renderer
2. Confirm column ai_marketplace.plugin_versions.skill_md_renderer exists.
3. SELECT count(*) FROM ai_marketplace.plugin_versions WHERE content_hash IS NOT NULL AND skill_md_renderer <> 'legacy';  expect 0
4. In a fresh ~/scratch clone of main, run scripts/audit_plugin_renderer_hashes.py --schema ai_marketplace.
   Expect onboarding-context-pack 1.0.8 = OK-FROZEN, no DRIFT.
5. Check the live app's error log in /ai/www/cgi-bin/ai-marketplace/logs for errors since the deploy,
   especially UndefinedColumn or skill_md_renderer. Read only; don't change anything in that folder.
Report the results, then delete the scratch clone.
```
