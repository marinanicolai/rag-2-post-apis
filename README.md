
```
DLP Hooks 0.2.1 — Known Gaps
Oct 9, 2026 · @Marina
Summary
Release 0.2.1 is not ready for a Board-wide handoff: the DLP rules work, but the unsigned exe cannot run on a managed Fed laptop, and when it cannot run the desktop app gives no protection and no warning.
Tested on 2026-10-02 to 2026-10-05 (pre-release build) and 2026-10-09 (release 0.2.1, commit b9542d0) on one Windows Fed laptop, in the Claude Code CLI and the desktop app's Code tab.
A small test round is possible only if the plugin runs from a location AppLocker allows (a signed exe, or a path IT allow-lists), and testers know the gaps below.
Coverage in the desktop app
The plugin fully protects only the Code tab; Chat needs the server-side inference hook (per DISTRIBUTION.md section 6).
Desktop surface
Plugin hooks run?
What is covered
Code tab (and CLI)
Yes, on the user's machine
Full pack: prompts, file reads, Office labels, paths, Bash, MCP arguments, if the exe can run
Cowork
In Cowork's VM, not the user's machine
Prompt and tool-argument text only; local files and labels are invisible; decision log stays in the VM
Chat
No
Nothing from the plugin; only the server-side inference hook (app/main.py)
Open question: does the Windows dlp-hook.exe run inside Cowork's VM at all?
What works
With the hook running (Python, loaded from the repo in the CLI), every core rule behaved as designed.
Behavior
Result
SSN in a prompt (123-45-6789)
Blocked at UserPromptSubmit by pii-ssn, with a reference id
Unmarked Office document
Blocked by classification-label-required (when auto-labeling is off or propose)
RESTRICTED FR document
Blocked by classification-ceiling; override refused (never_for)
Real Word label (FRSONLY, set in Word)
Read from docProps/custom.xml, allowed
Auto-labeling, apply mode (shipped default)
Writes INTERNAL FR - OFFICIAL USE\FRSONLY; Word shows the label without re-prompting; header written to word/headerDLP.xml; document body untouched
Claude after auto-labeling
Summarizes the file normally (the hook tells Claude the label it applied)
Word save after auto-labeling
Label metadata unchanged
Uninspectable files
Every non-PDF file the hook cannot read is denied (uninspectable-files matches all media types); PDFs without text are logged
Decision log
Every verdict recorded in %LOCALAPPDATA%\inference-hook-dlp\client-decisions.jsonl
Blockers
The exe fails open: wherever AppLocker blocks it, prompts and files reach Claude unchecked.
1. Documented install step is blocked. DISTRIBUTION.md 2a unzips to %TEMP% and runs dlp-hook.exe install there; AppLocker returns "This program is blocked by group policy."
2. Installed location is blocked. From an allow-listed folder (%USERPROFILE%\source\repos) the exe runs and installs, but into .claude\skills\inference-hook-dlp, where AppLocker blocks it again. The documented uninstall uses the same blocked exe; deleting the folder works.
3. Blocked hook = no protection.
    ◦ CLI: "UserPromptSubmit hook error ... Permission denied" shown as a non-blocking error; Claude answered a test SSN.
    ◦ Desktop Code tab: no error shown at all; the test SSN reached Claude. The decision log has no entry for the session.
    ◦ fail_mode: closed does not apply, because the hook never starts.
    ◦ Zscaler blocked one desktop request ("Access denied"), but not consistently; another session answered the SSN normally.
Required before any test round: option (a) sign the exe and _internal DLLs with the FRB publisher certificate, or (b) IT deploys to %ProgramFiles% with managed settings.
Suggested safety net: wrap the hook command in hooks.json so a launch failure exits with code 2 (block), for example ... || { echo "DLP hook could not run - blocked for safety" >&2; exit 2; }. Then "cannot run" means blocked, not allowed.
Gaps needing a fix or decision
Four fixes and two policy decisions are open; none blocks a small test round once the exe runs.
Gap
Type
Detail
Suggested action
/usage-restrictions blocks itself
Fix
dlp_status.py prints the classification ladder (RESTRICTED FR, RESTRICTED-CONTROLLED FR, CONFIDENTIAL FR); the PostToolUse hook matches those names and replaces the output with a new block
Drop the ladder from per-reference output, or exempt the hook's own status script
Ceiling matches label names in plain text
Fix
Any document that only mentions "RESTRICTED FR" (a policy doc, training slide) can be blocked
Match markings in headers and metadata, not any mention in body text
Auto-labeling on by default (apply)
Decision
The hook writes a label and header into users' Office files without asking; PACK.md marks this POLICY DECISION REQUIRED
InfoSec sign-off, or ship with propose for the test round
Default label FRSONLY
Decision
PACK.md: "POLICY: confirm sublabel"
InfoSec confirms the sublabel
User override
Fix (off by default)
In the pre-release build, an override was spent at UserPromptSubmit and the next PreToolUse blocked the same file 5 seconds later; release notes say overrides are now session-scoped
Retest before enabling
Ceiling override refusal message
Fix
Refusal says "no recent block with reference" instead of "this block cannot be overridden" (pre-release build)
Name the never_for rule in the message
Unknown binaries/archives
Settled
Denied, not logged; nothing falls through unmatched
None
Known issues for pilot testers
Testers should expect these and report them, not treat them as new bugs.
• First check can time out. The first hook check in a session took over 15 seconds and was blocked (fail closed). Retrying the same action worked.
• Header text is short. The auto-label header reads "INTERNAL FR", not Word's official FRSONLY marking "INTERNAL FR/OFFICIAL USE // FRSONLY".
• labeling.site_id is empty. Word still recognized the label on the test laptop; set the tenant id for production (shared privately, not in the repo).
• Files are in Compatibility Mode. The sample .docx files open in Compatibility Mode; real user files may behave differently.
• Plugin missing = no warning. A session without the plugin loaded shows nothing to the user; check that the SessionStart rule list appears.
Not yet tested
Five items from the DISTRIBUTION.md pilot checklist are still open.
[ ] Marketplace install (Path A): claude plugin list shows inference-hook-dlp@frb-infosec
[ ] Desktop Code tab with a working hook: SessionStart posts the rule list
[ ] claude plugin disable is refused under managed settings (needs IT)
[ ] Session-scoped user override in 0.2.x (off by default)
[ ] macOS (the checklist asks for one Windows and one macOS machine)
The checklist item "remove Python from PATH, every prompt is blocked" predates the 0.2.1 exe, which needs no Python; it should be rewritten for the exe.
Test environment and evidence
Item
Value
Machine
Windows Fed laptop, AppLocker enforced, Zscaler
Release tested
0.2.1, commit b9542d0 (main), package inference-hook-dlp-0.2.1-win-x64.zip
Pack
frb-baseline v2026.09.15, 12 rules, pack hash 30dfb9d6d75809c5
Clients
Claude Code CLI v2.1.286; Claude desktop app, Code tab
Decision log
%LOCALAPPDATA%\inference-hook-dlp\client-decisions.jsonl
Key references in the decision log:
• dlp_2d000db5a2ff: SSN prompt blocked by pii-ssn
• dlp_46e78a1728ac, dlp_e179b1ff452f: /usage-restrictions output replaced by classification-ceiling
• dlp_1a7805c668b3, dlp_d6777db8668c: pre-release override allowed at UserPromptSubmit, then blocked at PreToolUse
• dlp_e764578fbdb1: ceiling block, override refused
• No entries after 12:10 UTC on 2026-10-09: the exe sessions (CLI and desktop) never ran the hook
```
