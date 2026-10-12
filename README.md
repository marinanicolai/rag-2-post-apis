```
Use one author-match rule everywhere (precheck sections 4 and 11, and the sync script): lowercased email, then lowercased username, then kerberos_principal. Update the precheck accordingly, then write tmp/sync_prod_from_dev.sql now using that rule and the column names you already used. Don't re-explore the repo. End with ROLLBACK and the DRY RUN comment. Print path and line count when done.
```
```
git switch tmp/compare-sql
git add -f tmp/sync_precheck.sql
git commit -m "tmp: prod sync precheck (do not merge)"
git push
git switch -
```
