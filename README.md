```
SELECT s.display_id, s.created_at, s.name,
       left(s.content, 3) = '---' AS has_frontmatter,
       length(s.description) AS desc_len
FROM ai_marketplace.submissions s
WHERE s.status = 'admin_review'
ORDER BY s.created_at DESC
LIMIT 10;
```
