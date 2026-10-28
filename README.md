```
python scripts\build_zip.py
python -c "import zipfile; print([n for n in zipfile.ZipFile('dist/inference-hook-dlp.zip').namelist() if 'zscaler' in n.lower() or 'test' in n.lower() or 'sample' in n.lower()])"
```
