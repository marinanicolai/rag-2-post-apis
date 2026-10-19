```
#!/usr/bin/env python3
"""
make_manifest.py - build the approved-hashes manifest for one DLP plugin release.

Run this on a clean checkout of an InfoSec-approved release tag. The output
is what install.py checks every file against before installing anything.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Folders never included in the manifest. Must match install.py.
SKIP_DIRS = {".git", "release", "__pycache__", ".pytest_cache", ".venv", "venv"}
SKIP_SUFFIXES = {".pyc", ".pyo"}

HASH_RULE = "sha256; for text files (no NUL bytes) CRLF is normalized to LF before hashing"


# ---- Keep file_hash() and walk_files() identical in install.py ----
def file_hash(path: Path) -> str:
    data = path.read_bytes()
    if b"\0" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def walk_files(root: Path) -> list[str]:
    found = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.is_file() and p.suffix not in SKIP_SUFFIXES:
            found.append(rel.as_posix())
    return sorted(found)
# -------------------------------------------------------------------


def git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=root, capture_output=True,
                             text=True, check=True)
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Build approved-hashes.json for a plugin release.")
    ap.add_argument("--version", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--plugin-dir", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--plugin-name", default="inference-hook-dlp")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    root = Path(args.plugin_dir).resolve() if args.plugin_dir else Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"ERROR: plugin dir not found: {root}", file=sys.stderr)
        return 2

    commit = git(root, "rev-parse", "HEAD")
    if not args.allow_dirty:
        if commit is None:
            print("ERROR: not a git checkout.", file=sys.stderr)
            return 2
        if git(root, "status", "--porcelain", "--untracked-files=all"):
            print("ERROR: working tree has changes or untracked files.", file=sys.stderr)
            return 2
        tag_commit = git(root, "rev-list", "-n", "1", args.tag)
        if tag_commit != commit:
            print(f"ERROR: HEAD ({commit}) is not at tag {args.tag} ({tag_commit}).", file=sys.stderr)
            return 2

    files = {rel: file_hash(root / rel) for rel in walk_files(root)}
    if not files:
        print("ERROR: no files found to hash.", file=sys.stderr)
        return 2

    manifest = {
        "schema": 1,
        "plugin": args.plugin_name,
        "version": args.version,
        "tag": args.tag,
        "commit": commit,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hash_rule": HASH_RULE,
        "files": files,
    }

    out = Path(args.out) if args.out else root / "release" / "approved-hashes.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(manifest, indent=2) + "\n"
    out.write_text(body, encoding="utf-8", newline="\n")

    print(f"Wrote {out}")
    print(f"  {len(files)} files, release {args.version} ({args.tag}), commit {commit}")
    print(f"  Manifest SHA-256: {hashlib.sha256(body.encode('utf-8')).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
