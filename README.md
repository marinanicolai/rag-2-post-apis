```
Get-ChildItem -Recurse -Include *.py,*.yaml,*.yml,*.json -Exclude *.jsonl | Select-String -Pattern "file.name|filename|classification-ceiling" -List | Select-Object Path
```
