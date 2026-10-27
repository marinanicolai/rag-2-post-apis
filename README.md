```
Select-String -Path client\hook.py -Pattern "Segment\(" | Select-Object LineNumber, Line
```
