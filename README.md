```
grep -E '^INITIAL_ADMINS' /ai/www/cgi-bin/ai-marketplace/.env
export PGOPTIONS='-c default_transaction_read_only=on'
psql "$DATABASE_URL" -c "SELECT 'prod' env, username, role, is_platform_team, is_security_team, admin_scopes FROM ai_marketplace.users WHERE lower(username)='m3mxn08' UNION ALL SELECT 'dev', username, role, is_platform_team, is_security_team, admin_scopes FROM ai_marketplace_dev.users WHERE lower(username)='m3mxn08';"
```
```
git grep -n "INITIAL_ADMINS" -- apps libs
```
