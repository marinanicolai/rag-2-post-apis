```
Before committing, close the three open items:

Wrap AdminQueueView.installedPreview.test.tsx in a QueryClientProvider (match how other AdminQueueView tests do it).
author_id: confirmed in prod. GET /api/v1/admin/queue returns author_id on each item (e.g. “4382f30d-…” for Hameed). Make sure the QueueItem TypeScript type includes it, and that the approval UI uses it to hide or disable Approve for the author.
Content hash: trace every place compute_bundle_hash / content_hash is computed (submit, approve, the approval-count check, publish, download). Confirm they all hash the same input. My expectation: hash the stored content (body-only), never the output of with_name_description_fallback. If any path hashes the fallback output, change it to the stored content and add a test showing an approval recorded at submit time still counts at approve time for a skill without frontmatter.
Show me the diffs. Then commit the merge with message “Merge main into feature/approval-rules” and tell me. I’ll push.
```
