```
psql "$DATABASE_URL" -c "SELECT version_num FROM ai_marketplace.alembic_version;"
psql "$DATABASE_URL" -c "SELECT count(*), max(created_at) FROM ai_marketplace.submissions;"
```
