```
Re-enables the API test job, which has been commented out since May 18 (e3b3102, "Temporarily disable quality gates for rapid Phase 2 deployment").

Changes:
- test:api runs again, as a non-blocking job (allow_failure: true), so existing failures don't block deploys.
- Test DB URL pinned to the psycopg2 driver and a skillhub_test database on the job's own Postgres container.
- Quieter pytest output (--tb=short, --show-capture=no) so the log stays under GitLab's 4 MB limit, plus a JUnit report so results show in the pipeline's Tests tab.
- apps/api/pyproject.toml: declares prometheus-client (the app imports it but it was only in the root requirements.txt) and registers the "integration" pytest marker.

Baseline on main's code: 1243 passed, 690 failed, 185 errors, 35 skipped. Failures are pre-existing; triage follows in separate MRs. Lint, typecheck and security stages stay disabled for now.
```
