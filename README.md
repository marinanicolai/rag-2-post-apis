```
Confirmed: search_path = ai_marketplace_dev, current_database = ocaio. I'm connected on the dev server via psql. Write the Step 1 read-only investigation queries (skills + hooks duplicates with dependent-row counts). Put them in one .sql file that starts with SET search_path TO ai_marketplace_dev; so I can run it with psql -f and paste the output back.
```


```
psql "$DEV_DATABASE_URL" -f dedup_investigation.sql
```
