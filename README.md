```
You're working in the ai-marketplace repo (the Skillhub website). A user reported a bug and I want you to find the root cause and fix it. Don't guess and patch symptoms.

## Reported issue
User (Andrew Tellez): "I saved a draft skill, and when I try to open it the page sits on 'Loading skill data...'"
- Steps: create a skill, save it as a draft, then open it from wherever drafts are listed. The page never leaves the loading state.
- Expected: the draft opens in view/edit mode, or shows a clear error if it can't load.
- Also verify: Feedback tab → choose "Bug Report" from the dropdown → write a description → Submit. Confirm the submission is saved and shows up under the "Bug Reports" filter. Users are being sent there to report problems, so it has to work.

## How to work
1. **Use the skills.** Load `writing-plans` before you change anything, `test-driven-development` for the fix, and `requesting-code-review` at the end.
2. **Investigate first and edit nothing yet.** Trace the full path for opening a draft skill:
   - the route/page that renders "Loading skill data..." and the condition that clears it
   - the fetch/query it calls (API route, params, auth, status filter)
   - the backend handler and DB query. Check whether it filters on status = published/approved and so returns 404/null for drafts.
   - the error handling. Does a failed or empty response leave `loading` stuck at true forever?
   Do the same trace for the Feedback submit path (form → API → storage → list/filter).
3. **Write down 2–4 candidate root causes**, each with the file:line evidence for it. Likely suspects: a status filter that excludes drafts, an owner/permission check, an ID or slug mismatch between where drafts are saved and where the page reads them, a missing catch/finally that would reset the loading state, a draft record missing a field the page needs (e.g. null metadata crashing the render).
4. **Run `council`** on those hypotheses and your proposed fix. Have it weigh in on root-cause certainty, the side effects of exposing drafts (only the owner and admins should see their drafts, and drafts must never appear in public Discover/Skills), and UX for the loading, empty and error states.
5. **Reproduce before fixing.** Write a failing test (or a scripted repro) for the draft-loading case. Add one for feedback submission too if it's broken.
6. **Fix the root cause**, then fix the stuck-loading pattern itself. Any failed or empty fetch has to end in a visible error state with a way back, never an endless spinner. Keep error messages accessible: announce them with `role="alert"`/aria-live and keep focus handling sane (Section 508).
7. **Verify.** Run the test suite, lint and typecheck. Confirm by hand that:
   - an owner can open their own draft
   - another non-admin user cannot open someone else's draft and gets a proper message, not a spinner
   - an admin can open it
   - published skills still load
   - feedback bug reports submit and appear under the Bug Reports filter

## Constraints
- Don't change the admin review/approval workflow or submission statuses.
- No schema migrations unless they're truly required. If one is, stop and explain why first.
- Keep the diff small and focused. Note any unrelated problems you see; don't fix them.

## Deliverable
Make a short report covering:
- the root cause, with file:line
- what you changed and why
- the tests you added
- the council's main concerns and how you handled them
- anything still open
Then give me a ready-to-paste MR description for GitLab.
```
