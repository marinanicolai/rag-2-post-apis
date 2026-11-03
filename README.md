```
Yes, start with the red tests in tests/blueprints/test_profile_sync.py and give me
the commands; I'll run them and paste the output.
Plan for the overlap: fix/download-skill-500-traceback merges first. After it does,
I'll merge main into this branch, and then you update TestProfileSync500 to patch
StaffLookupService.lookup_user instead of enrich_user with create=True.
Add this bug's own dated entry in PROGRESS.md on this branch.
```
