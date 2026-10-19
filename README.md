```
# 1. Change one file on purpose
Add-Content .\README.md "tampered"

# 2. Run the check again - it should refuse
python C:\Users\M3MXN08\repo\dlp-installer\install.py --manifest C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json --manifest-sha256 $sha --source . --dry-run

# 3. Put the file back the way it was
git checkout -- README.md
git status
```
```
Get-Content $env:USERPROFILE\.claude\settings.json
```
