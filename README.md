```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
Select-String client\*.py -Pattern "CLAUDE_PLUGIN_ROOT|DLP_PACK|parent.parent" | Select-Object -First 8 | ForEach-Object { "$($_.Filename):$($_.LineNumber): $($_.Line.Trim())" }
Test-Path C:\temp\c4g-test\.claude\settings.json
(Select-String "$env:USERPROFILE\.claude\settings.json" -Pattern '"hooks"').Count
```
