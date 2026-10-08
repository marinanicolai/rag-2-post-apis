```

   rules:
  - id: skillhub-no-subprocess
    languages: [python]
    severity: ERROR
    message: "Skillhub policy: scripts may not launch other programs (subprocess, os.system, os.popen)."
    pattern-either:
      - pattern: import subprocess
      - pattern: from subprocess import $X
      - pattern: subprocess.$F(...)
      - pattern: os.system(...)
      - pattern: os.popen(...)
      - pattern: os.spawn$X(...)
      - pattern: os.exec$X(...)

  - id: skillhub-no-network
    languages: [python]
    severity: ERROR
    message: "Skillhub policy: scripts may not make network calls."
    pattern-either:
      - pattern: import socket
      - pattern: import requests
      - pattern: from requests import $X
      - pattern: import urllib
      - pattern: import urllib.request
      - pattern: from urllib import $X
      - pattern: from urllib.request import $X
      - pattern: import http.client
      - pattern: import httpx
      - pattern: import ftplib
      - pattern: import smtplib

  - id: skillhub-no-dynamic-code
    languages: [python]
    severity: ERROR
    message: "Skillhub policy: scripts may not run dynamic code (eval, exec, compile, __import__)."
    pattern-either:
      - pattern: eval(...)
      - pattern: exec(...)
      - pattern: compile(...)
      - pattern: __import__(...)
```
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

# Enforces the Skillhub script policy: no launching programs,
# no network calls, no dynamic code. Findings are saved as a report;
# the job itself does not fail yet (warn-only phase).
script_policy:
  stage: test
  image: semgrep/semgrep:latest
  script:
    - semgrep scan --config ci/semgrep/skillhub-rules.yml --metrics=off --json -o skillhub-policy.json .
  artifacts:
    when: always
    paths: [skillhub-policy.json]
    expire_in: 30 days
```
