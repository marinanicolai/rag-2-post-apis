```
Context: Skillhub (ai-marketplace) has a user feedback feature with three types:
feature request, bug report, praise. Right now all submissions are anonymous.
A user asked us to attach the submitter's identity to all of them.

Before changing anything:
1. Find where feedback is defined and handled: the DB model/schema, the API
   route or controller, the frontend form and the admin view.
2. Report what you found and give me a short plan. Wait for my approval before
   you edit any code.

Implementation requirements:
- Get identity from the authenticated session on the server. Never trust a
  name or user ID sent in the request body.
- Schema: add nullable fields such as submitted_by_user_id and
  submitted_by_name (or whatever matches our existing conventions), plus a
  migration. Leave existing records as they are: they stay anonymous and
  are not backfilled.
- Form: add a short notice above the submit button, like "Your name will be
  visible to the Skillhub team with this submission."
- Admin view: show "Submitted by <name>" on each submission, and "Anonymous"
  for older records that have no identity. Filtering by submitter is a
  nice-to-have.

Tests:
- Each type stores the identity from the session.
- A spoofed name or user ID in the request body is ignored.
- Older records with no identity show as "Anonymous" in the admin view.
- Run the existing test suite and lint before you finish.

Keep the change minimal and follow the repo's existing patterns. Summarize
the changed files at the end.
```
