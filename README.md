```
$src = "$env:USERPROFILE\.claude\plugins\marketplaces\frb-infosec\.claude\guides\SECURITY_AND_DATA_HANDLING.md"
Copy-Item $src "$env:TEMP\copytest.md"; "copy ok: $(Test-Path $env:TEMP\copytest.md)"
Select-String $src -Pattern "RESTRICTED|CONFIDENTIAL|CLASSIFIED|SSN|\d{3}-\d{2}-\d{4}" | Select-Object -First 5 | ForEach-Object { "$($_.LineNumber): $($_.Line.Trim())" }
```
