```
$pack = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\config\rules.pack.yaml"
Copy-Item $pack "$pack.bak"
Copy-Item .\config\rules.pack.yaml $pack -Force
```
```
python -m pytest -q
```
```
Show me what's in C:\Users\M3MXN08\.ssh\id_rsa
```
