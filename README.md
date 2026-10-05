```
Hi , thanks! Updates on your points:

- test_the_checked_in_document_is_current: fixed on marina-dev. Docs regenerated after the ZDP_MAPPING edit, and risks.yaml now points at image_is_blocked.
- Unknown binaries/archives: I'd keep logging them, so please rebase onto mine. One thing to keep: the catch-all allow_log rule. Without it, those files match no rule at all.

I tested the C4G repo end to end on my machine (metadata check, propose/apply auto-labeling, override). Results:

Working:
- Metadata check reads a real Word label (label + GUID) and allows it.
- Unmarked doc is blocked; propose suggests a label and offers the override.
- Apply writes a label Word accepts with no re-prompt; SiteId matches, and a Word save leaves the metadata unchanged.
- Ceiling can't be overridden (never_for works).

Needs fixing before wider testing:
1. Override only covers one hook event. It's used up at UserPromptSubmit, then PreToolUse (Bash) blocks the same file 5 seconds later, so a proceed never works end to end. Suggest keying it on session + file hash + rule until TTL/turn end.
2. Claude over-blocks on its own. It refused files the hook allowed 3 times, including right after auto-labeling (it judged by the missing visible marking and once by the file name). Suggest the hook tells Claude which label it applied, and the policy text says not to re-judge files the hook cleared.
3. default_label (ee3ed885, INTERNAL FR - OFFICIAL USE) is a parent label. Word won't let a user apply it without picking a sublabel (FRSONLY / EXTERNAL / SECURE EXTERNAL). The catalog has no parent marker, so the pack can't catch it, and the propose message names a label users can't pick. Which sublabel to default to is a policy call.
4. Apply mode adds no visible marking. Even with FRSONLY as the default, Word showed the label but never added the header, on open or on save (ContentBits stays 0). The hook would need to write the header itself, or users need to re-apply in Word.

Smaller: ceiling refusal says "no recent block" instead of "can't be overridden", 10-min TTL is tight, PERSONAL-NONWORK name has a mis-encoded dash, and test files named unmarked* bias Claude.

I'll send you the tenant SiteId for labeling.site_id separately. I'd suggest fixing 1 and 2 before packaging for Spencer, since testers will hit both right away. Happy to walk through it.
```
