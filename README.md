```
Confirmed in prod (read-only): skill_versions.content for grill-me (version id bdacce1a-…) starts with its own single frontmatter (name: grill-me, description: …). So the first block in the download and Full Skill view (name: Grill Me plus tags, category, how_to_use, short_desc, declared_divisions, division_justification) is generated at display/download time, not stored. Code fix only, no data change.
Read-only first: find the function(s) that build that header (probably the download endpoint and the Full Skill view; check whether it’s with_name_description_fallback or an older exporter). Show me file and line. Then propose the fix:

If content already has frontmatter, don’t add a second block. Only fill in a missing name/description.
When a header is generated, write only spec fields: name (the kebab-case slug, e.g. grill-me, never the display name “Grill Me”) and description. Never internal fields (short_desc, how_to_use, declared_divisions, division_justification, tags, category).
One shared function for download, the Full Skill view, the admin “As installed” preview and the publisher.
Tests: grill-me’s shape (existing frontmatter gives one block, unchanged), Hameed’s shape (no frontmatter gives one generated block), and a display name with spaces gives the slug.
Put this on its own branch fix/skill-download-frontmatter from main (stash or commit the PROGRESS update on feature/publisher-core first). Record it in PROGRESS.md as a Step 3 blocker. Show me the plan before coding.
```
