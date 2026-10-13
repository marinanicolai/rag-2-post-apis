```
  test:api on ci/reenable-test-api fails at conftest import: ModuleNotFoundError: No module named 'psycopg' (from libs/db/skillhub_db/session.py:14 create_engine). Runner, Docker, Postgres and the mirror all worked.

Fix the job's install step so it installs the same Python deps the app actually uses:
- Check how the deploy/build job and the Dockerfile install deps (requirements files, pip install -e of libs/db and libs/python-common, etc.) and mirror that in test:api.
- Confirm which driver DATABASE_URL uses (postgresql+psycopg:// = psycopg 3) and that psycopg[binary] (or the pinned version) gets installed from the mirror.
Don't change the app code or other jobs. Commit on ci/reenable-test-api, push, and tell me when to look at the pipeline.

```

