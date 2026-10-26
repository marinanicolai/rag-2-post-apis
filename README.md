```
               if tool == "mcp__workspace__bash":
                   refs = _vm_shell_refs(cmd, cwd, pack.settings.bash_max_files)
               else:
                   refs = _bash_file_refs(cmd, cwd, pack.settings.bash_max_files)
               for i, p in enumerate(refs, start=1):
```
