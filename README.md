```
Select-String -Path "$env:USERPROFILE\.claude\settings.json", "$env:USERPROFILE\.claude\plugins\*.json" -Pattern 'inference-hook-dlp' -SimpleMatch
claude plugin list
```
```
Select-String -Path deploy\*, scripts\*, rescue-tool\* -Pattern 'inference-hook-dlp\plugin', 'LOCALAPPDATA' -SimpleMatch | Select-Object Path, LineNumber -Unique
```
