
The prompt text is the segment with **`kind="text"`** (line 201). Every other kind is a tool input, tool result, or attachment, so we limit the new check to `"text"` and bash commands and file writes stay unaffected.

**Step 1.** Open the file with `code client\classification.py`. Just **above** `class PathDetector:` (line 243), add:

```python
# Path-like strings in prompt text, e.g. C:\..., ~/..., ./..., /...
_PROMPT_PATH_RE = re.compile(r"""(?:[A-Za-z]:[\\/]|~[\\/]|\.{1,2}[\\/]|[\\/])[^\s"'<>|`]+""")
```

**Step 2.** Inside `PathDetector`, replace the whole `find` method, from `def find(self, segment...` down to its final `return []`, with this. Keep the 4-space indentation, so `def` lines up with the other methods:

```python
    def _match_path(self, raw: str) -> list[Match]:
        path = raw.replace("\\", "/")
        lowered = path.lower()
        for g in self.globs:
            if fnmatch.fnmatchcase(lowered, g) or fnmatch.fnmatchcase(lowered.rsplit("/", 1)[-1], g):
                return [Match(path, "path", 0, 0)]
        if self.regex is not None and self.regex.search(path):
            return [Match(path, "path", 0, 0)]
        return []

    def find(self, segment: Segment) -> list[Match]:
        # Files Claude opens (unchanged behavior).
        if segment.kind == "attachment" and segment.file_name:
            return self._match_path(segment.file_name)
        # User prompt text: check path-like strings against the same rules.
        if segment.kind == "text" and segment.text:
            for m in _PROMPT_PATH_RE.finditer(segment.text):
                hits = self._match_path(m.group(0).rstrip(".,;:)]}"))
                if hits:
                    return hits
        return []
```

The attachment logic is the same as before, just moved into `_match_path`, so both paths share it.

**Step 3.** Save and run the full suite:

```powershell
python -m pytest -q
```

Send me the result. If everything passes, we'll add a test for this case and verify it in Claude desktop with the same swap method as before.

