```
Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail 5
```
```
python -c "import zipfile; print(zipfile.ZipFile(r'C:\temp\c4g-test\word-labeled.docx').read('docProps/custom.xml').decode())"
```
