```
Investigate a prod bug on this server (salt1). Read-only: do not edit files, restart services, change the database, or print secrets.

Environment facts:
- Shell is tcsh/csh by default; run commands under bash (bash -c '...') so 2>&1 and 2>/dev/null work.
- Skillhub (ai-marketplace) is a Python CGI app at /ai/www/cgi-bin/ai-marketplace, served by Apache at https://fweb.rsma.frb.gov/ai/cgi-bin/ai-marketplace/ai-marketplace.cgi. Apache runs on this host (httpd/apache2 processes exist), but /var/log/apache2 and /var/log/httpd don't exist, so it's a custom install.
- Auth: Kerberos SSO in Apache (.htaccess), the app maps the principal to a row in ai_marketplace.users and auto-creates the user if missing (auth.py:126-143). User ids are deterministic UUIDs from the principal.
- Database: Postgres database ocaio, prod schema ai_marketplace, dev schema ai_marketplace_dev. Prod was reset to an old snapshot over the weekend, then on Oct 12 we synced some users/skills/hooks/plugins from dev.

Problem: user Ben Miller gets HTTP 500 on /api/v1/users/me, /profile/me, /notifications and 401 on /auth/whoami. Others work. Hypothesis: auto-create fails with a unique violation (users_pkey or users_email_key) because a conflicting row exists under a different username/email form.

Steps:
1. Find the Apache install and its log files: ps -eo user,pid,cmd for httpd/apache2, then the binary's -S output and ErrorLog/CustomLog in its config. Report the error log and access log paths.
2. In the error log, for today only: count "violates unique constraint" by constraint name, and show the 5 most recent IntegrityError/duplicate key/Traceback blocks related to ai-marketplace (include the "Key (...)=(...)" detail line). Redact any tokens, cookies, Authorization headers or connection strings before showing output.
3. In the access log, find Ben's requests today (Kerberos principal is in the user field; search case-insensitively for "miller" or his principal) and show time, path, status.
4. Give me read-only SQL (I'll run it in psql with SET default_transaction_read_only = on) to show every ai_marketplace.users row that conflicts with Ben: same id (compute the UUID the app would generate for his principal, using the same function as auth.py), same email, or same principal ignoring case/realm. Show the same for ai_marketplace_dev.users.
5. Conclude: which constraint fails, which existing row blocks him, and a guarded fix (BEGIN; before SELECT; one targeted UPDATE or DELETE by id; after SELECT; I choose COMMIT or ROLLBACK). Don't run any write.
```

