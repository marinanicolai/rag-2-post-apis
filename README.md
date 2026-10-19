The installer works now. Since it never ran before, **the earlier "clean" practice run and the tamper test didn't actually check anything**. They were silent for the same reason. So let's redo both quickly, now for real.

Run these **one at a time**: paste one, press Enter, wait for the output, then the next.

**1. Go to the repo and read the seal code:**
```powershell
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
```
```powershell
$sha = (Get-FileHash C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json -Algorithm SHA256).Hash
```

**2. Practice run (should pass):**
```powershell
python C:\Users\M3MXN08\repo\dlp-installer\install.py --manifest C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```
Expected: `Checking 159 files...`, then `All files match.` and `Dry run: verification passed, nothing installed.`

**3. Tamper test (should refuse):**
```powershell
Add-Content .\README.md "tampered"
```
```powershell
python C:\Users\M3MXN08\repo\dlp-installer\install.py --manifest C:\Users\M3MXN08\repo\dlp-installer\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```
Expected: `modified: README.md`, then `BLOCKED: 1 file(s) do not match the approved release` and `Nothing was installed.`

**4. Put the file back:**
```powershell
git checkout -- README.md
```
```powershell
git status
```
Expected: `working tree clean`.

Send me a photo of the outputs from steps 2 and 3. Those two together are the proof for Andrew. Then we'll do the real install.
