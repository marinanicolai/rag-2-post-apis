```
  On branch feature/plugins-spine in ai-marketplace. MR !18 (feature/plugins-spine → main) is blocked: "Merge blocked: 1 check failed — Pipeline must succeed." Pipeline #225723 shows "waiting for manual action". deploy:dev passed; deploy:prod and deploy:prod:fresh-install are manual and were NOT run (and must not be run). fresh-install shows "allowed to fail"; deploy:prod does not.

Goal: make feature-branch pipelines complete without anyone clicking a prod job, and restrict prod deploys to main.

Rules:
- Do NOT trigger, retry, or play any pipeline job. Do NOT push. Do NOT run Python.
- Never print, copy, or echo credential values from any CI file. If a file contains literal secrets, leave those lines untouched and just tell me the file and line number.
- If the DLP hook blocks you from reading .gitlab/ci/deploy-prod.yml or .gitlab/ci/deploy-prod-fresh.yml, don't work around it. Instead, give me the exact edit to make by hand (job name, what to replace, new YAML).

Investigate:
1. In .gitlab-ci.yml and all included files under .gitlab/ci/, list every job with `when: manual` (in rules or at job level), its branch conditions, and whether allow_failure is true. Note: inside `rules:`, manual jobs default to allow_failure: false, which blocks the pipeline.
2. Confirm which job(s) put pipeline #225723 into "blocked/manual" state.

Fix:
3. deploy:prod: rules → only `$CI_COMMIT_BRANCH == "main"`, `when: manual`, `allow_failure: true`. No rule for any other branch.
4. deploy:prod:fresh-install: same restriction (main only, manual, allow_failure: true).
5. Any other manual job that would block feature-branch pipelines: report it, don't change it unless it's prod-related.
6. Don't change deploy:dev, build, test, or package jobs.

Then show me: the diff (or hand-edit instructions), what the pipeline for feature/plugins-spine will look like after the change (which jobs run, which don't appear), and the git commands to commit with message "ci: restrict prod deploy jobs to main".
```
