```
test:api still fails at conftest import with ModuleNotFoundError: No module named 'psycopg' (exit status 4, no tests collected). The install step isn't installing the Postgres driver.
Show me the exact install commands in the test:api script, and compare with how the Dockerfile / deploy job installs Python deps. Then add an explicit install of the driver the app uses (check libs/db pyproject or requirements: psycopg[binary] or psycopg2-binary, pinned version) from the mirror, before running pytest. Add `python -c "import psycopg"` as a check right after install so it fails fast if it's still missing. Commit, push, tell me the new pipeline.
```

