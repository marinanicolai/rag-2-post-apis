```
Decisions:

Yes, freeze: versions with a stored content_hash render with render_legacy_skill_md (old bytes, byte-identical to main); draft, pending and new versions use render_installed_skill_md. Golden-byte tests from main for each shape in your table, plus: a frozen version’s hash_tree is unchanged, a new version gets the new renderer, and the revocation check still matches stored hashes.
Yes: pass through spec frontmatter fields from the stored frontmatter: name, description, license, allowed-tools, metadata, compatibility. Never write internal DB fields (short_desc, how_to_use, declared_divisions, division_justification, tags, category, icon, author_name as a top-level key). Restore tests for license: MIT and metadata.author in the download.
Write the read-only comparison script (rebuild each pinned version with both renderers, compare with the stored hash), and put the full SQL query in a file too. Don’t run them against any DB; I’ll run them on salt1 read-only and send you the output.
Record in PROGRESS.md under Decisions: “Approved/hashed versions are rendered with the legacy renderer forever; the new renderer applies to unhashed and new versions only. Spec frontmatter fields pass through; internal fields never do.”
Then commit and tell me. Don’t push yet.
```
