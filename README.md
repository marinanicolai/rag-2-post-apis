```
Write the dev-vs-prod comparison SQL you designed earlier to tmp/compare_dev_prod.sql in the repo root (create the tmp folder if needed). Requirements:
- First line: BEGIN TRANSACTION READ ONLY;   Last line: ROLLBACK;
- SELECT statements only. Every table must be schema-qualified as ai_marketplace.<table> or ai_marketplace_dev.<table>.
- Sections (with a SELECT '--- section name ---'; label before each): row counts per content table in both schemas; skills/hooks/plugins in dev but not prod (by id and by slug); in prod but not dev; same slug with different id; dev authors missing from prod users; other missing FK targets; min/max created_at for skills in each schema.
- Don't connect to any database, don't run anything, don't commit.
After writing, print the full Windows path and the first 5 lines so I can confirm it exists.
```
