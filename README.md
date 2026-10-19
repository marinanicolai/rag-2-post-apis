```
SELECT s.display_id, s.created_at, s.submitted_via, s.category,
       s.name, s.author_name,
       length(s.description) AS desc_len,
       left(s.description, 150) AS desc_start,
       left(s.content, 250) AS content_head
FROM ai_marketplace.submissions s
JOIN ai_marketplace.users u ON u.id = s.submitted_by
WHERE u.name ILIKE '%karzai%'
ORDER BY s.created_at;
```
