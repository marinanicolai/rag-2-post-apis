```

   git checkout -b scan-test
   Set-Content plugins\test_bad.py 'import subprocess; subprocess.call("curl example.com", shell=True)
   API_KEY = "sk-test-1234567890abcdefghijklmnop"'
   git add .
   git commit -m "Scanner test, do not merge"
   git push -u origin scan-test
```
