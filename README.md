```
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```
```
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source .
```
```
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```
