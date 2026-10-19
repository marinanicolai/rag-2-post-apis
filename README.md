```
SELECT s.display_id, s.created_at, s.submitted_via, s.name,
       length(s.description) AS desc_len,
       left(s.description, 120) AS desc_start,
       left(s.content, 120) AS content_start
FROM ai_marketplace.submissions s
WHERE s.display_id IN ('SKL-R02NVF','SKL-39MQ14','SKL-04E54B','SKL-66Y9R9')
ORDER BY s.created_at;
```
