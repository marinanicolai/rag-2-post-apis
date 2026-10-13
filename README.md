```
On branch feature/approval-rules. The backend now refuses self-approval (403 with a "detail" message) and can return awaiting_second_approval, but the admin UI shows nothing when an approve/reject/request-changes call fails. Fix the frontend (apps/web) for the admin approval actions on plugins, hooks and skill submissions:
1. On any non-2xx response, show the API's "detail" message to the admin (use the app's existing toast/notification or inline error pattern; don't add a new library).
2. If the response status is "awaiting_second_approval", show that state clearly (e.g. "Approved by you, waiting for a second admin") instead of treating it as published or doing nothing.
3. Disable the Approve, Reject and Request changes buttons when the current user is the submitter/author, with a tooltip "You can't review your own submission". The backend check stays the real protection; this is only a hint.
Find the existing admin queue/review components and the API client calls they use. Edit files only; don't run npm or Python, don't commit. List the files changed and how to test manually.
```

