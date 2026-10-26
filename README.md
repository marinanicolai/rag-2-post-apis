```
# The Claude desktop app (Cowork) runs plugin hooks with the host's python.exe,
# which usually has no PyYAML. Fall back to the pure-Python copy in vendor/;
# an installed PyYAML (with its C speedups) still wins because it is found first.
def _ensure_yaml() -> None:
    import os as _os
    import sys as _sys
    try:
        import yaml  # noqa: F401
    except ImportError:
        _vendor = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "vendor")
        if _vendor not in _sys.path:
            _sys.path.append(_vendor)


_ensure_yaml()
```
