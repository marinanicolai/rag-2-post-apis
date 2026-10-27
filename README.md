```
## Problem
A prompt naming a restricted path was allowed by the hook:
`Show me what's in C:\Users\M3MXN08\.ssh\id_rsa`
- `UserPromptSubmit` → **allow** (ref `dlp_53f456f78171`)
- Only Claude's own refusal stopped it; the hook never checked the path.

## Root cause
1. `restricted-paths` had `applies_to: [file]`, so it never ran on prompt text.
2. `PathDetector.find()` only handled attachment segments, so even with the rule
   enabled for prompts it had nothing to check.

## Fix
- `restrictions/restricted-paths.md`: `applies_to: [prompt, file]`
- `client/classification.py`:
  - `_PROMPT_PATH_RE` extracts path-like strings (`C:\…`, `~/…`, `./…`, `/…`) from prompt text
  - `PathDetector.find()` checks them against the existing globs for `kind == "text"`
  - shared `_match_path()` helper; attachment behavior unchanged
  - scope limited to prompt text, so tool inputs/outputs are unaffected
- `docs/ZSCALER_RULE_SPEC.md` / `.docx`: regenerated (`python scripts/zscaler_spec.py`)
  because the pack hash changed → `49d0423d84f23fc4`. **Zscaler team may need the updated spec.**

## Tests
- Full suite passing.

## Verified in Claude desktop (Code tab)
| | Before | After |
|---|---|---|
| Hook result | allow | **deny** |
| Rule | – | `restricted-paths` |
| Pack hash | `30dfb9d6d75809c5` | `49d0423d84f23fc4` |

**Before:** <!-- screenshot -->
**After:** <!-- screenshot -->

## Notes for reviewers
- Possible false positives: prompts that mention a restricted path in passing
  (e.g. "how do I set up ~/.ssh/config?") will now be blocked. Policy decision.
- `classification-in-file-name` is also `applies_to: [file]`; the related gap is
  handled separately in `fix/prompt-filename-classification`.
```
