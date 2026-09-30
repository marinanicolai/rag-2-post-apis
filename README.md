```
ls /tmp/investigate_duplicates.sql
psql "$DEV_DATABASE_URL" -c "SET search_path TO ai_marketplace_dev;" -f /tmp/investigate_duplicates.sql > /tmp/investigate_output.txt 2>&1
cat /tmp/investigate_output.txt
```


```
psql "$DEV_DATABASE_URL" -f dedup_investigation.sql
```
