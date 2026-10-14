```
Prod bug: one user (Kerberos auth) can't use Skillhub since about a week ago; others can. His browser console shows:
- public endpoints OK: /api/v1/tags, /api/v1/flags
- 500 INTERNAL SERVER ERROR on /api/v1/profile/me, /api/v1/users/me, /api/v1/notifications, sometimes /skills and /categories/with-counts
- 401 on /auth/whoami, /skills, /categories/with-counts in another attempt
So Kerberos likely works and the app crashes when resolving or creating his user row.

Context: on Oct 12 prod was restored from an old snapshot, then a one-time SQL sync inserted 24 skills, 6 hooks, 1 plugin, 3 users, 3 categories from dev into prod with explicit ids.

Hypothesis to check first: the sync inserted explicit ids but didn't advance the Postgres sequences, so auto-creating his user (he may be missing from the restored snapshot) fails with a duplicate key on the primary key. Also possible: a duplicate username that differs by case/realm, or a row that conflicts with one of the 3 synced users.

Read-only, don't change anything:
1. Trace what happens on an authenticated request: where the Kerberos principal is read, how it maps to a users row, whether a missing user is auto-created (file:line), and what errors become 500 vs 401.
2. Give me read-only SQL for prod:
   a. his users row(s) by username, case-insensitive and with/without realm suffix
   b. for every table the sync touched (users, skills, hooks, plugins, categories, and any join/version tables it inserted into): SELECT max(id) and the sequence's last_value (pg_get_serial_sequence), so I can see which sequences are behind
3. Tell me the server log location and a grep command for his username and for "duplicate key" / "IntegrityError" / "Traceback" around his request times.
Then give the likely cause with evidence and a guarded fix: for sequences, one SELECT setval(pg_get_serial_sequence('<table>','id'), (SELECT max(id) FROM <table>)) per affected table, inside BEGIN ... show before/after ... then I choose COMMIT or ROLLBACK. Don't run anything on prod yourself.
```
