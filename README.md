```
#!/usr/bin/env python3
"""
install.py - verified installer for the inference-hook-dlp plugin.
Installs only if every file matches the approved manifest.
Exit codes: 0 = ok, 1 = verification failed, 2 = setup error.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

SKIP_DIRS = {".git", "release", "__pycache__", ".pytest_cache", ".venv", "venv"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
PLUGIN_ROOT_VAR = "${CLAUDE_PLUGIN_ROOT}"


# ---- Keep file_hash() and walk_files() identical in make_manifest.py ----
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
# -------------------------------------------------------------------------


def default_dest() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    if base:
        return Path(base) / "inference-hook-dlp" / "plugin"
    return Path.home() / ".local" / "share" / "inference-hook-dlp" / "plugin"


def default_settings() -> Path:
    return Path.home() / ".claude" / "settings.json"


def fail(msg: str, code: int = 1) -> int:
    print(f"BLOCKED: {msg}", file=sys.stderr)
    print("Nothing was installed.", file=sys.stderr)
    return code


def load_manifest(src: str, pinned_sha: str | None) -> dict:
    if src.lower().startswith("https://"):
        with urllib.request.urlopen(src, timeout=30) as r:
            raw = r.read()
    elif src.lower().startswith("http://"):
        raise ValueError("manifest URL must use https")
    else:
        raw = Path(src).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if pinned_sha and actual.lower() != pinned_sha.strip().lower():
        raise ValueError(f"manifest SHA-256 mismatch (expected {pinned_sha}, got {actual})")
    manifest = json.loads(raw.decode("utf-8"))
    if manifest.get("schema") != 1 or not isinstance(manifest.get("files"), dict) or not manifest["files"]:
        raise ValueError("manifest is not a valid approved-hashes file")
    return manifest


def verify(root: Path, manifest: dict) -> list[str]:
    expected = manifest["files"]
    actual = set(walk_files(root))
    problems = []
    for rel in sorted(set(expected) - actual):
        problems.append(f"missing: {rel}")
    for rel in sorted(actual - set(expected)):
        problems.append(f"not in approved release: {rel}")
    for rel in sorted(actual & set(expected)):
        if file_hash(root / rel) != expected[rel]:
            problems.append(f"modified: {rel}")
    return problems


def copy_verified(source: Path, dest: Path, manifest: dict) -> None:
    staging = dest.with_name(dest.name + ".new")
    if staging.exists():
        shutil.rmtree(staging)
    for rel in manifest["files"]:
        target = staging / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / rel, target)
    problems = verify(staging, manifest)
    if problems:
        shutil.rmtree(staging, ignore_errors=True)
        raise RuntimeError("copied files failed re-verification: " + "; ".join(problems[:5]))
    if dest.exists():
        shutil.rmtree(dest)
    staging.rename(dest)


def read_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    return json.loads(text) if text else {}


def backup_settings(path: Path) -> Path | None:
    if not path.exists():
        return None
    bak = path.with_name(f"{path.name}.bak-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(path, bak)
    return bak


def strip_our_hooks(settings: dict, marker: str) -> int:
    removed = 0
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return 0
    for event in list(hooks):
        groups = hooks[event] if isinstance(hooks[event], list) else []
        kept = []
        for g in groups:
            cmds = [h.get("command", "") for h in g.get("hooks", []) if isinstance(h, dict)]
            if any(marker in c for c in cmds):
                removed += 1
            else:
                kept.append(g)
        if kept:
            hooks[event] = kept
        else:
            del hooks[event]
    if not hooks:
        settings.pop("hooks", None)
    return removed


def register_hooks(settings_path: Path, dest: Path, hooks_file: str) -> None:
    plugin_hooks_path = dest / hooks_file
    if not plugin_hooks_path.exists():
        raise FileNotFoundError(f"hooks file not found in release: {hooks_file}")
    marker = dest.as_posix()
    text = plugin_hooks_path.read_text(encoding="utf-8").replace(PLUGIN_ROOT_VAR, marker)
    plugin_hooks = json.loads(text).get("hooks", {})
    if not plugin_hooks:
        raise ValueError(f"{hooks_file} has no 'hooks' entries")
    settings = read_settings(settings_path)
    strip_our_hooks(settings, marker)
    target = settings.setdefault("hooks", {})
    for event, groups in plugin_hooks.items():
        target.setdefault(event, []).extend(groups)
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")


def uninstall(dest: Path, settings_path: Path) -> int:
    bak = backup_settings(settings_path)
    settings = read_settings(settings_path)
    removed = strip_our_hooks(settings, dest.as_posix())
    if settings_path.exists():
        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    if dest.exists():
        shutil.rmtree(dest)
    print(f"Removed {removed} hook group(s) from {settings_path}")
    if bak:
        print(f"Settings backup: {bak}")
    print("Restart Claude for the change to take effect.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Verified installer for inference-hook-dlp.")
    ap.add_argument("--manifest")
    ap.add_argument("--manifest-sha256")
    ap.add_argument("--source", default=None)
    ap.add_argument("--dest", default=None)
    ap.add_argument("--settings", default=None)
    ap.add_argument("--hooks-file", default="hooks/hooks.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--uninstall", action="store_true")
    args = ap.parse_args()

    dest = Path(args.dest).resolve() if args.dest else default_dest()
    settings_path = Path(args.settings).resolve() if args.settings else default_settings()

    if args.uninstall:
        return uninstall(dest, settings_path)
    if not args.manifest:
        print("ERROR: --manifest is required", file=sys.stderr)
        return 2
    if not args.manifest_sha256:
        print("WARNING: no --manifest-sha256 given; the manifest itself is not pinned.", file=sys.stderr)

    source = Path(args.source).resolve() if args.source else Path(__file__).resolve().parent.parent
    if not source.is_dir():
        return fail(f"source folder not found: {source}", 2)
    try:
        manifest = load_manifest(args.manifest, args.manifest_sha256)
    except Exception as e:
        return fail(f"could not load approved manifest: {e}", 2)

    print(f"Checking {len(manifest['files'])} files against approved release "
          f"{manifest.get('version')} ({manifest.get('tag')})...")
    problems = verify(source, manifest)
    if problems:
        for p in problems[:20]:
            print(f"  - {p}", file=sys.stderr)
        if len(problems) > 20:
            print(f"  ... and {len(problems) - 20} more", file=sys.stderr)
        return fail(f"{len(problems)} file(s) do not match the approved release")
    print("  All files match.")
    if args.dry_run:
        print("Dry run: verification passed, nothing installed.")
        return 0
    try:
        copy_verified(source, dest, manifest)
        bak = backup_settings(settings_path)
        register_hooks(settings_path, dest, args.hooks_file)
    except Exception as e:
        return fail(str(e))
    print(f"Installed to {dest}")
    print(f"Hooks registered in {settings_path}")
    if bak:
        print(f"Settings backup: {bak}")
    print("Restart Claude, then test with a fake SSN.")
    return 0
```


if __name__ == "__main__":
    sys.exit(main())
