```
Get-ChildItem $cw -Recurse -Include *.py,*.exe,restricted-paths.md | ForEach-Object { $_.FullName.Substring($cw.Length) }
```
