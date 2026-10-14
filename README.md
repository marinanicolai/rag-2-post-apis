```
DO $$
DECLARE r record; mx bigint; lv bigint;
BEGIN
  FOR r IN
    SELECT c.relname AS tbl, a.attname AS col,
           pg_get_serial_sequence(quote_ident(n.nspname)||'.'||quote_ident(c.relname), a.attname) AS seq
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
    WHERE c.relkind = 'r' AND n.nspname = 'public'
      AND pg_get_serial_sequence(quote_ident(n.nspname)||'.'||quote_ident(c.relname), a.attname) IS NOT NULL
  LOOP
    EXECUTE format('SELECT max(%I) FROM %I', r.col, r.tbl) INTO mx;
    EXECUTE format('SELECT last_value FROM %s', r.seq) INTO lv;
    IF mx IS NOT NULL AND lv < mx THEN
      RAISE NOTICE 'BEHIND: %.% max=% seq=% (%)', r.tbl, r.col, mx, lv, r.seq;
    END IF;
  END LOOP;
  RAISE NOTICE 'check done';
END $$;
```
