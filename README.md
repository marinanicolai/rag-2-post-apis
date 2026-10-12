That settles it: **the function is the bug.** The real enum (`libs/db/skillhub_db/models/submission.py`) has no gate 2 states. A submission goes `SUBMITTED` → automated validation → `ADMIN_REVIEW` → admin decision, and `GateResult` is marked deprecated. So `review_submission` rejects every real submission, whatever the decision.

Before you call it "admin review is broken on main," run one more check:

```powershell
git grep -n "review_submission(" -- "*.py"
```

- **If an admin route calls it**, the bug is live for approve, reject, and changes-requested, and this MR fixes something real and serious. Say that in the MR title.
- **If only tests call it**, admins decide through some other function and this one is dead code. In that case, check which function the admin UI actually hits for changes-requested and make sure your resubmit test exercises that one.

The fix itself, in `apps\api\skillhub\services\submissions.py` around line 577:

```python
from skillhub_db.models.submission import SubmissionStatus  # if not already imported

reviewable_states = {SubmissionStatus.ADMIN_REVIEW.value}
```

Using the enum means a future rename breaks at import time instead of silently. While you're in the test file, add `approved` and `rejected` cases from `ADMIN_REVIEW`, so the MR proves the whole decision path works. Then rerun:

```powershell
cd apps\api
.\.venv\Scripts\python.exe -m pytest tests\services\test_resubmit_changes_requested.py -q -p no:cacheprovider
```

Separately, `docs/handoff/section-1-data-models.md` still lists `GATE3_CHANGES_REQUESTED`. Leave it for a follow-up so this MR stays focused, or fix it here if it's a one-line change.
