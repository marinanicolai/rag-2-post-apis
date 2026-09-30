

```
grep -n "^ROLLBACK\|^COMMIT" /tmp/cleanup_duplicates.sql
```
```
sed -i 's/^ROLLBACK;/COMMIT;/' /tmp/cleanup_duplicates.sql
grep -n "^ROLLBACK\|^COMMIT" /tmp/cleanup_duplicates.sql
```
```
psql "$DEV_DATABASE_URL" -f /tmp/cleanup_duplicates.sql > /tmp/cleanup_result.txt 2>&1
tail -5 /tmp/cleanup_result.txt
```
