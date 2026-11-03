```
(Select-String -Path ".\grill-me (6).md" -Pattern '^---$').Count
(Select-String -Path ".\<new grill-me file>.md" -Pattern '^---$').Count
```
