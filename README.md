```
.venv\Scripts\python.exe -m pytest apps/api/tests/blueprints/test_skills_download.py apps/api/tests/blueprints/test_500_responses_do_not_leak.py -q
```
```
.venv\Scripts\python.exe -m pytest apps/api/tests/blueprints/test_skills_download.py -q -k TestDownloadUnexpectedError
```
