```
Goal: redesign how review/scan results appear in SkillHub's admin UI, modeled on Claude's org admin "Plugins & skills" inventory (screenshot description below). Work in this worktree on a new branch feat/admin-scan-inventory from origin/main. Commit locally, don't push.

Inspiration (Claude admin → Plugins & skills → Inventory):
- Tabs: Inventory, Marketplaces, Requests, Policy
- Search box, filter chips (Source, Audience, "+ Add filter"), sort dropdown (Newest)
- Table columns: Name (with one-line description under it), Source, Security scan (a status pill such as "Passed" plus version "v1"), Capabilities (small icons), Audience ("Everyone · can install"), Users (30d), row "⋮" menu
- Clean, compact, scannable. The status is visible in the list without opening the item.

Current state: the submission review page shows Approve / Reject / Request Changes / Withdraw, a text-match note ("These are text matches only. Absence of a fact does not mean absence of risk."), and a "Model notes" panel (Hide model notes, Refresh, "Leads for a human reviewer to check. The model does not approve, reject or rate anything.", "Off for this division").

Hard constraint (from the LLM review design, don't break it): the model never approves, rejects, scores or rates. No model-driven pass/fail, severity, confidence or "safe" state anywhere. The isolation tests must still pass.

Step 1 (read-only, then stop and report):
1. Find the admin pages that list skills, hooks, plugins and submissions (the review queue and inventory), and the submission detail page.
2. Find what deterministic scan data exists (Gate 2 / scan_results, rule matches, versions) and what statuses it really has. Note the known bug where run_gate2_scan() sets a status that isn't in the enum.
3. Propose:
   a. A "Scan" column for the list/queue tables, driven ONLY by deterministic scan results, with honest labels (e.g. "No matches", "Matches found (3)", "Not scanned", "Scan error") plus the version, styled as status pills like the inspiration. Explain the label choice.
   b. Which other inspiration columns fit our data (Source, Capabilities icons for hooks/scripts/MCP, Audience/division, usage), and which don't exist in our data (don't invent them).
   c. Search, filter chips and sort for the queue.
   d. On the detail page: a scan summary card (status pill, version, rule matches list) above the actions, and the Model notes panel kept separate below it, clearly labeled as leads, never a status.
4. Show a text mockup or ASCII sketch of the new list and detail layout.
5. List the files you'd change and the tests you'd add.

Step 2 (after I approve):
- Implement with our existing components and theme. Accessible (WCAG 2.1 AA): status pills need text, not color alone, sufficient contrast, keyboard-usable filters, proper table semantics.
- Fix the run_gate2_scan() status enum bug if the new column depends on it, with a failing test first.
- Add or adjust tests: column rendering per status, filters, and an isolation test proving no model output feeds the Scan column.
- Commit locally, don't push. Give me git diff --stat and screenshots-in-words of each state.
```
