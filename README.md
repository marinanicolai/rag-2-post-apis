```
Move-Item .\dist\inference-hook-dlp.zip $HOME\Desktop\
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source .
```
```
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```
