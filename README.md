

```
Ran it — read /tmp/cleanup_preview.txt and summarize: rows that would flip to removed (skills vs hooks), any errors or constraint violations, and whether Section 8 matches what we expect. Also, for future commands, my database is ocaio and I connect with psql "$DEV_DATABASE_URL" — stop giving me the HOST/skillhub placeholder.

```

```
psql "$DEV_DATABASE_URL" -f /tmp/cleanup_duplicates.sql > /tmp/cleanup_preview.txt 2>&1
```
