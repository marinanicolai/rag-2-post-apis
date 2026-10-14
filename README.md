```
-- divisions in dev that are missing from prod
SELECT slug FROM ai_marketplace_dev.divisions
EXCEPT
SELECT slug FROM ai_marketplace.divisions;

-- Ben's division in dev (where enrichment succeeded)
SELECT username, division, department FROM ai_marketplace_dev.users WHERE username = 'm1bcm03';

-- how many divisions each side has
SELECT 'prod' AS env, count(*) FROM ai_marketplace.divisions
UNION ALL
SELECT 'dev', count(*) FROM ai_marketplace_dev.divisions;
```
