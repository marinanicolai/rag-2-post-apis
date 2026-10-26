```
def _read_payload(argv: list[str] | None = None) -> dict[str, Any]:
    """Hook JSON from stdin, or from the file given as --stdin-file PATH (Windows launcher)."""
    argv = sys.argv if argv is None else argv
    raw = ""
    if "--stdin-file" in argv:
        i = argv.index("--stdin-file")
        if i + 1 >= len(argv):
            raise PayloadError("--stdin-file needs a path")
        try:
            with open(argv[i + 1], "rb") as fh:
                raw = fh.read().decode("utf-8-sig", "replace")
        except OSError as exc:
            raise PayloadError(f"cannot read --stdin-file: {exc}") from exc
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    if not raw.strip():
        raise PayloadError("no payload on stdin")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PayloadError(f"stdin is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise PayloadError(f"stdin is a {type(data).__name__}, expected a JSON object")
    return data
```
