```
python -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml')); yaml.safe_load(open('.gitlab/ci/deploy-prod.yml')); print('YAML OK')"
```
