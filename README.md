```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
python -c "import zipfile; print([n for n in zipfile.ZipFile('dist/inference-hook-dlp.zip').namelist() if 'ZSCALER' in n.upper()])"
```
