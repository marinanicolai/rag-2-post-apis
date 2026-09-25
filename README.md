# 📦 Supply Chain RAG Explorer (React Frontend)

---
Start
----

#!/usr/bin/env python
"""Claude Code hook entry point for the restriction pack.

Wired by ``hooks/hooks.json`` (plugin) or a settings file (see
``scripts/render_hook_settings.py``). Claude Code runs this once per event with
a JSON payload on stdin. Supported events:

    SessionStart        load the pack; tell Claude the restrictions exist
    UserPromptSubmit    scan the prompt text and any ``@file`` it mentions
    PreToolUse          scan what a tool is about to read or send (Read, Edit,
                        Write, Bash, Grep, Glob, WebFetch, WebSearch, MCP tools)
    PostToolUse         scan what a tool returned (cannot block: flags and logs)

Blocking uses exit code 2 with the user-facing reason on stderr, which is the
one mechanism every Claude Code version honours for prompt and tool events.
Allow is exit 0 with no output. Everything is logged to the local decision
file (see ``client/audit.py``) with redacted samples only.

Behaviour switches (pack manifest, overridable by environment):

    enforcement     enforce | shadow        DLP_ENFORCEMENT
    fail_mode       closed | open           DLP_FAIL_MODE    (hook crash / pack unreadable)
    DLP_RESTRICTIONS_DIR                    where the pack lives
    DLP_AUDIT_LOG                           where decisions are written
"""

from __future__ import annotations

import json
import os
import re
import secrets
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Mapping

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import client  # noqa: E402,F401  (registers detectors)
from app.detectors import RuleConfigError  # noqa: E402
from app.engine import Decision, evaluate  # noqa: E402
from app.payload import Frame, Segment, normalize_text  # noqa: E402
from app.redaction import Redactor  # noqa: E402
from client.audit import Audit, load_salt, resolve_log_path  # noqa: E402
from client.files import FileContent, inspect_file  # noqa: E402
from client.pack import Pack, load_pack  # noqa: E402

SURFACE = "code"
MAX_SCAN_CHARS = 4 * 1024 * 1024
FILE_TOOLS_PATH_KEYS = ("file_path", "notebook_path", "path")
_AT_REF_RE = re.compile(r'(?<![\w./\\])@(?:"([^"]+)"|\'([^\']+)\'|([^\s@"\']+))')
_BASH_TOKEN_RE = re.compile(r'"([^"]+)"|\'([^\']+)\'|(\S+)')
_TRAILING_PUNCT = ",.;:)]}>\"'`"


@dataclass(slots=True)
class Outcome:
    exit_code: int = 0
    stdout: dict[str, Any] | None = None
    stderr: str | None = None
    record: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Inputs:
    segments: list[Segment] = field(default_factory=list)
    files: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


# ------------------------------------------------------------------ segment builders

def _text_segment(kind: str, role: str, text: str, index: int = 0, **kw: Any) -> Segment:
    if len(text) > MAX_SCAN_CHARS:
        text = text[:MAX_SCAN_CHARS]
    return Segment(kind, role, index, normalize_text(text), **kw)


def _json_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    except (TypeError, ValueError):
        return str(value)


def _resolve(path: str, cwd: str | None) -> str:
    path = os.path.expandvars(os.path.expanduser(path.strip()))
    if not os.path.isabs(path) and cwd:
        path = os.path.join(cwd, path)
    return os.path.normpath(path)


def add_file(inputs: Inputs, path: str, pack: Pack, index: int, *, content: bool = True) -> None:
    """Inspect ``path`` and add an attachment segment for it."""
    if not content:
        inputs.segments.append(Segment("attachment", "user", index, "", file_name=path, has_text=True))
        return
    fc: FileContent = inspect_file(path, pack.settings.max_file_bytes)
    if not fc.exists:
        return
    inputs.files.append({
        "path": fc.path, "size": fc.size, "media_type": fc.media_type, "extractor": fc.extractor,
        "has_text": fc.has_text, "truncated": fc.truncated, "labels": fc.labels, "error": fc.error,
    })
    inputs.segments.append(_text_segment(
        "attachment", "user", fc.text, index,
        file_name=fc.path, media_type=fc.media_type, has_text=fc.has_text,
    ))


def _prompt_file_refs(prompt: str, cwd: str | None) -> list[str]:
    out: list[str] = []
    for m in _AT_REF_RE.finditer(prompt):
        raw = next(g for g in m.groups() if g is not None).rstrip(_TRAILING_PUNCT)
        if not raw:
            continue
        p = _resolve(raw, cwd)
        if os.path.isfile(p) and p not in out:
            out.append(p)
    return out


