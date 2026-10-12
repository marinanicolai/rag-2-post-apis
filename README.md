```
git diff -- .gitlab/ci/deploy-prod.yml .gitlab/ci/deploy-prod-fresh.yml
# Which schema does prod's app actually use? (no password shown)
grep -E '^DATABASE_URL' /ai/www/cgi-bin/ai-marketplace/.env | sed -E 's#://[^@]*@#://***@#'

# Skills, hooks, plugins in each schema
psql "$DATABASE_URL" -c "
SELECT 'prod' env, (SELECT count(*) FROM ai_marketplace.skills) skills,
       (SELECT count(*) FROM ai_marketplace.hooks) hooks,
       (SELECT count(*) FROM ai_marketplace.plugins) plugins
UNION ALL
SELECT 'dev', (SELECT count(*) FROM ai_marketplace_dev.skills),
       (SELECT count(*) FROM ai_marketplace_dev.hooks),
       (SELECT count(*) FROM ai_marketplace_dev.plugins);"

# Skill status breakdown in prod
psql "$DATABASE_URL" -c "SELECT status, count(*) FROM ai_marketplace.skills GROUP BY status;"
```
