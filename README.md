```
In tmp/sync_precheck.sql, in the authors section, show for each author used by the rows to be copied (skills, hooks, plugin): dev user id, dev username, dev display/full name, dev email, matched prod user id, prod display/full name, and a column name_differs = true when the display names don't match. Also list which author-related columns exist on skills, hooks, plugins and plugin_versions (FK and free-text, e.g. author_id, submitted_by, author_name), and confirm whether author_name will be copied verbatim.
```
