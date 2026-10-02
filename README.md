```
Show me exactly how the in-app notification system works and where the email extension point is designed. Specifically:
1. Where notifications are created, and which notification types exist. Is there one for "submission waiting for admin review"?
2. The email extension point: what interface or hook is defined, and what an email implementation would need to provide.
3. How the app reads configuration (env vars, settings files), so new SMTP settings follow the same pattern.
4. Whether any background job mechanism exists (Redis queue, RQ, Celery, scheduled tasks) that email sending could use.
Cite file paths. Don't include hostnames or secrets.
```
