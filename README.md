```
      $d = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'dlp-test'
   New-Item -ItemType Directory -Force $d | Out-Null
   "name,ssn`r`nAda,219-09-1234" | Set-Content "$d\dlp-test-ssn.txt"
   $d
```
