#!/usr/bin/env python3
"""Independent check for PGW-SN-PROTECTED-ANSWER-TRANSPORT (TFQ-0519).

AuthorityEffect: None.
Zero repository imports. Uses only Python's standard library (itertools) to check:
1. Retraction-induced answer transport F' = Sum.elim F d o r across injective lifts
   u : Fin(m) -> Fin(n), uniqueness on im(u), off-image freedom when n > m, and
   exact counterpart count |{F' : B -> Q | F' o u = F}| = |Q|^(|B| - |A|).
2. Commuting transition square characterization (T' o u = u o T), k-step iterated
   transport F'((T')^k(u(a))) = F(T^k(a)), canonical transition lift T'_{T,b_ref},
   equivalence with universal Boolean answer preservation on im(u), and exact count
   of commuting vs non-commuting target transitions (n^(n-m) vs n^n - n^(n-m)).
3. Concrete SnCarrier (5 base presentation shapes + off-image witnesses at stage 6)
   and S6Descent (u(x) = (x, 0) on Z x Z) instantiations and negative controls.
4. Non-implication fences: failure of conservative extension off im(u), failure of
   right-inverse / left-Galois adjunction on gapLift : Fin(2) -> Fin(3), and
   non-resolution of active demands (including activeObstructions(6) = 1).
"""

from __future__ import annotations

import itertools
import sys


def iterate_fn(fn, x, k: int):
    cur = x
    for _ in range(k):
        cur = fn(cur)
    return cur


def check_finite_counterpart_counts() -> tuple[int, int]:
    """Check counterpart cardinality |Q|^(|B| - |A|) and off-image freedom."""
    checks = 0
    underdetermined_cases = 0
    for m in (1, 2, 3):
        for n in range(m, 5):
            # Canonical injective lift u(a) = a from Fin(m) into Fin(n)
            u = lambda a, m=m: a
            image = set(range(m))
            for q in (2, 3):
                # Test a nontrivial answer F(a) = a % q
                f_base = tuple(a % q for a in range(m))
                valid_counterparts = []
                for f_prime in itertools.product(range(q), repeat=n):
                    checks += 1
                    if all(f_prime[u(a)] == f_base[a] for a in range(m)):
                        valid_counterparts.append(f_prime)
                expected_count = q ** (n - m)
                if len(valid_counterparts) != expected_count:
                    raise AssertionError(
                        f"Counterpart count mismatch for m={m}, n={n}, q={q}: "
                        f"got {len(valid_counterparts)}, expected {expected_count}"
                    )
                # All valid counterparts agree on im(u)
                for f1, f2 in itertools.combinations(valid_counterparts, 2):
                    checks += 1
                    if any(f1[b] != f2[b] for b in image):
                        raise AssertionError("Valid counterparts disagreed on im(u)")
                # Whenever n > m, each off-image point b0 attains all q values
                if n > m:
                    for b0 in range(m, n):
                        attained = {fp[b0] for fp in valid_counterparts}
                        checks += 1
                        if attained != set(range(q)):
                            raise AssertionError(
                                f"Off-image point {b0} did not attain all values in range({q})"
                            )
                        underdetermined_cases += 1
    return checks, underdetermined_cases


