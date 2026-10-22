```
# DLP Hooks Demo: Stakeholder and InfoSec Walkthrough

**Presenter:** Marina Nicolai
**Release shown:** `inference-hook-dlp--v0.2.1` (rule pack frb-baseline v2026.09.15, 12 rules)
**Length:** about 30 minutes
**Status going in:** the Zscaler team has confirmed the packaging approach is fine with them.

---

## 1. Before the meeting (do this 30 minutes early)

### 1.1 Checklist

- [ ] Claude desktop app is open and the DLP hooks are installed (they are, from 2026-10-19).
- [ ] VS Code is open with a PowerShell terminal.
- [ ] Close or hide anything showing `settings.json`, because it contains your token.
- [ ] Rehearse every test prompt in section 5 once, so you know which ones block on your machine.
- [ ] Have Monday's screenshots ready as a backup: the pass, the tamper block, and the SSN block in the desktop app.
- [ ] Have the *DLP Hooks 0.2.1 Known Gaps* doc open in another window.

### 1.2 Set up the terminal

Run this once, in the PowerShell window you'll use for the demo:

```powershell
$repo = "C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo"
$tools = "C:\Users\M3MXN08\repo\dlp-installer"
$demo = "C:\Users\M3MXN08\repo\dlp-demo"
$log = "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl"
cd $repo
git status
```

You should see `HEAD detached at inference-hook-dlp--v0.2.1` and `working tree clean`.

Tip: copy only the code inside each grey box, never the explanation lines.

---

## 2. Agenda

| # | Part | Time |
|---|---|---|
| 1 | The problem and how the DLP works | 5 min |
| 2 | The rulebook | 3 min |
| 3 | Packaging and verified install | 7 min |
| 4 | Live testing in Claude | 8 min |
| 5 | The decision log | 3 min |
| 6 | Zscaler (optional) | 2 min |
| 7 | Coverage, gaps and decisions | 2 min |

---

## 3. Part 1: The problem and how the DLP works (talk, no demo)

**What to say:**

> Claude is useful, but it is also a way for sensitive data to leave by accident: a pasted SSN, a document marked above our ceiling, an API key. The DLP hooks check everything an employee sends to Claude, and everything Claude reads, against a rulebook owned by InfoSec, before it leaves the laptop.

**The design: one brain, three doors**

| Door | Covers | Status |
|---|---|---|
| Door 1: Claude Code hook | Code tab in the desktop app, on each laptop | Working, and what we demo today |
| Door 2: Inference-hook server | Chat, Cowork and Code, org-wide | Built and tested, not switched on yet |
| Path B: Zscaler rules | Block file uploads in Chat and Cowork | Spec with the Zscaler team |

**The four checkpoints in the Code tab:**

| Checkpoint | When it runs | What it does |
|---|---|---|
| SessionStart | Claude starts | Loads the rulebook |
| UserPromptSubmit | You send a prompt | Blocks the prompt if it breaks a rule |
| PreToolUse | Before Claude reads a file, runs a command or fetches a page | Blocks the action before it happens |
| PostToolUse | After a tool returns a result | Flags the result so Claude doesn't use it |

---

## 4. Part 2: The rulebook (show, don't read it all)

Show the folder in VS Code's explorer: `c4g-dlp-hooks-repo\restrictions\`.

**What to say:**

> Each rule is a plain-English file, versioned in git. The pack today has 12 rules: classification ceiling, classification in file names, SSNs, bank routing numbers, bulk contact data, credentials and more. InfoSec owns this rulebook; changing a rule means a new release.

Tip: show the file list. Don't scroll through the trigger patterns on screen; they're deliberately kept out of documents.

---

## 5. Part 3: Packaging and verified install (live)

**What to say first:**

> The original plan was an .exe, but on our laptops AppLocker blocks unsigned programs, and Zscaler blocks Claude from copying files that contain classification names. So we package it differently: an approved release, a checklist of fingerprints, and an installer that only installs files that match. The Zscaler team has confirmed this approach is fine with them.

### 5.1 Make the checklist from the approved release

```powershell
python $tools\make_manifest.py --version 0.2.1 --tag inference-hook-dlp--v0.2.1 --plugin-dir . --out $tools\approved-hashes.json
```

You should see `159 files` and a `Manifest SHA-256` code.

> This writes down a SHA-256 fingerprint for every file in the approved release. It refuses to run if anything in the folder was changed.

### 5.2 Check the files (should pass)

```powershell
$sha = (Get-FileHash $tools\approved-hashes.json -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```

You should see `All files match.`

### 5.3 Tamper test (should refuse)

```powershell
Add-Content .\README.md "tampered"
```

```powershell
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```

You should see `modified: README.md`, `BLOCKED` and `Nothing was installed.`

> One changed line, and the install is refused. Testers can only ever install the exact files that were approved.

Put the file back:

```powershell
git checkout -- README.md
git status
```

### 5.4 Full install into a test folder (optional)

```powershell
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dest $demo\plugin --settings $demo\settings.json
Get-Content $demo\settings.json | Select-String "hook.py"
```

You should see `Installed to ...dlp-demo\plugin` and 4 hook lines.

> Python copies the files, not Claude, so AppLocker and the Zscaler rule are not triggered. It checks the copy again, then registers the 4 hooks.

Clean up:

```powershell
python $tools\install.py --uninstall --dest $demo\plugin --settings $demo\settings.json
Remove-Item $demo -Recurse -Force
```

---

## 6. Part 4: Live testing in Claude (desktop app, Code tab)

Start a **new session** in the Code tab for each group of tests. All data below is fake.

### 6.1 A normal prompt (should be allowed)

```
Write a Python function that adds two numbers.
```

> Normal work isn't slowed down. Each check takes about 34 ms.

### 6.2 An SSN in a prompt (should be blocked)

```
check this record: employee 123-45-6789, start date Monday
```

You should see **"A hook blocked your prompt"**, with the rule explained and a reference number like `dlp_...`. Write the reference number down for Part 5.

### 6.3 Other rules in a prompt (pick the ones that blocked in your rehearsal)

| Rule | Example prompt (fake data) |
|---|---|
| Bank routing number | `Wire it to routing 021000021, account 12345678` |
| Credentials | `Here is the key: api_key = "sk_test_51HfakeFAKEfake1234567890"` |

Only show prompts that blocked when you rehearsed them.

### 6.4 A file Claude tries to read (should be blocked before the read)

Create a test file in PowerShell first:

```powershell
New-Item -ItemType Directory -Force C:\Users\M3MXN08\repo\dlp-demo-files | Out-Null
Set-Content C:\Users\M3MXN08\repo\dlp-demo-files\employee.txt "Employee: Jane Test, SSN 123-45-6789"
```

In the Code tab, open a session in `C:\Users\M3MXN08\repo\dlp-demo-files` and send:

```
Summarize employee.txt
```

> This is the before-check: Claude never gets to see the file's contents.

Remove the test file afterwards:

```powershell
Remove-Item C:\Users\M3MXN08\repo\dlp-demo-files -Recurse -Force
```

---

## 7. Part 5: The decision log (for the InfoSec specialist)

**What to say:**

> Every decision is logged locally, allowed or denied, with the sensitive value masked. InfoSec can answer "why was I blocked?" from the reference number, without ever seeing the sensitive data.

Show the last 3 decisions in a readable table:

```powershell
Get-Content $log -Tail 3 | ConvertFrom-Json | Select-Object ts, hook_event, action, deny_rule_id, reference_id | Format-Table
```

Look up the reference number from the blocked prompt in 6.2 (replace the example):

```powershell
Select-String -Path $log -Pattern "dlp_84ee51a92a28"
```

Point out:
- the SSN appears masked (for example `12*****89`), never in full
- `pack_hash` shows exactly which rulebook version made the decision
- `fail_mode: closed` in the session_start entry means that if the checker breaks, it blocks rather than allows

---

## 8. Part 6: Zscaler (optional, talk only)

**What to say:**

> Zscaler plays two roles. First, its endpoint rule blocks claude.exe from copying files with classification names, which is why the plugin is installed by Python instead. The Zscaler team has reviewed and confirmed this packaging approach. Second, for Chat and Cowork, where the local hook can't run, Jitesh handed the Zscaler team a spec to block file uploads and apply inline DLP. That's their control to switch on.

Don't try the regular plugin install live; it's blocked by design.

---

## 9. Part 7: Coverage, gaps and decisions

### 9.1 What's covered today

| Surface | Covered? |
|---|---|
| Code tab (desktop app) and Claude Code CLI | Yes, by the local hook |
| Chat | Not yet: needs Door 2 or Zscaler Path B |
| Cowork | Not yet: needs Door 2 or Zscaler Path B |

### 9.2 Known gaps

Use the current *DLP Hooks 0.2.1 Known Gaps* doc. Mention only what's still open, for example:
- the first check in a session can time out and block; retrying works
- the user override hasn't been tested yet

### 9.3 Decisions needed from InfoSec

1. **Sign-off:** who approves each release before the checklist is made, and where is the approval recorded?
2. **Release review:** should the review include a MartinAI report, automated scanners, or both?
3. **Checklist location:** where should the approved checklist and installer live, so testers can't edit them? Suggestion: a protected repo InfoSec controls.
4. **Auto-labeling:** should testers get labels applied to their files automatically (current default), or only suggested?
5. **Next step for Chat and Cowork:** who owns switching on Door 2?

---

## 10. If something goes wrong live

| Problem | What to do |
|---|---|
| A command prints nothing or shows red errors | Run section 1.2 again; the variables may be gone |
| A test prompt isn't blocked | Show Monday's screenshot instead, and note it as a finding |
| The first prompt times out | Say it's a known gap and retry |
| You run out of time | Skip 5.4 and 6.3; keep 5.3 (tamper) and 6.2 (SSN) |
```
