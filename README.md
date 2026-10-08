
```
  - id: skillhub-no-subprocess
    languages: [python]
    severity: ERROR
    message: "Skillhub policy: scripts may not launch other programs (subprocess, os.system, os.popen, os.spawn*, os.exec*)."
    pattern-either:
      - pattern: import subprocess
      - pattern: from subprocess import $X
      - pattern: subprocess.$F(...)
      - patterns:
          - pattern: os.$FUNC(...)
          - metavariable-regex:
              metavariable: $FUNC
              regex: ^(system|popen|spawn.*|exec.*)$
```
