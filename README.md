```
Go. Decisions:

Use the description column; leave how_to_use out of the file. Record in PROGRESS.md: Q4 closed, how_to_use is shown on the page, never written into SKILL.md.
Submitter edit view: out of scope. Note it under Phase 2: “the edit view must show body-only content, never the generated header, or saving would store a second block.”
Unparseable YAML: return unchanged and log a warning, as you said. Also make the admin preview show a visible “frontmatter could not be parsed” warning, so an admin doesn’t approve a broken file.
Q1/Q3: approval rules were deployed to dev and prod on Oct 20 from main pipeline 
#235708 (122b599). Step 2 = Done.

Create fix/skill-download-frontmatter from main, write the tests first, then the code. Run what you can, show me the diff, and commit. I’ll push.
```
