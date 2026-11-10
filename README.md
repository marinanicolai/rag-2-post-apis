```
Thanks, the diagnosis makes sense, and I've confirmed it. Here's everything you asked for.

## What I found
1. Prod docs page is unstyled (content loads, no CSS). View source shows the stylesheet link starts with /ai/cgi-bin/ai-marketplace-dev/docs/assets/... [adjust if Ctrl+U shows something different]
2. URLs:
   - Prod: https://fweb.rsma.frb.gov/ai/cgi-bin/ai-marketplace/docs/
   - Dev:  https://fweb.rsma.frb.gov/ai/cgi-bin/ai-marketplace-dev/docs/
   - So for prod, DOCS_BASE_PATH = /ai/cgi-bin/ai-marketplace/docs/
3. deploy:prod gets its docs from build:docs (the same single build dev uses), so prod ships the dev-path bundle.
4. Important: build:docs runs the VitePress build inside `docker run`, which only passes `-e HOME=/workspace`. So DOCS_BASE_PATH has to be passed into that container with `-e DOCS_BASE_PATH=...`. Setting it in GitLab alone won't reach the build.
5. Every pipeline has one allowed-to-fail job in the first stage: [job name]. It [is / is not] related to docs.
6. Branch pipelines stop at a manual deploy:dev. Prod deploys from main, so this fix needs to be merged to main and a new prod deploy run.

## build:docs job (.gitlab-ci.yml)
```yaml
build:docs:
  stage: build
  tags:
    - docker_build
  script:
    - echo "Building documentation in Docker container..."
    # Clean old node_modules using Docker as root
    - |
      docker run --rm \
        -v "$PWD:/workspace" \
        -w /workspace \
        alpine:latest \
        sh -c "rm -rf apps/docs/node_modules"
    # Inject Nexus credentials from the masked NEXUS_NPM_AUTH CI/CD variable.
    - |
      if [ -n "${NEXUS_NPM_AUTH}" ]; then
        echo "//nexus.frb.gov/repository/npm/:_auth=${NEXUS_NPM_AUTH}" >> .npmrc
      fi
    # Build docs in Node.js container
    - |
      docker run --rm \
        -v "$PWD:/workspace" \
        -w /workspace \
        -e HOME=/workspace \
        public.ecr.aws/docker/library/node:22 \
        bash -c "npm install && cd apps/docs && npm run docs:build"
    - tar czf marketplace-docs-latest.tar.gz apps/docs/src/.vitepress/dist
    - ls -lh marketplace-docs-latest.tar.gz
  artifacts:
    [paste the rest of the job: artifacts, rules, etc.]
```

## deploy:prod job (.gitlab/ci/deploy-prod.yml)
```yaml
deploy:prod:
  stage: deploy
  tags:
    - arc-server  # Same server as dev, different directory
  dependencies:
    - package:frontend  # Production frontend package
    - package:backend
    - build:docs  # VitePress documentation
  script:
    - echo "Deploying to PRODUCTION environment"
    - echo "Target /ai/www/cgi-bin/ai-marketplace/"
    - ls -la deploy-output/
    # Create prod directory structure if it doesn't exist
    - mkdir -p /ai/www/cgi-bin/ai-marketplace/{external,logs,scripts}
    - chmod 777 /ai/www/cgi-bin/ai-marketplace/logs
    # Copy artifacts to prod external directory
    - cp -v deploy-output/marketplace-backend-${CI_COMMIT_SHORT_SHA}.tar.gz [rest of line]
    - cp -v deploy-output/marketplace-frontend-${CI_COMMIT_SHORT_SHA}.tar.gz [rest of line]
    - cp -v marketplace-docs-latest.tar.gz /ai/www/cgi-bin/ai-marketplace/external/[rest of line]
    - echo "✓ All artifacts copied to external/"
    [paste the docs extract lines through the end of the job]
```

## What I need
Please write the exact YAML change:
- Add a `build:docs:prod` job: same as build:docs, but pass `-e DOCS_BASE_PATH=/ai/cgi-bin/ai-marketplace/docs/` into the node docker run, and write a separate tarball (e.g. marketplace-docs-prod-latest.tar.gz). Its rules should match when deploy:prod runs.
- Update deploy:prod to depend on `build:docs:prod` instead of `build:docs`, and to copy and extract the new tarball name.
- Leave build:docs and the dev deploy unchanged.
- Note that the tarball includes the path apps/docs/src/.vitepress/dist, so make sure the extract step still lands files in the right place.
- Tell me how to verify after deploy (what the prod stylesheet href should look like).
  ```
