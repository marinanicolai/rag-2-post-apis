```
cd C:\temp\c4g-test
claude plugin marketplace add https://gitlab.frb.gov/ai-program/platforms/tech-enablement/coding-tools/c4g-dlp-hooks-repo.git
claude plugin install inference-hook-dlp@frb-infosec --scope project
claude plugin list
```
```
  Get-Item "$env:USERPROFILE\.claude\plugins\marketplaces\frb-infosec\.claude\guides\SECURITY_AND_DATA_HANDLING.md" | Format-List FullName, Attributes, Length
```
