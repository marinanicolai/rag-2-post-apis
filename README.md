```
SELECT s.status, left(s.content, 3) = '---' AS has_frontmatter, count(*)
FROM ai_marketplace.submissions s
GROUP BY 1, 2
ORDER BY 1, 2;
```
