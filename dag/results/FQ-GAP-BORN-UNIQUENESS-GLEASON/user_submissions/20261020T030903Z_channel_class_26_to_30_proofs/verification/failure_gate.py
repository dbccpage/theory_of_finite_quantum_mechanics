import sys
checks=[]
def check(name, condition):
    if condition is not True:
        raise RuntimeError('FAIL ' + name + ': ' + str(condition))
    checks.append(name)
    print('PASS ' + name)
check("expected failure gate", False if sys.argv[1]=="false" else None)