def _bash_file_refs(command: str, cwd: str | None, limit: int) -> list[str]:
    out: list[str] = []
    if limit <= 0:
        return out
    for m in _BASH_TOKEN_RE.finditer(command):
        tok = next(g for g in m.groups() if g is not None).strip().rstrip(_TRAILING_PUNCT)
        if not tok or tok.startswith("-") or len(tok) > 512:
            continue
        if "/" not in tok and "\\" not in tok and "." not in tok:
            continue
        for part in re.split(r"[;|&<>]+", tok):
            part = part.strip()
            if not part:
                continue
            p = _resolve(part, cwd)
            if os.path.isfile(p) and p not in out:
                out.append(p)
                if len(out) >= limit:
                    return out
    return out


def build_inputs(event: str, payload: Mapping[str, Any], pack: Pack) -> Inputs:
    inputs = Inputs()
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None

    if event == "UserPromptSubmit":
        prompt = payload.get("prompt")
        if not isinstance(prompt, str):
            prompt = payload.get("user_input")
        prompt = prompt if isinstance(prompt, str) else ""
        inputs.segments.append(_text_segment("text", "user", prompt))
        if pack.settings.scan_prompt_file_refs:
            for i, p in enumerate(_prompt_file_refs(prompt, cwd), start=1):
                add_file(inputs, p, pack, i)
        return inputs

    tool = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), Mapping) else {}

    if event == "PreToolUse":
        if tool == "Read":
            fp = tool_input.get("file_path")
            if isinstance(fp, str) and fp:
                add_file(inputs, _resolve(fp, cwd), pack, 1)
        elif tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
            fp = next((tool_input.get(k) for k in FILE_TOOLS_PATH_KEYS if isinstance(tool_input.get(k), str)), None)
            if fp:
                add_file(inputs, _resolve(fp, cwd), pack, 1, content=False)
            inputs.segments.append(_text_segment("tool_use", "assistant", _json_text(tool_input), tool_name=tool))
        elif tool == "Bash":
            cmd = tool_input.get("command")
            cmd = cmd if isinstance(cmd, str) else _json_text(tool_input)
            inputs.segments.append(_text_segment("tool_use", "assistant", cmd, tool_name=tool))
            for i, p in enumerate(_bash_file_refs(cmd, cwd, pack.settings.bash_max_files), start=1):
                add_file(inputs, p, pack, i)
        elif tool in ("Grep", "Glob"):
            target = tool_input.get("path")
            if isinstance(target, str) and target:
                add_file(inputs, _resolve(target, cwd), pack, 1, content=False)
            inputs.segments.append(_text_segment("tool_use", "assistant", _json_text(tool_input), tool_name=tool))
        else:
            # WebFetch, WebSearch, MCP tools, anything else: what is sent out.
            inputs.segments.append(_text_segment("tool_use", "assistant", _json_text(tool_input), tool_name=tool))
        return inputs

    if event == "PostToolUse":
        resp = payload.get("tool_response")
        text = resp if isinstance(resp, str) else _json_text(resp)
        inputs.segments.append(_text_segment("tool_result", "user", text, tool_name=tool))
        return inputs

    return inputs


# ------------------------------------------------------------------ decision

def _frame(inputs: Inputs, payload: Mapping[str, Any], reference_id: str) -> Frame:
    frame = Frame("prompt", reference_id, None, "user", None, None, "claude-code",
                  payload.get("session_id") if isinstance(payload.get("session_id"), str) else None, None)
    frame.segments = [s for s in inputs.segments if s.text or s.kind == "attachment"]
    frame.message_count = 1
    frame.scan_bytes = sum(len(s.text) for s in frame.segments)
    frame.blind_attachments = sum(1 for s in frame.segments if s.kind == "attachment" and not s.has_text)
    return frame


