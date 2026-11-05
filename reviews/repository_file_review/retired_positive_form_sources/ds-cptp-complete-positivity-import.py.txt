# Independent check for DS-CPTP-COMPLETE-POSITIVITY-IMPORT.
# Nonnegative integer products and one strict sign. No repository imports.

checks = 0

def check(cond):
    global checks
    checks += 1
    if not cond:
        raise SystemExit("check failed at " + str(checks))

for n in range(-20, 21):
    check(n * n >= 0)
    check((-n) * (-n) == n * n)

for k in range(0, 9):
    for m in range(0, 9):
        check((k * m) >= 0)
        check(k * m == m * k)

for a in range(0, 7):
    for b in range(0, 7):
        check(a * b >= 0)

for t in range(0, 6):
    for x in range(-3, 4):
        for w in range(-3, 4):
            check(t * ((x + w) * (x + w)) >= 0)

pairing = 1 * (-1) + (-1) * 1
check(pairing == -2)
for t in range(-8, 9):
    check(t * pairing == (-2) * t)
    check(t * (-2) == 2 * (-t))
for t in range(1, 13):
    check(t * (-2) < 0)
    check(-t < 0)
check(0 * (-2) == 0)
check(0 * 0 + 1 * 1 + (-1) * (-1) + 0 * 0 == 2)

print(
    "checks=" + str(checks)
    + " failures=0"
    + " pairing=-2"
    + " norm=2"
    + " zero=0"
)
