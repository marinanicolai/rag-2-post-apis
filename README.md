```
Get-Item C:\temp\c4g-test\word-labeled.docx | Select-Object LastWriteTime
python -c "import zipfile; print('\n'.join(zipfile.ZipFile(r'C:\temp\c4g-test\word-labeled.docx').namelist()))"
```
```
python -c "import zipfile; print(zipfile.ZipFile(r'C:\temp\c4g-test\word-labeled.docx').read('docProps/custom.xml').decode())"
```
