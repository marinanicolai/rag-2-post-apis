```
git checkout main
git pull
git worktree add ..\amp-publisher -b feature/publisher-core origin/main
git worktree add ..\amp-hook-versions -b feature/hook-versions-060 origin/main
git worktree add ..\amp-llm-review -b feature/llm-review origin/main
git worktree list
```
```
Decisions: 1) yes, drop the staleness filter with --division. 2) --schema required
for every run. 3) yes, add --limit. 4) same branch.
Map: add the three "and" spellings (dcca, mfs, sr). Hold "Chief Operating Officer"
until someone confirms coo vs bdm.
Order: finish Task A first if it's not done. Then implement step 2 plus the three map
entries on feature/enrichment-unknown-check, with tests. Give me the test commands to
run. Don't commit. I'll review later today.
```