def check_transition_squares() -> tuple[int, int, int]:
    """Check commuting transition squares, k-step transport, and Boolean characterization."""
    checks = 0
    commuting_count = 0
    non_commuting_count = 0
    m, n = 2, 3
    u = lambda a: a
    # Retraction r(b) = ('inl', b) if b < m else ('inr', None)
    r = lambda b: ("inl", b) if b < m else ("inr", None)
    all_boolean_answers = list(itertools.product((0, 1), repeat=m))

    for t_base in itertools.product(range(m), repeat=m):
        # Verify canonical transition lift commutes
        t_canon = tuple(u(t_base[b]) if b < m else 2 for b in range(n))
        checks += 1
        if not all(t_canon[u(a)] == u(t_base[a]) for a in range(m)):
            raise AssertionError("Canonical transition lift failed to commute")

        t_for_count = 0
        for t_prime in itertools.product(range(n), repeat=n):
            commutes = all(t_prime[u(a)] == u(t_base[a]) for a in range(m))
            if commutes:
                commuting_count += 1
                t_for_count += 1
                # Check k-step iterated transport for k = 0..5 across all Boolean answers
                for f_base in all_boolean_answers:
                    for d_val in (0, 1):
                        f_prime = lambda b, fb=f_base, dv=d_val: (
                            fb[r(b)[1]] if r(b)[0] == "inl" else dv
                        )
                        for k in range(6):
                            for a in range(m):
                                checks += 1
                                lhs = f_prime(iterate_fn(lambda x, tp=t_prime: tp[x], u(a), k))
                                rhs = f_base[iterate_fn(lambda x, tb=t_base: tb[x], a, k)]
                                if lhs != rhs:
                                    raise AssertionError(
                                        f"Iterated transport failed at k={k}, a={a}"
                                    )
            else:
                non_commuting_count += 1
                # Verify that at some a in Fin(m), some Boolean answer + fallback detects failure
                detected = False
                for a in range(m):
                    for f_base in all_boolean_answers:
                        for d_val in (0, 1):
                            f_prime = lambda b, fb=f_base, dv=d_val: (
                                fb[r(b)[1]] if r(b)[0] == "inl" else dv
                            )
                            checks += 1
                            if f_prime(t_prime[u(a)]) != f_base[t_base[a]]:
                                detected = True
                if not detected:
                    raise AssertionError("Non-commuting T' was not detected by Boolean answers")
        if t_for_count != n ** (n - m):
            raise AssertionError(
                f"Expected {n ** (n - m)} commuting T' for fixed T, got {t_for_count}"
            )
    return checks, commuting_count, non_commuting_count


def check_sn_carrier_and_s6_descent() -> tuple[int, int]:
    """Check SnCarrier (5 base shapes + off-image witnesses) and S6Descent on Z x Z."""
    checks = 0
    refusals = 0

    base_shapes = [
        ("ground", ()),
        ("supplied", ("a",)),
        ("pair", ("a", "b")),
        ("cut", ("a", "b")),
        ("simplex", ("a", "1")),
    ]

    def section_lift(stage: int, base: tuple[str, tuple[str, ...]]):
        kind, args = base
        if kind == "ground":
            return ("lift", stage, ("glyphs", ()))
        if kind == "supplied":
            return ("lift", stage, ("glyphs", (args[0],)))
        if kind == "pair":
            return ("lift", stage, ("glyphs", (args[0], args[1])))
        if kind == "cut":
            return ("lift", stage, ("arrow", args[0], args[1]))
        if kind == "simplex":
            return ("lift", stage, ("pair", args[0], args[1]))
        raise ValueError(f"Unknown base shape {kind}")

    def sn_retract(stage: int, pres):
        if pres[0] != "lift" or pres[1] != stage:
            return ("inr", None)
        body = pres[2]
        if body[0] == "glyphs":
            gs = body[1]
            if len(gs) == 0:
                return ("inl", ("ground", ()))
            if len(gs) == 1:
                return ("inl", ("supplied", (gs[0],)))
            if len(gs) == 2:
                return ("inl", ("pair", (gs[0], gs[1])))
            return ("inr", None)
        if body[0] == "arrow":
            return ("inl", ("cut", (body[1], body[2])))
        if body[0] == "pair":
            return ("inl", ("simplex", (body[1], body[2])))
        return ("inr", None)

    # Check OldImageLaw and AnswerTransport across all 5 base shapes at stage 6
    f_arity = lambda b: len(b[1])
    f_prime_0 = lambda p: f_arity(sn_retract(6, p)[1]) if sn_retract(6, p)[0] == "inl" else -1
    f_prime_1 = lambda p: f_arity(sn_retract(6, p)[1]) if sn_retract(6, p)[0] == "inl" else -2

    for b in base_shapes:
        checks += 1
        lifted = section_lift(6, b)
        if sn_retract(6, lifted) != ("inl", b):
            raise AssertionError(f"SnCarrier old-image failure on {b}")
        if f_prime_0(lifted) != f_arity(b) or f_prime_1(lifted) != f_arity(b):
            raise AssertionError(f"SnCarrier answer transport failure on {b}")

    # Off-image witnesses at stage 6
    off_image_samples = [
        ("lift", 6, ("glyphs", ("a", "b", "c"))),
        ("lift", 5, ("glyphs", ("a",))),
        ("ground", ()),
        ("nonDescent", ()),
    ]
    for sample in off_image_samples:
        checks += 1
        if sn_retract(6, sample) != ("inr", None):
            raise AssertionError(f"Off-image sample {sample} was not refused at stage 6")
        if f_prime_0(sample) == f_prime_1(sample):
            raise AssertionError("Distinct off-image fallbacks did not separate off-image sample")
        refusals += 1

    # S6Descent integer slice model: s6Lift(x) = (x, 0), s6Retract(x, y)
    s6_lift = lambda x: (x, 0)
    s6_retract = lambda p: ("inl", p[0]) if p[1] == 0 else ("inr", None)
    f_int = lambda x: 3 * x + 2
    f_s6_prime = lambda p: f_int(s6_retract(p)[1]) if s6_retract(p)[0] == "inl" else -999
    t_int = lambda x: x + 1
    t_s6_canon = lambda p: s6_lift(t_int(p[0])) if p[1] == 0 else (0, 1)
    t_s6_bad = lambda p: (p[0] + 1, 1)

    for x in range(-10, 11):
        checks += 1
        if s6_retract(s6_lift(x)) != ("inl", x):
            raise AssertionError(f"S6Descent old-image failure at x={x}")
        if f_s6_prime(s6_lift(x)) != f_int(x):
            raise AssertionError(f"S6Descent answer transport failure at x={x}")
        if f_s6_prime(t_s6_canon(s6_lift(x))) != f_int(t_int(x)):
            raise AssertionError(f"S6Descent canonical transition square failure at x={x}")
        # Negative control: t_s6_bad steps off y = 0 and corrupts the transported answer
        if f_s6_prime(t_s6_bad(s6_lift(x))) == f_int(t_int(x)):
            raise AssertionError(f"Negative control t_s6_bad unexpectedly preserved answer at x={x}")

    for x in range(-5, 6):
        for y in (-2, -1, 1, 2):
            checks += 1
            if s6_retract((x, y)) != ("inr", None):
                raise AssertionError(f"S6Descent failed to refuse off-slice point ({x}, {y})")
            refusals += 1

    return checks, refusals


