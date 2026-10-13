```
git push origin --delete ci/deploy-dev-main-only
git branch -D ci/deploy-dev-main-only
```
```
git switch -c fix/test-deploy-rule origin/main
git commit --allow-empty -m "test: check deploy:dev is manual on branches"
git push -u origin fix/test-deploy-rule
```

