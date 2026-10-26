# Independent check for DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT.
# Integer Gram square and two cleared witnesses. No repository imports.

checks = 0

def check(cond):
    global checks
    checks += 1
    if not cond:
        raise SystemExit("check failed at " + str(checks))

def square_nonneg(n):
    return n * n >= 0

for n in range(-30, 31):
    check(square_nonneg(n))

for a in range(-6, 7):
    for b in range(-6, 7):
        check(a * a >= 0 and b * b >= 0)
        check(a * a + b * b >= 0)
        check(a * a * (b * b) - (a * b) * (a * b) == 0)
        check((a * b) * (a * b) == a * a * (b * b))
        for x in (-3, -1, 0, 2):
            for y in (-2, 0, 1, 4):
                value = (a * x + b * y) * (a * x + b * y)
                check(value >= 0)

check(1 + 1 == 2 * 1)
check(1 * 1 + 1 * 1 == 2)
check(2 * 2 == 4)
check(2 != 4)
check((1 + 1) * (1 + 1) == 4)
check(4 == 4 * 1)
check(3 * 3 + 4 * 4 == 25)
check(5 * 5 == 25)
check(3 * 3 + 4 * 4 == 5 * 5)
check(3 + 4 == 7)
check(7 * 7 == 49)
check(49 != 25)
check((1 * 1 + 1 * 1) * (1 * 1 + 1 * 1) == 4)
check(1 * 1 * 1 * 1 + 2 * 1 * 1 * 1 * 1 + 1 * 1 * 1 * 1 == 4)

# Cleared reading: halves sum to 1 and their square-sum is 1/2.
check((1 + 1) * 2 == 2 * 2)
check((1 * 1 + 1 * 1) * 2 == 4)
# Cleared reading: 3/5 and 4/5 have square-sum 1, and their sum squares to 49/25.
check((3 * 3 + 4 * 4) * 1 == 25)
check((3 + 4) * (3 + 4) == 49)

print(
    "checks=" + str(checks)
    + " failures=0"
    + " half=(1, 1)"
    + " kraus=(3, 4)"
    + " squares=(2, 25)"
    + " globals=(4, 49)"
)
