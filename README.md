```
$cwc = "$cw\client\classification.py"
$cwr = "$cw\restrictions\restricted-paths.md"
Copy-Item $cwc "$cwc.bak"
Copy-Item $cwr "$cwr.bak"
Copy-Item .\client\classification.py $cwc -Force
Copy-Item .\restrictions\restricted-paths.md $cwr -Force
```
