```
   $cw = (Get-ChildItem "$env:LOCALAPPDATA\Claude-3p" -Recurse -Filter dlp_hook_launcher.ps1 | Select-Object -First 1).Directory.Parent.FullName
$cw
Get-ChildItem $cw -Recurse -Include *.py,*.exe,restricted-paths.md | Select-Object FullName
```
