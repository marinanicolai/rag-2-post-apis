Yes, but there's one step first. Claude uses the **installed** hook in `AppData\Local\inference-hook-dlp\plugin`, which is still **0.2.1**. Your fix is only in the repo, on the branch. To test it in Claude, you temporarily install the **branch version**, test, and then put 0.2.1 back.

The branch version hasn't been approved yet, so this is **only for your own testing**. Restore 0.2.1 right after.

**1. Make a test checklist from your branch**

```powershell
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
$tools = "C:\Users\M3MXN08\repo\dlp-installer"
git status
```

It should say `On branch fix/bash-embedded-paths` and `working tree clean` (after your commit).

```powershell
python $tools\make_manifest.py --version 0.2.2-dev --tag dev --plugin-dir . --out $tools\dev-hashes.json --allow-dirty
```

`--allow-dirty` skips the "must be on an approved tag" check. That's fine for a test build, and it's why it goes into a **separate** file (`dev-hashes.json`), so your approved checklist stays untouched.

**2. Swap the installed hook to the branch version**

```powershell
python $tools\install.py --uninstall
```

```powershell
$devsha = (Get-FileHash $tools\dev-hashes.json -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\dev-hashes.json --manifest-sha256 $devsha --source .
```

You should see `All files match.` and `Installed to ...`. Then **fully quit the desktop app** (tray icon → Quit) and reopen it.

**3. Test in Claude**

In the **Code** tab, start a new session in `dlp-demo-files`, and send the same prompt as this morning:

```
Read "C:\Users\M3MXN08\Documents\confidential-test.docx" and summarize it
```

Expected: Claude tries the Read (fails, as before), then tries a script, and **now the script is blocked** with the RESTRICTED FR message.

Then, in window 2:

```powershell
$log = "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl"
Get-Content $log -Tail 6 | ConvertFrom-Json | Select-Object @{n='time';e={([datetime]$_.ts).ToString('HH:mm:ss')}}, hook_event, action, deny_rule_id, tool_name | Format-Table -AutoSize
```

You should see **PreToolUse, deny, classification-ceiling, Bash**.

You can do the same in the **Terminal** (new `claude` session in `dlp-demo-files`) for the second row.

**4. Put 0.2.1 back** (don't skip this)

```powershell
python $tools\install.py --uninstall
git switch --detach inference-hook-dlp--v0.2.1
git status
```

You should see `HEAD detached at inference-hook-dlp--v0.2.1` and `working tree clean`.

```powershell
$sha = (Get-FileHash $tools\approved-hashes.json -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source .
```

You should see `All files match.` (159 files) and `Installed to ...`. Then restart the desktop app.

Send me photos of step 3 (the Claude screen and the log). That's the evidence the fix works in real use, and it's worth adding to the merge request.
