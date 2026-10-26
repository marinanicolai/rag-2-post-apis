```
"""Cowork (Claude desktop app) support: translate task-VM paths back to host paths.

In the Claude desktop app the hooks run on the Windows host, but Claude works in a
Linux VM. What a hook sees:

    cwd                       <...>\\local-agent-mode-sessions\\<org>\\<user>\\<task>\\host-cwd  (empty)
    Read / Edit / Write path  a host (Windows) path
    shell tool                tool_name "mcp__workspace__bash", command uses VM paths:
                              /sessions/<id>/mnt/uploads/x.docx, /sessions/<id>/mnt/<folder>/...
    dragged-in file           <task>\\uploads\\x.docx; prompt starts with
                              <uploaded_files><file><file_path>C:\\...\\x.docx</file_path>...

``to_host`` maps a VM path to the host file the hook can open:

    /sessions/<id>/mnt/uploads/...   -> <task>\\uploads\\...
    /sessions/<id>/mnt/outputs/...   -> <task>\\outputs\\...
    /sessions/<id>/mnt/<name>/...    -> a connected folder named <name>: learned from host
                                        paths seen in file-tool calls (folders.json), else a
                                        folder called <name> directly under one of the search
                                        roots (Downloads, Documents, Desktop, OneDrive*, the
                                        profile; override with DLP_HOST_FOLDER_SEARCH_ROOTS,
                                        os.pathsep-separated).

A VM path that cannot be mapped returns None; the caller decides (hook.py fails closed
for file-looking paths under a connected folder).
"""

from __future__ import annotations

import glob
import json
import os
import re
from typing import Any, Mapping

SHELL_TOOLS = ("Bash", "mcp__workspace__bash")
VM_MNT_RE = re.compile(r"^/sessions/[^/]+/mnt/([^/]+)(?:/(.*))?$")
SHORT_MNT_RE = re.compile(r"^/mnt/(uploads|outputs)(?:/(.*))?$")
UPLOADED_FILE_RE = re.compile(r"<file_path>\s*(.*?)\s*</file_path>", re.DOTALL)
_STATE_FILE = "folders.json"
_MAX_LEARNED = 400


def task_dir(cwd: str | None) -> str | None:
    """The Cowork task folder (parent of ``host-cwd``), or None outside Cowork."""
    if not cwd:
        return None
    norm = cwd.rstrip("\\/")
    if os.path.basename(norm.replace("\\", "/")).lower() == "host-cwd":
        return os.path.dirname(norm.replace("\\", os.sep).replace("/", os.sep)) or None
    return None


def is_cowork(payload: Mapping[str, Any]) -> bool:
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None
    return task_dir(cwd) is not None or str(payload.get("tool_name") or "") == "mcp__workspace__bash"


def is_vm_path(path: str) -> bool:
    return bool(VM_MNT_RE.match(path) or SHORT_MNT_RE.match(path))


def _state_path(state_dir: str) -> str:
    return os.path.join(state_dir, _STATE_FILE)


def _load(state_dir: str) -> dict[str, str]:
    try:
        with open(_state_path(state_dir), "rb") as fh:
            data = json.load(fh)
        anc = data.get("ancestors") if isinstance(data, dict) else None
        return {str(k): str(v) for k, v in (anc or {}).items()}
    except (OSError, ValueError):
        return {}


def learn(host_path: str, state_dir: str) -> None:
    """Remember every ancestor directory of a host path by basename (lower-cased)."""
    if not host_path or is_vm_path(host_path) or not os.path.isabs(host_path):
        return
    anc = _load(state_dir)
    before = dict(anc)
    d = os.path.dirname(os.path.normpath(host_path))
    for _ in range(12):
        name = os.path.basename(d)
        if not name:
            break
        anc.setdefault(name.lower(), d)
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    if anc == before:
        return
    if len(anc) > _MAX_LEARNED:
        anc = dict(list(anc.items())[-_MAX_LEARNED:])
    try:
        os.makedirs(state_dir, exist_ok=True)
        tmp = _state_path(state_dir) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump({"ancestors": anc}, fh, indent=1)
        os.replace(tmp, _state_path(state_dir))
    except OSError:
        pass


def search_roots() -> list[str]:
    env = os.environ.get("DLP_HOST_FOLDER_SEARCH_ROOTS")
    if env:
        raw = [p for p in env.split(os.pathsep) if p.strip()]
    else:
        home = os.path.expanduser("~")
        raw = [os.path.join(home, n) for n in ("Downloads", "Documents", "Desktop")]
        raw += [os.path.join(home, "OneDrive*"), os.path.join(home, "OneDrive*", "*"), home]
    out: list[str] = []
    for r in raw:
        r = os.path.expandvars(os.path.expanduser(r.strip()))
        for hit in (sorted(glob.glob(r)) if any(c in r for c in "*?[") else [r]):
            if os.path.isdir(hit) and hit not in out:
                out.append(hit)
    return out


def _join(base: str, rest: str | None) -> str:
    return os.path.normpath(os.path.join(base, *(rest or "").split("/"))) if rest else os.path.normpath(base)


def to_host(path: str, cwd: str | None, state_dir: str) -> str | None:
    """Map a VM path to a host path; None when it cannot be mapped. Non-VM paths pass through."""
    m = VM_MNT_RE.match(path) or SHORT_MNT_RE.match(path)
    if not m:
        return path
    name, rest = m.group(1), m.group(2)
    task = task_dir(cwd)
    if name in ("uploads", "outputs"):
        return _join(os.path.join(task, name), rest) if task else None
    if name.startswith("."):
        return None  # .local-plugins and other app-internal mounts
    learned = _load(state_dir).get(name.lower())
    if learned and os.path.isdir(learned):
        return _join(learned, rest)
    for root in search_roots():
        cand = os.path.join(root, name)
        if os.path.isdir(cand):
            return _join(cand, rest)
        if os.path.basename(root).lower() == name.lower():
            return _join(root, rest)
    return None


def uploaded_files(prompt: str) -> list[str]:
    """Host paths listed in Cowork's <uploaded_files> block."""
    if "<uploaded_files>" not in prompt and "<file_path>" not in prompt:
        return []
    out: list[str] = []
    for m in UPLOADED_FILE_RE.finditer(prompt):
        p = m.group(1).strip()
        if p and p not in out:
            out.append(p)
    return out


def task_roots(cwd: str | None) -> list[str]:
    task = task_dir(cwd)
    if not task:
        return []
    return [d for d in (os.path.join(task, "uploads"), os.path.join(task, "outputs")) if os.path.isdir(d)]
```
