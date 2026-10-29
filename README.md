```
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```
```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
git stash
git switch --detach inference-hook-dlp--v0.2.1
Move-Item .\dist\inference-hook-dlp.zip C:\Users\M3MXN08\repo\ -Force -ErrorAction SilentlyContinue
$tools = "C:\Users\M3MXN08\repo\dlp-installer"
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```