class _Safe(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def user_message(decision: Decision, pack: Pack, inputs: Inputs, event: str, tool: str) -> str:
    reason = decision.deny_reason or pack.settings.default_deny_reason
    first_file = inputs.files[0]["path"] if inputs.files else ""
    reason = reason.format_map(_Safe(file=os.path.basename(first_file), path=first_file, tool=tool))
    prefix = ""
    if event == "PreToolUse" and first_file:
        prefix = f"Blocked {tool} of {first_file}: "
    elif event == "PreToolUse":
        prefix = f"Blocked {tool}: "
    elif event == "UserPromptSubmit":
        prefix = "Prompt blocked: "
    msg = prefix + reason
    if pack.settings.contact:
        msg += " " + pack.settings.contact
    return msg


def _load_pack_or_none(errors: list[str]) -> Pack | None:
    try:
        return load_pack()
    except (RuleConfigError, OSError) as exc:
        errors.append(str(exc))
        return None


# Least strict first. An environment value below the pack's own setting is
# ignored: the environment belongs to the person the policy applies to, so
# honouring it would make `DLP_ENFORCEMENT=shadow` a one-line bypass needing
# no privileges. Tightening is still allowed, so an operator can harden a
# machine without republishing the pack.
_STRICTNESS: dict[str, tuple[str, ...]] = {
    "DLP_ENFORCEMENT": ("shadow", "enforce"),
    "DLP_FAIL_MODE": ("open", "closed"),
}


def _env_choice(
    name: str,
    default: str,
    allowed: tuple[str, ...],
    ignored: list[str] | None = None,
) -> str:
    v = os.environ.get(name, "").strip().lower()
    if not v:
        return default
    if v not in allowed:
        if ignored is not None:
            ignored.append(f"{name}={v} (not a valid value)")
        return default
    order = _STRICTNESS.get(name)
    if order and v in order and default in order and order.index(v) < order.index(default):
        if ignored is not None:
            ignored.append(f"{name}={v} (weaker than {default})")
        return default
    return v


def handle(event: str, payload: Mapping[str, Any]) -> Outcome:
    t0 = time.perf_counter()
    reference_id = "dlp_" + secrets.token_hex(6)
    errors: list[str] = []
    env_ignored: list[str] = []
    pack = _load_pack_or_none(errors)

    log_path = resolve_log_path(pack.settings.audit_log if pack else None)
    audit = Audit(log_path)
    redactor = Redactor(load_salt(log_path))
    session_id = payload.get("session_id")
    tool = str(payload.get("tool_name") or "")
    base: dict[str, Any] = {
        "reference_id": reference_id, "hook_event": event, "tool_name": tool or None,
        "session_id": session_id, "cwd": payload.get("cwd"),
    }

    if pack is None:
        fail_mode = _env_choice("DLP_FAIL_MODE", "closed", ("closed", "open"), env_ignored)
        rec = audit.record("pack_error", **base, fail_mode=fail_mode,
                           env_ignored=env_ignored or None, error="; ".join(errors))
        msg = ("Claude usage restrictions could not be loaded, so this action is blocked "
               f"(fail mode closed). Ask an administrator to fix the restriction pack. Reference: {reference_id}. "
               f"Detail: {'; '.join(errors)[:400]}")
        if event == "SessionStart":
            return Outcome(0, {"systemMessage": "inference-hook-dlp: restriction pack failed to load: " + "; ".join(errors)[:500]}, None, rec)
        if event == "PostToolUse":
            return Outcome(0, {"systemMessage": "inference-hook-dlp: restriction pack failed to load; output not checked."}, None, rec)
        if fail_mode == "closed":
            return Outcome(2, None, msg, rec)
        return Outcome(0, None, None, rec)

    enforcement = _env_choice(
        "DLP_ENFORCEMENT", pack.settings.enforcement, ("enforce", "shadow"), env_ignored
    )

    if event == "SessionStart":
        lines = [
            f"Organization usage restrictions are active (inference-hook-dlp pack '{pack.settings.name}' "
            f"v{pack.settings.version}, {len(pack.ruleset.rules)} rules, classification ceiling {pack.settings.ceiling}, "
            f"mode {enforcement}). Hooks check prompts, files you read and data you send. "
            "Do not read files marked above the ceiling, do not paste personal identifiers or credentials, "
            "and if a hook blocks an action tell the user which rule fired instead of working around it.",
            "Rules:",
        ]
        for r in pack.ruleset.rules:
            if r.enabled:
                lines.append(f"- {r.id} ({r.action}, {r.severity}): {r.description or ''}".rstrip(": "))
        rec = audit.record("session_start", **base, pack=pack.summary(),
                           enforcement=enforcement, env_ignored=env_ignored or None)
        return Outcome(0, {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(lines)[:4000]}}, None, rec)

    inputs = build_inputs(event, payload, pack)
    frame = _frame(inputs, payload, reference_id)
    decision = evaluate(frame, pack.ruleset, SURFACE, redactor, reference_id)
    policy_action = decision.action
    would_deny = decision.is_deny
    action = "deny" if (would_deny and enforcement == "enforce" and event != "PostToolUse") else "allow"

    rec = audit.record(
        "verdict", **base,
        action=action, policy_action=policy_action, enforcement=enforcement, would_deny=would_deny,
        env_ignored=env_ignored or None,
        deny_rule_id=decision.deny_rule_id, severity=decision.severity,
        matched_rule_ids=decision.matched_rule_ids, hits=[h.as_dict() for h in decision.hits],
        files=inputs.files, segments_scanned=decision.segments_scanned, scan_bytes=frame.scan_bytes,
        blind_attachments=frame.blind_attachments, rules_evaluated=decision.rules_evaluated,
        pack_hash=pack.hash, pack_name=pack.settings.name,
        latency_ms=round((time.perf_counter() - t0) * 1000, 1),
    )

    if not would_deny:
        return Outcome(0, None, None, rec)

    msg = user_message(decision, pack, inputs, event, tool)
    if event == "PostToolUse":
        # Already executed. Tell Claude not to use it and surface it to the user.
        return Outcome(0, {
            "hookSpecificOutput": {"hookEventName": "PostToolUse", "decision": "block", "reason": msg},
            "systemMessage": f"inference-hook-dlp: {tool} output matched {decision.deny_rule_id} "
                             f"({'flagged, shadow mode' if enforcement != 'enforce' else 'Claude was told not to use it'}). "
                             f"Reference {reference_id}.",
        }, None, rec)
    if action == "deny":
        return Outcome(2, None, msg, rec)
    return Outcome(0, {"systemMessage": f"inference-hook-dlp (shadow): would block {event}"
                                        f"{' ' + tool if tool else ''} under {decision.deny_rule_id}. Reference {reference_id}."}, None, rec)


