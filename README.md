```
How does migration 059 reach prod? Read .gitlab-ci.yml and run-migrations.sh and tell me:
1. Which job runs the Alembic migrations, on which branches, and whether it's automatic or manual.
2. Whether the deploy job is guaranteed to start only after the migration job succeeds
   (stage order or needs:). If not, what should change.
3. Which schema it migrates on prod (it must be ai_marketplace), and where that comes from.
4. How to confirm after the merge that 059 applied: the read-only query to check the
   alembic version and that plugin_versions.skill_md_renderer exists and
   onboarding-context-pack 1.0.8 is 'legacy' in ai_marketplace.
Don't change anything; report first.
```
