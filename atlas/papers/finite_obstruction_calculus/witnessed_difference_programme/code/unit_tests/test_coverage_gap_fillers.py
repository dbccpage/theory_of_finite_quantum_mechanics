"""Targeted unit tests covering edge validation paths, exception triggers, and branch conditions across witnessed_difference modules."""

from fractions import Fraction
import pytest

from witnessed_difference.cochains import _edge_value, _validate_cochain
from witnessed_difference.context_reflection import ContextHom, ContextSystem
from witnessed_difference.duration import ClockProfile, Occurrence, check_clock
from witnessed_difference.empirical_repair import Scenario, iid_l1_failure, sampling_tolerance

Q = Fraction
from witnessed_difference.finite_adequacy import BooleanEventValuation
from witnessed_difference.finite_observer_adapter_completeness import (
    DescentError,
    Operation,
    Structure,
    descend,
)
from witnessed_difference.finite_observer_descent import FiniteConstrainedSite
from witnessed_difference.finite_routing import Refusal, guarded_edit, terminalize
from witnessed_difference.ground import triangle_identity
from witnessed_difference.observer_world_adapter import FiniteObserverWorld
from witnessed_difference.obstruction import FiniteComplex
from witnessed_difference.proposal_admission_bridge import (
    DecisionTable,
    DeclaredTransitions,
    Occurrence as ProposalOccurrence,
    ReplayReceipt,
    decision_decoder,
    joint_commit_table,
    replay,
)
from witnessed_difference.quantum_measurement_replay import (
    FiniteInstrumentModel,
    FinitePositiveMixture,
    GaussianRational,
    is_outcome_repeatable,
    outcome_record,
)
from witnessed_difference.relational_retention import (
    RelationalModel,
    bounded_traces,
    is_bisimulation,
)
from witnessed_difference.semantic_legacy_observers import (
    SourceCustody,
)
from witnessed_difference.vector_obstruction import (
    VectorObstruction,
)


def test_cochains_coverage():
    with pytest.raises(ValueError, match="missing cochain value"):
        _edge_value({("a", "b"): Fraction(1)}, "x", "y")

    complex_ = FiniteComplex(vertices=("a", "b"), edges=(("a", "b"),), faces=())
    with pytest.raises(ValueError, match="cochain keys must be oriented edge pairs"):
        _validate_cochain(complex_, {"not_tuple": 1})


def test_context_reflection_coverage():
    with pytest.raises(ValueError, match="invalid finite carrier"):
        ContextSystem(profiles=(), transitions=(), contexts=0)

    with pytest.raises(TypeError, match="profile identifiers must be integers"):
        ContextSystem(profiles=("not_int",), transitions=((0,),), contexts=1)

    with pytest.raises(ValueError, match="transition shape mismatch"):
        ContextSystem(profiles=(0,), transitions=(), contexts=1)

    cs1 = ContextSystem(profiles=(0,), transitions=((0,),), contexts=1)
    cs2 = ContextSystem(profiles=(0,), transitions=((0, 0),), contexts=2)
    with pytest.raises(ValueError, match="context vocabularies differ"):
        ContextHom(source=cs1, target=cs2, mapping=(0,))


def test_duration_coverage():
    with pytest.raises(ValueError, match="occurrence labels must be hashable"):
        Occurrence(label={}, index=0)

    cp = ClockProfile(
        unit="s",
        denominator=1,
        covered_occurrences=frozenset({0}),
        required_occurrences=frozenset({0}),
        coupling_verified="not_bool",
    )
    res = check_clock(cp)
    assert res.detail == "clock coupling flag must be boolean"


