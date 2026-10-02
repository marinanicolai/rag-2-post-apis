```
Get-ChildItem $HOME -Recurse -Filter "word-labeled*" -ErrorAction SilentlyContinue | Select-Object FullName
```
