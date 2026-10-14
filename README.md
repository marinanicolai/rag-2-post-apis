```
Ruled out on prod: id, email and username collisions (no other row), and divisions (prod and dev both have the same 15 slugs). Ben's dev row also has empty division/department, so enrichment never completed for him in dev either.
His prod row: id 2530ffd9-a08d-5a78-9091-5dba8eda2411, created today 10:10, division/kerberos_principal/last_login_at NULL.
users has: users_division_fkey (division -> divisions.slug), varchar limits (e.g. role 100, phone 50, name 255), NOT NULL on email/username/name/role/is_platform_team/is_security_team/admin_scopes.

Give me a read-only script to run on salt1 that calls the same staff enrichment lookup the app uses for m1bcm03 and prints every field it would write to the users row (especially division and role), without touching the database. Then tell me which value would violate a constraint: a division slug not in the 15, a value over its varchar limit, a NULL into a NOT NULL column, or a role the app doesn't accept.
```
