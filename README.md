```
Get-ChildItem $HOME -Recurse -Include *.docx,*.xlsx,*.pptx,*.pdf -ErrorAction SilentlyContinue |
  Where-Object LastWriteTime -gt (Get-Date).Date |
  Select-Object LastWriteTime, FullName
```
