```
git fetch
git worktree add ..\ai-marketplace-hook-card -b fix/hook-card-match-skill-plugin origin/main
cd ..\ai-marketplace-hook-card
claude
```
```
Task: make the Hook detail page header card match the Skill and Plugin detail cards.
You're in a separate git worktree on branch fix/hook-card-match-skill-plugin (from
origin/main). Another agent is working in the main checkout; don't touch that folder.

What I see on the dev site (ai-marketplace-dev):
- Skill (#/skills/frontend-board-design) and Plugin (#/plugins/onboarding-context-pack)
  share one layout: letter icon; title (+ type badge for plugin); slug subtitle;
  "by" + avatar initials + display name + a line under it (role · division);
  outlined Save and Fork buttons top right; a stats row with dividers (skill: Installs,
  Rating, Forks, Favorites; plugin: Published, Skills, Hooks, References, Forks);
  tabs (Overview, Full Skill, How to Use, Install, Versions, Reviews); and an Overview
  panel with the description and "Authorized division(s)".
- Hook (#/hooks/ponytail-mode) is different: event name (SessionStart) as the subtitle;
  description inside the card; a metadata line "Category · Author: Nicolai, Marina
  (last, first, no avatar) · official · Installs: 0"; tag chips; "Copy to Clipboard" and a
  filled "Install" button; no stats row, no tabs; a long Description section below.
  The top accent bar color also differs.

Do this:
1. Investigate first: find the three detail page components and any shared card or
   header component. Tell me why Hook diverged (separate component, older code,
   different data shape) and list every visual and structural difference.
2. Plan before coding: reuse the shared component Skill and Plugin use (or extract one if
   they duplicate), and map hook fields onto it:
   - subtitle, avatar and author format the same as skill/plugin
   - stats row using only data that really exists for hooks (installs etc.); don't
     invent fields or call APIs that don't exist; list any gaps instead
   - tabs that make sense for hooks (e.g. Overview, Configuration for the hook JSON,
     How to Use, Install); say which tabs you'd drop and why. Hooks have no versions yet.
   - keep hook-specific info visible: the event (SessionStart) as a badge or chip, the
     category, tags, and the Copy to Clipboard / Install actions in the same button
     style as Save/Fork
   - same accent bar color logic as the other types, or explain the rule
3. Accessibility (Section 508 / WCAG 2.1 AA): heading order, tab semantics
   (role=tablist/tab/tabpanel, keyboard arrows), button labels, and color contrast of
   badges and the stats text. Don't make anything worse than the skill/plugin cards.
4. Wait for my OK on the plan. Then implement, keeping the Skill and Plugin pages
   visually unchanged. Add or update component tests if the frontend has them.
5. Tell me exactly how to check it locally or on dev (which pages to open), and include
   before/after notes. Don't commit; I'll review the diff.
Note: a DLP hook may block you from running some binaries. If a command is blocked,
don't work around it; give me the command to run myself.
```
