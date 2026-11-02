"""Exact check of the Galois-conjugate non-Born weight over Q(sqrt2) (refuting_everett_assessment.md, sec. 2, B2).
Elements of Q(sqrt2) are pairs (p, q) meaning p + q*sqrt2, with p, q rational."""
from fractions import Fraction as Fr
from math import sqrt

def mul(x, y): return (x[0]*y[0] + 2*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
def add(x, y): return (x[0]+y[0], x[1]+y[1])
def sigma(x): return (x[0], -x[1])                 # the second real embedding sqrt2 -> -sqrt2
def real(x): return float(x[0]) + float(x[1])*sqrt(2)

a = (Fr(-3, 17), Fr(-8, 17)); c = (Fr(12, 17), Fr(-2, 17))
a2, c2 = mul(a, a), mul(c, c)
assert add(a2, c2) == (1, 0)                         # a^2 + c^2 = 1: a normalized K-state
assert a2 == (Fr(137, 289), Fr(48, 289))
s_a2, s_c2 = sigma(a2), sigma(c2)
assert add(s_a2, s_c2) == (1, 0)                     # conjugate weights still sum to 1
assert real(s_a2) >= 0 and real(s_c2) >= 0           # and are nonnegative (sigma(x^2) = sigma(x)^2)
assert abs(real(s_a2) - real(a2)) > 0.4              # but differ from Born
# sigma is multiplicative, so tensor/sequential composition is preserved
assert sigma(mul(a2, c2)) == mul(s_a2, s_c2)
# a weight positive in the standard order but not totally positive is NOT a sum of squares, hence not realizable
w = (Fr(-1), Fr(1))                                  # sqrt2 - 1 > 0, sigma = -sqrt2 - 1 < 0
assert real(w) > 0 and real(sigma(w)) < 0
print(f"Born a^2 = {real(a2):.6f}, conjugate sigma(a^2) = {real(s_a2):.6f}; c^2 = {real(c2):.6f}, sigma(c^2) = {real(s_c2):.6f}. OK")
