```
There is no separate read-only account. The only login is DATABASE_URL (the app's,
ocaio_admin). Don't use it yourself. Instead, write me the exact Q2 SQL, built from the
models (correct column names), that finds the author of skill slug frontend-board-design
in ai_marketplace_dev and shows only: user id, username/M1 id, display name, division,
job_title, enriched_on (or whatever the enrichment timestamp column is). No password,
token or email columns. Wrap it in BEGIN READ ONLY; ... ROLLBACK;. I'll run it in psql
and paste the result. Also give me the grep for Q4 (log lines for that M1 id) that I can
run myself once we have the id.
Skip Q6: don't read pgreader's password. If the row and logs don't settle it, I'll ask
whoever owns the staff DB.
```
```
bash
psql "$DATABASE_URL"
```
