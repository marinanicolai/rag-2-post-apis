```
@'
import os, sys, tempfile
sys.path.insert(0, ".")
from client import cowork
t = os.path.join(tempfile.gettempdir(), "cw-test", "task1")
os.makedirs(os.path.join(t, "host-cwd"), exist_ok=True)
cwd = os.path.join(t, "host-cwd")
print("task  :", cowork.task_dir(cwd))
print("upload:", cowork.to_host("/sessions/abc/mnt/uploads/x.docx", cwd, tempfile.gettempdir()))
print("drag  :", cowork.uploaded_files("<uploaded_files><file><file_path>C:/a/b.docx</file_path></file></uploaded_files>"))
print("vm?   :", cowork.is_vm_path("/sessions/abc/mnt/Reports/q3.docx"), cowork.is_vm_path("C:/x.docx"))
'@ | python -
```
