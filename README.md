```
Here's the handoff doc with the test values replaced by placeholders: the SSN, password, AWS key, classification markings and SSH paths. Copy from the formatted text below, not a code view, and Word will keep the headings, bold text and tables.

---

# DLP Hooks – Handoff Walkthrough

**Repo:** c4g-dlp-hooks-repo · **Installer:** dlp-installer · **Release tested:** inference-hook-dlp--v0.2.1
**Prepared by:** Marina · **For:** Jitesh · **Date:** October 2026

## 1. Summary

While you were out, I tested the v0.2.1 release end to end in the Claude desktop app (Code tab, Terminal and Cowork). I compared it against how things behave with Zscaler alone, and I fixed two gaps where the hook let a prompt through.

| Item | Status |
|---|---|
| Release v0.2.1 installed and tested (Code tab, Cowork) | Done |
| Gap: restricted classification marking in a file name in prompt text | Fixed – MR open |
| Gap: restricted path in prompt text | Fixed – MR open |
| Zscaler rule spec (docs/ZSCALER_RULE_SPEC.md / .docx) | Regenerated (pack hash changed) |
| New approved release manifest | **Needed** before the fixes can be installed |

## 2. Branches and MRs

| Branch | Purpose | Files changed | Status |
|---|---|---|---|
| fix/prompt-filename-classification | Detect classification markings written with underscores in file names in prompt text | client/classification.py, tests/test_classification_filename.py (new) | MR open |
| fix/prompt-restriction-path | Check restricted paths (key and credential locations) in prompt text | client/classification.py, restrictions/restricted-paths.md, docs/ZSCALER_RULE_SPEC.md, docs/ZSCALER_RULE_SPEC.docx | MR open |
| cowork-support | Cowork packaging (dist/inference-hook-dlp.zip, vendored yaml) | – | Existing |
| fix/bash-embedded-paths | Find file paths hidden inside bash one-liners and scripts | client/hook.py, tests/test_bash_file_refs.py | Existing – reviewed; does **not** cover prompt text |
| fix/ceiling-message-no-label | Existing branch – may relate to finding 6.3 (item 3) | – | To confirm with you |

Note: the two fix branches are separate. Each was branched from main, so neither contains the other's change. They touch client/classification.py in different places.

## 3. The edits

### 3.1 Fix 1 – Underscored markings in prompt text

**Problem:** A prompt naming a file whose name contained `<RESTRICTED-MARKING>` with underscores (for example, `Q3_budget_<RESTRICTED-MARKING>.txt`) was allowed at UserPromptSubmit (dlp_7bc86c3685d9). Zscaler then blocked it at the network with a generic "Access denied" (403).

**Root cause:** _marking_regex() let the space inside a two-word marking match only spaces or dashes, so the underscored form never matched.

**Change:** in client/classification.py, in _marking_regex():

Before:
`parts.append(rf"(?:\s*[{re.escape(_DASHES)}]\s*|\s+)")`

After:
`parts.append(rf"(?:\s*[{re.escape(_DASHES)}]\s*|[\s_]+)")`

The compiled pattern's boundaries, `(?<![A-Za-z0-9])…(?![A-Za-z0-9])`, already treat _ as a boundary, so no other change was needed. Because this is the shared marking pattern, the fix applies everywhere text is scanned.

**Tests:** tests/test_classification_filename.py checks three things: an underscored name matches, spaces and dashes still match, and notes_internal.txt does not match. The full suite passes.

**Result:** The same prompt is now denied at UserPromptSubmit by classification-ceiling (dlp_77813262451d, 39 ms).

### 3.2 Fix 2 – Restricted paths in prompt text

**Problem:** A prompt asking to show the contents of `<restricted path>` (a private key file) was allowed at UserPromptSubmit (dlp_53f456f78171). Only Claude's own refusal stopped it.

**Root cause (two parts):**
1. restrictions/restricted-paths.md had `applies_to: [file]`, so the rule never ran on prompts.
2. PathDetector.find() only handled attachment segments, so even if the rule had been enabled for prompts, it had nothing to check.

**Changes:**

restrictions/restricted-paths.md:
`applies_to: [prompt, file]`

client/classification.py:
- New _PROMPT_PATH_RE, placed below DEFAULT_CEILING. It can't go directly above class PathDetector, because that class has an @dataclass(slots=True) decorator.
- New _match_path() helper that holds the existing glob and regex logic.
- find() now handles three cases:
  - Attachments keep their existing behavior, via _match_path().
  - User prompt text (segment.kind == "text", from hook.py line ~201) is searched for path-like strings, and each one is checked against the same globs.
  - All other kinds (tool_use, tool_result) are unchanged, so bash commands and file writes are not affected.

docs/ZSCALER_RULE_SPEC.md and .docx were regenerated with `python scripts/zscaler_spec.py`. The test test_zscaler_spec.py::test_the_checked_in_document_is_current requires the spec to name the current pack hash, and the hash changed.

| | Before | After |
|---|---|---|
| Hook result | allow | **deny** |
| Rule | – | restricted-paths |
| Pack hash | 30dfb9d6d75809c5 | 49d0423d84f23fc4 |

Something I learned along the way: config/rules.pack.yaml is **not** what the hook loads. client/pack.py loads the restriction pack **directory** and reads each restrictions/*.md file. find_pack_dir() looks in DLP_RESTRICTIONS_DIR first, then the plugin root, then Program Files. Valid applies_to values are prompt, file, tool_input, tool_output and all.

## 4. Manifest and install

### 4.1 Installer options

`install.py [--manifest MANIFEST] [--manifest-sha256 MANIFEST_SHA256] [--source SOURCE] [--dest DEST] [--settings SETTINGS] [--hooks-file HOOKS_FILE] [--dry-run] [--uninstall]`

There is no skip or dev option. Every install is verified against the approved manifest.

### 4.2 Install the approved release

```
$tools = "C:\Users\<user>\repo\dlp-installer"
cd C:\Users\<user>\repo\c4g-dlp-hooks-repo
git fetch --tags
git switch --detach inference-hook-dlp--v0.2.1
$sha = (Get-FileHash "$tools\approved-hashes.json" -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source .
```

Expected output: "Checking 159 files against approved release 0.2.1 (inference-hook-dlp--v0.2.1)..."

The way `$sha` is computed here is question 9.1.

**Install blocks I hit (all correct behavior):**

| Message | Cause | Resolution |
|---|---|---|
| 40 file(s) do not match – not in approved release: vendor/yaml/... | Installing from cowork-support | Install from the v0.2.1 tag |
| 1 file(s) do not match – dist/inference-hook-dlp.zip | Untracked Cowork build artifact left in dist/ | Move the zip out temporarily |

### 4.3 Uninstall

`python $tools\install.py --uninstall`

This removes 4 hook groups from %USERPROFILE%\.claude\settings.json and writes a timestamped backup. Restart Claude afterward.

### 4.4 Tamper test

```
Add-Content .\README.md "tampered"
python $tools\install.py --manifest $tools\approved-hashes.json --manifest-sha256 $sha --source . --dry-run
```

Expected: the install is blocked. Revert the README afterward.

## 5. Activating the plugin

### 5.1 Code tab and Terminal

1. Install the release (section 4.2).
2. Confirm the hooks are registered:
   `Get-Content $env:USERPROFILE\.claude\settings.json | Select-String "hook.py"`
3. Fully quit and reopen the Claude desktop app.
4. Start a new session. In the Code tab, the hook runs from %LOCALAPPDATA%\inference-hook-dlp\plugin\client\hook.py.

### 5.2 Cowork

Cowork uses a **separately uploaded plugin** (inference-hook-dlp@inline), started by dlp_hook_launcher.ps1 through powershell.exe with -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass.

Location: %LOCALAPPDATA%\Claude-3p\local-agent-mode-sessions\<id>\...\cowork_plugins\marketplaces\local-desktop-app-uploads\inference-hook-dlp

It runs from Python source (including client/cowork.py), uses the same release pack (30dfb9d6d75809c5), and writes to the same log file.

[Marina: add the steps used to upload the Cowork plugin]

### 5.3 Reading the log

All surfaces log to %LOCALAPPDATA%\inference-hook-dlp\client-decisions.jsonl.

```
function Last($n = 1) { Get-Content "$env:LOCALAPPDATA\inference-hook-dlp\client-decisions.jsonl" -Tail $n | ConvertFrom-Json | Format-List }
Last
Last 3
```

`Last` shows the newest entry, and `Last 3` shows the last three. A file read can log a prompt check plus a tool check, so `Last 3` is useful there.

Key fields: hook_event, tool_name, action, deny_rule_id, reference_id, files, pack_hash, latency_ms. Cowork entries can be identified by a cwd under Claude-3p\local-agent-mode-sessions.

## 6. Test results

### 6.1 Code tab (v0.2.1)

| # | Test | Result | Caught by | Rule | Reference |
|---|---|---|---|---|---|
| 001 | PII in prompt | Pass | Hook – UserPromptSubmit | pii-ssn | dlp_4c3085606eaa |
| 002 | File read | Pass | Hook – PreToolUse (Read) | secrets-credentials | dlp_4720e43b8f08 |
| 003 | Bash bypass (new session) | Pass | Hook – PreToolUse (Bash) | secrets-credentials | dlp_8ffee79e3273 |
| 004 | Write sensitive data | Pass | Hook – PreToolUse (Write) | secrets-credentials | dlp_a62a01eb4792 |
| 005 | Exfiltration | Not tested by hook | Claude declined | – | – |
| 006 | Label (marked-memo.txt) | Pass | Hook – PreToolUse (Read) | classification-ceiling | dlp_9eb9e20747a4 |
| 007 | AWS keys in prompt | Pass | Hook – UserPromptSubmit | secrets-credentials | TBD |
| 008 | Password in prompt | Pass | Hook – UserPromptSubmit | secrets-credentials | dlp_9421f68af2df |
| 009 | Private key in prompt | TBD | | | |
| 010 | Classification marking | TBD | | | |
| 011 | Restricted file name | **Fail → fixed** | Zscaler (before fix) | classification-ceiling (after) | dlp_7bc86c3685d9 → dlp_77813262451d |
| 012 | Restricted path | **Gap → fixed** | Claude declined (before fix) | restricted-paths (after) | dlp_53f456f78171 → TBD |

Blocks took 31–53 ms. Only one rule is reported as the reason for each verdict, but matched_rule_ids lists everything found. For example, one file read matched bank routing, SSN, credentials and private key.

### 6.2 Cowork (v0.2.1 + uploaded plugin)

| # | Test | Result | Caught by | Rule | Reference |
|---|---|---|---|---|---|
| 001 | PII in prompt | Pass | Hook – UserPromptSubmit | pii-ssn | dlp_743343a237e5 |
| 002 | File attached | Pass | Hook – UserPromptSubmit (attachment scanned) | secrets-credentials | dlp_617292fc1f9e |
| 003 | Bash bypass | Pass (blocked at prompt – file attached) | Hook – UserPromptSubmit | secrets-credentials | dlp_9ec9a3054f0b |
| 004 | Write sensitive data | Pass – Claude retried with placeholders, allowed | Hook – PreToolUse (Write) | secrets-credentials | dlp_68f628c29ffe / dlp_3ddb0df8c553 |
| 005–010 | | TBD | | | |
| 011 | Restricted file name | Fail on release; fix being verified | Claude declined | | TBD |
| 012 | Restricted path | Fix being verified | | | TBD |

The hook also checks Cowork's workspace bash tool (mcp__workspace__bash); both PreToolUse and PostToolUse entries were logged.

### 6.3 Known gaps and observations

1. **Typos bypass keyword rules.** A misspelled password keyword (`passord=<REDACTED>`) was allowed by the hook and not blocked by Zscaler.
2. **Tool output is scanned but not blocked.** PostToolUse logs allow. A directory search returned a file name containing `<RESTRICTED-MARKING>`. The name went to the model, and Zscaler blocked the next request (403). The hook later blocked mcp__ccd_turn__wrap_up (dlp_b7e9dba614b2). Consider blocking at PostToolUse.
3. **The deny message may trigger Zscaler (to confirm).** After a correct hook block on marked-memo.txt, the chat showed "Access denied". The likely cause is that the deny message names the marking and Zscaler blocks it. This may be addressed by fix/ceiling-message-no-label.
4. **Session titles keep sensitive values.** A blocked prompt still produced a sidebar title containing the test SSN.
5. **Policy inconsistency.** The card rule allows documentation test card numbers, but the credentials rule blocks AWS's published documentation example key (`<AWS example key>`).
6. **False-positive risk from the fixes.** Code identifiers containing a marking with underscores, and harmless questions that mention `<restricted path>`, will now be blocked. This is a policy decision.
7. **classification-in-file-name is still applies_to: [file].** Prompt-text coverage currently comes from the marking fix (3.1), not from this rule.
8. **The Cowork bash path** was not tested with a connected folder.
9. **The hits.samples field:** confirm it never stores raw matched values.

## 7. Demo script (about 10 minutes)

**Setup:** release installed, PowerShell open with Last defined, and a new session for each test.

**Part A – Hook vs Zscaler only**
1. Show the Zscaler-only screenshot: "Access denied – check your permissions", with no reason given.
2. In the Code tab, send a prompt with a test SSN (`XXX-XX-XXXX` format). The hook shows its message with the rule and how to fix the prompt. Run Last (pii-ssn, ~30 ms).
3. The point: the prompt was blocked on the laptop, the user was told why, and the event was logged.

**Part B – Tool coverage**
4. In a new session, ask Claude to print the demo data file with a shell command. The hook blocks it at Bash, and Last shows the file was scanned.
5. In Cowork, ask Claude to create config.env with a sample AWS access key and secret key. The first write is blocked, and Claude retries with placeholders. The point: the hook steers Claude to a compliant result.

**Part C – The two fixes (before / after)**
6. Show the before screenshots: the prompts were allowed (dlp_7bc86c3685d9, dlp_53f456f78171).
7. Show the after screenshots: the prompts were denied (dlp_77813262451d, restricted-paths).
8. Walk through the diffs (sections 3.1 and 3.2) and the test run.

**Part D – Gaps and next steps**
9. Section 6.3.
10. Next steps (section 8).

**Local verification method used for the fixes.** This is a dev-only method outside the approved process, and the original files were restored afterward:

```
$dst  = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\client\classification.py"
$rule = "$env:LOCALAPPDATA\inference-hook-dlp\plugin\restrictions\restricted-paths.md"
Copy-Item $dst "$dst.bak"; Copy-Item $rule "$rule.bak"
Copy-Item .\client\classification.py $dst -Force
Copy-Item .\restrictions\restricted-paths.md $rule -Force
Copy-Item "$dst.bak" $dst -Force; Copy-Item "$rule.bak" $rule -Force
```

Restart Claude and test between the second Copy-Item line and the restore line. The same approach was used on the Cowork plugin folder, with backups saved as .bak next to each file.

## 8. Next steps

1. Review and merge fix/prompt-filename-classification and fix/prompt-restriction-path.
2. Cut a new release and generate a new approved manifest.
3. Rebuild the Cowork plugin from the new release and re-upload it.
4. Send the regenerated Zscaler spec to the Zscaler team (Andrew).
5. Decide on PostToolUse blocking (gap 2), and confirm whether fix/ceiling-message-no-label covers gap 3.
6. Finish the TBD rows in section 6.

## 9. Questions for Jitesh

1. **Manifest SHA:** I computed $sha locally from approved-hashes.json. Where should the trusted SHA come from in the real process?
2. **Rule pack sources:** what is config/rules.pack.yaml used for, given that the hook loads restrictions/*.md?
3. **Cowork plugin:** what is the intended build and upload process from cowork-support?
4. **-ExecutionPolicy Bypass in the Cowork launcher:** what's the approved justification for InfoSec?
5. **Fail mode:** the pack is set to fail_mode: closed. Has that been tested end to end?

---

If Word pastes the code lines in the same font as the text, select them and switch them to a monospace font such as Consolas.
```
