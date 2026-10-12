```
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f /tmp/$USER-cmp/sync_commit.sql > /tmp/$USER-cmp/commit.out 2>&1
grep -c ERROR /tmp/$USER-cmp/commit.out
tail -3 /tmp/$USER-cmp/commit.out
```
