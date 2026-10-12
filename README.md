```
psql "$DATABASE_URL" -c "SELECT p.slug prod_slug, p.status::text prod_status, d.slug dev_slug, d.status::text dev_status FROM ai_marketplace.skills p LEFT JOIN ai_marketplace_dev.skills d ON d.slug = p.slug OR lower(d.name) = lower(p.name) ORDER BY 1;"
```
