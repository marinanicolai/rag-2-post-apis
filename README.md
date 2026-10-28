```
# DLP Hooks – Handoff Walkthrough

**Repo:** `c4g-dlp-hooks-repo` · **Installer:** `dlp-installer` · **Release tested:** `inference-hook-dlp--v0.2.1`
**Prepared by:** Marina · **For:** Jitesh · **Date:** October 2026

---

## 1. Summary

While you were out I tested the v0.2.1 release end to end in the Claude desktop app (Code tab, Terminal, Cowork), compared it against Zscaler-only behavior, and fixed two gaps where the hook let a prompt through.

| Item | Status |
|---|---|
| Release v0.2.1 installed and tested (Code tab, Cowork) | Done |
| Gap: restricted file name in prompt text (`..._RESTRICTED_FR...`) | Fixed – MR open |
| Gap: restricted path in prompt text (`C:\...\.ssh\id_rsa`) | Fixed – MR open |
| Zscaler rule spec (`docs/ZSCALER_RULE_SPEC.md` / `.docx`) | Regenerated (pack hash changed) |
| New approved release manifest | **Needed** before the fixes can be installed |

---

## 2. Branches and MRs

| Branch | Purpose | Files changed | Status |
|---|---|---|---|
| `fix/prompt-filename-classification` | Detect classification markings written with underscores (e.g. `Q3_budget_RESTRICTED_FR.txt`) in prompt text | `client/classification.py`, `tests/test_classification_filename.py` (new) | MR open |
| `fix/prompt-restriction-path` | Check restricted paths (`.ssh`, `id_rsa`, …) in prompt text | `client/classification.py`, `restrictions/restricted-paths.md`, `docs/ZSCALER_RULE_SPEC.md`, `docs/ZSCALER_RULE_SPEC.docx` | MR open |
| `cowork-support` | Cowork packaging (`dist/inference-hook-dlp.zip`, vendored `yaml`) | – | Existing |
| `fix/bash-embedded-paths` | Find file paths hidden inside bash one-liners and scripts | `client/hook.py`, `tests/test_bash_file_refs.py` | Existing – reviewed; does **not** cover prompt text |
| `fix/ceiling-message-no-label` | Existing branch – may relate to finding 6.3 below | – | To confirm with you |

> Note: the two fix branches are separate. Each was branched from `main`, so neither contains the other's change. They touch `client/classification.py` in different places.

---

## 3. The edits

### 3.1 Fix 1 – Underscored markings in prompt text

**Problem:** `open Q3_budget_RESTRICTED_FR.txt` → `UserPromptSubmit` **allow** (`dlp_7bc86c3685d9`), then Zscaler blocked it at the network with a generic "Access denied" (403).

**Root cause:** `_marking_regex()` let the space in a marking like `RESTRICTED FR` match only spaces or dashes, so `RESTRICTED_FR` never matched.

**Change** – `client/classification.py`, in `_marking_regex()`:

```python
# before
parts.append(rf"(?:\s*[{re.escape(_DASHES)}]\s*|\s+)")
# after
parts.append(rf"(?:\s*[{re.escape(_DASHES)}]\s*|[\s_]+)")
```

The compiled pattern's boundaries (`(?<![A-Za-z0-9])…(?![A-Za-z0-9])`) already treat `_` as a boundary, so no other change was needed. Because this is the shared marking pattern, it applies everywhere text is scanned.

**Tests:** `tests/test_classification_filename.py` – underscored name matches; spaces and dashes still match; `notes_internal.txt` does not match. Full suite passing.

**Result:** same prompt → `UserPromptSubmit` **deny**, `classification-ceiling` (`dlp_77813262451d`, 39 ms).

### 3.2 Fix 2 – Restricted paths in prompt text

**Problem:** `Show me what's in C:\Users\<user>\.ssh\id_rsa` → `UserPromptSubmit` **allow** (`dlp_53f456f78171`). Only Claude's own refusal stopped it.

**Root cause (two parts):**
1. `restrictions/restricted-paths.md` had `applies_to: [file]`, so the rule never ran on prompts.
2. `PathDetector.find()` only handled `attachment` segments, so even if enabled for prompts it had nothing to check.

