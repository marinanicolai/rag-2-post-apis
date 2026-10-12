```
1. Commit the current hash work on this branch first (message: "Use shared full SHA-256 bundle hash for skills and submissions").
2. Fix the GATE3_CHANGES_REQUESTED bug on a separate branch from origin/main named bug/resubmit-changes-requested: the one-line fix plus lines 658 and 899, with a test proving resubmission after "changes requested" works. Commit it there, and show me the test results.
3. Then come back to this branch. Question: why is passing reference_files into compute_bundle_hash deferred until after plugins-spine? Covering reference files is the main goal. If skills on main already have reference_files, pass them now at the call sites in this branch.
4. Run the new tests and the full backend suite on this branch, and show me the results. Note which failures, if any, are caused by the resubmission bug and not by this change.
```
