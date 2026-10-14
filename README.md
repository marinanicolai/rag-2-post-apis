```
Thanks. Don't apply anything yet. Before choosing Fix A or B I'll run the diagnostics on prod.

Give me, ready to paste into psql (read-only, SELECT only):
1. Query 2a for two users: Ben Miller (username [Ben's username]) and Will McClennan (username [Will's username]). Match username case-insensitively, with and without any @realm suffix, and also by email (ILIKE '%miller%' / '%mcclennan%'). Show id, username, email, is_admin/role, created_at.
2. Query 2b: max(id) vs sequence last_value for users, skills, hooks, plugins, plugin_versions, categories, and any other table the Oct 12 sync inserted into.
3. The exact grep command for the prod app log (path on the Salt server) to find the IntegrityError / duplicate key traceback for Ben's requests today, so I can confirm which constraint fails (users_pkey or users_email_key).

I'll send you the output. Then:
- if any sequence is BEHIND, we do Fix A for those tables
- if Ben's or Will's row exists under a different username form, we do Fix B for that row
- if an email collides with a different person's row, you write the exact statement after I decide which row is right
Keep the auth.py hardening (case/realm-insensitive lookup, catch IntegrityError) for a separate MR after prod is fixed.
```
