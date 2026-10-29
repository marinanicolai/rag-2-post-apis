```
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```
```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
git worktree add ..\c4g-v021 inference-hook-dlp--v0.2.1
$tools = "C:\Users\M3MXN08\repo\dlp-installer"
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source ..\c4g-v021 --dry-run
```
