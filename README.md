```
git add libs/db/migrations/versions/058_add_plugin_publish_data_model.py libs/db/skillhub_db/models/publishing.py libs/db/skillhub_db/models/plugin.py libs/db/skillhub_db/models/__init__.py apps/api/tests/models/test_publishing_models.py apps/api/tests/migrations/test_058_publish_data_model.py
git commit -m "feat: migration 058, plugin publish data model (publish fields, scan_results, review_events, jobs)"
git rebase origin/main
git push -u origin feature/publish-data-model
```

