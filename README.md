```
On ci/reenable-test-api: test:api fails at conftest import with ModuleNotFoundError: No module named 'psycopg' (exit 4, no tests collected). Fix only the test:api install step:
- Mirror how the Dockerfile/deploy job installs Python deps (requirements + pip install -e of libs/db, libs/python-common).
- Install the Postgres driver the app uses (check libs/db for psycopg version; use psycopg[binary]) from the mirror.
- Add `python -c "import psycopg"` right after install.
Don't touch app code or other jobs. Commit, push, give me the pipeline link.
```

