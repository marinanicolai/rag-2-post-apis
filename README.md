```
Context
- Repo: ai-marketplace, branch fix/skill-download-frontmatter at c22286e (GitLab:
  https://gitlab.frb.gov/ai-program/platforms/tech-enablement/coding-tools/ai-marketplace.git).
  The branch adds Alembic migration 059: plugin_versions.skill_md_renderer
  ('legacy' / 'v2'), with 'legacy' backfilled for rows that have a content_hash.
- Database "ocaio" via $DATABASE_URL. Its default search_path is ai_marketplace_dev.
  Prod schema = ai_marketplace, shared dev = ai_marketplace_dev.
- Prod audit today (--schema ai_marketplace): 1 row, onboarding-context-pack 1.0.8
  [published], WOULD-CHANGE, stored hash == legacy rebuild. It relies on 059's legacy freeze.
- The prod deploy job (.gitlab/ci/deploy-prod.yml, manual, main only) extracts the new
  code into /ai/www/cgi-bin/ai-marketplace, runs pip install, and only THEN runs
  alembic upgrade head. So new code can run against the old schema for a few minutes.
- My attempt to set up a venv failed: pip install -r requirements.txt can't install.

Question: does 059 need to be applied before the deploy, and if so, how do I do it safely?

Do this:
1. Work only in ~/scratch/mig-059 (clone the branch there). Never touch
   /ai/www/cgi-bin/ai-marketplace: that is the live app.
2. Set up a venv with only what alembic and the audit script need. Find out
   why requirements.txt fails and work around it with minimal packages
   (alembic, sqlalchemy, psycopg, opentelemetry-api, pyyaml, etc.).
3. Read-only investigation:
   a. Read libs/db/migrations/env.py, the 059 migration file, and run-migrations.sh.
      Tell me how the schema is chosen and the exact URL/options needed to target
      ai_marketplace_dev and ai_marketplace.
   b. For BOTH schemas, report the current alembic revision and confirm the branch head
      is 059 and that only 059 is pending. If anything else is pending, stop and tell me.
   c. Generate the offline SQL for 059 only (alembic upgrade <058>:<059> --sql) and
      show it. Confirm it is additive (one column with a default plus a backfill UPDATE).
   d. Check whether the current $DATABASE_URL role can ALTER plugin_versions in each
      schema (has_table_privilege / ownership). Don't try the write to find out.
   e. Check whether the current code on main would break with the new column present
      (it should ignore it), and whether the new code would break if the column is missing.
4. Give me your recommendation: pre-apply 059 (dev first, then prod), or deploy as-is.
   Include exact commands.
5. STOP before any write. Don't run alembic upgrade or any INSERT, UPDATE, ALTER or
   DELETE on any schema until I reply "go dev". Prod is never done by you; I'll take
   that to Zach.

Afterwards, remove the scratch venv and clone unless I ask to keep them.
```
