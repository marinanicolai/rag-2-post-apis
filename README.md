```
git add docs/script-support/PROGRESS.md
git commit -m "Record prod renderer audit: 1 WOULD-CHANGE, no DRIFT" -m "Ran on salt1 at 520098b with --schema ai_marketplace (database ocaio).
onboarding-context-pack 1.0.8 [published]: stored hash equals legacy rebuild,
so migration 059's legacy freeze keeps it valid. No DRIFT rows in prod; both
DRIFT rows were dev only. Migration 059 must be applied before the code deploys."
git push
```
