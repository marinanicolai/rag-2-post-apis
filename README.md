```
unset PGOPTIONS
mkdir -p ~/scratch && cd ~/scratch
git clone --depth 1 -b fix/skill-download-frontmatter https://gitlab.frb.gov/ai-program/platforms/tech-enablement/coding-tools/ai-marketplace.git audit-am
cd audit-am
git log --oneline -1
```
