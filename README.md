

```
The pipeline for fix/duplicate-submissions (#213197) only has 3 stages (build, validate, package) and 7 jobs. The earlier pipeline on feature/plugins-spine had 4 stages including deploy (deploy:dev, deploy:prod, deploy:prod:fresh-install).

Investigate only — don't change .gitlab-ci.yml yet:
1. Read .gitlab-ci.yml (and any included files) and explain exactly why the deploy jobs didn't run for this branch. Quote the rules/only conditions.
2. Tell me the intended path for a fix/* branch to reach dev: merge into which branch, a manual job, a branch naming convention, etc.
3. Confirm whether there's any test job in the pipeline at all. The Tests tab shows 0, so I think pytest never runs in CI.
4. Recommend the safest way to get this fix tested on dev without deploying to prod.

Summarize the findings, then wait for me before changing anything.


```
