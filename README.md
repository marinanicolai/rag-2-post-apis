```
Select-String -Path client\hook.py -Pattern "pack\s*=|load_pack|load_ruleset|RuleStore"
Get-Content app\rules.py | Select-Object -Skip 312 -First 50
```
