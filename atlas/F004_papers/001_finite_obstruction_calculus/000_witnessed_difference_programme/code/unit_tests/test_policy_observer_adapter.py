
from witnessed_difference.native_functionals import representative_mass
from dataclasses import replace
from fractions import Fraction as Q

import pytest
from witnessed_difference.obstruction import MatrixQuotientCertificate, verify_matrix_certificate
from witnessed_difference.outcomes import Accepted
from witnessed_difference.policy_observer_adapter import (
    PolicyCarrier,
    PolicyComparisonDomain,
    PolicyGaugeAction,
    PolicyObserverProblem,
    PolicyRepairOperator,
    PolicyTerminalRules,
    SignedPermutation,
    adapt_policy_observer,
    verify_policy_evaluation,
)
from witnessed_difference.semantic_legacy_observers import SourceCustody


def problem():
    identity = PolicyGaugeAction.identity(2, 2, 2, 1)
    swap = PolicyGaugeAction((1, 0), (1, 0), SignedPermutation((0, 1), (-1, -1)),
                            SignedPermutation((0,), (-1,)))
    matrix = ((Q(1), Q(0)), (Q(0), Q(1)))
    return PolicyObserverProblem(
        PolicyCarrier(("a", "b"), ("x", "y"), ((Q(0), Q(0)), (Q(1), Q(1)))),
        PolicyComparisonDomain(("a-to-b", "b-to-a"), ((0, 1), (1, 0)), (matrix, matrix)),
        (identity, swap), PolicyRepairOperator(("opposite-shift",), ((Q(1),), (Q(-1),))),
        PolicyTerminalRules(frozenset({"WithinTolerance", "AboveTolerance"}), Q(1),
                            "WithinTolerance", "AboveTolerance"), (Q(1), Q(1)),
        SourceCustody("omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/"
                      "005_the_authority_gap/the_authority_gap.md",
                      "18b82368bc45731e29ce5baf72d2aa0fcaf177fe8344532df09c9d7b0d78e42d",
                      ("Current local authority-gap Layer3 compressed C,D,G,R,T definition; "
                       "historical Paper031 naming is a separate source citation",),
                      ("historical scoped authority tag",)))


def certificate(p, delta=(Q(1), Q(1)), alpha=(Q(0),), dual=(Q(1), Q(1))):
    residual = tuple(x-sum((a*b for a, b in zip(row, alpha)), Q(0))
                     for x, row in zip(delta, p.repair.map))
    return MatrixQuotientCertificate(p.repair.map, len(p.repair.coordinates), delta, p.norm_weights,
                                    alpha, residual, representative_mass(residual, p.norm_weights), dual)


def receipt(p):
    return adapt_policy_observer(p).evaluate(0, certificate(p))


def test_actual_five_fields_and_additional_norm_bridge_are_preserved():
    p = problem()
    observer = adapt_policy_observer(p)
    assert observer.problem == p
    assert observer.defects == ((Q(1), Q(1)), (Q(-1), Q(-1)))
    forward = receipt(p)
    reverse = observer.evaluate(1, certificate(p, (Q(-1), Q(-1)), dual=(Q(-1), Q(-1))))
    assert forward.value == reverse.value == 2
    assert forward.status == "AboveTolerance"
    assert verify_policy_evaluation(p, forward)
    t = replace(p, terminal_rules=replace(p.terminal_rules, tolerance=Q(2),
                                        within_tolerance="Authorized",
                                        permitted_statuses=frozenset({"Authorized", "AboveTolerance"})))
    tolerant = receipt(t)
    assert tolerant.value == forward.value
    assert tolerant.status == "Authorized"  # A spelling, no authority type.
    assert verify_policy_evaluation(t, tolerant)
    assert not verify_policy_evaluation(t, forward)


def test_freshly_rehashed_false_records_and_source_metadata_are_rejected():
    p = problem()
    actual = receipt(p)
    for altered in (
            replace(actual, status="WithinTolerance"), replace(actual, value=Q(0)),
            replace(actual, defect=(Q(0), Q(0))), replace(actual, comparison_name="other-pair"),
            replace(actual, problem_digest="b"*64), replace(actual, comparison=True)):
        assert not verify_policy_evaluation(p, altered.refresh_digest())
    changed = replace(p, source=replace(p.source, source_authority_tags=("changed tag",)))
    assert not verify_policy_evaluation(changed, actual)
    changed = replace(p, carrier=replace(p.carrier, values=((Q(0), Q(0)), (Q(2), Q(2)))))
    assert not verify_policy_evaluation(changed, actual)
    # Python's int/Fraction equality is not a substitute for canonical exact
    # evidence: copying the old digest must not hide changed payload types.
    assert not verify_policy_evaluation(p, replace(actual, value=2))
    assert not verify_policy_evaluation(p, replace(actual, defect=(1, 1)))


