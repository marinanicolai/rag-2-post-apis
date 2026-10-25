```
git add restrictions/classification-ceiling.md tests/test_client_hook.py tests/test_server_pack_dir.py docs/ZSCALER_RULE_SPEC.md docs/ZSCALER_RULE_SPEC.docx
git status
git commit -m "Do not name the label in the classification-ceiling message" -m "The deny message named the file's label. Claude sends the hook's message back to the model with the next request, and Zscaler then blocks that request (403), so users saw 'Access denied' instead of the hook's reason and the session could not continue. The message now says the content is above the approved level without naming the label. Tests updated to match; the label is still recorded in the decision log. Regenerated docs/ZSCALER_RULE_SPEC (pack hash changes to 52fd7fed6ca1898c)."
git push -u origin fix/ceiling-message-no-label
```
```
Draft: Do not name the label in the classification-ceiling message
```



```
## Problem
When the hook blocks a file above the INTERNAL FR ceiling, its message named the file's label. Claude sends the hook's message back to the model with the next request, and Zscaler then blocks that request (403). Users saw "Access denied... check your permissions" instead of the hook's reason, and the session could not continue.

Evidence (2026-10-23, Code tab): the hook denied a Bash command at 14:51:12 and 15:10:45 (classification-ceiling); in both cases the next model request got Zscaler 403. Earlier requests in the same sessions, including a prompt containing the word "confidential", went through.

## Fix
- `restrictions/classification-ceiling.md`: the user message no longer includes `{label}`. It now says the content "carries a classification above the level approved for use with Claude (INTERNAL FR)".
- The label is still recorded in the decision log for InfoSec.
- Tests updated for the new wording (`tests/test_client_hook.py`, `tests/test_server_pack_dir.py`).
- Regenerated `docs/ZSCALER_RULE_SPEC` (`python scripts/zscaler_spec.py`); pack hash changes from 30dfb9d6d75809c5 to 52fd7fed6ca1898c.

## Tests
- Full suite: 358 passed, 3 skipped.
- Manual: PreToolUse Read on a document above the ceiling is denied (exit 2) with the new message; the old wording is gone.
- In Claude: [to add: block, then "hello" in the same session]

## For InfoSec
This changes rulebook text, so the pack hash changes. Should the pack version (2026.09.15) be bumped?

## Related
- fix/bash-embedded-paths (Bash bypass fix). Both proposed for release 0.2.2.
```
```
$inst = "$env:LOCALAPPDATA\inference-hook-dlp\plugin"
Select-String -Path "$inst\restrictions\classification-ceiling.md" -Pattern "carries a classification" -Quiet
Select-String -Path "$inst\client\hook.py" -Pattern "_embedded_candidates" -Quiet
```
```
cd C:\Users\M3MXN08\repo\c4g-dlp-hooks-repo
git branch --show-current
$tools = "C:\Users\M3MXN08\repo\dlp-installer"
python $tools\make_manifest.py --version 0.2.2-dev --tag dev --plugin-dir . --out $tools\dev-hashes.json --allow-dirty
python $tools\install.py --uninstall
$devsha = (Get-FileHash $tools\dev-hashes.json -Algorithm SHA256).Hash
python $tools\install.py --manifest $tools\dev-hashes.json --manifest-sha256 $devsha --source .
```