# ------------------------------------------------------------------ main

def _read_payload() -> dict[str, Any]:
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def main(argv: list[str]) -> int:
    payload = _read_payload()
    event = str(payload.get("hook_event_name") or (argv[1] if len(argv) > 1 else "") or "")
    if not event:
        sys.stderr.write("inference-hook-dlp: no hook event name (pass it as argv[1] or in stdin JSON)\n")
        return 0
    try:
        outcome = handle(event, payload)
    except Exception as exc:  # noqa: BLE001 - the hook must fail deterministically
        fail_mode = _env_choice("DLP_FAIL_MODE", "closed", ("closed", "open"))
        try:
            Audit(resolve_log_path(None)).record("hook_error", hook_event=event, error=f"{type(exc).__name__}: {exc}", fail_mode=fail_mode)
        except Exception:  # noqa: BLE001
            pass
        if fail_mode == "closed" and event in ("UserPromptSubmit", "PreToolUse"):
            sys.stderr.write(f"Claude usage restrictions check failed ({type(exc).__name__}); action blocked (fail mode closed).\n")
            return 2
        return 0
    if outcome.stdout is not None:
        sys.stdout.write(json.dumps(outcome.stdout))
    if outcome.stderr:
        sys.stderr.write(outcome.stderr)
    return outcome.exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
---
End
----

## 🧠 RAG System Architecture

Below is the high-level architecture of the full system (Frontend + Backend + AI Pipeline):

![RAG Architecture](./rag-frontend/src/assets/rag-1.png)

---

## 🧱 Tech Stack

* ⚛️ React 19
* 🟦 TypeScript
* ⚡ Vite
* 🎨 Custom dark/green UI
* 🌐 REST API integration (`upload` + `ask`)
* 🧠 RAG Pipeline (via FastAPI backend)
* 🔍 FAISS Vector Database
* 🤖 Groq LLaMA 3.3

---

## 📂 What This Repo Includes

* Upload UI for documents
* Question input & answer panel
* Status messages & error handling
* API connection layer (`src/api.ts`)
* Ready for deployment on **Vercel**

❗ This repo does **not** include the backend.
You must run the FastAPI RAG backend separately.

---

## 🔑 Environment Setup

Create a `.env` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If using a deployed backend (Railway, etc.):

```env
VITE_API_BASE_URL=https://your-backend-url.up.railway.app
```

---

## ▶️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/your-repo-name.git

# 2. Move into the project
cd your-repo-name

# 3. Install dependencies
npm install

# 4. Start the app
npm run dev
```

Then open:

```
http://localhost:5173
```

Make sure your **FastAPI backend is running at the API URL**.

---

## 🔄 How the RAG Flow Works

1. User uploads a file
2. Frontend sends it to the FastAPI backend
3. Backend:

   * Chunks the file
   * Creates embeddings
   * Stores them in FAISS
4. User asks a question
5. Backend:

   * Finds the most relevant chunks
   * Sends them to Groq LLaMA
6. AI-generated answer is returned to the UI

---

## 🚀 Deployment

This frontend is optimized for:

* ✅ **Vercel**
* ✅ **Netlify**
* ✅ Any static Vite-compatible host

Build command:

```bash
npm run build
```

Output folder:

```bash
dist
```

---

## 🎯 Who This Is For

* Developers learning **RAG architecture**
* Students exploring **LLMs + vector databases**
* Frontend engineers integrating **real AI systems**
* Anyone building **AI-powered document Q&A**

---
