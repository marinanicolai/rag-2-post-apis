```
$rule = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\restrictions\restricted-paths.md"
Copy-Item $rule "$rule.bak"
Copy-Item .\restrictions\restricted-paths.md $rule -Force
```
