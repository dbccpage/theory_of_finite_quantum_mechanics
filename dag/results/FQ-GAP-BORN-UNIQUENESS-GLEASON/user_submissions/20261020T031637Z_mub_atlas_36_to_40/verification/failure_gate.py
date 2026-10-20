import sys
checks=[]
def check(name, cond):
    if cond is not True:
        raise RuntimeError('FAIL ' + name + ': ' + str(cond))
    checks.append(name)
    print('PASS ' + name)
check("expected failure gate", False if sys.argv[1]=="false" else None)
