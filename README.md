
```
\x
SELECT 'prod' AS env, * FROM ai_marketplace.users
WHERE username ILIKE '%miller%' OR email ILIKE '%miller%'
   OR username ILIKE '%mcclennan%' OR email ILIKE '%mcclennan%';

SELECT 'dev' AS env, * FROM ai_marketplace_dev.users
WHERE username ILIKE '%miller%' OR email ILIKE '%miller%'
   OR username ILIKE '%mcclennan%' OR email ILIKE '%mcclennan%';
```
