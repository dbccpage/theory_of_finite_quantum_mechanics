from fractions import Fraction

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import (
    DiagnosticClass,
    degree_one_window,
    evaluation_preorder,
    obstruction_signature,
    promote_diagnostic,
    verify_quotient_certificate,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.quotient_observer import (
    check_passivity,
    grammar_resolution,
    make_linear_quotient_observer,
    quotient_observer_layers,
)
from witnessed_difference.receipts import make_receipt, verify_receipt
from witnessed_difference.simplicial import from_facets

HALF_FILLED = FiniteComplex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2)), ((0, 1, 2),))
OPEN_CYCLE = (0, 0, 1, -1, 1)
CASES = {
    "exact": (1, 1, 1, 3, 2),
    "closed_residual": (0, 0, 1, 0, 0),
    "active": (1, 1, 0, 0, 0),
}


def _value(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def test_window_signature_certificate_observer_and_firewall_pipeline() -> None:
    order = _value(evaluation_preorder(tuple(CASES), (("exact", "closed_residual"), ("closed_residual", "active"))))
    assert ("exact", "active") in order
    window = _value(degree_one_window(HALF_FILLED))
    assert all(entry == 0 for row in window.composite for entry in row)
    observer = _value(make_linear_quotient_observer(HALF_FILLED, (OPEN_CYCLE,)))
    assert _value(quotient_observer_layers(observer, ("presentation", "evaluator"))).layers == (
        "presentation",
        "evaluator",
    )
    classes = {}
    for name, values in CASES.items():
        cochain = dict(zip(HALF_FILLED.edges, values))
        signature = _value(obstruction_signature(HALF_FILLED, cochain, closure_declared=True))
        assert _value(verify_quotient_certificate(signature.certificate)) == signature.certificate
        assert signature.gamma2 <= signature.d1_opnorm * signature.phi1
        passivity = _value(check_passivity(observer, cochain))
        assert passivity.phi1 == signature.phi1 and passivity.observer_norm <= signature.phi1
        for target in ("ExactRepair", "StabilizedSurvivor", "OpenObstruction", "authority"):
            refusal = promote_diagnostic(signature, target)
            assert isinstance(refusal, Refused) and refusal.code is RefusalCode.SCOPE_VIOLATION
        classes[name] = signature.diagnostic_class
        inputs = {"case": name, "cochain": tuple(Fraction(value) for value in values)}
        output = {"phi1": signature.phi1, "gamma2": signature.gamma2, "class": signature.diagnostic_class}
        receipt = _value(make_receipt("degree-one-obstruction", inputs, output, ("WDP-CH04-P04", "WDP-CH10-P01")))
        assert _value(verify_receipt(receipt, inputs, output)) is True
        assert receipt.authority_effect is AuthorityEffect.NONE
    assert classes == {
        "exact": DiagnosticClass.EXACT_CLASS,
        "closed_residual": DiagnosticClass.CLOSED_RESIDUAL,
        "active": DiagnosticClass.ACTIVE_CLOSURE_FAILURE,
    }
    grammar = _value(grammar_resolution(tuple(CASES), {name: cls.value[:1] for name, cls in classes.items()}, ("e", "c", "a")))
    assert grammar.visible_classes == 3 and grammar.collision is None


def test_undeclared_closure_stops_the_pipeline_before_classification() -> None:
    cochain = dict(zip(HALF_FILLED.edges, CASES["active"]))
    outcome = obstruction_signature(HALF_FILLED, cochain, closure_declared=False)
    assert isinstance(outcome, Refused) and outcome.code is RefusalCode.NO_RULE
    layers = quotient_observer_layers(_value(make_linear_quotient_observer(HALF_FILLED, (OPEN_CYCLE,))), ("authority",))
    assert isinstance(layers, Refused) and layers.code is RefusalCode.SCOPE_VIOLATION


def test_graph_window_and_simplicial_branch_agree_on_every_class() -> None:
    oriented = _value(from_facets((0, 1, 2, 3), ((0, 1, 2), (2, 3), (0, 3))))
    for values in CASES.values():
        cochain = dict(zip(HALF_FILLED.edges, values))
        graph = _value(obstruction_signature(HALF_FILLED, cochain, closure_declared=True))
        branch = _value(oriented.degree_k_signature(1, {edge: cochain[edge] for edge in oriented.k_simplices(1)}))
        assert (branch.phi, branch.gamma, branch.diagnostic_class) == (
            graph.phi1,
            graph.gamma2,
            graph.diagnostic_class,
        )
# Executable finite evidence; AuthorityEffect: None.
