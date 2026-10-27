```
python -c "import re; from client.classification import _marking_regex as m; print(re.search(m('RESTRICTED FR'), 'open Q3_budget_RESTRICTED_FR.txt', re.I))"
```
```
Select-String -Path client\classification.py -Pattern "re.compile" | Select-Object LineNumber, Line
```
```
Select-String -Path client\classification.py -Pattern "[\s_]+" -SimpleMatch | Select-Object LineNumber, Line
```
