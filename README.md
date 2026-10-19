```
Get-Item C:\Users\M3MXN08\repo\dlp-installer\*.py | Select-Object Name, Length
```
```
   $sha = (Get-FileHash C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json -Algorithm SHA256).Hash
   python C:\Users\M3MXN08\repo\dlp-installer\install.py --manifest C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```
