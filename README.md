```
SELECT string_agg(slug, ',' ORDER BY slug) FROM ai_marketplace.divisions;
```
```
SELECT column_name, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_schema = 'ai_marketplace' AND table_name = 'users'
  AND column_name IN ('email','name','first_name','last_name','preferred_name','display_name',
                      'job_title','department','phone','photo_url','supervisor_name','supervisor_email','division','role');
```
