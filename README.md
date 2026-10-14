
```
New evidence: Ben's row exists in prod and matches dev.
prod: id 2530ffd9-a08d-5a78-9091-5dba8eda2411, username m1bcm03, email m1bcm03@frb.gov, kerberos_principal NULL, role User, created_at 2026-10-14 10:10 (today, so auto-create worked), last_login_at NULL.
dev: same id/username/email, kerberos_principal m1bcm03@BOARD.WIN.FRB.GOV.
So it's not a users_pkey/email collision. His requests still 500 on /users/me, /profile/me, /notifications and 401 on /auth/whoami; kerberos_principal and last_login_at never get saved, so something fails after the lookup and rolls back.

Read-only. Trace the request path after the user is found: what auth.py does next (updating kerberos_principal / last_login_at, session/JWT creation, role/admin_scopes handling), and what /users/me, /profile/me and /notifications load (related tables, NOT NULL or enum columns, joins). List every place that would raise for a freshly auto-created user with NULLs in these columns, or for a principal in the BOARD.WIN.FRB.GOV realm vs RB.WIN.FRB.ORG (other users have RB.WIN.FRB.ORG). Give me read-only SQL to compare his prod row's columns with a working user's row, and with any related tables those endpoints read. Don't change anything.
```
