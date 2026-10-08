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
