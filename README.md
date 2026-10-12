```
   head -5 ~/compare_dev_prod.sql      # should start with BEGIN TRANSACTION READ ONLY;
   psql "$DATABASE_URL" -f ~/compare_dev_prod.sql > ~/compare_dev_prod.out 2>&1
   less ~/compare_dev_prod.out
```
