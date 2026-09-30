```
git checkout main
git pull
git rm -r -q .
git clean -fdx
Set-Content README.md "# skillhub-spike-test-plugin`n`nTest repo for Skillhub plugin spike."
git add -A
git commit -m "Clear repo for plugin spike testing"
git push
```
