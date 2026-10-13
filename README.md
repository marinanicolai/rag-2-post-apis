```
.\.venv\Scripts\python.exe -m pytest tests\test_content_hash.py tests\test_versioning_integration.py tests\test_admin_approvals.py -q -p no:cacheprovider --no-cov --tb=no -rfE
```
```
git stash push -u -m "wip: reference_files in bundle hash"
.\.venv\Scripts\python.exe -m pytest tests\test_content_hash.py tests\test_versioning_integration.py tests\test_admin_approvals.py -q -p no:cacheprovider --no-cov --tb=no
git stash pop
```
