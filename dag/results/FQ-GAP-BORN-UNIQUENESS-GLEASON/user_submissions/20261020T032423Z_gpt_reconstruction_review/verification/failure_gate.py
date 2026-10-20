import sys
import sympy as s
checks=[]
def check(name, condition):
    if condition is not True and condition is not s.true:
        raise RuntimeError('FAIL ' + name + ': ' + str(condition))
    checks.append(name)
    print('PASS ' + name)
check("expected failure gate", False if sys.argv[1]=="false" else None)
