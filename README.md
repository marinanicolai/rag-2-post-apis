```
On branch feature/approval-rules. Self-review is now blocked (approve, reject, request changes). Submitters need a way to take back their own submission. Add a "withdraw" action for hooks, plugin versions and skill submissions:
1. Service layer: withdraw(subject, actor_id). Allowed only when actor_id is the submitter/author AND the item is pending review (or changes_requested). It moves the item back to draft (so it can be edited or deleted with the existing draft flow). If an item type has no draft state, set it to removed instead. Anything else (not the submitter, already published, rejected) → PermissionError/ValueError mapped to 403/400 like the existing endpoints.
2. Record a review_events row with action 'withdraw' (add WITHDRAW to the ReviewAction constants; the column is a plain string, so no migration — confirm there's no CHECK constraint that would reject it).
3. Endpoints: POST .../withdraw next to the existing approve/reject routes for each type, requiring login (not admin).
4. UI (apps/web): show a "Withdraw" button to the submitter on their own pending items (admin queue and their own submissions page), with a confirm dialog; show the API's detail message on errors.
5. Tests (mock-based, like test_approval_rules.py): submitter can withdraw pending; non-submitter can't; can't withdraw published; review event written.
Edit files only; don't run Python/npm, don't commit. List files changed and manual test steps.
```

