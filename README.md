```
@'
import re

from client.classification import _marking_regex


def _pattern():
    return re.compile(_marking_regex("RESTRICTED FR"), re.I)


def test_marking_matches_underscored_file_name_in_prompt():
    assert _pattern().search("open Q3_budget_RESTRICTED_FR.txt")


def test_marking_still_matches_spaces_and_dashes():
    assert _pattern().search("RESTRICTED FR")
    assert _pattern().search("Restricted - FR")


def test_marking_ignores_unrelated_file_name():
    assert not _pattern().search("open notes_internal.txt")
'@ | Set-Content -Path tests\test_classification_filename.py -Encoding UTF8
```
```
python -m pytest tests\test_classification_filename.py -q
```
```
git add client\classification.py tests\test_classification_filename.py
git commit -m "fix: detect classification markings in underscored file names in prompt text"
git push -u origin fix/prompt-filename-classification
```
