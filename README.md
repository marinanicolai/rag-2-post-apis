```
bash
export DEV_DATABASE_URL='postgresql://skillhub_user:REAL_PASSWORD@REAL_HOST:5432/REAL_DB?options=-csearch_path%3Dai_marketplace_dev'
psql "$DEV_DATABASE_URL" -c "SHOW search_path;" -c "SELECT current_database();"
```


```
psql "$DEV_DATABASE_URL" -c "SET search_path TO ai_marketplace_dev;" -c "SHOW search_path;" -c "SELECT current_database();"
```
