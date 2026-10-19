```
   Get-ChildItem $env:USERPROFILE\Downloads -Filter *.py
```
```
   Move-Item $env:USERPROFILE\Downloads\make_manifest.py, $env:USERPROFILE\Downloads\install.py $env:USERPROFILE\source\repos\dlp-installer\
```
```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
python $env:USERPROFILE\source\repos\dlp-installer\make_manifest.py --version 0.2.1 --tag inference-hook-dlp--v0.2.1 --plugin-dir . --out $env:USERPROFILE\source\repos\dlp-installer\approved-hashes.json
```
