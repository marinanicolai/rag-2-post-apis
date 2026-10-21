```
SELECT s.name, v.id, left(v.content, 200) AS content_start
FROM ai_marketplace.skills s
JOIN ai_marketplace.skill_versions v ON v.skill_id = s.id
WHERE s.name ILIKE '%grill%';
```
```
\d ai_marketplace.skills
\d ai_marketplace.skill_versions
```