def test_empirical_repair_coverage():
    with pytest.raises(ValueError, match="invalid finite scenario"):
        Scenario(measurements=0, outcomes=2, contexts=((0,),))

    with pytest.raises(ValueError, match="contexts must be increasing"):
        Scenario(measurements=2, outcomes=2, contexts=((1, 0),))

    with pytest.raises(ValueError, match="declared section budget exhausted"):
        Scenario(measurements=2, outcomes=10, max_sections=5, contexts=((0,),))

    with pytest.raises(ValueError, match="declared section budget exhausted"):
        Scenario(measurements=2, outcomes=2, max_sections=1, contexts=((0,), (1,)))

    with pytest.raises(ValueError, match="positive exact radius"):
        iid_l1_failure(trials=0, outcomes=2, radius=Q(1))

    sc = Scenario(measurements=1, outcomes=2, contexts=((0,),))
    with pytest.raises(ValueError, match="one actual nonempty run list"):
        sampling_tolerance(sc, runs=[], radii=[Q(1)])


def test_finite_adequacy_coverage():
    with pytest.raises(ValueError, match="event masks must belong"):
        BooleanEventValuation(size=1, events=(-1,), values=(Q(0),))

    bv = BooleanEventValuation(size=1, events=(0, 1), values=(Q(0), Q(1)))
    with pytest.raises(TypeError, match="extension choice must be a Boolean"):
        bv.singleton_extension(choose_last="not_bool")


def test_finite_observer_adapter_completeness_coverage():
    s = Structure((1,), ())
    with pytest.raises(DescentError, match="invalid sizes"):
        descend(s, (-1,), ((0,),))

    with pytest.raises(DescentError, match="invalid sort map"):
        descend(s, (1, 2), ((0,),))

    s2 = Structure((1,), (Operation((0,), 0, (0,)),))
    descend(s2, (1,), ((0,),))


def test_finite_observer_descent_coverage():
    with pytest.raises(ValueError, match="distinct objects must contain"):
        FiniteConstrainedSite(carrier=frozenset({0}), families=())

    context_0 = frozenset()
    context_1 = frozenset({0})
    report_0 = ()
    report_1 = ((0, 0),)

    site = FiniteConstrainedSite(
        carrier=context_1,
        families=(
            (context_0, (report_0,)),
            (context_1, (report_1,)),
        ),
    )
    with pytest.raises(ValueError, match="target and one local section per context"):
        site.descent_fiber(context_1, (context_1,), (report_1, report_1))

    with pytest.raises(ValueError, match="local sections must be admissible"):
        site.descent_fiber(context_1, (context_1,), (((0, 1),),))


def test_finite_routing_coverage():
    class DummyCert:
        matrix = ()
        columns = 0
        weights = ()

    class DummyBefore:
        certificate = DummyCert()

    assert guarded_edit(DummyBefore(), DummyBefore(), damage_budget="invalid") == Refusal.INVALID_CONTRACT

    assert terminalize(None, None) == Refusal.MISSING_POLICY
    assert terminalize(None, ("Hold",)) == Refusal.MISSING_POLICY


def test_relational_retention_coverage():
    model = RelationalModel(reports=(0,), successors=((frozenset(),),))
    assert not is_bisimulation(model, frozenset({("invalid", 0)}))

    with pytest.raises(ValueError, match="valid state and nonnegative"):
        bounded_traces(model, state=0, depth=-1)

    with pytest.raises(ValueError, match="one labelled successor row"):
        RelationalModel(reports=(0, 1), successors=((frozenset(),),))


