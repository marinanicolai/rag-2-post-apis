```
UI fix for the docs site (apps/docs). Work on a new branch fix/docs-outline-aside from origin/main.

Problem: on our docs (e.g. /docs/api/plugins.html) the "On this page" outline shows as a collapsed dropdown at the top-left of the content, even on a wide desktop window. FedQuery's docs (same VitePress default-theme style) show it as a sticky right-hand column at the top right of the page ("On this page" with the heading list), at the same window size. I want ours to match FedQuery.

Step 1 (read-only, report first):
1. Find why our aside/outline column is hidden or collapsed. Check:
   - custom theme CSS from the restyle (overrides on .VPDoc .aside, .aside-container, .content-container max-width, --vp-layout-max-width, media queries, display:none)
   - frontmatter in pages (aside: false, outline: false, layout settings)
   - themeConfig.outline / aside settings in config.ts
   - any custom Layout component or slot overrides
2. If the FedQuery repo is available locally (C:\Users\M3MXN08\repo\) or via a read-only shallow clone, compare its themeConfig.outline, aside settings and theme CSS with ours.

Step 2 (after I approve):
- Make the outline render as the right-hand column on desktop widths (VitePress default: at 1280px+), with the dropdown kept only for narrow screens.
- Set themeConfig.outline to { level: [2, 3], label: 'On this page' } so the API pages list their sections, not just one heading.
- Keep the restyled look (colors, fonts, the left sidebar title "SkillHub Docs"), the base-path logic, ignoreDeadLinks, Mermaid and favicon unchanged.
- Check keyboard focus and contrast on the outline links (WCAG 2.1 AA).
- Commit locally, don't push. Give me git diff --stat and which file caused the issue.
```
