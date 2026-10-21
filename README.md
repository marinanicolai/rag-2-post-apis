```
SELECT name, left(content, 200) AS content_start
FROM ai_marketplace.skills
WHERE name ILIKE '%grill%';
```
