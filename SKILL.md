---
name: dlp-rule-change
description: Step-by-step workflow for adding, enabling, re-scoping or changing the action of a rule in the DLP restriction pack (the restrictions/ folder of data-loss-protection-toolkit), and for fixing the test failures that follow. Use this skill whenever the user edits a restriction rule, changes a detector, moves a rule between deny and allow_log, adds a rule file, or sees failures in validate_pack.py, test_risk_register.py or test_zscaler_spec.py after a pack change, even if they only say "change the rule" or "fix these tests".
---

# Changing a rule in the DLP restriction pack

A rule's behavior is written down in several places besides the rule file.
Changing only the rule makes the pack behave correctly while the corpus,
samples, tests, risk register and Zscaler spec still describe the old
behavior. The work is to update each of those on purpose, in order, and to
regenerate generated files rather than edit them.

Read `references/change-map.md` for the full list of places and what each
one encodes, and `references/gotchas.md` before touching detectors.

## Working rules

- One step at a time: edit, save, run the checks, then move on.
- Paste changes rather than retyping them; most bugs in this repo's history
  were typos in hand-edited lines (a misplaced parenthesis, a misspelled rule
  id). After each edit, confirm the file on disk with `Select-String`.
- Commit with named files only (`git add <file>`), never `git add -A`,
  `git add .` or `git commit -a`. The repo root holds secrets and local notes
  that must never be committed; the plugin's git guard hook enforces this.
- Never hand-edit generated files: `docs/RISK_REGISTER.*`,
  `docs/evidence/risk-evidence.json`, `docs/ZSCALER_RULE_SPEC.*`.
- Don't write classification marking names into files you create or edit;
  refer to levels by their position in the `PACK.md` ladder instead. The
  ceiling rule blocks files that spell them out.

## The loop

1. **Edit the rule** in `restrictions/<rule-id>.md`: frontmatter (`id`,
   `severity`, `action`, `enabled`, `applies_to`, `detector`) plus the prose
   and the `## Message to user` section. Rewrite any prose that describes the
   old behavior, such as a "known limitations" note the change resolves.
2. **Validate the pack**: `python scripts/validate_pack.py`. It loads the
   pack, lists every rule and runs the corpus in `restrictions/tests.yaml`.
   A failing corpus case that describes the old behavior gets its `expect`
   and `rules` updated; a failing case that describes still-wanted behavior
   means the rule change is wrong.
3. **Run the suite**: `python -m pytest tests -q`. Sort the failures into
   three groups:
   - **Behavior tests** (`test_client_hook.py`, `test_client_proxy.py`, and the
     cases in `scripts/proxy_selftest.py` and `samples/*.json`) that encode
     the old outcome. Update the expectation and rename the test so its name
     states the new behavior. Keep the test; it now proves the change.
   - **Risk register** (`test_risk_register.py`): the rule must be listed in
     some risk's `rules:` in `docs/risks.yaml`, and that risk's evidence
     fixtures must expect the new outcome.
   - **Zscaler spec** (`test_zscaler_spec.py`): the rule needs an entry in the
     mapping dict in `scripts/zscaler_spec.py`, and hard-coded assertions
     about which rules log or deny may need updating.
   Before editing a test, ask: does this failure show the rule is wrong, or
   the test is out of date? A failure where an unrelated file is caught
   (for example a CSV caught by an Office-only rule) is a bug, not a stale
   test.
4. **Regenerate**, each command on its own line:
   `python scripts/zscaler_spec.py`, then `python scripts/risk_register.py`
   (no `--probe`; that one uses the network).
5. **Run the suite again** until it's green, then check
   `git status --short`, add the changed files by name, and commit.

## Finishing

Summarize for the user: which rule changed and how, which tests were
updated (and why each was stale rather than a real regression), what was
regenerated, and anything left for the policy owner to decide.
