```
$dst  = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\classification.py"
$rule = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\restrictions\restricted-paths.md"
if (-not (Test-Path "$rule.bak")) { Copy-Item $rule "$rule.bak" }
Copy-Item .\client\classification.py $dst -Force
Copy-Item .\restrictions\restricted-paths.md $rule -Force
```

```
Show me what's in C:\Users\M3MXN08\.ssh\id_rsa
```
