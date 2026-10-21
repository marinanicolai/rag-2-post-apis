```
Here's a script for the meeting. Run each block **one at a time**: paste it, press Enter, and wait for the output.

It doesn't touch your real install. The demo install goes into a test folder with a test settings file, so your working DLP setup stays as it is.

**0. Set up the folders** (saves typing the long paths)

```powershell
$repo = "C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo"
$tools = "C:\Users\M3MXN08\repo\dlp-installer"
$demo = "C:\Users\M3MXN08\repo\dlp-demo"
cd $repo
git status
```
Expected: `HEAD detached at inference-hook-dlp--v0.2.1` and `working tree clean`.

**1. Make the checklist from the approved release**

```powershell
python $tools\make_manifest.py --version 0.2.1 --tag inference-hook-dlp--v0.2.1 --plugin-dir . --out $tools\approved-hashes.json
```
Expected: `159 files` and a `Manifest SHA-256` code.

What to say: *"This writes down a fingerprint for every file in the approved release."*

**2. Read the seal and check the files (should pass)**

```powershell
$sha = (Get-FileHash $tools\approved-hashes.json -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```
Expected: `All files match.` and `Dry run: verification passed, nothing installed.`

**3. Tamper test (should refuse)**

```powershell
Add-Content .\README.md "tampered"
```
```powershell
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```
Expected: `modified: README.md`, `BLOCKED: 1 file(s) do not match the approved release`, and `Nothing was installed.`

What to say: *"One changed line, and the install is refused."*

**4. Put the file back**

```powershell
git checkout -- README.md
git status
```
Expected: `working tree clean`.

**5. Full install into a test folder**

```powershell
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dest $demo\plugin --settings $demo\settings.json
```
```powershell
Get-Content $demo\settings.json | Select-String "hook.py"
```
Expected: `Installed to ...dlp-demo\plugin`, then 4 lines pointing at `dlp-demo/plugin/client/hook.py`.

What to say: *"It copies the verified files, checks the copy again, and registers the 4 hooks. Python does the copying, not Claude."*

**6. Clean up the test install**

```powershell
python $tools\install.py --uninstall --dest $demo\plugin --settings $demo\settings.json
Remove-Item $demo -Recurse -Force
```

**7. Optional: the live block in Claude**

Your real install is still active. In the desktop app's **Code** tab, start a new session and send:

```
check this record: employee 123-45-6789, start date Monday
```
Expected: "A hook blocked your prompt".

**Before the meeting**, crop or close anything showing your `settings.json` token if you share your screen. None of the commands above print it.
```
