```
Investigate why the deploy:dev job fails for branch bug/resubmit-changes-requested in ai-marketplace. READ-ONLY: do not edit files, commit, push, run alembic, connect to any database, or trigger pipelines. Do not run Python. Git read commands and reading files are fine.

Failure from the job log:
  alembic -c libs/db/alembic.ini upgrade heads
  ERROR: Can't locate revision identified by '057_add_plugin_fork_lineage'
Deploy target dir: /ai/www/cgi-bin/ai-marketplace-dev

My hypothesis: the dev DB was migrated by feature/plugins-spine (migrations 047-057), which isn't merged; main stops at 046, so any main-based branch can't find the DB's current revision. Confirm or refute this:

1. git fetch --all. Find which branches/commits contain a migration with revision id 057_add_plugin_fork_lineage (git log --all -S "057_add_plugin_fork_lineage" --oneline; git branch -a --contains <commit>). Confirm it is NOT on origin/main or my branch.
2. List migration files in libs/db/migrations/versions on origin/main vs origin/feature/plugins-spine. Show each side's head revision and the down_revision chain from 046 onward. Flag any duplicate revision numbers or multiple heads.
3. Read .gitlab-ci.yml (and any included CI files). For deploy:dev, deploy:prod, deploy:prod:fresh-install, report: which branches/conditions trigger each (rules/only/when: manual), whether they share a database or env file, what commands they run (migrations, seeds, drops). Explain exactly what deploy:prod:fresh-install does and whether it is destructive.
4. Determine from CI config whether any branch (not just main) can deploy to dev, which is how plugins-spine would have migrated the shared dev DB.
5. Check whether the deploy script has any protection against a DB revision not present in code (e.g. alembic current check) and whether prod could hit the same problem.

Report: confirmed cause, evidence (commits, file paths, CI line numbers), whether prod is at risk, and 2-3 options for unblocking dev (e.g. wait for plugins-spine merge, deploy plugins-spine-based build, coordinated alembic stamp by DB owner) with the tradeoffs of each. Recommend, don't act.
```
