```
Diff is OK. Commit with your message. Leave osec for a follow-up after I check the staff names.
Before pushing: git fetch, and if origin/main now includes the test:api CI job, rebase fix/division-slug-map onto origin/main. Then push and give me the MR link. In the MR description, include: root cause (rr/rb slugs from bf41b71 vs live rs/rbops, users_division_fkey failure on commit), the guard, the migration 003 drift follow-up, and that the seed_data import in libs/db tests is broken (separate issue).
```
