Two of his points are quick fixes, and one is a decision for you.

## 1. The stale spec

The checked-in `ZSCALER_RULE_SPEC.md` was generated before your last edit to the mapping. Most likely the spec ran before the `zscaler_spec.py` edit was saved, or the regenerated files weren't the ones committed. Confirm and fix:

```powershell
git checkout marina-dev
git pull
python -m pytest tests\test_zscaler_spec.py -q
```

If `test_the_checked_in_document_is_current` fails, regenerate:

```powershell
python scripts\zscaler_spec.py
```

## 2. `risks.yaml` still references the old test name

Risk 11's `pytest` evidence line selects tests by keyword, and it still includes `image_is_allowed`. You renamed that test to `test_read_image_is_blocked`, so the keyword quietly matches nothing.

Open `docs\risks.yaml` (`Ctrl+P`, then `docs/risks.yaml`, then `Ctrl+F` for `image_is_allowed`). On the `- {type: pytest, select: [...]}` line under risk 11, change `image_is_allowed` to `image_is_blocked`. Save, confirm, then regenerate the register:

```powershell
Select-String -Path docs\risks.yaml -Pattern "image_is"
python scripts\risk_register.py
python -m pytest tests -q
```

The first command should show only `image_is_blocked`. If everything's green, commit the regenerated docs with the YAML:

```powershell
git status --short
git add docs\risks.yaml docs\ZSCALER_RULE_SPEC.md docs\ZSCALER_RULE_SPEC.docx docs\RISK_REGISTER.md docs\RISK_REGISTER.docx docs\RISK_REGISTER.xlsx docs\evidence\risk-evidence.json
git commit -m "Regenerate Zscaler spec and risk register; point risk 11 at renamed image test"
git push
```

Add only the files `git status` shows as modified.

## 3. Archives and unknown binaries: log or deny

He'll go with whichever you pick. I'd keep **logging** for now, for two reasons. It matches his own approach for scanned PDFs: measure the false-positive rate first, then decide. And denying would block everyday attachments like a `.zip` of code or logs before anyone knows how common they are. Switching later is a one-line change.

## 

Testing the metadata check, auto-labeling, and user override from the C4G DLP Hooks repo is separate. Do it after this, on a fresh clone, so it doesn't mix with `marina-dev`. Your E-step demo folder works as the test setup.

A reply you could send:

> Thanks! Fixed both: reran zscaler_spec.py and risk_register.py, and pointed risks.yaml at image_is_blocked. Pushed to marina-dev. For unknown binaries and archives, let's keep logging for now, same as scanned PDFs, and decide once the decision log shows how often they come up. I'll pull the C4G DLP Hooks repo next and test the metadata check, auto-labeling and user override on my machine.
