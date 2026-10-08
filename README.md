
```
git checkout main
git pull
git checkout scan-test -- .gitlab-ci.yml ci/semgrep/skillhub-rules.yml
git commit -m "Add Skillhub script policy rules"
git push
```
