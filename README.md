```
  test:api now runs tests, but the log hits GitLab's 4 MB limit ("Job's log exceeded limit") because of SQLAlchemy query logging in failing tests, so the summary is cut off.
In test:api only:
1. Run pytest with: -q --tb=short --show-capture=no -p no:cacheprovider, plus -r fE so the summary lists failures and errors.
2. Add --junitxml=report.xml and in the job: artifacts: when: always, reports: junit: report.xml (keep it 7 days).
3. Find what turns on SQL echo/debug logging in tests (an env var like SQL_ECHO or LOG_LEVEL, or echo=True in the test engine/config) and turn it off for test:api via an env var, not by changing app code. Tell me what it was.
Don't commit; tell me when ready and I'll commit and push.
```