**Changes:**

`restrictions/restricted-paths.md`:
```yaml
applies_to: [prompt, file]
```

`client/classification.py`:
- New `_PROMPT_PATH_RE` (placed below `DEFAULT_CEILING`, **not** above `class PathDetector` – that class has an `@dataclass(slots=True)` decorator).
- New `_match_path()` helper holding the existing glob/regex logic.
- `find()` now:
  - attachments → unchanged behavior via `_match_path()`
  - `segment.kind == "text"` (user prompt, from `hook.py` line ~201) → extract path-like strings and check each against the same globs
  - all other kinds (tool_use, tool_result) → unchanged, so bash commands and file writes are not affected

`docs/ZSCALER_RULE_SPEC.md` + `.docx`: regenerated with `python scripts/zscaler_spec.py` because `test_zscaler_spec.py::test_the_checked_in_document_is_current` requires the spec to name the current pack hash.

| | Before | After |
|---|---|---|
| Hook result | allow | **deny** |
| Rule | – | `restricted-paths` |
| Pack hash | `30dfb9d6d75809c5` | `49d0423d84f23fc4` |

> Learned along the way: `config/rules.pack.yaml` is **not** what the hook loads. `client/pack.py` loads the restriction pack **directory** (`find_pack_dir()`: `DLP_RESTRICTIONS_DIR` → plugin root → Program Files) and reads each `restrictions/*.md` file. Valid `applies_to` values: `prompt`, `file`, `tool_input`, `tool_output`, or `all`.

---

## 4. Manifest and install

### 4.1 Installer options

```text
install.py [--manifest MANIFEST] [--manifest-sha256 MANIFEST_SHA256] [--source SOURCE]
           [--dest DEST] [--settings SETTINGS] [--hooks-file HOOKS_FILE]
           [--dry-run] [--uninstall]
```

There is no skip/dev option – every install is verified against the approved manifest.

### 4.2 Install the approved release

```powershell
$tools = "C:\Users\<user>\repo\dlp-installer"
cd C:\Users\<user>\repo\c4g-dlp-hooks-repo
git fetch --tags
git switch --detach inference-hook-dlp--v0.2.1
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash   # see question 7.1
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source .
```

Expected: `Checking 159 files against approved release 0.2.1 (inference-hook-dlp--v0.2.1)...`

**Install blocks I hit (all correct behavior):**

| Message | Cause | Resolution |
|---|---|---|
| `40 file(s) do not match` – `not in approved release: vendor/yaml/...` | Installing from `cowork-support` | Install from the v0.2.1 tag |
| `1 file(s) do not match` – `dist/inference-hook-dlp.zip` | Untracked Cowork build artifact left in `dist/` | Move the zip out temporarily |

### 4.3 Uninstall

```powershell
python $tools\install.py --uninstall
```

Removes 4 hook groups from `%USERPROFILE%\.claude\settings.json` and writes a timestamped backup. Restart Claude afterward.

### 4.4 Tamper test

```powershell
Add-Content .\README.md "tampered"
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```

Expected: blocked. Revert the README afterward.

---

## 5. Activating the plugin

### 5.1 Code tab and Terminal

1. Install (4.2).
2. Confirm hooks are registered:
   ```powershell
   Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"
   ```
3. Fully quit and reopen the Claude desktop app.
4. Start a new session. In the Code tab, the hook runs from
   `%LOCALAPPDATA%\inference-hook-dlp\plugin\client\hook.py`.

### 5.2 Cowork

Cowork uses a **separately uploaded plugin** (`inference-hook-dlp@inline`), started by:

```text
powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass
  -File "...\cowork_plugins\marketplaces\local-desktop-app-uploads\inference-hook-dlp\scripts\dlp_hook_launcher.ps1"
  -Root "...\inference-hook-dlp" -HookEvent UserPromptSubmit
```

Location: `%LOCALAPPDATA%\Claude-3p\local-agent-mode-sessions\<id>\...\cowork_plugins\marketplaces\local-desktop-app-uploads\inference-hook-dlp`

