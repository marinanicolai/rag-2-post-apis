```
git show HEAD | Out-File -Encoding utf8 last-commit.diff
git grep -n "restore-map\|load_rules\|labels\|patterns" -- "*.py" | Out-File -Encoding utf8 loader-search.txt
```
