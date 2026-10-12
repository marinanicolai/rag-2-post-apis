```
# 1. What statuses exist now?
git grep -n -A 25 "class SubmissionStatus"

# 2. Who still uses the old gate2 strings?
git grep -n -i "gate2_passed\|gate2_flagged"

# 3. The commit that removed GATE3_CHANGES_REQUESTED shows the intended new flow
git log -S "GATE3_CHANGES_REQUESTED" --oneline
```
```
  reviewable_states = {SubmissionStatus.ADMIN_REVIEW.value}  # plus any others the new flow allows
```
