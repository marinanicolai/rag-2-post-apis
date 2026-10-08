```
default:
  tags:
    - eks-fleet

include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Secret-Detection.gitlab-ci.yml

workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push"'
      when: never
    - when: always

sast:
  variables:
    KUBERNETES_MEMORY_REQUEST: "2Gi"
    KUBERNETES_MEMORY_LIMIT: "4Gi"

```
