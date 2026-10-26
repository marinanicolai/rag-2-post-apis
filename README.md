```
Select-String -Path "$env:USERPROFILE\.claude\settings.json", "$env:USERPROFILE\.claude\plugins\*.json" -Pattern 'inference-hook-dlp' -SimpleMatch
claude plugin list
```
