```
Select-String -Path restrictions\PACK.md -Pattern "labeling|overrides" -Context 0,8
Get-Content restrictions\label_catalog.json
```

```
New-Item -ItemType Directory -Force C:\temp\c4g-test | Out-Null
Copy-Item samples\files\*labeled*.docx, samples\files\protected_memo.docx C:\temp\c4g-test\
Copy-Item C:\temp\dlp-demo\unmarked.docx, C:\temp\dlp-demo\restricted.docx C:\temp\c4g-test\
Get-ChildItem C:\temp\c4g-test
```
