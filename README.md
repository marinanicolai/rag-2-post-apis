```
cd apps\api
.\.venv\Scripts\python.exe -m pytest tests\services\test_approval_rules.py tests\services\test_resubmit_changes_requested.py tests\test_phase1_approval.py -q -p no:cacheprovider --no-cov --tb=short -rfE
cd ..\..```

