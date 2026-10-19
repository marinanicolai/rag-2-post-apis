```

Go with:

Verify first: download one published skill (one without frontmatter in content) and confirm the installed SKILL.md has name and description frontmatter. Tell me which skill you checked and show the first lines.
Put this on the fix branch: in the admin detail panel, show the SKILL.md as it will be installed (generated frontmatter + content), built with the same function the download/publish path uses, not a copy of its logic, so the preview can’t drift from what gets installed. Label it “As installed”. Add a test with an item shaped like SKL-39MQ14 (no frontmatter; “→”, quotes and backticks in the description) asserting the preview starts with valid frontmatter that round-trips through yaml.safe_load.
how_to_use override: explain in 3–4 lines what it does today and when it overrides content. Don’t change it yet.
No UPDATE to Hameed’s rows. Then commit on top of Phase 1, show me the diff and tell me when it’s ready. I’ll push
```
