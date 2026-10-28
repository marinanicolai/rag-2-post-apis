```
Get-Content scripts\build_zip.py -TotalCount 25
```
```
Select-String -Path scripts\build_zip.py -Pattern "tests|sample|exclude|include|glob" | Select-Object LineNumber, Line
```
