import sys
import sympy as s
checks=[]
def check(name, cond):
    if cond is not True and cond is not s.true:
        raise RuntimeError('FAIL ' + name + ': ' + str(cond))
    checks.append(name)
    print('PASS ' + name)
check("expected failure gate", False if sys.argv[1]=="false" else None)
