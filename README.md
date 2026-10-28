```
$cw = (Get-ChildItem "$env:LOCALAPPDATA\Claude-3p" -Recurse -Filter dlp_hook_launcher.ps1 -ErrorAction SilentlyContinue | Select-Object -First 1).Directory.Parent.FullName
(Get-ChildItem $cw -Recurse -File).Count
Test-Path "$cw\restrictions\tests.yaml", "$cw\config\rules_tests.yaml", "$cw\scripts\make_sample_files.py"
```
```
git log cowork-support --since="5 days ago" --name-only --oneline
```
