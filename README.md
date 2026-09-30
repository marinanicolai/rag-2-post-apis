

```
Subject: RE: SkillsHub updates

Hi Missy,

Thanks for following up, and great ideas!

1.) Hooks: yes, we have a few official examples in the library now (Block Destructive Commands, Ponytail Mode, Test Runner Reminder). I love your ideas, especially the documentation update on commit and logging coding tool expense... both are low risk and would make really good examples, so I'll work on those. And agreed, once we have a good set we should get the word out. I'd love your input on the ToU piece too, since hooks run automatically on the user's machine and some awareness/guidelines would help.

2.) Duplicates: good catch! Most of them were actually my own test submissions from when I was testing the hooks flow (oops, sorry about that). I also found the bug that was letting duplicates in, where the system would create a new copy instead of rejecting a name that already existed. That's fixed and in review now, and I cleaned everything up in dev. The same cleanup goes to production once the review is done. There are two skills (glab-pm and privacy-engineer) that have two published versions each, so I'm checking with the authors before I remove anything.

3.) Chase's PDF skill: totally agree, that one would be a big win for the non-data scientists. It uses scripts, which we block right now for security, but I'm working with Zach on a way to support skills/plugins with scripts through SkillsHub with the right review in place. Chase's skill is at the top of my list once that's ready!

Thanks so much for the support, I'll keep you posted!

Marina
```
