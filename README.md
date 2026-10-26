```
   _VM_PATH_IN_TEXT_RE = re.compile(r"(?:/sessions/[^/\s'\"`]+)?/mnt/[^\s'\"`;|&<>(){}\[\]]+")


   def _state_dir() -> str:
       return os.environ.get("DLP_STATE_DIR") or os.path.dirname(resolve_log_path(None))


   def _vm_shell_refs(command: str, cwd: str | None, limit: int) -> list[str]:
       """Cowork mcp__workspace__bash: host files named by VM paths in the command.

       Finds /sessions/<id>/mnt/... paths anywhere in the text (also inside python -c "..."),
       follows `cd /abs && cat rel`, and maps each one to the host file (client/cowork.py).
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
           if not cowork.is_vm_path(part):
               continue
           host = cowork.to_host(part, cwd, _state_dir())
           if host and os.path.isfile(host) and host not in found:
               found.append(host)
               if len(found) >= limit:
                   break
       return found
```
