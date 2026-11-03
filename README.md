```
.venv\Scripts\python.exe -m pytest tests/blueprints/test_skills_download.py tests/blueprints/test_500_responses_do_not_leak.py -q
```
```
.venv\Scripts\python.exe -m pytest tests/blueprints/test_skills_download.py -q -k TestDownloadUnexpectedError
```
