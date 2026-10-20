```
Agreed, keep the plugin hash as the installed-bytes hash (hash_tree). Add one line to PROGRESS.md Decisions: “Plugin approval hash = installed-bytes hash (hash_tree), same as revocation; editing name/description changes it and resets approvals by design.”
QueueItem: author_id is confirmed. The prod GET /api/v1/admin/queue response includes author_id on every item. Make sure the TypeScript QueueItem type has author_id: string, and that the QueryClientProvider wrapper fix for AdminQueueView.installedPreview.test.tsx is done.
Then commit the merge with “Merge main into feature/approval-rules” and tell me when it’s done. I’ll push.
```
