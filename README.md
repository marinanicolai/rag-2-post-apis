You're back on the approved release, and both rules check out. Next is getting the demo ready.

**1. Update section 6.3 of your demo guide.** Replace the whole section with this. It uses placeholders, so it won't get blocked:

````markdown
### 6.3 Other rules in a prompt

| Rule | Example prompt | Expected log rule |
|---|---|---|
| Payment card | `Charge this card: [FAKE CARD, not a documentation test number], exp 12/28` | payment card |
| Credentials (AWS-style key) | `Use these AWS keys: [FAKE AWS KEY]` | secrets-credentials |
| Credentials (password) | `Log in with username admin and password=[FAKE PASSWORD]` | secrets-credentials |
| Private key | `Is this key valid? [FAKE PRIVATE KEY BLOCK]` | secrets-private-key |
| Classification marking | `Summarize this memo: [MARKING ABOVE CEILING]. Budget notes.` | classification-ceiling |
| Bulk contacts | `Make a mailing list: [30 FAKE EMAILS on a non-excluded domain]` | pii-bulk-contact-data |

> The card rule deliberately allows well-known documentation test numbers (such as 4111...), and the bulk-contact rule only fires at 25+ addresses and ignores internal and example domains. These are policy choices InfoSec can review.

After each prompt, run `Last` in PowerShell to show which rule fired.
````

**2. Add two questions to section 9.3** (Decisions needed from InfoSec):

```markdown
7. **Test card numbers:** the hook allows well-known documentation test card numbers, but Zscaler blocks them. Should the two layers agree?
8. **Bulk contact threshold:** the rule fires at 25+ email addresses and ignores frb.gov, federalreserve.gov, example.com and example.org. Is 25 the right threshold?
```

**3. Update your Notepad test note**
- Card: `4539148803436467`
- Bulk contacts: generate the list in PowerShell, then copy it:
  ```powershell
  (1..30 | ForEach-Object { "person$_@contoso-test.net" }) -join ", " | Set-Clipboard
  ```
  Then paste it after `Make a mailing list: `.

