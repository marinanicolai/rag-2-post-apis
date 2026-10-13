```
  cd apps\api
  .\.venv\Scripts\python.exe -m pytest ..\..\libs\python-common\tests\test_bundle_hash.py tests\services\test_submission_content_hash.py tests\services\test_resubmit_changes_requested.py tests\integration\test_fork_creation.py tests\integration\test_fork_sync.py -q -p no:cacheprovider --no-cov --tb=short -rfE
```
