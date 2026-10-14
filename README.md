```
Don't add --continue-on-collection-errors. Instead: apps/api/tests/services/test_notification_atomicity.py fails with an ImportError at collection in CI. Find what it imports that no longer exists, and propose the smallest fix (update the import, or if the code it tests was removed, tell me so I can decide whether to delete the test). Show me before editing.
Optional: register the "integration" marker in pyproject.toml's pytest config.
```
