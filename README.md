```
Second commit: after a file-name block, Claude's own reply named the label and Zscaler 403'd the next request. SessionStart now tells Claude not to repeat classification names. Verified: blocked (dlp_8954d714d0ed), Claude's reply didn't name the label, "hello" in the same session got a normal answer.

Note: this is an instruction to Claude, not a hard guarantee. Worth discussing with the Zscaler team whether label names in conversation text (not file content) should be blocked.
```
