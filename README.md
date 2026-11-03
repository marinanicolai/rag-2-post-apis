```
../../.venv/Scripts/python.exe -m pytest tests/blueprints/test_profile_sync.py tests/test_division_slug_map.py -q -p no:cacheprovider
```
```
cd ..\..
git status
git add -A
git commit -m "Fix profile sync: call enrich_user through StaffLookupService"
git push -u origin fix/profile-sync-enrich-user
```
