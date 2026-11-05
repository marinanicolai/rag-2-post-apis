```
ls -l ~/.git-credentials
git config --global --get credential.helper
git config --global --unset credential.helper
rm -f ~/.git-credentials
```
```
   git add docs/script-support/adr-amendment.md docs/script-support/IMPLEMENTATION-GUIDE.md
   git commit -m "Add ADR amendment and implementation guide"
   git push
```
