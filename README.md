```
git diff -- .gitlab/ci/deploy-prod.yml .gitlab/ci/deploy-prod-fresh.yml
```

```
git tag --sort=-creatordate | Select-Object -First 5
```

```
git add .gitlab/ci/deploy-prod.yml .gitlab/ci/deploy-prod-fresh.yml
git commit -m "ci: restrict prod deploy jobs to main"
git push
```
