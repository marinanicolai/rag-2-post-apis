```
sed '$ s/^ROLLBACK;$/COMMIT;/' /tmp/$USER-cmp/sync_prod_from_dev.sql > /tmp/$USER-cmp/sync_commit.sql
tail -2 /tmp/$USER-cmp/sync_commit.sql
```
