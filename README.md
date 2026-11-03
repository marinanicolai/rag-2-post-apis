```
unset PGOPTIONS
cd ~/scratch && git clone --depth 1 -b fix/skill-download-frontmatter https://gitlab.frb.gov/ai-program/platforms/tech-enablement/coding-tools/ai-marketplace.git mig-059
cd mig-059 && git rev-parse --short HEAD     # expect c22286e
python3 -m venv --system-site-packages .venv-mig && source .venv-mig/bin/activate
pip install -r requirements.txt
export PYTHONPATH=apps/api:libs/db:libs/python-common
```