def test_proposal_admission_bridge_coverage():
    with pytest.raises(ValueError, match="immutable tables required"):
        DecisionTable(reports=[0], decisions=(True,))

    with pytest.raises(ValueError, match="domain mismatch"):
        DecisionTable(reports=(0, 1), decisions=(True,))

    with pytest.raises(ValueError, match="invalid decision table"):
        decision_decoder("not_table")

    with pytest.raises(ValueError, match="domain mismatch"):
        joint_commit_table((True,), (True, False))

    with pytest.raises(ValueError, match="invalid carrier"):
        DeclaredTransitions(states=0, events=1, rule="r", scope="s", table=())

    with pytest.raises(ValueError, match="declared rule and scope required"):
        DeclaredTransitions(states=1, events=1, rule="", scope="s", table=(0,))

    with pytest.raises(ValueError, match="invalid transition table"):
        DeclaredTransitions(states=1, events=1, rule="r", scope="s", table=())

    dt = DeclaredTransitions(states=1, events=1, rule="r", scope="s", table=(0,))
    with pytest.raises(ValueError, match="invalid declaration"):
        ReplayReceipt(declaration="not_decl", initial=0, events=(), occurrences=(), final=0)

    with pytest.raises(ValueError, match="invalid receipt occurrences"):
        ReplayReceipt(declaration=dt, initial=0, events=(), occurrences=("not_occ",), final=0)

    with pytest.raises(ValueError, match="occurrence outside declared domain"):
        ReplayReceipt(
            declaration=dt,
            initial=0,
            events=(),
            occurrences=(ProposalOccurrence(index=0, event=5, before=0, after=0),),
            final=0,
        )

    with pytest.raises(ValueError, match="receipt event outside declared domain"):
        ReplayReceipt(declaration=dt, initial=0, events=(5,), occurrences=(), final=0)

    with pytest.raises(ValueError, match="invalid replay input"):
        replay(dt, initial=-1, events=())


def test_quantum_measurement_replay_coverage():
    with pytest.raises(ValueError, match="positive finite dimension"):
        FiniteInstrumentModel(dimension=0, groups=())

    g1 = ((("not_tuple",),),)
    with pytest.raises(ValueError, match="Kraus groups must be immutable tuples"):
        FiniteInstrumentModel(dimension=1, groups=(["not_tuple"],))

    with pytest.raises(ValueError, match="Kraus operator has wrong exact square shape"):
        FiniteInstrumentModel(dimension=1, groups=g1)

    with pytest.raises(ValueError, match="nonempty immutable positive mixture required"):
        FinitePositiveMixture(components=()).density(1)

    mix_invalid = ((Fraction(-1), (GaussianRational(1, 0),)),)
    with pytest.raises(ValueError, match="mixture weight/vector is invalid"):
        FinitePositiveMixture(components=mix_invalid).density(1)

    with pytest.raises(ValueError, match="instrument/state/outcome does not bind"):
        outcome_record("invalid", "invalid", 0)

    with pytest.raises(ValueError, match="validated square instrument required"):
        is_outcome_repeatable("invalid")


def test_observer_world_adapter_coverage():
    with pytest.raises(ValueError, match="invalid finite world labels"):
        FiniteObserverWorld(
            alphabet=("",),
            profiles=("p",),
            contexts=("c",),
            grammar=("g",),
            histories=((0,),),
            presented_profiles=(0,),
            context_actions=((0,),),
            witnesses=(),
        )

    with pytest.raises(ValueError, match="invalid history carrier"):
        FiniteObserverWorld(
            alphabet=("a",),
            profiles=("p",),
            contexts=("c",),
            grammar=("g",),
            histories=(),
            presented_profiles=(),
            context_actions=(),
            witnesses=(),
        )

    with pytest.raises(ValueError, match="invalid witness tuple"):
        FiniteObserverWorld(
            alphabet=("a",),
            profiles=("p",),
            contexts=("c",),
            grammar=("g",),
            histories=((0,),),
            presented_profiles=(0,),
            context_actions=((0,),),
            witnesses=((0, 0),),
        )

    with pytest.raises(ValueError, match="world receipt is not bound"):
        fow = FiniteObserverWorld(
            alphabet=("a",),
            profiles=("p",),
            contexts=("c",),
            grammar=("g",),
            histories=((0,),),
            presented_profiles=(0,),
            context_actions=((0,),),
            witnesses=(),
        )
        fow.verify_against("invalid_source")


def test_semantic_legacy_observers_coverage():
    with pytest.raises(ValueError, match="source identity required"):
        SourceCustody(
            path="",
            recorded_sha256="a" * 64,
        )

    with pytest.raises(ValueError, match="source digest must be a SHA256 spelling"):
        SourceCustody(
            path="path",
            recorded_sha256="invalid",
        )


