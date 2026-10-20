ok=True
checks=[]
def check(name, cond):
    global ok
    if cond is None:
        passed = False
    else:
        try: passed = bool(cond)
        except TypeError: passed = False
    ok = ok and passed
    checks.append({"name": name, "passed": passed})
    print(("PASS " if passed else "FAIL ") + name)
    return passed
check("INJECTED FALSE",False)
check("INJECTED UNKNOWN",None)
if not ok: raise SystemExit(1)
