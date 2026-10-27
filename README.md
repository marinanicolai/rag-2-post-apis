```
Select-String -Path client\hook.py,client\classification.py,config\rules.pack.yaml -Pattern "restricted|\.ssh|id_rsa|build_path|PathDetector" | Select-Object Path, LineNumber, Line
```
