```
Andrew, I wanted to show you the two files we discussed: the manifest and the Python installer.

The packaging and local verification are working. The installer validates all 159 files against the approved manifest before installation, and I tested that modifying a file causes the installation to fail.

What I'd like to accomplish next is move from local validation to testing on a managed Board laptop.

I'd also like your guidance on the endpoint DLP issue you encountered with `claude.exe`, and whether our existing hook can be used as a preflight tool in Cowork.

My main question is: **Once we validate these two files in your environment, what are the requirements and approvals needed to move this into an officially distributed plugin?**

I'd like to leave with an agreed next step, including what I should implement or document and what needs to be handled by the security or deployment team.
```
```
# DLP Hooks: Zscaler Meeting Prep

Sources: Jitesh's *DLP Hooks Progress Overview* (2026-09-21) and Marina's testing on 2026-10-19.

## 1. Where the work fits: one brain, three doors

| Door | What it covers | Status | Depends on | In today's Zscaler meeting? |
|---|---|---|---|---|
| Door 1: Claude Code hook (`client/hook.py`) | Code tab, on each laptop | Live | Marina + Zscaler + InfoSec; the verified installer is how it gets onto laptops safely | Yes |
| Door 2: Inference-hook server (`app/main.py`) | Chat + Cowork + Code, org-wide | Not switched on | IT hosting + Anthropic/FedStart admin (not Zscaler) | Only if asked |
| Path B: Zscaler rules | Block file uploads in Chat/Cowork + inline DLP | Waiting | Zscaler (spec already handed to them by Jitesh) | Yes |

## 2. Release sign-off process

| Step | What happens | Who | Status | Notes / decision |
|---|---|---|---|---|
| 1 | Release is tagged (e.g. `inference-hook-dlp--v0.2.1`) | Jitesh / team | Done | v0.2.1 = commit a695d11 |
| 2 | Automatic checks: regression tests + scanners + MartinAI review (if Andrew confirms). Output is a report. | To confirm with Andrew | To decide | |
| 3 | InfoSec signs off on that exact tag; approval recorded (GitLab approval, ticket or email) | InfoSec (owns the rulebook) | To decide | |
| 4 | Checklist (manifest) generated from the approved tag, ideally by an automated GitLab job | `make_manifest.py` | Built & tested | 159 files on 2026-10-19 |
| 5 | Checklist + seal code published somewhere read-only | To decide (protected repo?) | To decide | |
| 6 | Testers install with the checker; anything that doesn't match is refused | `install.py` | Built & tested | Tamper test blocked; SSN blocked in desktop app |

## 3. What belongs where (answer to Andrew's A/B/C question)

How it works today: git clone from GitLab → `install.py` verifies the SHA-256 of every file → python copies the files to `%LOCALAPPDATA%` → hooks registered in `settings.json`.

| Category | Item | Notes |
|---|---|---|
| Inside the package | Plugin files (today: all 159 files in the repo) | Could be trimmed to what the hook needs: `client/`, `hooks/`, `restrictions/`, `config/`, the engine. Fewer files with classification names to approve. |
| Outside the package | `install.py` and `make_manifest.py` | Kept separate so the checker isn't part of what it checks |
| Outside the package | Approved checklist (`approved-hashes.json`) + its SHA-256 seal | Must be read-only for testers |
| Outside the package | User's `settings.json` | Installer adds 4 hook entries; backup kept |
| Outside the package | Decision log (`client-decisions.jsonl`) | `%LOCALAPPDATA%\inference-hook-dlp` |
| Needs Zscaler approval | How files reach the laptop: git clone from GitLab | Was blocked on Andrew's machine (`PACK.md`) |
| Needs Zscaler approval | Alternative: one ZIP with a known SHA-256 from an internal location | Option C; one file to approve instead of a clone |
| Which programs touch the rule files | `git.exe` (clone), `python.exe` (hash, copy, hook at runtime) | `claude.exe` never opens them; it only reads `settings.json` and launches python |

## 4. Questions for the Zscaler meeting

| # | Topic | Question | Answer | Follow-up / owner |
|---|---|---|---|---|
| 1 | Transfer | Which is easier for you to approve: a git clone from GitLab, or one ZIP with a known SHA-256 from an internal location? | | |
| 2 | The rule | Can your rule allow these files when `python.exe` (the installer) handles them, or only when they match approved hashes? | | |
| 3 | MartinAI | Do you want the MartinAI review in step 2 for every release? If yes, which MartinAI/Bedrock setup should I use? | | |
| 4 | Sign-off | What evidence do you need from InfoSec's approval, and where should it be recorded? | | |
| 5 | Path B | What's the status of the upload-block and inline DLP spec Jitesh sent you for Chat and Cowork? | | |

## 5. Test evidence (Marina's Fed laptop, 2026-10-19)

| Test | Expected | Result | Reference / detail |
|---|---|---|---|
| Manifest generated from tag v0.2.1 | Checklist of every file | Pass | 159 files; matches `git ls-files` count (159) |
| Dry run on approved files | All files match | Pass | Checking 159 files... All files match |
| Tamper test (1 line added to `README.md`) | Install blocked | Pass | modified: README.md; BLOCKED; nothing installed |
| Real install | Files copied + hooks registered | Pass | `AppData\Local\inference-hook-dlp\plugin`; 4 hooks in `settings.json` |
| Rule pack loads from installed copy | SessionStart loads pack | Pass | frb-baseline v2026.09.15, 12 rules, fail_mode closed |
| SSN prompt in desktop app, Code tab | Prompt blocked | Pass | `dlp_84ee51a92a28`, rule pii-ssn, ~34 ms |

*Note: Jitesh's overview says 10 rules; the current pack has 12. The document predates the current pack.*
```
