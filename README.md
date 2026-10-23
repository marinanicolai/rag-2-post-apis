```
def _bash_file_refs(command: str, cwd: str | None, limit: int) -> list[str]:
    out: list[str] = []
    if limit <= 0:
        return out

    def consider(cand: str) -> bool:
        """Add cand if it is an existing file. Returns True once the limit is reached."""
        cand = cand.strip().strip("'\"").rstrip(_TRAILING_PUNCT)
        if not cand or cand.startswith("-") or len(cand) > 512:
            return False
        p = _resolve(cand, cwd)
        if os.path.isfile(p) and p not in out:
            out.append(p)
            return len(out) >= limit
        return False

    for m in _BASH_TOKEN_RE.finditer(command):
        tok = next(g for g in m.groups() if g is not None).strip().rstrip(_TRAILING_PUNCT)
        if not tok:
            continue
        # 1. The token itself, split on shell operators (original behaviour).
        if not tok.startswith("-") and len(tok) <= 512 and ("/" in tok or "\\" in tok or "." in tok):
            for part in re.split(r"[;|&<>]+", tok):
                if consider(part):
                    return out
        # 2. Paths inside the token, e.g. a quoted one-liner.
        for cand in _embedded_candidates(tok):
            if consider(cand):
                return out

    # 3. Scripts the command runs: check the files they reference too.
    for p in list(out):
        if os.path.splitext(p)[1].lower() in _SCRIPT_EXTS:
            for cand in _embedded_candidates(_read_script_text(p)):
                if consider(cand):
                    return out
    return out
```

