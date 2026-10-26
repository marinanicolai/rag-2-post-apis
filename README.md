```
python -c "import zipfile,glob; z=zipfile.ZipFile(glob.glob('dist/*.zip')[0]); n=z.namelist(); print('.claude-plugin/plugin.json' in n, 'hooks/hooks.json' in n, 'scripts/dlp_hook_launcher.ps1' in n, 'client/cowork.py' in n, any(x.startswith('bin/') for x in n))"
```
```
Add-Content .gitignore "dist/"
```
