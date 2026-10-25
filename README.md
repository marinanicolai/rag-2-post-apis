```
python $tools\install.py --uninstall
git switch --detach inference-hook-dlp--v0.2.1
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash
$opts = @("--manifest", "$tools\approved-hashes.json", "--manifest-sha256", $sha, "--source", ".")
python $tools\install.py @opts
```
