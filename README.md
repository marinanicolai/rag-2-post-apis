```
SELECT count(*) AS total,
       count(*) FILTER (WHERE NOT has_enrichment_fields) AS not_enriched,
       count(*) FILTER (WHERE name = upper(username)) AS placeholder_name,
       count(*) FILTER (WHERE division IS NULL OR division = 'unknown') AS no_division
FROM ai_marketplace.users;
```
