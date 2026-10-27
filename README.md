```
Select-String -Path $pack -Pattern "id: restricted-paths" -Context 0,10
```
```
Select-String -Path "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\pack.py" -Pattern "rules.pack|PACK_|environ|cache" | Select-Object LineNumber, Line
```
