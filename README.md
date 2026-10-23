```
import os

from client.hook import _bash_file_refs, _embedded_candidates


def _found(refs, path):
    return any(os.path.samefile(p, path) for p in refs)


def test_plain_path_still_found(tmp_path):
    doc = tmp_path / "secret.docx"
    doc.write_bytes(b"x")
    assert _found(_bash_file_refs(f"cat {doc}", str(tmp_path), 20), doc)


def test_path_inside_python_one_liner(tmp_path):
    doc = tmp_path / "secret.docx"
    doc.write_bytes(b"x")
    cmd = f'python -c "import zipfile; print(zipfile.ZipFile(r\'{doc}\').read(\'word/document.xml\')[:200])"'
    assert _found(_bash_file_refs(cmd, str(tmp_path), 20), doc)


def test_relative_path_inside_one_liner(tmp_path):
    doc = tmp_path / "secret.docx"
    doc.write_bytes(b"x")
    cmd = 'python -c "import zipfile; zipfile.ZipFile(\'secret.docx\')"'
    assert _found(_bash_file_refs(cmd, str(tmp_path), 20), doc)


def test_path_with_spaces_inside_one_liner(tmp_path):
    sub = tmp_path / "My Docs"
    sub.mkdir()
    doc = sub / "secret.docx"
    doc.write_bytes(b"x")
    cmd = f'python -c "open(r\'{doc}\')"'
    assert _found(_bash_file_refs(cmd, str(tmp_path), 20), doc)


def test_path_inside_script_the_command_runs(tmp_path):
    doc = tmp_path / "secret.docx"
    doc.write_bytes(b"x")
    script = tmp_path / "extract.py"
    script.write_text(f"import zipfile\nzipfile.ZipFile(r'{doc}')\n")
    assert _found(_bash_file_refs(f"python {script}", str(tmp_path), 20), doc)


def test_limit_is_respected(tmp_path):
    for i in range(5):
        (tmp_path / f"f{i}.txt").write_text("x")
    cmd = 'python -c "' + "; ".join(f"open('f{i}.txt')" for i in range(5)) + '"'
    assert len(_bash_file_refs(cmd, str(tmp_path), 3)) == 3


def test_escaped_windows_backslashes():
    cands = _embedded_candidates(r'''open("C:\\Users\\me\\x.docx")''')
    assert r"C:\Users\me\x.docx" in cands


def test_no_false_matches(tmp_path):
    assert _bash_file_refs('python -c "print(1.5)"', str(tmp_path), 20) == []
```

