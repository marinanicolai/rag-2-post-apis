```
build:docs and build:docs:prod fail with:
[vitepress] siteConfig.ignoreDeadLinks.some is not a function
file: apps/docs/src/backend/flask-app.md (and backend/libraries.md in the other job)

1. In config.ts, change ignoreDeadLinks from a bare function to an array: ignoreDeadLinks: [(url) => url.includes('/ai/cgi-bin/')]. VitePress 2.0 alpha expects an array.
2. That error only fires because those pages have dead links. Since there's no local build, statically check every internal link in all docs pages (relative .md links and anchors) against the files in apps/docs/src, and fix or remove the broken ones. List what you changed.
Commit locally, don't push.
```
