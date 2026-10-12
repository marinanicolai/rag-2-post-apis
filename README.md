```
Update tmp/sync_precheck.sql only. Add an authors section: for each author referenced by the rows that will be copied (published dev skills not in prod, published dev hooks, and the published version of plugin onboarding-context-pack), show dev user id, dev username, dev display/full name, dev email, matched prod user id (match by email, then username), prod display/full name, and name_differs = true when the display names differ (or prod match is missing). Also list which author-related columns exist on skills, hooks, plugins, plugin_versions (FK and free-text like author_name) and whether author_name is copied verbatim. Use column names you already know from the file; open only libs/db/skillhub_db/models/user.py (or wherever User is) if needed. Keep it read-only, SELECTs only, before the final ROLLBACK. Print the new line count when done.
```
```
git switch tmp/compare-sql
git add -f tmp/sync_precheck.sql
git commit -m "tmp: prod sync precheck (do not merge)"
git push
git switch -
```
