```
# 1. Folder for the installer scripts (inside the allow-listed source\repos)
mkdir $env:USERPROFILE\source\repos\dlp-installer -Force
Move-Item $env:USERPROFILE\Downloads\make_manifest.py, $env:USERPROFILE\Downloads\install.py $env:USERPROFILE\source\repos\dlp-installer\

# 2. Go to your clone and switch to the approved release
cd $env:USERPROFILE\source\repos\c4g-dlp-hooks-repo
git fetch --tags
git checkout inference-hook-dlp--v0.2.1
git status

# 3. Find the plugin root and its hooks file
Get-ChildItem -Recurse -Filter plugin.json | Select-Object FullName
Get-ChildItem -Recurse -Filter hooks.json | Select-Object FullName
Get-ChildItem -Recurse -Filter hooks.json | Select-String "CLAUDE_PLUGIN_ROOT"
```
