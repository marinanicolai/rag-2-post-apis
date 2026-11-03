```
Context: branch fix/skill-download-frontmatter. Commit 3e32471 records a "prod" plugin
renderer audit (scripts/audit_plugin_renderer_hashes.py, run on salt1 with
PGOPTIONS=-c default_transaction_read_only=on). It reported 10 versions: 2 DRIFT
(onboarding-context-pack 1.0.3, testnicolai 1.0.0), 6 NO-HASH, 2 WOULD-CHANGE.
docs/script-support/PROGRESS.md open question 3 asks for a read-only
plugin_version_hooks count for testnicolai 1.0.0 to tell whether its drift came
from a pinned hook or from a skill edit after approval.

What I found today on salt1:
- $DATABASE_URL connects to database "ocaio"; its default search_path is
  ai_marketplace_dev. Prod is schema ai_marketplace; dev is ai_marketplace_dev
  (plus per-developer schemas like ai_marketplace_dev_zach).
- SELECT ... FROM ai_marketplace.plugins WHERE slug ILIKE '%testnicolai%' returns 0 rows.
- So the earlier pinned_hooks = 0 is meaningless (subquery returned NULL).
- The audit printed testnicolai's stored hash as 45d25cbf1e0a...

Tasks:
1. Read scripts/audit_plugin_renderer_hashes.py and the DB code it uses
   (libs/db, python-common). Tell me exactly which connection string and which
   schema/search_path it used. Did it read ai_marketplace (prod) or
   ai_marketplace_dev?
2. Explain how the audit labels a row "it/testnicolai@1.0.0": which columns
   ("it" and "testnicolai") does it print, and is "testnicolai" the slug, the
   name, or something else?
3. Give me read-only SQL, with every table schema-qualified, that:
   a) finds the version whose content_hash starts with 45d25cbf1e0a in BOTH
      ai_marketplace and ai_marketplace_dev, showing schema, slug, name, version, status, id
   b) counts plugin_version_hooks for that version id in the schema where it exists
4. If the audit read the wrong schema, fix the script so the schema is explicit
   (a required --schema argument, or a check that refuses to run when
   search_path is not the expected one, and that prints current_database()
   and search_path at the top of its output). Add a test if the script has tests.
   Then give me the exact salt1 command to rerun it against ai_marketplace.
5. Update PROGRESS.md: correct the audit entry if it was not prod, record the
   testnicolai finding, and set "Last updated" to 2026-11-03.

Rules:
- Read-only against every database. Never run or suggest INSERT, UPDATE, DELETE,
  or the cleanup_duplicates.sql scripts in my shell history.
- Don't guess column names; check the models in libs/db/skillhub_db/models/.
- Don't commit or push until I've reviewed the diff.
- Report findings first, before changing any code.
```
