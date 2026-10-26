```
                 if event == "PreToolUse" and cowork.is_cowork(payload):
        _ti = payload.get("tool_input") if isinstance(payload.get("tool_input"), Mapping) else {}
        for _k in ("file_path", "notebook_path", "path"):
            _v = _ti.get(_k)
            if isinstance(_v, str) and _v and not cowork.is_vm_path(_v):
                cowork.learn(_resolve(_v, cwd), _state_dir())
```
