```
Prod investigation, read-only. Don't change code, config or data.

User m1mlc04 (Missy Clark, an admin) looks correct in dev (name "Clark, Melissa Louise", email missy.l.clark@frb.gov, division it) but in prod shows placeholder values: name "M1MLC04", email m1mlc04@frb.gov, division unknown, last login empty. So her prod row was never enriched from the staff directory. Her division (IT -> it) is a valid slug, so this is not the rr/rs bug.

1. When does enrichment run? Only on login (auth.py before_request), or also via an admin action, scheduled job or backfill script? Does it skip rows that already exist, or rows with has_enrichment_fields / staff_data_last_updated_at set?
2. What can turn enrichment off or break it in prod: the STAFF_ENRICHMENT_ENABLED setting (tell me how to check its value in prod's .env without printing other secrets), the boardstaff/bankstaff DB connection (pgreader@sql) being unreachable from the prod web server, or anything else that differs between dev and prod config.
3. Give me read-only SQL to compare her prod and dev rows (all enrichment columns: name, display_name, email, division, department, has_enrichment_fields, enriched_on, staff_data_last_updated_at, last_login_at, kerberos_principal, created_at), and to count how many prod users are in the same placeholder state.
4. Propose the fix options with tradeoffs:
   a. she simply logs in to prod (if enrichment works on login),
   b. a one-off backfill that runs the app's own enrichment for placeholder users (read-only preview first, then a guarded write),
   c. copying enrichment fields from her dev row (guarded one-row UPDATE).
Don't run anything; give me the commands and SQL.
```
