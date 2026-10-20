```
Add to PROGRESS.md (on docs/publisher-plan):

Step 3, checks: the prod DB user is ocaio_admin and owns jobs, plugin_versions and review_events, so the publisher has the INSERT/UPDATE rights it needs. Check closed.
Side issues, security: (1) DATABASE_URL is masked but NOT protected, so any branch pipeline can read prod DB credentials. Fix: mark it Protected after confirming only main/tag jobs use it (you’re checking). (2) The app connects as ocaio_admin, an admin account on the shared ocaio database. Recommend a dedicated app user with rights on the ai_marketplace schema only (infra). (3) review_events append-only is enforced by a trigger, and the table owner could bypass it.
Then answer my earlier question: which CI jobs use DATABASE_URL, and on which refs?
```
