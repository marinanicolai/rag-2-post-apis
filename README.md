```
Select-String -Path .\tests\test_client_hook.py, .\tests\test_server_pack_dir.py -Pattern "is marked|carries a classification|RESTRICTED FR" | Select-Object Filename, LineNumber, Line
```
```
python -m pytest tests\test_zscaler_spec.py -q --tb=short 2>&1 | Select-Object -Last 15
```
