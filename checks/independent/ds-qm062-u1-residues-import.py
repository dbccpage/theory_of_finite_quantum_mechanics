# Independent check for DS-QM062-U1-RESIDUES-IMPORT.
# Integer matrix of order 4 and remainders modulo 4. No repository imports.

checks = 0

def check(cond):
    global checks
    checks += 1
    if not cond:
        raise SystemExit("check failed at " + str(checks))

def mm(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)

eye = (1, 0, 0, 1)
jay = (0, -1, 1, 0)
jay2 = (-1, 0, 0, -1)
jay3 = (0, 1, -1, 0)
reps = (eye, jay, jay2, jay3)

def powj(k):
    value = eye
    for _ in range(k):
        value = mm(value, jay)
    return value

check(mm(jay, jay) == jay2)
check(mm(jay2, jay) == jay3)
check(mm(jay3, jay) == eye)
check(jay != eye)
check(jay2 != eye)
check(jay3 != eye)
check(0 * 0 - 1 * 1 == -1)
check((-1) * (-1) == 1)
for n, r in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 0)):
    check(n % 4 == r)
check(powj(1) == jay)
check(powj(2) == jay2)
check(powj(3) == jay3)
check(powj(4) == eye)

for k in range(0, 40):
    check((k + 4) % 4 == k % 4)
    check((k + 1) % 4 == (k % 4 + 1) % 4)
    check(powj(k) == reps[k % 4])
    check((powj(k) == eye) == (k % 4 == 0))
    check(powj(k + 4) == powj(k))
    if k % 4 < 4:
        check(mm(reps[k % 4], jay) == reps[(k % 4 + 1) % 4])

print(
    "checks=" + str(checks)
    + " failures=0"
    + " order=4"
    + " square=(-1, 0, 0, -1)"
    + " cube=(0, 1, -1, 0)"
    + " fourth=(1, 0, 0, 1)"
)
