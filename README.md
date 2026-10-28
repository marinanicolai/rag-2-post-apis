```
$cw
Get-ChildItem "$env:LOCALAPPDATA\Claude-3p" -Recurse -Filter dlp_hook_launcher.ps1 -ErrorAction SilentlyContinue | Select-Object FullName
```
```
Select-String -Path scripts\build_zip.py -Pattern "tests|sample|exclude|include|glob" | Select-Object LineNumber, Line
```
