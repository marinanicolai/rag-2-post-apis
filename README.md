```
test:api now connects to the DB but stops at collection: ERROR apps/api/tests/services/test_notification_atomicity.py, "Interrupted: 1 error during collection" (exit 2).
In test:api only:
1. Add --continue-on-collection-errors to the pytest command, so one broken file doesn't stop the whole run.
2. Register the "integration" marker in the pytest config (pyproject or pytest.ini) to remove the Unknown mark warnings.
Then look at test_notification_atomicity.py and tell me why it fails to import (read only, don't fix it yet).
Don't commit; tell me when the edit is ready and I'll commit and push.
```
