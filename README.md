

```
   Write the cleanup script now as a file in /tmp: SET search_path TO ai_marketplace_dev; at the top, a preview SELECT of every row that will change, then the UPDATEs (status = 'removed', re-point installs/votes/reviews to the kept row) inside BEGIN ... ROLLBACK so the first run changes nothing.


```

```
   psql "$DEV_DATABASE_URL" -f /tmp/cleanup_duplicates.sql
```
