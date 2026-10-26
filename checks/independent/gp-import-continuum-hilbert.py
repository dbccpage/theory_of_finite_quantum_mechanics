# Independent check for GP-IMPORT-CONTINUUM-HILBERT.
# Finite dyadic window and the geometric power-of-four tail. No repository imports.

def pow4(n):
    value = 1
    for _ in range(n):
        value *= 4
    return value

def sum_pow4(n):
    total = 0
    for j in range(n):
        total += pow4(j)
    return total

checks = 0

def check(cond):
    global checks
    checks += 1
    if not cond:
        raise SystemExit("check failed at " + str(checks))

for n in range(0, 41):
    partial = sum_pow4(n)
    check(3 * partial + 1 == pow4(n))
    check(pow4(n) - 3 * partial == 1)
    check(sum_pow4(n + 1) - partial == pow4(n))
    coords = [2 ** (n - 1 - k) for k in range(n)] if n else []
    check(sum(c * c for c in coords) == partial)

coords = (8, 4, 2, 1)
squares = tuple(c * c for c in coords)
check(squares == (64, 16, 4, 1))
check(sum(squares) == 85)
check(8 * 8 + 4 * 4 + 2 * 2 + 1 * 1 == 85)
check(3 * 85 + 1 == 256)
check(pow4(4) == 256)
check(sum_pow4(4) == 85)
check((64 - 16, 16 - 4, 4 - 1) == (48, 12, 3))
check((3 * 16, 3 * 4, 3 * 1) == (48, 12, 3))
check(8 == 4 + 4 and 4 == 2 + 2 and 2 == 1 + 1)
for z in range(0, 8):
    check(not (z > 0 and z + z == 1))

# Cleared geometric sum: sum_{k=0}^{n-1} 4^{-k} = (4^n - 1) / (3 * 4^{n-1}) for n >= 1.
for n in range(1, 21):
    numerator = pow4(n) - 1
    denominator = 3 * pow4(n - 1)
    check(numerator % 3 == 0)
    check(3 * sum_pow4(n) == numerator)
    check(denominator == 3 * pow4(n - 1))
    check(numerator + 1 == pow4(n))

print(
    "checks=" + str(checks)
    + " failures=0"
    + " window=(8, 4, 2, 1)"
    + " squares=(64, 16, 4, 1)"
    + " sum=85"
    + " scaled=256"
    + " lengths=41"
)
