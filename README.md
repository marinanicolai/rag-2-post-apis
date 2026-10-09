
```

Select-String docs\DISTRIBUTION.md -Pattern "^#" | ForEach-Object { "$($_.LineNumber): $($_.Line)" }

```