It runs Python source (includes `client/cowork.py`), uses the same release pack (`30dfb9d6d75809c5`), and writes to the same log file.

> [Marina: add the steps used to upload the Cowork plugin]

### 5.3 Reading the log

All surfaces log to `%LOCALAPPDATA%\inference-hook-dlp\client-decisions.jsonl`.

```powershell
function Last($n = 1) { Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail $n | ConvertFrom-Json | Format-List }
Last      # newest entry
Last 3    # last three (a file read can log a prompt check plus a tool check)
```

Key fields: `hook_event`, `tool_name`, `action`, `deny_rule_id`, `reference_id`, `files`, `pack_hash`, `latency_ms`. Cowork entries can be identified by `cwd` under `Claude-3p\local-agent-mode-sessions`.

---

## 6. Test results

### 6.1 Code tab (v0.2.1)

| # | Test | Result | Caught by | Rule | Reference |
|---|---|---|---|---|---|
| 001 | PII in prompt | Pass | Hook – UserPromptSubmit | `pii-ssn` | `dlp_4c3085606eaa` |
| 002 | File read | Pass | Hook – PreToolUse (Read) | `secrets-credentials` | `dlp_4720e43b8f08` |
| 003 | Bash bypass (new session) | Pass | Hook – PreToolUse (Bash) | `secrets-credentials` | `dlp_8ffee79e3273` |
| 004 | Write sensitive data | Pass | Hook – PreToolUse (Write) | `secrets-credentials` | `dlp_a62a01eb4792` |
| 005 | Exfiltration | Not tested by hook | Claude declined | – | – |
| 006 | Label (marked-memo.txt) | Pass | Hook – PreToolUse (Read) | `classification-ceiling` | `dlp_9eb9e20747a4` |
| 007 | AWS keys in prompt | Pass | Hook – UserPromptSubmit | `secrets-credentials` | TBD |
| 008 | Password in prompt | Pass | Hook – UserPromptSubmit | `secrets-credentials` | `dlp_9421f68af2df` |
| 009 | Private key in prompt | TBD | | | |
| 010 | Classification marking | TBD | | | |
| 011 | Restricted file name | **Fail → fixed** | Zscaler (before fix) | `classification-ceiling` (after) | `dlp_7bc86c3685d9` → `dlp_77813262451d` |
| 012 | Restricted path | **Gap → fixed** | Claude declined (before fix) | `restricted-paths` (after) | `dlp_53f456f78171` → TBD |

Latency on blocks: 31–53 ms. Only one rule fires per verdict, but `matched_rule_ids` lists everything found (e.g. one file read matched bank routing, SSN, credentials and private key).

### 6.2 Cowork (v0.2.1 + uploaded plugin)

| # | Test | Result | Caught by | Rule | Reference |
|---|---|---|---|---|---|
| 001 | PII in prompt | Pass | Hook – UserPromptSubmit | `pii-ssn` | `dlp_743343a237e5` |
| 002 | File attached | Pass | Hook – UserPromptSubmit (attachment scanned) | `secrets-credentials` | `dlp_617292fc1f9e` |
| 003 | Bash bypass | Pass (blocked at prompt – file attached) | Hook – UserPromptSubmit | `secrets-credentials` | `dlp_9ec9a3054f0b` |
| 004 | Write sensitive data | Pass – Claude retried with placeholders, allowed | Hook – PreToolUse (Write) | `secrets-credentials` | `dlp_68f628c29ffe` / `dlp_3ddb0df8c553` |
| 005–010 | | TBD | | | |
| 011 | Restricted file name | Fail on release; fix being verified | Claude declined | | TBD |
| 012 | Restricted path | Fix being verified | | | TBD |

Cowork's workspace bash tool (`mcp__workspace__bash`) is checked by the hook (PreToolUse and PostToolUse entries logged).

### 6.3 Known gaps and observations