def test_vector_obstruction_coverage():
    from witnessed_difference.vector_obstruction import _sqrt_six_decimals
    with pytest.raises(ValueError, match="a squared norm cannot be negative"):
        _sqrt_six_decimals(Fraction(-1))


def test_ground_coverage():
    with pytest.raises(ValueError, match="triangle_identity requires a binary-labelled carrier"):
        triangle_identity(1, 2, 3)


def test_projective_coverage_more():
    from witnessed_difference.projective import ProjectiveRepresentation
    with pytest.raises(ValueError, match="the product table must be total"):
        ProjectiveRepresentation(elements=("g",), product="not_map", matrices={})

    with pytest.raises(ValueError, match="every element needs exactly one"):
        ProjectiveRepresentation(elements=("g",), product={("g", "g"): "g"}, matrices="not_map")


def test_histories_coverage_more():
    from witnessed_difference.histories import FiniteHistoryGraph, WeightedEdge
    with pytest.raises(ValueError, match="history edge source must be a named vertex"):
        WeightedEdge(source="", target="b", weight=Fraction(1))

    with pytest.raises(ValueError, match="history edge target must be a named vertex"):
        WeightedEdge(source="a", target="", weight=Fraction(1))

    with pytest.raises(ValueError, match="history edges must be WeightedEdge values"):
        FiniteHistoryGraph(vertices=("a",), edges=("not_edge",))


def test_policy_observer_adapter_coverage_more():
    from witnessed_difference.policy_observer_adapter import _wire
    with pytest.raises(ValueError, match="noncanonical policy payload"):
        _wire(1.5)


def test_linear_sensing_presentation_coverage_more():
    from witnessed_difference.linear_sensing_presentation import (
        LinearSensingPresentation,
        LinearSensingQuotient,
    )
    with pytest.raises(ValueError, match="invalid repair dimension"):
        LinearSensingPresentation(report_rows=(), repair_rows=(), repair_columns=-1)

    with pytest.raises(ValueError, match="checked sensing required"):
        LinearSensingQuotient(sensing="not_sensing")


def test_retention_choices_coverage_more():
    from witnessed_difference.retention_choices import RetentionSignature, TypedRetention
    sig = RetentionSignature(states=1, labels=1, reports=1)

    with pytest.raises(ValueError, match="typed function shape mismatch"):
        TypedRetention(signature=sig, updates=(), readouts=(0,), comparison=frozenset())

    with pytest.raises(ValueError, match="update outside memory"):
        TypedRetention(signature=sig, updates=((5,),), readouts=(0,), comparison=frozenset())

    with pytest.raises(ValueError, match="readout outside report alphabet"):
        TypedRetention(signature=sig, updates=((0,),), readouts=(5,), comparison=frozenset())

    with pytest.raises(ValueError, match="comparison outside report alphabet"):
        TypedRetention(signature=sig, updates=((0,),), readouts=(0,), comparison=frozenset({(0, 5)}))


def test_observer_coverage_more():
    from witnessed_difference.observer import (
        RetentionPacket,
        adapt_operational,
        adapt_quotient,
        validate_report_profile_separation,
    )
    assert adapt_quotient("not_quotient", None).detail == "quotient observer has the wrong type"
    assert adapt_operational("not_op", None).detail == "operational observer has the wrong type"
    assert validate_report_profile_separation("not_op").detail == "operational observer has the wrong type"

    with pytest.raises(ValueError, match="reports must cover all memory carrier states"):
        RetentionPacket(
            memory_carrier=("m0", "m1"),
            inputs=("i0",),
            update_map=(("m0", "i0", "m0"), ("m1", "i0", "m1")),
            report_map=(("m0", "r0"),),
            comparison=(),
        )


def test_obstruction_coverage_more():
    from witnessed_difference.obstruction import LinearProgramSolution, verify_standard_lp
    assert not verify_standard_lp("invalid", (), (), None)
    assert not verify_standard_lp((Fraction(1),), ((Fraction(1),),), (Fraction(1),), "not_solution")

