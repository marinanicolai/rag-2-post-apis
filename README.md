```
python -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml', encoding='utf-8')); yaml.safe_load(open('.gitlab/ci/deploy-prod.yml', encoding='utf-8')); print('YAML OK')"
```
