```
lOn a new feature branch, fix duplicate submissions in Skillhub.

Root cause (confirmed from dev DB): when a skill or hook is submitted with a title/slug that already exists, the app appends a random suffix (e.g. "-19a43813") and creates a NEW row instead of rejecting it or versioning it. This produced many duplicates.

Change the skill and hook submission flow (API + admin review) so that:
- An exact slug/title match (case- and whitespace-insensitive) against a non-removed item is rejected with a clear message, or updates the existing item as a new version if that's how versioning works here. Explain which fits our model before implementing.
- Near-duplicates (same content/config) are flagged to the admin reviewer.
- Rows with status 'removed' don't block a new submission with the same name.
Add tests. Don't touch any database directly. Summarize the change for the MR.
```
