```
Select-String -Path config\rules.pack.yaml -Pattern "id: restricted-paths" -Context 0,8
```
```
Get-ChildItem "$env:LOCALAPPDATA\inference-hook-dlp", "." -Recurse -Filter restricted-paths.md | Select-Object FullName
```
