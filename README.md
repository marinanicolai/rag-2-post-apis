```
$cw = (Get-ChildItem "$env:LOCALAPPDATA\Claude-3p" -Recurse -Filter dlp_hook_launcher.ps1 -ErrorAction SilentlyContinue | Select-Object -First 1).Directory.Parent.FullName
$cw
```