1. **Typos bypass keyword rules.** `passord=Summer2026!2` was allowed by the hook and not blocked by Zscaler.
2. **Tool output is scanned but not blocked.** `PostToolUse` logs `allow`. A directory search returned `Q3_budget_RESTRICTED_FR.txt`; the name went to the model and Zscaler blocked the next request (403). Hook later blocked `mcp__ccd_turn__wrap_up` (`dlp_b7e9dba614b2`). Consider blocking at `PostToolUse`.
3. **Deny message may trigger Zscaler (to confirm).** After a correct hook block on `marked-memo.txt`, the chat showed "Access denied". Likely the deny message names the marking and Zscaler blocks it. Possibly addressed by `fix/ceiling-message-no-label`.
4. **Session titles keep sensitive values.** A blocked prompt still produced a sidebar title containing the SSN.
5. **Policy inconsistency.** The card rule allows documentation test numbers (4111…); the credentials rule blocks AWS's documentation example key (`AKIA…EXAMPLE`).
6. **False-positive risk from the fixes.** Code identifiers like `RESTRICTED_FR = ...` and prompts like "how do I set up ~/.ssh/config?" will now be blocked. Policy decision.
7. **`classification-in-file-name` is still `applies_to: [file]`.** Prompt-text coverage currently comes from the marking fix (3.1), not this rule.
8. **Cowork bash path** not tested with a connected folder.
9. **`hits.samples` field** – confirm it never stores raw matched values.

---

## 7. Demo script (about 10 minutes)

**Setup:** release installed, PowerShell open with `Last` defined, new session per test.

### Part A – Hook vs Zscaler only
1. Show the Zscaler-only screenshot: "Access denied – check your permissions", no reason.
2. Code tab: `Summarize this record: Jane Testperson, SSN 123-45-6789` → hook message with rule and fix. Run `Last` (`pii-ssn`, ~30 ms).
3. Point: blocked on the laptop, user told why, event logged.

### Part B – Tool coverage
4. New session: `Run this command: type C:\Users\<user>\dlp-demo\dlp_demo_data.txt` → blocked at Bash. `Last` shows the file was scanned.
5. Cowork: `Create a file called config.env with a sample AWS access key and secret key in the standard format.` → first write blocked, Claude retries with placeholders. Point: the hook steers Claude to a compliant result.

### Part C – The two fixes (before / after)
6. Show before screenshots: prompt allowed (`dlp_7bc86c3685d9`, `dlp_53f456f78171`).
7. Show after screenshots: denied (`dlp_77813262451d`, restricted-paths).
8. Walk through the diffs (sections 3.1, 3.2) and the test run.

### Part D – Gaps and next steps
9. Section 6.3.
10. Next steps (section 8).

**Local verification method used for the fixes** (dev only – outside the approved process, restored afterward):

```powershell
$dst  = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\classification.py"
$rule = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\restrictions\restricted-paths.md"
Copy-Item $dst "$dst.bak"; Copy-Item $rule "$rule.bak"
Copy-Item .\client\classification.py $dst -Force
Copy-Item .\restrictions\restricted-paths.md $rule -Force
# restart Claude, test, then restore:
Copy-Item "$dst.bak" $dst -Force; Copy-Item "$rule.bak" $rule -Force
```

The same approach was used on the Cowork plugin folder (backups saved as `.bak` next to each file).

---

## 8. Next steps

1. Review and merge `fix/prompt-filename-classification` and `fix/prompt-restriction-path`.
2. Cut a new release and generate a new approved manifest.
3. Rebuild the Cowork plugin from the new release and re-upload.
4. Send the regenerated Zscaler spec to the Zscaler team (Andrew).
5. Decide on `PostToolUse` blocking (gap 2) and confirm `fix/ceiling-message-no-label` covers gap 3.
6. Finish the TBD rows in section 6.

---

## 9. Questions for Jitesh

1. **Manifest SHA:** I computed `$sha` locally from `approved-hashes.json`. Where should the trusted SHA come from in the real process?
2. **Rule pack sources:** what is `config/rules.pack.yaml` used for, given the hook loads `restrictions/*.md`?
3. **Cowork plugin:** what is the intended build and upload process from `cowork-support`?
4. **`-ExecutionPolicy Bypass`** in the Cowork launcher – what's the approved justification for InfoSec?
5. **Fail mode:** the pack is `fail_mode: closed`. Has that been tested end to end?
6. ```
