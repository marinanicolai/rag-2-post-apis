```
 cd apps\api
.\.venv\Scripts\python.exe -m pytest ..\..\libs\python-common\tests\test_bundle_hash.py tests\services\test_submission_content_hash.py tests\test_reference_files_review_carrythrough.py tests\services\test_resubmit_changes_requested.py -q -p no:cacheprovider --no-cov --tb=short -rfE
```
```
Get-ChildItem -Path tests -Recurse -Include test_content_hash.py,test_versioning_integration.py,test_admin_approvals.py | Select-Object FullName
```
