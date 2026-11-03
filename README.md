```
go dev. Apply 059 to ai_marketplace_dev only. Then show me:
1. SELECT version_num FROM alembic_version;  (expect 059)
2. SELECT count(*) FROM plugin_versions WHERE content_hash IS NOT NULL AND skill_md_renderer <> 'legacy';  (expect 0)
3. The audit: scripts/audit_plugin_renderer_hashes.py --schema ai_marketplace_dev  (markers should no longer say "no column yet")
Don't touch ai_marketplace. Then remove ~/scratch/mig-059, ~/scratch/mig-059-venv, probe.py and render059.py.
```
