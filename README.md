You're in the shell, so start psql first. Type these one at a time:

```
psql "$DATABASE_URL"
```
Wait for the `ocaio=>` prompt, then:
```
SET default_transaction_read_only = on;
```
Then paste the two queries, with Ben's real domain filled in:
```sql
SELECT id, username, email, created_at
FROM ai_marketplace.users
WHERE lower(email) = 'ben.miller@<domain>';

SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'ai_marketplace' AND column_name ILIKE '%email%';
```

If `psql` says `DATABASE_URL` is empty, it's because this is a new terminal. Load it the same way you did before, from prod's `.env`. Send me a screenshot of the results.
