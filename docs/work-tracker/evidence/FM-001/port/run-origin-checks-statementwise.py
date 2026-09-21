import ast, sys, io, json, traceback, contextlib, pathlib
path = pathlib.Path(__file__).parent / "test_origin_against_core.py"
src = path.read_text(); tree = ast.parse(src)
ns = {"__file__": str(path), "__name__": "__main__"}
results, errors = [], []
def check(name, ok):
    results.append((name, bool(ok)))
for node in tree.body:
    seg = ast.get_source_segment(src, node) or ""
    if seg.startswith("def check(") or "sys.exit" in seg and "FAILS" in seg:
        continue
    code = compile(ast.Module([node], []), str(path), "exec")
    ns["check"] = check
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            exec(code, ns)
    except SystemExit:
        pass
    except BaseException as e:
        names = [n.args[0].value for n in ast.walk(node) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "check" and n.args and isinstance(n.args[0], ast.Constant)]
        errors.append((node.lineno, type(e).__name__ + ": " + str(e)[:90], names))
ok = [n for n, r in results if r]; bad = [n for n, r in results if not r]
errd = [n for _l, _e, ns_ in errors for n in ns_]
print(f"ran {len(results)} checks: {len(ok)} pass, {len(bad)} fail; {len(errors)} statements crashed, taking {len(errd)} checks with them")
json.dump({"pass": ok, "fail": bad, "errors": errors}, open("/tmp/_stmt.json", "w"), ensure_ascii=False, indent=1)
