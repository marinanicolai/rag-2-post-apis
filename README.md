```
unset PGOPTIONS
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 <<'SQL'
BEGIN;
DO $$
DECLARE n int;
BEGIN
  UPDATE ai_marketplace.users
     SET role = 'admin', is_platform_team = true, updated_at = now()
   WHERE lower(username) = 'm3mxn08';
  GET DIAGNOSTICS n = ROW_COUNT;
  IF n <> 1 THEN RAISE EXCEPTION 'expected 1 row, got %', n; END IF;
END $$;
SELECT username, role, is_platform_team, is_security_team FROM ai_marketplace.users WHERE lower(username) = 'm3mxn08';
COMMIT;
SQL
```
