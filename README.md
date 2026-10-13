```
   git grep -n "join(PluginVersion\|join(Plugin\b\|join(models.Plugin" -- apps libs
```
```
   cd apps\api
   .\.venv\Scripts\python.exe -m pytest tests\models\test_publishing_models.py -q -p no:cacheprovider --no-cov --tb=short
```

