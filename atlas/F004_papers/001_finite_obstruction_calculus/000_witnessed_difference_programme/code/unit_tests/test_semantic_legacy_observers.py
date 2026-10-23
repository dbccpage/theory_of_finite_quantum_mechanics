import json
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path

import pytest
from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.context_reflection import ContextSystem
from witnessed_difference.observer import (
    OperationalObserverPacket,
    QuotientObserver,
    RetentionPacket,
)
from witnessed_difference.obstruction import MatrixQuotientCertificate
from witnessed_difference.outcomes import Accepted
from witnessed_difference.quantum_measurement_replay import (
    FiniteInstrumentModel,
    FinitePositiveMixture,
    GaussianRational,
    exact_matrix,
)
from witnessed_difference.quotient_observer import (
    LinearQuotientObserver,
    make_linear_quotient_observer,
)
from witnessed_difference.semantic_legacy_observers import (
    FiniteEvaluator,
    Memory,
    Presentation,
    SourceCustody,
    adapt_linear,
    adapt_operational,
    adapt_quantum,
    adapt_quotient,
    adapt_report_context,
    attach_evaluator,
    attach_memory,
    self_report,
)


def custody():
    return SourceCustody("retained-source.md", "a"*64, ("historical receipt",), ("source authorized tag",))


def contexts():
    return ContextSystem((0,1), ((0,),(1,)), 1)


def presentation():
    return Presentation(("s0","s1"),("r0","r1"),(0,1),contexts())


def packet():
    return RetentionPacket(("m0","m1"),("tick",),(("m0","tick","m0"),("m1","tick","m1")),
                           (("m0","r0"),("m1","r1")),(("r0","r0"),("r1","r1")))


def cert(value):
    return MatrixQuotientCertificate(((Q(0),),),1,(Q(value),),(Q(1),),(Q(0),),(Q(value),),Q(value),(Q(int(value>0)),))


def test_quotient_and_context_maps_do_not_invent_missing_layers():
    source=QuotientObserver(("s0","s1"),(frozenset({"s0","s1"}),),"comparison label")
    adapted=adapt_quotient(source,custody())
    assert adapted.presentation.q == (0,0)
    assert adapted.presentation.contexts is None
    assert adapted.memory is adapted.policy is adapted.evaluator is None
    assert adapted.custody.source_authority_tags == custody().source_authority_tags
    blind=adapt_report_context(Presentation(("s0","s1"),("one",),(0,0),contexts()),custody())
    assert not blind.presentation.contexts.related(0,1)
    assert blind.presentation.q == (0,0)
    with pytest.raises(ValueError):
        Presentation(("s0","s1"),("r",),(0,),contexts())


def test_memory_requires_total_functional_updates_and_explicit_reaccess_bridge():
    detached=Memory(packet())
    with pytest.raises(ValueError):
        detached.reaccess(0)
    with pytest.raises(ValueError):
        attach_memory(adapt_report_context(presentation(),custody()),detached)
    linked=Memory(packet(),("m0","m1"),("r0","r1"))
    assert linked.reaccess(1)=="r1"
    with pytest.raises(ValueError):
        Memory(packet(),("m0","m0"),("r0","r1"))
    with pytest.raises(ValueError):
        Memory(replace(packet(), update_map=packet().update_map[:1]))


def test_operational_packet_preserves_start_and_rejects_erased_transition():
    source=OperationalObserverPacket(("s0","s1"),"s1",("tick",),
        (("s0","tick","s1"),("s1","tick","s0")),(("s0","same"),("s1","same")),(("s0","p0"),("s1","p1")))
    adapted=adapt_operational(source,custody())
    assert adapted.operational.start_state=="s1"
    assert adapted.presentation.contexts.transitions==((1,),(0,))
    assert adapted.presentation.q==(0,0)
    assert adapted.memory is adapted.policy is None
    with pytest.raises(ValueError):
        adapt_operational(replace(source,transitions=source.transitions[:1]),custody())


