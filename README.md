```
BEGIN READ ONLY;
SELECT 'dev' AS env, count(*) FROM ai_marketplace_dev.users WHERE division = 'unknown'
UNION ALL
SELECT 'prod', count(*) FROM ai_marketplace.users WHERE division = 'unknown';
ROLLBACK;
```
```
New branch from main: fix/hide-unknown-division.
In the shared author/user identity card, don't render the division line when division is
NULL, empty, or "unknown" (case-insensitive). Keep the layout tidy when it's missing (no
stray "·" separator). Add tests for all three cases. Show me the plan first.
```
```
set -a; source /ai/www/cgi-bin/ai-marketplace/.env; set +a
echo ${DATABASE_URL:+DATABASE_URL is set}
```
PGOPTIONS="-c default_transaction_read_only=on" psql "$DATABASE_URL" -c "SELECT 'dev' AS env, count(*) FROM ai_marketplace_dev.users WHERE division = 'unknown' UNION ALL SELECT 'prod', count(*) FROM ai_marketplace.users WHERE division = 'unknown';"
```
