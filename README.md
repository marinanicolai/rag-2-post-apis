```
git add client\hook.py client\cowork.py
git commit -m "hook.py: handle Cowork shell tool, VM paths and dragged-in files"
```
```
Select-String -Path client\hook.py -Pattern "uploaded_files"
```
```
python -c "import ast; ast.parse(open('client/hook.py', encoding='utf-8').read()); print('OK')"
```
