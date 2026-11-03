```
Prod audit on salt1 at 520098b, --schema ai_marketplace (database ocaio):
1 version: WOULD-CHANGE it/onboarding-context-pack@1.0.8 [published],
stored=5556904bb070 legacy=5556904bb070 v2=5e544cd6419f. No DRIFT, no NO-HASH.
summary {"WOULD-CHANGE": 1}. Exit code: [fill in].

Update PROGRESS.md: record this as the prod audit, close the "prod audit
outstanding" item, and rewrite the merge-request checklist. Migration 059 must be
applied before the code deploys (1.0.8 depends on the legacy freeze), and drop the
"expect exit code 1 / DRIFT rows" note for prod. Leave uncommitted for my review.
```

