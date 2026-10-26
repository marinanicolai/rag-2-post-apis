```
$code = @'


_VM_PATH_IN_TEXT_RE = re.compile(r"(?:/sessions/[^/\s'\"`]+)?/mnt/[^\s'\"`;|&<>(){}\[\]]+")


def shell_refs(command: str, cwd: str | None, limit: int, state_dir: str) -> list[str]:
    """Host files named by VM paths in a Cowork mcp__workspace__bash command.

    Finds /sessions/<id>/mnt/... paths anywhere in the text (also inside python -c "..."),
    follows `cd /abs && cat rel`, and maps each one to the host file.
    """
    found: list[str] = []
    words = [next(g for g in t if g) for t in re.findall(r'"([^"]+)"|\'([^\']+)\'|(\S+)', command)]
    vm_cwd = None
    for i, w in enumerate(words):
        if i > 0 and words[i - 1] == "cd" and w.startswith("/"):
            vm_cwd = w.rstrip("/")
    candidates = [m.group(0) for m in _VM_PATH_IN_TEXT_RE.finditer(command)]
    if vm_cwd:
        candidates += [vm_cwd + "/" + w for w in words if not w.startswith(("/", "-")) and "." in w]
    for part in candidates:
        part = part.rstrip(",.;:)]}>\"'`")
        if not is_vm_path(part):
            continue
        host = to_host(part, cwd, state_dir)
        if host and os.path.isfile(host) and host not in found:
            found.append(host)
            if len(found) >= limit:
                break
    return found
'@
[IO.File]::AppendAllText("$PWD\client\cowork.py", $code.Replace("`r`n", "`n") + "`n")
```
