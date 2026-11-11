```
Looks good. One update first: CI now sets DOCS_BASE_PATH for both environments (build:docs = dev path, build:docs:prod = prod path, passed in via docker run -e), so please update that stale comment at the top of config.ts. Then commit and push the branch.
```
