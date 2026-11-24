```
Answers:

The diff: it's the core of this page, so a cycle 1 without it isn't worth shipping.
First check: can we compute the diff client-side from existing endpoints (e.g. fetch file
contents for the submitted version and the last approved version, then diff in the
browser)? If yes, do that and cycle 1 stays UI-only.
If not, the read-only diff endpoint is the one allowed backend exception, under these
conditions: GET only, no schema/migration changes, purely additive, with its own focused
tests that don't depend on the client_with_db fixtures I'm still fixing. It can be built
in the worktree now but won't merge until the API suite is green.

In cycle 1:
- "Next in queue →": yes, derive it from the list.
- Lead kind chips: yes, using the existing lead / mismatch / gap kinds. These are categories,
  not severity, so style them neutrally (no red/amber).
- "Jump to line" and "Next file with a lead": yes.
- Footer "Not read by model … check it yourself": yes, but only when coverage data
  exists. Otherwise show the "coverage unknown" state.
- Decision bar "Model notes were opened: recorded with your decision": yes, it uses the
  existing ai_panel_opened record.
- "Claimed by you" and "Approve (1 of 2)": show them only when the queue item has the data.
  Hide them otherwise, don't fake them.

Out of scope:
- "Model review (new)" side-nav item. That's a separate page. Leave it for later and note it
  in the plan.

Update the plan with these answers and send it back for approval. Don't build yet.
```
