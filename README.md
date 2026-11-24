```
My answers:

1. Yes, drop model severity and the lead-count badge. The repo rule already forbids both, and
   since the model reads the submission, a submitter can push a "low" rating. To show which
   files have leads, use a neutral marker (e.g. a small dot with the screen-reader label
   "has leads"), with no number.

2. No red/amber on the banner either. Use a neutral icon and strong text for "Not fully
   scanned" and name the unread files. Color can't be the only signal anyway, for 508.

3. Cycle 1 is UI-only on existing endpoints. The API test suite is still being fixed, so I
   don't want backend changes mixed in yet. If a field the design needs (like per-file read
   coverage) isn't available, show an honest "coverage unknown" state instead of faking or
   guessing it. List the small additive fields as cycle 2, to do once tests are green.

Fold these into the decisions section of the plan file, and note where the plan now differs
from the Figma (severity chips, lead-count badge, banner color) so I can update the design.
Then send me the updated plan. Don't start building until I approve.
```
