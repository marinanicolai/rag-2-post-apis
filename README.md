```
Fix: Bash commands could read above-ceiling files through quoted scripts
```
```
## Problem
During DLP testing on 2026-10-23, Claude read a Word document labeled above the INTERNAL FR ceiling in the Code tab and the CLI.

- Claude Code's Read tool rejected the .docx before calling the hook (no PreToolUse Read entry in the decision log).
- Claude then ran a Python one-liner (zipfile) to extract the text. PreToolUse and PostToolUse for Bash both returned allow.
- A manual PreToolUse Read on the same file is denied by classification-ceiling, so label detection works; the Bash path detection missed the file.

Cause: `_bash_file_refs` treats a quoted script as one token, so a path inside it was never resolved or inspected. Tokens over 512 characters were skipped entirely.

## Fix
- `_bash_file_refs` now also looks for paths inside each token (quoted strings and path-like words, with escaped backslashes undone).
- Paths are taken from the token before trailing punctuation is stripped, so quoted paths with spaces are found.
- Scripts the command runs (for example `python extract.py`) are read and scanned for file paths too.
- Existing behaviour for plain paths and the `bash_max_files` limit is unchanged.

## Tests
- New: `tests/test_bash_file_refs.py` (8 tests: plain path, one-liner, relative path, path with spaces, script file, limit, escaped backslashes, no false matches).
- Full suite passes locally on Python 3.14.
- Manual: the zipfile one-liner is now denied by classification-ceiling, exit code 2 (dlp_5a0c21c9e1cd).
- In Claude (Code tab, dev build): asked Claude to read the labeled .docx; Claude's script was denied: `PreToolUse deny classification-ceiling Bash` at 14:51:12. With 0.2.1 the same flow was `allow`.

## Pipeline note
The `tests` job also fails on `main` (same error). The runner uses the shell executor with system Python 3.9, but `app/config.py` uses `@dataclass(slots=True)`, which needs Python 3.10+. Not caused by this change.

## Not covered
- Claude Code's Read tool rejecting .docx before the hook runs is Claude Code behaviour, not the hook's.

## Related
- fix/ceiling-message-no-label: after a block, Zscaler 403'd the next request because the label was named. Both proposed for release 0.2.2.

## Release
Proposed for 0.2.2, after review and InfoSec sign-off, with a new checklist (`make_manifest.py`).
```
