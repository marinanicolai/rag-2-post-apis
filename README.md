```
Option 1. The traceback from the failed job goes through sqlalchemy/dialects/postgresql/psycopg.py:497 (import_dbapi -> import psycopg), called from libs/db/skillhub_db/session.py:14 create_engine, during conftest import. So the URL in use is postgresql+psycopg://..., not postgresql://.

Find which variable conftest/session.py actually reads (TEST_DATABASE_URL vs DATABASE_URL, and any other env var), then in the test:api job only, explicitly set those variables to the job's own Postgres container with the psycopg2 driver, e.g. postgresql+psycopg2://skillhub:skillhub@<postgres host>:5432/skillhub_test. This overrides any project-level CI variable. Don't add psycopg 3 and don't change app code. Commit, push, give me the pipeline link.

```