def test_independently_valid_unrelated_certificates_do_not_bind_this_comparison():
    p = problem()
    unrelated = certificate(p, (Q(2), Q(2)))
    assert isinstance(verify_matrix_certificate(unrelated), Accepted)
    forged = replace(receipt(p), certificate=unrelated, value=Q(4), defect=(Q(2), Q(2))).refresh_digest()
    assert not verify_policy_evaluation(p, forged)
    broken = replace(receipt(p), certificate=replace(certificate(p), dual=(Q(0), Q(0)))).refresh_digest()
    assert not verify_policy_evaluation(p, broken)
    changed = replace(p, comparison_domain=replace(p.comparison_domain,
                                                 restrictions=(((Q(2), Q(0)), (Q(0), Q(2))),
                                                               ((Q(2), Q(0)), (Q(0), Q(2))))))
    # The substituted input may also violate its gauge law; either way the old
    # output is never promoted to a receipt for the actual changed problem.
    assert not verify_policy_evaluation(changed, receipt(p))


def test_nonunique_l1_optimal_residuals_remain_distinct_valid_evidence():
    p = problem()
    one = receipt(p)
    another = adapt_policy_observer(p).evaluate(0, certificate(p, alpha=(Q(1),)))
    assert another.value == one.value
    assert another.certificate.residual != one.certificate.residual
    assert verify_policy_evaluation(p, another)


def test_group_alone_does_not_determine_repairs_norm_or_terminal_status():
    p = problem()
    all_repairs = replace(p, repair=replace(p.repair, map=((Q(1),), (Q(1),))))
    exact = adapt_policy_observer(all_repairs).evaluate(0, certificate(all_repairs, alpha=(Q(1),), dual=(Q(0), Q(0))))
    assert p.gauge_group == all_repairs.gauge_group
    assert exact.value == 0 and receipt(p).value == 2
    norm = replace(p, norm_weights=(Q(2), Q(2)))
    scaled = adapt_policy_observer(norm).evaluate(0, certificate(norm, dual=(Q(2), Q(2))))
    assert norm.gauge_group == p.gauge_group and norm.repair == p.repair
    assert scaled.value == 4


def test_all_gauge_hypotheses_have_concrete_failed_instances():
    p = problem()
    g = p.gauge_group[1]
    bad_actions = (
        replace(g, states=(0, 0)),
        replace(g, defects=SignedPermutation.identity(2)),
        replace(g, repairs=SignedPermutation.identity(1)),
    )
    for bad in bad_actions:
        with pytest.raises(ValueError):
            adapt_policy_observer(replace(p, gauge_group=(p.gauge_group[0], bad)))
    with pytest.raises(ValueError):
        adapt_policy_observer(replace(p, gauge_group=(g,)))
    swap_coordinates = replace(g, states=(0, 1), comparisons=(0, 1),
                               defects=SignedPermutation((1, 0), (1, 1)))
    with pytest.raises(ValueError):
        adapt_policy_observer(replace(p, gauge_group=(p.gauge_group[0], swap_coordinates),
                                     norm_weights=(Q(1), Q(2))))
    zero = replace(p, carrier=replace(p.carrier, values=((Q(0), Q(0)), (Q(0), Q(0)))),
                   repair=PolicyRepairOperator((), ((), ())))
    identity = PolicyGaugeAction.identity(2, 2, 2, 0)
    x = replace(identity, defects=SignedPermutation((0, 1), (-1, 1)))
    y = replace(identity, defects=SignedPermutation((0, 1), (1, -1)))
    with pytest.raises(ValueError, match="composition closure"):
        adapt_policy_observer(replace(zero, gauge_group=(identity, x, y)))


def test_each_required_typed_field_refuses_missing_or_false_semantics():
    p = problem()
    bad = (
        replace(p, carrier=replace(p.carrier, names=("a", "a"))),
        replace(p, carrier=replace(p.carrier, values=((0, Q(0)), (Q(1), Q(1))))),
        replace(p, comparison_domain=replace(p.comparison_domain, restrictions=())),
        replace(p, comparison_domain=replace(p.comparison_domain, pairs=((0, True), (1, 0)))),
        replace(p, repair=replace(p.repair, map=((), (Q(-1),)))),
        replace(p, norm_weights=(Q(0), Q(1))),
        replace(p, terminal_rules=replace(p.terminal_rules, tolerance=Q(-1))),
        replace(p, terminal_rules=replace(p.terminal_rules, permitted_statuses=frozenset())),
        replace(p, source="looks like a source tag"),
    )
    for malformed in bad:
        with pytest.raises(ValueError):
            adapt_policy_observer(malformed)


def test_nonlinear_repair_set_and_seminorm_do_not_gain_quotient_exactness_laws():
    repair_set = (Q(0), Q(1))
    def distance(x):
        return min(representative_mass((x-a,)) for a in repair_set)
    assert Q(0)-Q(-1) in repair_set
    assert distance(Q(0)) == 0 and distance(Q(-1)) == 1
    # Mere nonnegativity does not separate nonzero cochains from zero.
    defect, seminorm_weights = (Q(0), Q(1)), (Q(1), Q(0))
    assert any(defect) and representative_mass(defect, seminorm_weights) == 0
