"""Statically recover main.py from each downloaded notebook without executing notebook code.

Order of preference: the notebook's published output archive, a %%writefile main.py cell,
then AST-extracted string literals decoded via base64/base85 + zlib/lzma/gzip (+ tar).
A recovered file is accepted only if it matches an EXPECTED_*SHA256 literal when one exists.

Usage: python tools/extract_notebooks.py <dir>
  <dir> holds one sub-directory per notebook, as written by `kaggle kernels pull <ref> -p <dir>/<name> -m`.
  main.py is written next to each notebook and a summary to <dir>/extract_report.json.
"""
import ast, base64, glob, gzip, hashlib, io, json, lzma, re, sys, tarfile, zlib
from pathlib import Path

HERE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()


def sha(b): return hashlib.sha256(b).hexdigest()


def literal_strings(src):
    """Yield (name, value) for module-level string assignments, joining ''.join((...)) and (a 'b' ...) forms."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        tree = ast.parse("\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("%", "!"))))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            v = node.value
            name = node.targets[0].id
            try:
                if isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute) and v.func.attr == "join":
                    parts = ast.literal_eval(v.args[0])
                    yield name, "".join(parts)
                else:
                    val = ast.literal_eval(v)
                    if isinstance(val, (str, bytes)):
                        yield name, val
            except Exception:
                pass


def decodes(s):
    if isinstance(s, str):
        s = s.encode()
    raw = []
    for f in (base64.b85decode, base64.a85decode, base64.b64decode, base64.urlsafe_b64decode):
        try:
            raw.append(f(s))
        except Exception:
            pass
    out = []
    for r in raw:
        out.append(r)
        for dec in (zlib.decompress, lzma.decompress, gzip.decompress):
            try:
                out.append(dec(r))
            except Exception:
                pass
    return out


def from_tar(b):
    try:
        with tarfile.open(fileobj=io.BytesIO(b)) as t:
            return {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
    except Exception:
        return None


def main():
    report = {}
    for d in sorted(p for p in HERE.iterdir() if p.is_dir()):
        nbs = list(d.glob("*.ipynb"))
        if not nbs:
            continue
        cells = [''.join(c['source']) for c in json.load(open(nbs[0], encoding='utf-8'))['cells'] if c['cell_type'] == 'code']
        allsrc = "\n".join(cells)
        expected = set(re.findall(r"EXPECTED_(?:MAIN_)?SHA256\s*=\s*['\"]([0-9a-f]{64})", allsrc))
        found, how, extra = None, None, {}
        # 1) published outputs
        for arc in sorted((d / "out").glob("*.tar.gz")):
            files = from_tar(arc.read_bytes())
            if files and "main.py" in files:
                found, how, extra = files["main.py"], f"output:{arc.name}", {k: v for k, v in files.items() if k != "main.py"}
                break
        if found is None and (d / "out" / "main.py").exists():
            found, how = (d / "out" / "main.py").read_bytes(), "output:main.py"
        # 2) %%writefile main.py
        if found is None:
            for c in cells:
                m = re.match(r"\s*%%writefile\s+(?:-a\s+)?(\S+)\s*\n", c)
                if m and Path(m.group(1)).name == "main.py":
                    found, how = c[m.end():].encode(), "writefile"
        # 3) literal payloads
        if found is None:
            for c in cells:
                for name, val in literal_strings(c):
                    if len(val) < 2000:
                        continue
                    for b in decodes(val):
                        files = from_tar(b)
                        if files:
                            for k, v in files.items():
                                if Path(k).name == "main.py" and (not expected or sha(v) in expected):
                                    found, how = v, f"literal:{name}:tar:{k}"
                                    extra = {kk: vv for kk, vv in files.items() if kk != k}
                        elif b[:200].lstrip().startswith((b'#', b'"""', b'import', b'from', b"'''")) and (not expected or sha(b) in expected):
                            found, how = b, f"literal:{name}"
                        if found is not None:
                            break
                    if found is not None:
                        break
                if found is not None:
                    break
        ok = found is not None and (not expected or sha(found) in expected or how.startswith("output") or how == "writefile")
        if found is not None:
            (d / "main.py").write_bytes(found)
            for k, v in extra.items():
                if Path(k).name != k:
                    continue
                (d / k).write_bytes(v)
        report[d.name] = dict(how=how, sha=sha(found) if found else None, bytes=len(found) if found else 0,
                              expected=sorted(expected), hash_match=bool(found and sha(found) in expected),
                              extra=sorted(extra))
        print(f"{d.name:44s} {str(how):40s} {report[d.name]['bytes']:>8} match={report[d.name]['hash_match']} exp={len(expected)} extra={sorted(extra)}")
    (HERE / "extract_report.json").write_text(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
