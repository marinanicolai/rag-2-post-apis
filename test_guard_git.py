"""Tests for the git guard hook. Run from the plugin root: python -m pytest tests -q"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "hooks" / "guard_git.py"


def run(command: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": command}, "cwd": str(cwd) if cwd else None}
    return subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=30)


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "rule.md").write_text("x")
    (tmp_path / "hash.salt").write_text("secret")
    return tmp_path


@pytest.mark.parametrize("command", [
    "git add -A", "git add --all", "git add .", "git add -u",
    "git add restrictions/rule.md hash.salt", "git add .env", "git add config\\local.env",
    "git commit -am 'wip'", "git commit -a -m wip", "git commit --all -m wip",
    "git status && git add .",
])
def test_blocks(command, tmp_path):
    out = run(command, tmp_path)
    assert out.returncode == 2, command
    assert "git guard" in out.stderr


@pytest.mark.parametrize("command", [
    "git add restrictions/rule.md tests/test_x.py",
    "git add .env.example",
    "git add .gitignore",
    'git commit -m "Add a rule"',
    'git commit -m "-a is mentioned in the message"',
    "git commit -mAdd",
    "git status --short",
    "git push",
])
def test_allows(command, repo):
    out = run(command, repo)
    assert out.returncode == 0, (command, out.stderr)


def test_commit_blocked_when_secret_is_staged(repo):
    subprocess.run(["git", "add", "hash.salt"], cwd=repo, check=True)
    out = run('git commit -m "oops"', repo)
    assert out.returncode == 2
    assert "hash.salt" in out.stderr


def test_commit_allowed_with_named_files_staged(repo):
    subprocess.run(["git", "add", "rule.md"], cwd=repo, check=True)
    assert run('git commit -m "rule"', repo).returncode == 0


def test_bad_input_fails_open():
    out = subprocess.run([sys.executable, str(GUARD)], input="not json", capture_output=True, text=True)
    assert out.returncode == 0
    assert "skipped" in out.stderr


def test_hooks_json_points_at_the_guard():
    cfg = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    handlers = cfg["hooks"]["PreToolUse"][0]["hooks"]
    assert {h["if"] for h in handlers} == {"Bash(git add *)", "Bash(git commit *)"}
    assert all("guard_git.py" in h["command"] for h in handlers)


def test_manifest_and_skill():
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == ROOT.name
    skill = (ROOT / "skills" / "dlp-rule-change" / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\n") and "name: dlp-rule-change" in skill
    for ref in ("change-map.md", "gotchas.md"):
        assert (ROOT / "skills" / "dlp-rule-change" / "references" / ref).is_file()
