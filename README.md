```
H, before I package the DLP plugin for the stakeholders, I want to make sure I build the right thing:
What do you mean by packaging? A plugin zip they install (Python version or the exe version like release 0.2.1), or just a way for them to install and try it?
Where will stakeholders test it: in the Claude desktop app or in the CLI?
On which machines: standard Fed laptops, or a test VM?
The reason I’m asking: on Fed laptops, the real plugin can be tested in the CLI today (loaded straight from the repo, no approval needed). In the desktop app, the plugin install is blocked by AppLocker and endpoint DLP. Desktop testing works through Claude settings with the same hook and rules, but as a true plugin it would need an InfoSec exception or a test VM.

 
```

