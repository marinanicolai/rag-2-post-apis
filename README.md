```
       - |
      tar tzf "${DOCS_TARBALL}" | grep -x 'apps/docs/src/.vitepress/dist/index.html' >/dev/null || { echo "ERROR: unexpected tarball layout"; exit 1; }
```
