# dlp-pack-workflow

A Claude Code plugin for maintaining the DLP restriction pack in
data-loss-protection-toolkit. It packages what we learned changing rules
there: one skill for the workflow, and one hook that keeps secrets and bulk
changes out of commits.

## What's inside

```
dlp-pack-workflow/
├── .claude-plugin/plugin.json
├── skills/dlp-rule-change/
│   ├── SKILL.md                  the change loop and working rules
│   └── references/
│       ├── change-map.md         every place a rule's behavior is written down
│       └── gotchas.md            detector, Windows and debugging lessons
├── hooks/
│   ├── hooks.json                PreToolUse on Bash, only for git add / git commit
│   └── guard_git.py              the guard (Python, standard library only)
└── tests/test_guard_git.py       pytest suite
```

**Skill `dlp-rule-change`** walks Claude through a rule change: edit the rule,
validate the pack, sort test failures into behavior tests, risk register and
Zscaler spec, fix each group, regenerate the generated docs, and commit named
files. It loads only when a rule change or those test failures come up.

**Git guard hook** runs only for `git add` and `git commit` (through the hook
`if` field, so no other Bash command pays for it). It blocks with an
explanation:

- `git add -A`, `--all`, `.`, `*`, `-u`
- `git commit -a` / `-am` / `--all`
- staging or committing `hash.salt`, `.env` files, `*.salt`, `*.pem`,
  `*.key`, `id_rsa*`, `*.pfx` (`.env.example` is allowed)

If the guard itself errors it allows the command and prints a warning. It
backs up a habit; it is not a security control.

## Try it

```
python -m pip install pytest
python -m pytest tests -q
claude --plugin-dir ./dlp-pack-workflow
```

In that session, ask Claude to run `git add -A`: the hook should block it and
explain why.

The hook calls `python`. On a Mac where only `python3` exists, change the
command in `hooks/hooks.json`.
