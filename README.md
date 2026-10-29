```
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source ..\c4g-v021
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```
