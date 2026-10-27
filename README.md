The error is one line, and it breaks every test because they all import `classification.py`. Python rejects line 244, where `_PROMPT_PATH_RE` is defined.

Most likely, `class PathDetector:` has a decorator above it (a line starting with `@`), and the new lines got pasted **between the decorator and the class**. Python doesn't allow anything there. The triple quotes may also have been changed into curly quotes when copying.

The fix is to move the line somewhere safe and use simpler quoting.

**1.** Delete the two lines you added above `class PathDetector:`, the comment and `_PROMPT_PATH_RE = ...`.

**2.** Find `DEFAULT_CEILING = "INTERNAL FR"` (line 60) and add this line right **below** it:

```python
_PROMPT_PATH_RE = re.compile(r"(?:[A-Za-z]:[\\/]|~[\\/]|\.{1,2}[\\/]|[\\/])[^\s'\"<>|`]+")
```

**3.** Save, then check that the file loads:

```powershell
python -c "import client.classification; print('ok')"
```

If it prints `ok`, rerun `python -m pytest -q`. If it errors, send me this:

```powershell
Get-Content client\classification.py | Select-Object -Skip 236 -First 12
```
