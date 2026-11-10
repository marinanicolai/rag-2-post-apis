```
build:docs:
  extends: .build-docs
  variables:
    DOCS_BASE_PATH: /ai/cgi-bin/ai-marketplace-dev/docs/
    DOCS_TARBALL: marketplace-docs-latest.tar.gz
  artifacts:
    name: "docs-${CI_COMMIT_SHORT_SHA}"
    paths:
      - marketplace-docs-latest.tar.gz

build:docs:prod:
  extends: .build-docs
  variables:
    DOCS_BASE_PATH: /ai/cgi-bin/ai-marketplace/docs/
    DOCS_TARBALL: marketplace-docs-prod-latest.tar.gz
  artifacts:
    name: "docs-prod-${CI_COMMIT_SHORT_SHA}"
    paths:
      - marketplace-docs-prod-latest.tar.gz
```
