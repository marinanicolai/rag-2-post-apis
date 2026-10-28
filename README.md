```
  $tools = "C:\Users\M3MXN08\repo\dlp-installer"
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash
$sha
```
