```
Bcs an unreviewed file must not be reachable by anything that installs. If it sits on an installable git branch, a user who knows the path can pull it. Keyed by hash, the same content uploaded twice is recognised, and no name collision can slip a different file under a known name. One write door, so one thing to watch. Idk if you need that level of security but that what I would do.
```
```
After approval: GitLab, protected branch, tag. The service account commits the archive onto a branch where nobody else pushes and force push is off. Why: immutability isn't a property of git, it's a property of branch protection. Without it, anyone with rights rewrites history. With it, the repo becomes an append-only ledger. The tag gives each version a readable name. And keep the archive itself with its hash: the day you need to prove "these exact bytes were approved on this date"

```
```
One commit per approval and by the service account. Not the submitter. Why: if the submitter commits, they control the commit content and could push something other than what was reviewed. The service account commits what Skillhub holds in quarantine, so the reviewed bytes. Reviewer's name in the message, so the trail travels with the code. Signed if GitLab has a key for that account, so it's provable.

```
```
Then for the pin : the sha field in marketplace.json. Claude Code accepts a sha on git sources, and when it's there it checks out exactly that commit even if the branch moved. Why it matters: a branch or tag is a pointer that can move, a sha is more like the content.

```
```
But their is one thing I couldn't confirm after going trhough the documentation of LiteLLM. The LiteLLM API shows a version field, no sha on the source object. If LiteLLM doesn't pass the sha through to the marketplace.json it serves, nothing is pinned. So in your spike, after registering, read /claude-code/marketplace.json back and check the sha is there. You should do that because a version marked published without a pin is worse than one not published, because everyone believes it's safe. Again Idk what is the level of security that you want, but I prefer to be safe with my recommendations.

```
```
If it doesn't come through, two fallbacks. Skillhub serves its own marketplace.json, Claude Code takes a direct URL as a source, so you control what's served. Or an archive source with a sha256, where Claude Code refuses the download if the hash doesn't match. That second one is honestly the strongest guarantee of the three. And if you don't like those option you can always ask Claude for other.

```
```
Metadata: three tables and Redis. plugin_versions (or whatever you'd like to call it), one row per immutable thing. Then scan_results separate, because a scan from last year with old rules isn't equivalent to today's and you need to record which version of each tool ran. A third table for review events (Review_event for ex), where you can only add lines and never change or delete them, because an audit trail you can edit isn't an audit trail. And a simple queue for the scans, so an upload doesn't sit waiting for the scanner to finish, and a failed scan can be retried without losing anything.

```
```
Sorry there is a lot here, but I think this is important because this is the foundations of your Company using AI. If it's not good at the beginning it will cause issue later I think


```
```
For all the updates and rollback. Every new upload is a new version with a fresh review because the whole system rests on "what was reviewed is what gets delivered", the upside is that rolling back just means pointing at the previous version again, no need for a second review, and revoking means removing it from the catalog and telling the machines that already have it to drop it.

```
