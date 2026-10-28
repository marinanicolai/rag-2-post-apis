
Here's the demo in three parts, with the expected result after each step. Run everything from `C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo` in PowerShell.

I don't know what the Zscaler blocker in Part 1 actually looks like on your machine, so record what you see and use that.

## Part 0: Start clean

```powershell
$tools = "C:\Users\M3MXN08\repo\dlp-installer"
python $tools\install.py --uninstall
git stash
git switch --detach inference-hook-dlp--v0.2.1
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```

- **Expected:** the last command prints nothing, so no hooks are installed. Fully quit and reopen Claude.
- `git stash` matters if you have uncommitted changes. Your fix branch isn't in the approved release, so you need to be on the tag.
- If `dist\inference-hook-dlp.zip` is back, move it out, or the installer will block later: `Move-Item .\dist\inference-hook-dlp.zip $HOME\Desktop\`

## Part 1: Without the installer

**1a. The normal plugin route (from GitLab).** Start Claude in the terminal and run:

```text
claude
/plugin marketplace add <your GitLab repo URL>
/plugin install inference-hook-dlp@<marketplace name>
```

- **Expected blocker:** Zscaler stops the download (403, certificate, or access-denied error), so the plugin never installs.
- Take a screenshot. This is the problem the installer solves.

**1b. Loading the repo folder directly, with no checks.**

```powershell
Add-Content .\README.md "tampered"
claude --plugin-dir .
```

- **Expected:** the plugin loads anyway, even though a file was changed. Nothing checks the files against the approved release, so a modified hook would run silently.
- If your Claude Code version doesn't recognize `--plugin-dir`, skip 1b. Part 2 still shows the tamper check.
- Exit Claude, then undo the change: `git checkout -- README.md`

## Part 2: With the installer and manifest

**2a. Tamper test.** The installer should refuse:

```powershell
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash
Add-Content .\README.md "tampered"
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```

**Expected:** `BLOCKED: 1 file(s) do not match the approved release` and `Nothing was installed.`

**2b. Clean dry run:**

```powershell
git checkout -- README.md
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```

**Expected:** `Checking 159 files against approved release 0.2.1 (inference-hook-dlp--v0.2.1)...` with no mismatches.

**2c. Install:**

```powershell
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source .
Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
```

**Expected:** the second command now lists the hook lines.

**2d. Prove it works.** Fully quit and reopen Claude. In a new Code tab session, send:

```text
Summarize this record: Jane Testperson, SSN 123-45-6789
```

Then in PowerShell:

```powershell
function Last($n = 1) { Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail $n | ConvertFrom-Json | Format-List }
Last
```

**Expected:** `UserPromptSubmit`, **deny**, `pii-ssn`.

## The story for the meeting

| | Without installer | With installer and manifest |
|---|---|---|
| Install from GitLab | Blocked by Zscaler | Not needed; installs from a local copy |
| Changed or tampered files | Run without anyone knowing | Install is refused |
| Proof of what's installed | None | Every file checked against the approved release |

When you're done, go back to your work with `git switch fix/prompt-restriction-path` and then `git stash pop`.

Be ready for this question: `$sha` here is computed from the manifest file itself, so it doesn't prove the manifest is genuine. That's question 9.1 for Jitesh.

