```
python -c "import zipfile; print('\n'.join(zipfile.ZipFile(r'C:\temp\c4g-test\word-labeled.docx').namelist()))"
Get-Item C:\temp\c4g-test\word-labeled.docx | Select-Object LastWriteTime
```
