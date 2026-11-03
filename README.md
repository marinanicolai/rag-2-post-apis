```
git checkout main
git pull
git checkout -b fix/profile-sync-enrich-user
```
```
New item on branch fix/profile-sync-enrich-user (from main).
Earlier you found that users.py (POST /profile/sync) calls
staff_lookup.enrich_user(user) at module level, but staff_lookup.py only defines
it as a method on StaffLookupService. That suggests the endpoint always fails.

1. Confirm it: read users.py and staff_lookup.py and git log/blame both to see when
   they diverged and whether anything else calls enrich_user.
2. Tell me what profile sync is supposed to do, who calls it (frontend, cron,
   login), and what users see when it fails.
3. Give me a read-only way to confirm it fails in prod (a log grep I can run on salt1,
   or a safe request), with no writes.
4. Plan the fix: the correct way to call StaffLookupService, and a test that would
   have caught this (one that does NOT patch enrich_user away).
Plan only, no code yet. Note: the DLP hook may block you from running Python, so
give me the pytest commands to run myself.
```