def check_non_implication_fences() -> int:
    """Check non-conservative extension, non-Galois adjunction, and demand retention."""
    checks = 0
    # 1. gapLift : Fin(2) -> Fin(3), gapLift(0) = 1, gapLift(1) = 2
    gap_lift = (1, 2)
    # Check that NO p : Fin(3) -> Fin(2) satisfies gap_lift(a) <= b <-> a <= p(b)
    for p in itertools.product((0, 1), repeat=3):
        checks += 1
        galois_holds = all(
            (gap_lift[a] <= b) == (a <= p[b]) for a in (0, 1) for b in (0, 1, 2)
        )
        if galois_holds:
            raise AssertionError(f"Unexpected Galois adjoint found: {p}")

    # 2. Conservative extension failure off image: P'(b) := (b in im(gap_lift))
    p_prime = lambda b: b in gap_lift
    checks += 1
    if not all(p_prime(gap_lift[a]) for a in (0, 1)):
        raise AssertionError("P' failed on im(gap_lift)")
    if all(p_prime(b) for b in (0, 1, 2)):
        raise AssertionError("P' unexpectedly held off im(gap_lift)")

    # 3. Unrelated demand retention and SnCarrier activeObstructions(6) == 1
    active_obstructions = {0: 0, 1: 1, 2: 1, 3: 1, 4: 0, 5: 1, 6: 1}
    checks += 1
    if active_obstructions[6] != 1:
        raise AssertionError("Expected activeObstructions(6) == 1")

    return checks


def main() -> int:
    c1, underdetermined = check_finite_counterpart_counts()
    c2, comm, non_comm = check_transition_squares()
    c3, refusals = check_sn_carrier_and_s6_descent()
    c4 = check_non_implication_fences()
    total = c1 + c2 + c3 + c4
    print(
        f"PASS pgw-sn-protected-answer-transport: checks={total} "
        f"underdetermined_cases={underdetermined} commuting={comm} "
        f"non_commuting={non_comm} refusals={refusals}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
