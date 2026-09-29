"""PreToolUse guard for git commands run through Claude Code's Bash tool.

Blocks (exit 2, reason on stderr):
  - bulk staging: git add -A / --all / . / * / :/
  - committing everything: git commit -a / --all / -am ...
  - staging or committing secret files (hash.salt, .env files, keys)

Everything else is allowed (exit 0). If the guard itself fails it allows the
command and prints a warning: it is a safety net for a named-files habit, not
a security control.
"""
from __future__ import annotations

import fnmatch
import json
import re
import shlex
import subprocess
import sys
from pathlib import PurePath

SECRET_PATTERNS = ("hash.salt", "*.salt", ".env", "*.env", ".env.*", "*.pem", "*.key", "id_rsa*", "*.pfx")
ALLOWED_SECRET_LOOKALIKES = (".env.example", "env.example")
BULK_ADD = {"-A", "--all", ".", "*", ":/", "--no-ignore-removal"}


def is_secret(path: str) -> bool:
    name = PurePath(path.replace("\\", "/")).name
    if name in ALLOWED_SECRET_LOOKALIKES:
        return False
    return any(fnmatch.fnmatch(name.lower(), p) for p in SECRET_PATTERNS)


def git_invocations(command: str) -> list[list[str]]:
    """Split a shell line on && || ; | and return the argv of each git call."""
    calls = []
    for part in re.split(r"&&|\|\||;|\|", command):
        try:
            argv = shlex.split(part, posix=True)
        except ValueError:
            argv = part.split()
        # skip leading env assignments like FOO=1 git ...
        while argv and "=" in argv[0] and not argv[0].startswith("-"):
            argv = argv[1:]
        if len(argv) >= 2 and PurePath(argv[0]).name.lower() in ("git", "git.exe"):
            calls.append(argv[1:])
    return calls


def check_add(args: list[str]) -> str | None:
    flags = [a for a in args[1:] if a.startswith("-")]
    paths = [a for a in args[1:] if not a.startswith("-")]
    bulk = [a for a in args[1:] if a in BULK_ADD]
    if bulk:
        return (f"'git add {' '.join(bulk)}' stages everything, including local secrets and notes. "
                "Add the changed files by name instead (git add <file> ...).")
    if "-u" in flags or "--update" in flags:
        return "'git add -u' stages every modified file. Add the changed files by name instead."
    secrets = [p for p in paths if is_secret(p)]
    if secrets:
        return f"refusing to stage secret file(s): {', '.join(secrets)}. Keep them out of git (add them to .gitignore)."
    return None


VALUE_SHORT = set("mFCct")          # short commit options that take a value
VALUE_LONG = {"--message", "--file", "--reuse-message", "--reedit-message", "--template", "--author", "--date"}


def commit_all_flag(args: list[str]) -> bool:
    """True if a git commit argv (without 'commit') uses -a/--all."""
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            break
        if a == "--all":
            return True
        if a in VALUE_LONG:
            i += 2
            continue
        if a.startswith("-") and not a.startswith("--") and len(a) > 1:
            for pos, ch in enumerate(a[1:]):
                if ch == "a":
                    return True
                if ch in VALUE_SHORT:
                    if pos == len(a) - 2:   # value is the next argument
                        i += 1
                    break                   # rest of this cluster is the value
        i += 1
    return False


def check_commit(args: list[str], cwd: str | None) -> str | None:
    if commit_all_flag(args[1:]):
        return ("'git commit -a' commits every modified file. Stage the changed files by name, "
                "check git status, then commit without -a.")
    try:
        staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=cwd or None,
                                capture_output=True, text=True, timeout=10).stdout.split()
    except Exception:
        return None
    secrets = [p for p in staged if is_secret(p)]
    if secrets:
        return (f"secret file(s) are staged: {', '.join(secrets)}. "
                f"Unstage with 'git restore --staged {' '.join(secrets)}' and add them to .gitignore.")
    return None


def decide(payload: dict) -> str | None:
    command = (payload.get("tool_input") or {}).get("command") or ""
    cwd = payload.get("cwd")
    for argv in git_invocations(command):
        sub = argv[0]
        if sub == "add":
            reason = check_add(argv)
        elif sub == "commit":
            reason = check_commit(argv, cwd)
        else:
            reason = None
        if reason:
            return reason
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        reason = decide(payload)
    except Exception as exc:  # never break the user's session over the guard itself
        print(f"git guard skipped: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 0
    if reason:
        print(f"Blocked by dlp-pack-workflow git guard: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
