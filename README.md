```
python -c "import zipfile,json; z=zipfile.ZipFile('dist/inference-hook-dlp.zip'); h=json.loads(z.read('hooks/hooks.json')); print(h['hooks']['UserPromptSubmit'][0]['hooks'][0]['command'])"
```
