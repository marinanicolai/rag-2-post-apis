```
Hi A

I wanted to flag a Zscaler block I'm hitting with the Cowork version of our DLP plugin, and ask for your help.

Background: on 10/26 I uploaded the plugin (inference-hook-dlp.zip) to the Claude desktop app for Cowork, and it worked. I tested it there successfully. Yesterday I removed it to demonstrate a fresh install to a teammate, and I haven't been able to upload it again since.

The block: when I try to upload the zip, Windows shows "You don't have permission to open this file. Contact the file owner or an administrator." The Zscaler app's Data Protection log shows the matching entries: "An application opened one or more files that contain potentially sensitive data. This activity was blocked by your organization," with File Name: inference-hook-dlp.zip and Destination: Claude.exe. The first block was 10/28 at 13:48. Both screenshots attached.

What I think changed: on 10/26 I was on Claude Desktop 3.1623.4. The app has since updated to 4.29.0, and every upload on the new version is blocked.

Could you check whether the endpoint DLP policy, or any exception for Claude.exe, is tied to the app version, hash or signature, so that 4.29.0 isn't covered? If not, could I get a temporary exception for my machine, or for this zip's hash, to finish internal testing? The zip contains only plugin code, rule definitions and synthetic test data, no real data. Hash: [paste SHA-256]

The attempts in the log are from my troubleshooting. I'll hold off on further uploads until I hear from you. Happy to jump on a quick call.

Thanks,
Marina
```
