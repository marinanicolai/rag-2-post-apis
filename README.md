```
$lines = Get-Content .\client\hook.py
165..235 | ForEach-Object { "{0}: {1}" -f $_, $lines[$_-1] }
```
