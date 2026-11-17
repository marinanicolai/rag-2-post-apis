```
Hi team,

I wanted to give you a quick update on Skillhub email notifications and ask for your help with a blocker.

**The issue**
Skillhub can't send email right now because the mail relay won't accept mail from any host we can send from:

• **fweb** (where Skillhub runs): the relay rejects the connection, so the server can't send.
• **salt1** (the off-host worker candidate): also rejected. The RCPT TO probe returned `554 5.7.1 ... Client host rejected: IP address not allowed`.

In simple terms, email is blocked because neither server's IP is on the relay's allowlist.

**Possible solutions**
1. Get the IP for fweb or salt1 added to the relay's allowlist. Does anyone know who owns the relay, or which ticket queue handles this?
2. Use a Teams channel for notifications instead of email. Skillhub would post to the channel through a webhook or a Power Automate workflow. That avoids the relay completely, but we'd need a channel and approval to set up the webhook.

Which option makes more sense, or is there another route I'm missing? Any pointers would help a lot.

Thanks!
Marina
```
