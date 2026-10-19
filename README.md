```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
```
```
$sha = (Get-FileHash C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json -Algorithm SHA256).Hash
```
```
python C:\Users\M3MXN08\repo\dlp-installer\install.py --manifest C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json --manifest-sha256 $sha --source .
```
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```
