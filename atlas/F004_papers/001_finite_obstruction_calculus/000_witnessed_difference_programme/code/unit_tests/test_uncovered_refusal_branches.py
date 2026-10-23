"""Exercise shipped refusal branches that the happy-path suite does not enter."""

from fractions import Fraction

import pytest

from witnessed_difference.ports import (
    L1Solution,
    ObstructionSolveRequest,
    QuotientCertificate,
    WdpObstructionSolution,
)

from witnessed_difference.ch19_o01_sensor_repair import (
    PARTITION_P,
    _bin_one,
    _frequency,
    bin_context,
)
from witnessed_difference.finite_observer_adapter_completeness import (
    DescentError,
    Structure,
    descend,
)
from witnessed_difference.finite_observer_descent import FiniteConstrainedSite
from witnessed_difference.finite_routing import Refusal, check_lift, guarded_edit, terminalize
from witnessed_difference.native_functionals import (
    FunctionalEvaluationError,
    _unique_fields,
    decode,
    encode,
)
from witnessed_difference.outcomes import RefusalCode
from witnessed_difference.probability import FiniteWitnessSpace, disjoint_additivity
from witnessed_difference.projective import GaussianRational
from witnessed_difference.quantum import (
    CABELLO_CONTEXTS,
    CABELLO_RAYS,
    FiniteMatrixRecovery,
    H017Fin,
    H020,
    IntegerWeights,
    PhaseBlindReadout,
    _unit,
    fixed_scale_phase,
    to_gaussian_rational,
)
from witnessed_difference.quantum_measurement_replay import outcome_record
from witnessed_difference.semantic_legacy_observers import (
    AdaptedObserver,
    Presentation,
    SourceCustody,
    adapt_linear,
    adapt_linear_sensing,
    adapt_operational,
    adapt_quantum,
    adapt_quotient,
    adapt_report_context,
    attach_evaluator,
    attach_memory,
)


