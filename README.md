```
grep -iE "database|postgres|DB_" .env
```


```
export DEV_DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d= -f2- | tr -d "'\"")"
psql "$DEV_DATABASE_URL" -c "SET search_path TO ai_marketplace_dev;" -c "SHOW search_path;" -c "SELECT current_database();"
```
