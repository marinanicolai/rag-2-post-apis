```
git status                                   # should say "nothing to commit, working tree clean"
git grep -n "<<<<<<<\|>>>>>>>" HEAD -- apps  # should print nothing
```
```
cd apps\api
.\.venv\Scripts\python.exe -m pytest tests\services\test_resubmit_changes_requested.py tests\services\test_plugin_submission.py tests\blueprints\test_plugins_admin.py tests\test_reference_files_review_carrythrough.py tests\test_revision_endpoints.py tests\test_phase1_service.py tests\test_phase1_approval.py tests\test_submissions_blueprint.py tests\test_division_enforcement.py -q -p no:cacheprovider --tb=no -rfE
```
