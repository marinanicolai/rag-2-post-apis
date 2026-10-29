```
$cw = (Get-ChildItem "$env:LOCALAPPDATA\Claude-3p" -Recurse -Filter dlp_hook_launcher.ps1 -ErrorAction SilentlyContinue | Select-Object -First 1).Directory.Parent.FullName
$cw
Test-Path "$cw\restore-map.json"
Select-String -Path "$cw\restrictions\classification-ceiling.md" -Pattern "SAMPLEID|TERM\d|INTERNAL|RESTRICTED" | Select-Object -First 5 Line
```
