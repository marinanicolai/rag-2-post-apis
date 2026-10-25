```
git add client/hook.py
git status
git commit -m "Tell Claude not to repeat classification names after a block" -m "After a block, Claude's reply could name the label (inferred from the file name), and that reply is sent with the next request, so Zscaler blocked it (403). The SessionStart context now asks Claude to say 'above the approved level' instead. Verified in Claude: block, then 'hello' in the same session gets a normal answer."
git push
```
