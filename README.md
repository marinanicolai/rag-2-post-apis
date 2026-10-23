```
# Paths can hide inside a quoted script or one-liner, for example
#   python -c "import zipfile; zipfile.ZipFile(r'C:\Users\me\doc.docx')"
# The whole quoted script is one token, so look inside tokens too.
_EMBEDDED_QUOTED_RE = re.compile(r"""(['"])([^'"\r\n]{1,512})\1""")
_EMBEDDED_PATH_RE = re.compile(
    r"""(?:[A-Za-z]:[\\/]|\\\\|~[\\/]|\.{1,2}[\\/]|/)[^\s'"`<>|;,(){}\[\]]+"""
    r"""|[^\s'"`<>|;,(){}\[\]=:\\/]+\.[A-Za-z][A-Za-z0-9]{0,7}\b"""
)
# Scripts a command runs (python extract.py) are read and scanned for paths too.
_SCRIPT_EXTS = {".py", ".ps1", ".sh", ".bash", ".bat", ".cmd", ".js", ".rb", ".pl", ".r"}
_MAX_EMBEDDED_SCAN_CHARS = 50_000
_MAX_SCRIPT_BYTES = 200_000


def _embedded_candidates(text: str) -> list[str]:
    """Possible file paths inside a token or script: quoted strings and path-like words."""
    if not text:
        return []
    text = text[:_MAX_EMBEDDED_SCAN_CHARS]
    cands = [m.group(2) for m in _EMBEDDED_QUOTED_RE.finditer(text)]
    cands += [m.group(0) for m in _EMBEDDED_PATH_RE.finditer(text)]
    # Undo escaped backslashes from string literals: C:\\Users -> C:\Users
    return [c.replace("\\\\", "\\") for c in cands]


def _read_script_text(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return f.read(_MAX_SCRIPT_BYTES).decode("utf-8", errors="ignore")
    except OSError:
        return ""
```
```