def test_shipped_refusal_branches_are_reached():
    with pytest.raises(ValueError, match="sensor alphabet"):
        _bin_one(4, PARTITION_P)
    with pytest.raises(ValueError, match="sensor alphabet"):
        bin_context((4,), PARTITION_P)
    with pytest.raises(ValueError, match="not a section"):
        _frequency(((2,),), ((0,), (1,)))
    with pytest.raises(ValueError, match="at least one"):
        _frequency((), ((0,),))

    with pytest.raises(TypeError):
        encode(1.5)
    with pytest.raises(FunctionalEvaluationError, match="strings"):
        decode(1)
    with pytest.raises(FunctionalEvaluationError, match="invalid native rational"):
        decode("1/0")
    with pytest.raises(FunctionalEvaluationError, match="noncanonical"):
        decode("2/4")
    with pytest.raises(FunctionalEvaluationError, match="duplicate"):
        _unique_fields((("field", 1), ("field", 2)))

    assert check_lift(None, None, None) is Refusal.MISSING_CONTRACT
    assert guarded_edit(None, None, None) is Refusal.MISSING_CONTRACT
    assert terminalize(None, None) is Refusal.MISSING_POLICY
    assert terminalize(None, ("Hold",)) is Refusal.MISSING_POLICY

    assert to_gaussian_rational(1.5) is None
    assert to_gaussian_rational(1.0) == GaussianRational(Fraction(1), Fraction(0))
    assert to_gaussian_rational((1, "bad")) is None
    assert to_gaussian_rational(Fraction(1, 2)) == GaussianRational(Fraction(1, 2), Fraction(0))
    assert to_gaussian_rational(object()) is None
    assert _unit(object(), 1e-12) is False
    assert fixed_scale_phase(True, 1).code is RefusalCode.INVALID_INPUT
    assert fixed_scale_phase(float("nan"), 1.0).code is RefusalCode.INVALID_INPUT
    assert fixed_scale_phase(0, 0).code is RefusalCode.INVALID_INPUT
    assert fixed_scale_phase(0.0, 1.0).value == GaussianRational(Fraction(1), Fraction(0))

    with pytest.raises(ValueError, match="immutable tuple"):
        IntegerWeights([("a", 1)])
    with pytest.raises(ValueError, match="pairs"):
        IntegerWeights((("a",),))
    with pytest.raises(ValueError, match="Invalid amplitude"):
        PhaseBlindReadout.readout((object(),))
    assert PhaseBlindReadout.fiber_relative_phase((1,), (1, 0)) is False
    with pytest.raises(TypeError, match="finite matrix recovery"):
        H017Fin(object())
    with pytest.raises(ValueError, match="square"):
        H017Fin(
            FiniteMatrixRecovery(
                basis_images=((GaussianRational(1),),),
                matrix=((GaussianRational(1), GaussianRational(0)),),
                adjoint=((GaussianRational(1),),),
                other_matrix=((GaussianRational(1),),),
                composition=((GaussianRational(1),),),
            )
        )
    with pytest.raises(ValueError, match="eighteen rays"):
        H020((), CABELLO_CONTEXTS)
    bad_rays = CABELLO_RAYS[:-1] + ((0, 0, 1),)
    with pytest.raises(ValueError, match="four-dimensional"):
        H020(bad_rays, CABELLO_CONTEXTS)
    bad_contexts = CABELLO_CONTEXTS[:-1] + ((0, 1, 2, 99),)
    with pytest.raises(ValueError, match="outside the declared rays"):
        H020(CABELLO_RAYS, bad_contexts)

    space = FiniteWitnessSpace(("a", "b"))
    outside = disjoint_additivity(space, frozenset({"a"}), frozenset({"z"}))
    assert outside.code is RefusalCode.EVENT_OUTSIDE_SPACE

    with pytest.raises(ValueError, match="unique finite"):
        Presentation((), ("report",), ())
    with pytest.raises(ValueError, match="total typed map"):
        Presentation(("state",), ("report",), (2,))

    custody = SourceCustody("declared/path", "a" * 64)
    bare = AdaptedObserver(custody)
    with pytest.raises(ValueError, match="checked quotient"):
        adapt_quotient(object(), custody)
    with pytest.raises(ValueError, match="explicit context"):
        adapt_report_context(Presentation(("state",), ("report",), (0,)), custody)
    with pytest.raises(ValueError, match="typed operational"):
        adapt_operational(object(), custody)
    with pytest.raises(ValueError, match="report-to-memory"):
        attach_memory(bare, object())
    with pytest.raises(ValueError, match="evaluator domain"):
        attach_evaluator(bare, object())
    with pytest.raises(ValueError, match="linear quotient"):
        adapt_linear(object(), custody)
    with pytest.raises(ValueError, match="exact instrument"):
        adapt_quantum(object(), object(), custody)
    with pytest.raises(ValueError, match="linear sensing"):
        adapt_linear_sensing(object(), custody)
    with pytest.raises(ValueError, match="source binding"):
        from witnessed_difference.legacy_six_observer import SixObserver

        SixObserver("not-custody", (), (), (), (), (), (), ())

    with pytest.raises(ValueError, match="instrument/state/outcome"):
        outcome_record(object(), object(), 0)

    with pytest.raises(DescentError, match="invalid sizes"):
        descend(Structure((-1,)), (1,), ((0,),))
    with pytest.raises(DescentError, match="invalid sort map"):
        descend(Structure((1,)), (1,), ())
    with pytest.raises(ValueError, match="empty and full"):
        FiniteConstrainedSite(frozenset({"a"}), ())
    with pytest.raises(ValueError, match="valid and distinct"):
        FiniteConstrainedSite(
            frozenset({"a"}),
            (
                (frozenset(), ((),)),
                (frozenset({"a"}), ((("a", "0"),),)),
                (frozenset({"b"}), ((),)),
            ),
        )


def test_unset_certificate_maps_stay_unset() -> None:
    solution = L1Solution(
        phi1_value=Fraction(1),
        potential=None,
        residual=None,
        dual=None,
        is_exact=False,
    )
    assert solution.potential is None
    assert solution.residual is None
    assert solution.dual is None
    assert solution["phi1"] == Fraction(1)

    request = ObstructionSolveRequest(
        vertices=("a",),
        edges=(("a", "b"),),
        cochain=None,
        weights=None,
    )
    assert request.cochain is None
    assert request.weights is None
    assert request.vertices == ("a",)

    certificate = QuotientCertificate(
        phi1=Fraction(0),
        potential=None,
        residual=None,
        dual_witness=None,
        is_exact=True,
    )
    assert certificate.potential is None
    assert certificate.residual is None
    assert certificate.dual_witness is None

    obstruction = WdpObstructionSolution(
        phi1=Fraction(0),
        is_exact=True,
        potential=None,
        residual=None,
    )
    assert obstruction.potential is None
    assert obstruction.residual is None
    assert obstruction.dual_witness is None
