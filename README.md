```
$dst = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\classification.py"
Copy-Item $dst "$dst.bak"
Copy-Item .\client\classification.py $dst -Force
```
