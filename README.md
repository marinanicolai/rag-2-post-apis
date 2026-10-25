```
Select-String -Path .\client\*.py, .\restrictions\PACK.md -Pattern "additionalContext|SessionStart|usage restrictions" | Select-Object Filename, LineNumber, Line
```
