```
Hi all, quick update on packaging the DLP hooks.

As Andrew suggested, I built the checker first, and it works in the Claude desktop app with no .exe.

How it works
1. A checklist is made from the approved release (inference-hook-dlp--v0.2.1). It records a fingerprint (SHA-256) for each of the 159 files.
2. A small Python installer compares every file to that checklist. If all files match, it installs the plugin and turns on the hooks. If any file is changed, missing or extra, it stops and installs nothing.
3. It runs as python.exe, so AppLocker allows it, and claude.exe never copies the rule files, so the Zscaler rule isn't triggered.

Tested today on my Fed laptop
- Approved files: all 159 matched and the install passed.
- Tamper test: after a one-line change to one file, the install was blocked and nothing was installed.
- Desktop app, Code tab: an SSN prompt was blocked by the installed hook (reference dlp_84ee51a92a28). Each check took about 34 ms.

Next step: the review before each release
Andrew, next is the MartinAI review step you mentioned. Do you want MartinAI to review each new release before the checklist is made, and is there a MartinAI/Bedrock setup I should use for it?

Two decisions for the team
- Who gives the final approval after the MartinAI review? InfoSec, or someone on our team?
- Where should the checklist and installer live so testers can't edit them? I'd suggest a protected repo.

Happy to demo it.
```
