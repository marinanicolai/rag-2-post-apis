```
setenv PGOPTIONS "-c default_transaction_read_only=on"
psql
```
```
SELECT count(*) AS pinned_hooks FROM plugin_version_hooks WHERE plugin_version_id = (SELECT pv.id FROM plugin_versions pv JOIN plugins p ON p.id = pv.plugin_id WHERE p.slug = 'testnicolai' AND pv.version = '1.0.0');
```
