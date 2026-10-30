```
**Cowork – DLP plugin status (10/30):** Worked before 10/27 on Claude Desktop 3.1623 — hook behaved same as Claude Code. Removed 10/28 for a demo; could not re-import (Zscaler blocks the desktop app from opening the zip — rule `FRB-C4G-Endpoint-Application-File-Access`, triggered by marking words in the rule files). Jitesh added a temporary fix (`obfuscate_build.py`) obscuring above-ceiling labels, which lets the zip import. Import now works, but hook enforcement in Cowork is still not working (under investigation — likely the obfuscated labels need restoring after extraction before the hook loads).

If you need it even tighter for one cell:

**Cowork:** Worked pre-10/27 (Claude 3.1623), hook matched Claude Code behavior. Removed for demo; re-import blocked by Zscaler (marking words in rule files). Temp fix (obfuscate above-ceiling labels) lets the zip import, but hook enforcement not yet working — under investigation.
```
