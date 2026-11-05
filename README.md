```
Treat both confirmed Part 1 findings as must-fix: re-read the full hook row after taking
the lock before comparing, and make "unhashable" its own failing audit verdict, never OK.
Each needs a test (concurrent edit; unhashable content).
For the rest of the list: fix every should-fix that touches integrity, security or
the audit. List the cosmetic or style items separately; I'll decide those. For the items
that need a design decision from me, give each as a short question with your
recommendation.
```
