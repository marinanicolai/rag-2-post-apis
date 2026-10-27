```
## Problem
A prompt that names a file above the classification ceiling was allowed by the hook
and only stopped later by Zscaler at the network, with a generic "Access denied" (403).

Example prompt: `open Q3_budget_RESTRICTED_FR.txt`
- Hook: `UserPromptSubmit` → **allow** (ref `dlp_7bc86c3685d9`)
- Result: request left the laptop and was blocked by Zscaler

## Root cause
`_marking_regex()` in `client/classification.py` let the spaces in a marking
(e.g. "RESTRICTED FR") match only spaces or dashes. Underscores, common in file
names, did not match, so `RESTRICTED_FR` was never detected in prompt text.

## Fix
Allow underscores as a separator in `_marking_regex()`:

    |\s+)   →   |[\s_]+)

The boundary check (`(?<![A-Za-z0-9])…(?![A-Za-z0-9])`) already treats `_`
as a boundary, so no other change was needed. Because this is the shared marking
pattern, the fix applies wherever text is scanned (prompts, Bash commands, Write content).

## Tests
- New: `tests/test_classification_filename.py`
  - underscored file name in prompt → match
  - spaces and dashes still match (no regression)
  - unrelated file name (`notes_internal.txt`) → no match
- Full suite: all passing

## Verified in Claude desktop (Code tab)
| | Before | After |
|---|---|---|
| Hook result | allow | **deny** |
| Rule | – | `classification-ceiling` (critical) |
| Reference | `dlp_7bc86c3685d9` | `dlp_77813262451d` |
| Caught by | Zscaler (403, no reason) | Hook (clear message, local) |
| Latency | – | 39 ms |

**Before:**
<!-- paste screenshot -->

**After:**
<!-- paste screenshot -->

Verified locally by temporarily replacing the installed `classification.py`
(original restored afterward). Needs a new approved release manifest before rollout.

## Notes for reviewers
- **Possible false positives:** code identifiers such as `RESTRICTED_FR = ...`
  will now be blocked. Narrowing the match to file-name-like tokens is an option
  if this proves noisy (policy decision).
- **Related gap, not in this MR:** tool output (e.g. directory listings) is not
  scanned, so file names returned by tools can reach the model. Consider
  `PostToolUse` scanning in a follow-up.
```
