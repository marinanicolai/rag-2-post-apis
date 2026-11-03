```
git fetch
git show origin/main:.gitlab/ci/deploy-prod.yml | Select-String -Pattern "stage|rules|only|alembic|upgrade|extract|deploy-from|set -e|exit" -Context 0,1
```
