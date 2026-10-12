```
    export PGOPTIONS='-c default_transaction_read_only=on'
   psql "$DATABASE_URL" -f ~/compare_dev_prod.sql > ~/compare_dev_prod.out 2>&1
```
