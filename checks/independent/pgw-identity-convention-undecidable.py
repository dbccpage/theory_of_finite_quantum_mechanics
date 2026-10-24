"""Independent exact-arithmetic verifier for PGW-IDENTITY-CONVENTION-UNDECIDABLE (TFQ-0423).

AuthorityEffect: None. No repository imports.

Verifies:
1. Observation-family Pre-Genesis regimes over token sets of size n in {1, 2, 3},
   non-empty presented subsets P, and observation families O of k in {0, 1, 2} boolean
   predicates:
   - Supplying x not in P preserves O_1 = O_0 and enlarges |P| by +1.
   - Profile equality matches SameProfile over indexed observations and collapses to a
     single quotient class when O is empty.
   - Branch divergence for Prompt 12 (P_0 = {<>}, O_0 = (), x = <a>): opaque gives False
     (delta = 0), exact-inscription gives True (delta = +1), and queryNewState(None)
     keeps both branches as ('undecidable', False, True).
   - State-count bound stateCount(opaque) <= stateCount(exact), and exact branch agreement
     criterion on fresh inscriptions and injective observation families.
2. Genesis unary-form regimes over n in {1, 2, 3, 4} data and m in {0, 1, 2} unary forms
   (all 2^(n*m) instance tables):
   - Exact equivalence between unary observation profile equality and Genesis Collapsed(r, i, j).
   - Unformed 2-datum regime vs firstSeparationRegime contrast.
3. Scope fences:
   - No convention-independent boolean evaluator simultaneously matches both opaque and
     exact-inscription conventions on the Prompt 12 fixture.
   - Recorded Prompt 12 trial replies (opaque, opaque, exact) realize both branches.
"""

from __future__ import annotations

from itertools import combinations, product
import sys


def obs_profile(obs_family: tuple[int, ...], x: int) -> tuple[int, ...]:
    return tuple((pred_mask >> x) & 1 for pred_mask in obs_family)


def same_profile(obs_family: tuple[int, ...], x: int, y: int) -> bool:
    return all(((pred_mask >> x) & 1) == ((pred_mask >> y) & 1) for pred_mask in obs_family)


def is_new_state_under(
    convention: str,
    presented: frozenset[int],
    obs_family: tuple[int, ...],
    x: int,
) -> bool:
    if convention == "opaque":
        existing_profiles = {obs_profile(obs_family, p) for p in presented}
        return obs_profile(obs_family, x) not in existing_profiles
    if convention == "exact":
        return x not in presented
    raise ValueError(f"Unknown convention: {convention}")


def query_new_state(
    opt_convention: str | None,
    presented: frozenset[int],
    obs_family: tuple[int, ...],
    x: int,
) -> tuple[str, bool, bool] | tuple[str, bool]:
    if opt_convention is None:
        return (
            "undecidable",
            is_new_state_under("opaque", presented, obs_family, x),
            is_new_state_under("exact", presented, obs_family, x),
        )
    return ("decided", is_new_state_under(opt_convention, presented, obs_family, x))


def state_count_under(
    convention: str,
    presented: frozenset[int],
    obs_family: tuple[int, ...],
) -> int:
    if convention == "opaque":
        return len({obs_profile(obs_family, p) for p in presented})
    if convention == "exact":
        return len(presented)
    raise ValueError(f"Unknown convention: {convention}")


def _verify_observation_family_regimes_cases_1_cases_2(checks, failures, inj_all, n, obs_fam, presented):
    for x in range(n):
        for y in range(n):
            eq_prof = obs_profile(obs_fam, x) == obs_profile(obs_fam, y)
            eq_same = same_profile(obs_fam, x, y)
            if eq_prof == eq_same and (len(obs_fam) > 0 or eq_prof is True):
                checks += 1
            else:
                failures += 1

        # Check supply and branch agreement on x
        supplied = presented | {x}
        if x not in presented:
            if len(supplied) == len(presented) + 1:
                checks += 1
            else:
                failures += 1
            b_op = is_new_state_under("opaque", presented, obs_fam, x)
            b_ex = is_new_state_under("exact", presented, obs_fam, x)
            fresh_prof = obs_profile(obs_fam, x) not in {
                obs_profile(obs_fam, p) for p in presented
            }
            if b_ex is True and (b_op == b_ex) == fresh_prof:
                checks += 1
            else:
                failures += 1
        if inj_all:
            if is_new_state_under("opaque", presented, obs_fam, x) == is_new_state_under(
                "exact", presented, obs_fam, x
            ):
                checks += 1
            else:
                failures += 1
    return checks, failures


def _verify_observation_family_regimes_cases_1(checks, failures, n, obs_families, presented):
    for obs_fam in obs_families:
        # Check state_count_under inequality
        c_op = state_count_under("opaque", presented, obs_fam)
        c_ex = state_count_under("exact", presented, obs_fam)
        if 1 <= c_op <= c_ex:
            checks += 1
        else:
            failures += 1

        # Check injective profile condition on the full token carrier
        full_profiles = [obs_profile(obs_fam, x) for x in range(n)]
        inj_all = len(set(full_profiles)) == n
        if inj_all:
            if c_op == c_ex:
                checks += 1
            else:
                failures += 1

        # Check pairwise profile vs SameProfile
        checks, failures = _verify_observation_family_regimes_cases_1_cases_2(checks, failures, inj_all, n, obs_fam, presented)
    return checks, failures


