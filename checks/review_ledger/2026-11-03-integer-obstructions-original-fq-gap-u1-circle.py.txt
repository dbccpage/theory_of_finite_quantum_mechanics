"""Independent integer check for the FQ-GAP-U1-CIRCLE narrowing.

Recomputes the 3-4-5 identity, the mod-5 square residues, a finite scan of
5*a*a = 4*b*b, and a finite scan of the cleared pair
5*(a*a - b*b) = 3*(d*d) together with a*a + b*b = d*d.
Does not import repository code. The scan is finite. The all-integer
descent is the Lean module U1CircleIntegerWitness.
"""
from __future__ import annotations

BOUND = 2000
BOX = 12

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


def is_square(n: int) -> bool:
    if n < 0:
        return False
    lo = 0
    hi = n
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == n:
            return True
        if sq < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


check(3 * 3 + 4 * 4 == 5 * 5, "3*3 + 4*4 = 5*5")

residues = sorted({(n * n) % 5 for n in range(5)})
check(residues == [0, 1, 4], f"squares mod 5 are {residues}")

for residue in (0, 1, 4):
    zero = (4 * residue) % 5 == 0
    check(zero == (residue == 0), f"4*{residue} mod 5")

nat_hits = 0
for b in range(1, BOUND + 1):
    num = 4 * b * b
    if num % 5 == 0 and is_square(num // 5):
        nat_hits += 1
check(nat_hits == 0, f"natural hits below {BOUND}: {nat_hits}")

zero_ok = (5 * (0 - 0) == 3 * 0) and (0 + 0 == 0)
check(zero_ok, "zero triple")

real_part = 5 * (3 * 3 - 4 * 4)
norm = 3 * 3 + 4 * 4
check(norm == 5 * 5 and real_part != 3 * (5 * 5), "3,4,5 fails the real-part equation")

box_hits = []
for a in range(-BOX, BOX + 1):
    for b in range(-BOX, BOX + 1):
        for d in range(-BOX, BOX + 1):
            real = 5 * (a * a - b * b) == 3 * (d * d)
            unit = a * a + b * b == d * d
            if real and unit:
                box_hits.append((a, b, d))
check(box_hits == [(0, 0, 0)], f"box hits {box_hits}")

print(
    f"checked 3*3+4*4=5*5; squares mod 5 = {{0,1,4}}; "
    f"4*square residue is 0 mod 5 only at residue 0; "
    f"no natural b in 1..{BOUND} has 5*a*a = 4*b*b; "
    f"integers a,b,d in -{BOX}..{BOX} solve both cleared equations only at 0,0,0"
)
print(f"failures={failures}")
raise SystemExit(failures)
