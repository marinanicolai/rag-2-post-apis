

```
cp /tmp/cleanup_preview.txt ~/cleanup_preview_$(date +%Y%m%d).txt

```

```
psql "$DEV_DATABASE_URL" -f /tmp/cleanup_duplicates.sql > /tmp/cleanup_result.txt 2>&1
tail -20 /tmp/cleanup_result.txt
```