def test_actual_evaluator_maps_certificates_transform_and_terminalizer():
    base=adapt_report_context(presentation(),custody())
    evaluator=FiniteEvaluator(contexts(),(cert(0),cert(2)),((0,1),),Q(1))
    low=attach_evaluator(base,evaluator)
    high=attach_evaluator(base,replace(evaluator,tolerance=Q(3)),("Emit","RequestData"))
    assert low.evaluator.status(1)=="AboveTolerance"
    assert high.evaluator.status(1)=="WithinTolerance"
    assert low.evaluator.certificates[1].value==high.evaluator.certificates[1].value
    assert low.policy is None
    with pytest.raises(ValueError):
        replace(evaluator,transforms=((1,0),))
    with pytest.raises(ValueError):
        replace(evaluator,certificates=(cert(0),replace(cert(2),value=Q(0))))
    with pytest.raises(ValueError):
        attach_evaluator(base,evaluator,("Emit",))


def test_linear_adapter_rechecks_actual_annihilation_not_names_or_receipt_tags():
    complex_=FiniteComplex((0,1,2),((0,1),(1,2),(0,2)))
    outcome=make_linear_quotient_observer(complex_,((1,1,-1),))
    assert isinstance(outcome,Accepted)
    adapted=adapt_linear(outcome.value,custody())
    assert adapted.linear.report_rows==((Q(1),Q(1),Q(-1)),)
    assert adapted.memory is adapted.policy is None
    with pytest.raises(ValueError):
        adapt_linear(LinearQuotientObserver(complex_,((Q(1),Q(0),Q(0)),)),custody())


def test_quantum_adapter_retains_density_and_instrument_outcome_semantics():
    instrument=FiniteInstrumentModel(2,((exact_matrix(((1,0),(0,1))),),))
    mixture=FinitePositiveMixture(((Q(1),(GaussianRational(Q(1)),GaussianRational(Q(0)))),))
    adapted=adapt_quantum(instrument,mixture,custody())
    assert adapted.quantum[3][0].probability==1
    assert adapted.quantum[3][0].post_state==mixture.density(2)
    assert adapted.memory is adapted.policy is adapted.evaluator is None
    with pytest.raises(ValueError):
        adapt_quantum(instrument,FinitePositiveMixture(((Q(2),(GaussianRational(Q(1)),GaussianRational(Q(0)))),)),custody())


def test_self_target_requires_same_owner_component_and_decoded_reaccess():
    adapted=attach_memory(adapt_report_context(presentation(),custody()),Memory(packet(),("m0","m1"),("r0","r1")))
    assert self_report(adapted,custody(),1,"m1",{"r0":0,"r1":1})==(1,"r1",1)
    with pytest.raises(ValueError):
        self_report(adapted,custody(),1,"m0",{"r0":0,"r1":1})
    with pytest.raises(ValueError):
        self_report(adapted,replace(custody(),path="other.md"),0,"m0",{"r0":0,"r1":1})
    with pytest.raises(ValueError):
        self_report(adapt_report_context(presentation(),custody()),custody(),0,"m0",{"r0":0})


def test_inventory_covers_every_manifest_occurrence_and_protects_missing_vocabulary():
    paper=Path(__file__).resolve().parents[2]
    inventory=json.loads((paper/"docs/legacy_observer_inventory.json").read_text(encoding="utf-8"))
    source=json.loads((paper/"source_provenance.json").read_text(encoding="utf-8"))
    assert len(inventory["original_files"])==len(source["files"])==44
    assert len(inventory["absorbed_snapshots"])==len(source["absorbed_snapshots"])==15
    for recorded, observed in zip(source["absorbed_snapshots"],inventory["absorbed_snapshots"],strict=True):
        assert recorded["id"]==observed["id"]
        assert [(f["path"],f["sha256"]) for f in recorded["files"]]==[(f["recorded_path"],f["recorded_sha256"]) for f in observed["files"]]
        assert all(f["recorded_git_object"]["matches_recorded_bytes"] for f in observed["files"])
    genesis=next(f for f in inventory["identified_families"] if f["family"]=="six-component genesis")
    assert genesis["fields"] == ["M", "U", "p", "rho", "G", "T"]
    assert inventory["https_original_recovery"]["original_exact_count"] == 44
    assert all(f["https_source_recovery"]["exact_match"] for f in inventory["original_files"])
