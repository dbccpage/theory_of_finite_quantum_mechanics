# Independent check for DS-CONTINUOUS-TIME-EXP-GENERATOR.
# No repository imports.

checks = 0

def check(cond):
    global checks
    checks += 1
    if not cond:
        raise SystemExit("check failed at " + str(checks))

def toggle(q):
    return not q

check(toggle(False) is True)
check(toggle(True) is False)

def maps():
    for ff in (False, True):
        for ft in (False, True):
            def sigma(q, ff=ff, ft=ft):
                return ff if q is False else ft
            yield sigma

found = False
for sigma in maps():
    if sigma(sigma(False)) is toggle(False) and sigma(sigma(True)) is toggle(True):
        found = True
check(found is False)

def gadd(x, y):
    return (x[0] + y[0], x[1] + y[1])

def gmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

def mmul(A, B):
    return (
        gadd(gmul(A[0], B[0]), gmul(A[1], B[2])),
        gadd(gmul(A[0], B[1]), gmul(A[1], B[3])),
        gadd(gmul(A[2], B[0]), gmul(A[3], B[2])),
        gadd(gmul(A[2], B[1]), gmul(A[3], B[3])),
    )

scaled = ((1, 1), (1, -1), (1, -1), (1, 1))
neg = ((-1, -1), (-1, 1), (-1, 1), (-1, -1))
four = ((0, 0), (4, 0), (4, 0), (0, 0))
check(mmul(scaled, scaled) == four)
check(mmul(neg, neg) == four)
check(scaled != neg)
check(gadd((2, 3), (5, 7)) == (7, 10))
check(gmul((1, 1), (1, -1)) == (2, 0))

def cayley(t):
    left = (1 - t * t) * (1 - t * t) + 4 * (t * t)
    right = (1 + t * t) * (1 + t * t)
    return left == right

for t in range(-20, 21):
    check(cayley(t))

def energy(k):
    return 2 * k + 1

check(energy(0) == 1)
check(energy(1) == 3)
for k1 in range(-12, 13):
    for k2 in range(-12, 13):
        check((k1 == k2) or (energy(k1) != energy(k2)))

check((-1) * (-1) + 1 * 1 == 2)

def nilpotent(a, b, c, d):
    return (
        a + 1 == 0 and b == 1 and c == 1 and d + 1 == 0 and
        a * a + b * c == 0 and a * b + b * d == 0 and
        c * a + d * c == 0 and c * b + d * d == 0
    )

check(nilpotent(-1, 1, 1, -1) is False)
# The swap forces these four integers, and the corner is 2 rather than 0.
check(not nilpotent(-1, 1, 1, -1))

print(
    "checks=" + str(checks)
    + " failures=0"
    + " toggle=2"
    + " maps=4"
    + " four=((0, 0), (4, 0), (4, 0), (0, 0))"
    + " energy=(1, 3)"
    + " corner=2"
)
