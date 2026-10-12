```
unset PGOPTIONS
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f /tmp/$USER-cmp/sync_prod_from_dev.sql > /tmp/$USER-cmp/dryrun.out 2>&1
grep -n ERROR /tmp/$USER-cmp/dryrun.out
tail -60 /tmp/$USER-cmp/dryrun.out
```
