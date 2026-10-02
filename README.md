```
           - {type: pytest, select: [uninspectable, without_label, image_is_blocked, png]}
```
```
Select-String -Path docs\risks.yaml -Pattern "image_is"
python scripts\risk_register.py
python -m pytest tests -q
git status --short
```