def verify_observation_family_regimes() -> tuple[int, int]:
    checks = 0
    failures = 0

    # Prompt 12 canonical fixture: tokens 0=ground (<>), 1=markA (<a>), 2=markB (<b>), 3=markAB (<ab>)
    p0 = frozenset({0})
    o0: tuple[int, ...] = ()
    mark_a = 1
    p1 = p0 | {mark_a}

    if (
        len(p0) == 1
        and len(p1) == 2
        and is_new_state_under("opaque", p0, o0, mark_a) is False
        and is_new_state_under("exact", p0, o0, mark_a) is True
        and query_new_state(None, p0, o0, mark_a) == ("undecidable", False, True)
        and query_new_state("opaque", p0, o0, mark_a) == ("decided", False)
        and query_new_state("exact", p0, o0, mark_a) == ("decided", True)
        and state_count_under("opaque", p0, o0) == 1
        and state_count_under("exact", p0, o0) == 1
        and state_count_under("opaque", p1, o0) == 1
        and state_count_under("exact", p1, o0) == 2
        and (state_count_under("exact", p1, o0) - state_count_under("opaque", p1, o0)) == 1
    ):
        checks += 12
    else:
        failures += 1

    # Exhaustive sweep over n in {1, 2, 3}, all non-empty presented subsets P, and observation families
    for n in (1, 2, 3):
        all_preds = list(range(1 << n))
        obs_families: list[tuple[int, ...]] = [()]
        for p_mask in all_preds:
            obs_families.append((p_mask,))
        for p1_mask, p2_mask in combinations(all_preds, 2):
            obs_families.append((p1_mask, p2_mask))

        for r_size in range(1, n + 1):
            for p_tuple in combinations(range(n), r_size):
                presented = frozenset(p_tuple)
                checks, failures = _verify_observation_family_regimes_cases_1(checks, failures, n, obs_families, presented)

    return checks, failures


def unary_sep(n_forms: int, inst_mask: int, n_data: int, i: int, j: int) -> bool:
    for f in range(n_forms):
        has_i = bool((inst_mask >> (f * n_data + i)) & 1)
        has_j = bool((inst_mask >> (f * n_data + j)) & 1)
        if (has_i and not has_j) or (has_j and not has_i):
            return True
    return False


def genesis_unary_profile(n_forms: int, inst_mask: int, n_data: int, i: int) -> tuple[bool, ...]:
    return tuple(bool((inst_mask >> (f * n_data + i)) & 1) for f in range(n_forms))


def verify_genesis_unary_bridge() -> tuple[int, int]:
    checks = 0
    failures = 0

    # Unformed 2-datum regime (n_data=2, n_forms=0, inst_mask=0) vs firstSeparationRegime (n_data=2, n_forms=1, inst_mask=1)
    if (
        genesis_unary_profile(0, 0, 2, 0) == ()
        and genesis_unary_profile(0, 0, 2, 1) == ()
        and not unary_sep(0, 0, 2, 0, 1)
        and genesis_unary_profile(1, 1, 2, 0) == (True,)
        and genesis_unary_profile(1, 1, 2, 1) == (False,)
        and unary_sep(1, 1, 2, 0, 1)
    ):
        checks += 6
    else:
        failures += 1

    for n_data in (1, 2, 3, 4):
        for n_forms in (0, 1, 2):
            for inst_mask in range(1 << (n_data * n_forms)):
                for i, j in product(range(n_data), repeat=2):
                    prof_eq = genesis_unary_profile(n_forms, inst_mask, n_data, i) == genesis_unary_profile(
                        n_forms, inst_mask, n_data, j
                    )
                    collapsed = (not unary_sep(n_forms, inst_mask, n_data, i, j)) and (
                        not unary_sep(n_forms, inst_mask, n_data, j, i)
                    )
                    if prof_eq == collapsed:
                        checks += 1
                    else:
                        failures += 1

    return checks, failures


def verify_scope_fences() -> tuple[int, int]:
    checks = 0
    failures = 0

    p0 = frozenset({0})
    o0: tuple[int, ...] = ()
    mark_a = 1

    # Fence 1: No single boolean return value matches both opaque and exact-inscription on Prompt 12
    op_ans = is_new_state_under("opaque", p0, o0, mark_a)
    ex_ans = is_new_state_under("exact", p0, o0, mark_a)
    for candidate_val in (False, True):
        matches_both = (candidate_val == op_ans) and (candidate_val == ex_ans)
        if not matches_both:
            checks += 1
        else:
            failures += 1

    # Fence 2: Prompt 12 trial record realizes both conventions
    trials = ("opaque", "opaque", "exact")
    trial_answers = tuple(is_new_state_under(c, p0, o0, mark_a) for c in trials)
    if (
        trial_answers == (False, False, True)
        and ("opaque" in trials)
        and ("exact" in trials)
        and len(set(trial_answers)) == 2
    ):
        checks += 4
    else:
        failures += 1

    # Fence 3: Explicit semantic mutants fail on Prompt 12 or separated fixture
    p_sep = frozenset({0})
    o_sep = (0b10,)  # predicate separating 0 (val 0) and 1 (val 1)
    if (
        is_new_state_under("opaque", p_sep, o_sep, 1) is True
        and is_new_state_under("exact", p_sep, o_sep, 1) is True
        and is_new_state_under("opaque", p0, o0, 1) != is_new_state_under("opaque", p_sep, o_sep, 1)
    ):
        checks += 3
    else:
        failures += 1

    return checks, failures


def main() -> int:
    c1, f1 = verify_observation_family_regimes()
    c2, f2 = verify_genesis_unary_bridge()
    c3, f3 = verify_scope_fences()

    total_checks = c1 + c2 + c3
    total_failures = f1 + f2 + f3

    print(
        f"PGW-IDENTITY-CONVENTION-UNDECIDABLE independent check: "
        f"checks={total_checks} obs_regimes={c1} genesis_bridge={c2} fences={c3} "
        f"failures={total_failures}"
    )
    return 0 if total_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
