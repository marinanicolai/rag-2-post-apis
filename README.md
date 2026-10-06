```

Hi, I ran this by the team first, and they agreed with the approach.

For the Skillhub script-support work, I'd like to set up the skillhub-approved-plugins repo. Could you give me Maintainer access to it (or permission to create it, if it doesn't exist yet)?

I need it to:
- Protect main and version tags so only the Skillhub service account can push, with force push off
- Create a project access token for that service account, limited to pushing to this repo
- Register a dedicated runner for scanning
- Add the CI config for scheduled re-scans of approved plugins, before main is locked

Once setup is done, I'd suggest keeping the Maintainer list to the service account plus one or two admins, since this repo becomes the record of approved code.

Thanks!

```
