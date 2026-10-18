from __future__ import annotations

from dataclasses import replace
from inspect import signature

import pytest

from omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge import (
    ActiveObstructionV1,
    BridgeError,
    BridgeProblemV1,
    CECChildPacketV1,
    ClosurePolicy,
    ConservativeExtensionProposal,
    ConservativeExtensionProposalV1,
    ObserverPresentationV1,
    PrimitiveCarrierV1,
    ProfileRowV1,
    RefusalCode,
    RetainedDiffV1,
    RetractionRowV1,
    SameLevelRepair,
    SameLevelRepairCandidateV1,
    SearchExhaustionV1,
    SignatureMapRowV1,
    StateMapRowV1,
    StateRenamingV1,
    TerminalKind,
    TransitionRowV1,
    TypedRefusal,
    active_obstruction_of_components,
    active_obstructions,
    demand_orbits,
    evaluate_cec_child_packet,
    orbit_transition_congruent,
    profile_difference,
    replay_cec_child_packet,
    terminal_kind,
    terminalize_declared_search,
    validate_same_level_repair,
    zero_rel_r,
)


def _identity_transitions(
    signature: tuple[str, ...], states: tuple[str, ...]
) -> tuple[TransitionRowV1, ...]:
    return tuple(
        TransitionRowV1(operation, state, state)
        for operation in signature
        for state in states
    )


def _problem(
    *,
    protected: tuple[tuple[str, str], ...] = (("s0", "s1"),),
    retained: tuple[RetainedDiffV1, ...] | None = None,
    closure_policy: ClosurePolicy = ClosurePolicy.EXPLICIT_PROTECTED_ONLY,
) -> BridgeProblemV1:
    if retained is None:
        retained = (RetainedDiffV1("s0", "s1", "retained:w01"),)
    primitive = PrimitiveCarrierV1(
        carrier_id="carrier:base",
        states=("s0", "s1", "s2"),
        retained_differences=retained,
    )
    observer = ObserverPresentationV1(
        primitive_id=primitive.primitive_id,
        signature_id="signature:base",
        signature=("old:constant",),
        profiles=(
            ProfileRowV1("s0", ("old:constant",)),
            ProfileRowV1("s1", ("old:constant",)),
            ProfileRowV1("s2", ("old:constant",)),
        ),
        transitions=_identity_transitions(("old:constant",), ("s0", "s1", "s2")),
        protected_pairs=protected,
        closure_policy=closure_policy,
    )
    return BridgeProblemV1(primitive, observer)


def _same_level(problem: BridgeProblemV1) -> SameLevelRepairCandidateV1:
    return SameLevelRepairCandidateV1(
        problem_id=problem.problem_id,
        carrier_id=problem.primitive.carrier_id,
        signature_id=problem.observer.signature_id,
        profiles=(
            ProfileRowV1("s0", ()),
            ProfileRowV1("s1", ("old:constant",)),
            ProfileRowV1("s2", ("old:constant",)),
        ),
        resolved_orbit_ids=tuple(orbit.orbit_id for orbit in demand_orbits(problem)),
        producer_id="fixture:same-level",
    )


def _cec_packet(
    problem: BridgeProblemV1,
    *,
    mark_s2: bool = False,
    preserve_retained: bool = True,
    preserve_profile: bool = True,
) -> CECChildPacketV1:
    orbits = demand_orbits(problem)
    state_map = {"s0": "n0", "s1": "n1", "s2": "n2"}
    retained = (
        (RetainedDiffV1("n0", "n1", "retained:w01:transported"),)
        if preserve_retained
        else ()
    )
    child_primitive = PrimitiveCarrierV1(
        carrier_id="carrier:child",
        states=("n0", "n1", "n2", "n3"),
        retained_differences=retained,
    )
    old_feature = ("old:constant",) if preserve_profile else ()
    child_observer = ObserverPresentationV1(
        primitive_id=child_primitive.primitive_id,
        signature_id="signature:child",
        signature=("new:mark", "old:constant"),
        profiles=(
            ProfileRowV1("n0", old_feature),
            ProfileRowV1("n1", tuple(sorted((*old_feature, "new:mark")))),
            ProfileRowV1(
                "n2",
                tuple(sorted((*old_feature, *(("new:mark",) if mark_s2 else ())))),
            ),
            ProfileRowV1("n3", ()),
        ),
        transitions=_identity_transitions(
            ("new:mark", "old:constant"), ("n0", "n1", "n2", "n3")
        ),
        protected_pairs=(("n0", "n1"),),
        closure_policy=ClosurePolicy.EXPLICIT_PROTECTED_ONLY,
    )
    proposal = ConservativeExtensionProposalV1(
        parent_problem_id=problem.problem_id,
        child_primitive=child_primitive,
        child_observer=child_observer,
        state_embedding=tuple(
            StateMapRowV1(old, new) for old, new in state_map.items()
        ),
        state_retraction=(
            RetractionRowV1("n0", "s0"),
            RetractionRowV1("n1", "s1"),
            RetractionRowV1("n2", "s2"),
            RetractionRowV1("n3", "s2"),
        ),
        signature_embedding=(SignatureMapRowV1("old:constant", "old:constant"),),
        signature_retraction=(
            RetractionRowV1("new:mark", "old:constant"),
            RetractionRowV1("old:constant", "old:constant"),
        ),
        resolved_orbit_ids=tuple(orbit.orbit_id for orbit in orbits),
        producer_id="fixture:cec:b" if mark_s2 else "fixture:cec:a",
    )
    return CECChildPacketV1(problem, orbits, proposal)


def _complete(
    same_level: tuple[SameLevelRepairCandidateV1, ...] = (),
    cec: tuple[CECChildPacketV1, ...] = (),
) -> SearchExhaustionV1:
    return SearchExhaustionV1(
        same_level_declared_complete=True,
        cec_declared_complete=True,
        same_level_candidate_ids=tuple(
            candidate.candidate_id for candidate in same_level
        ),
        cec_packet_ids=tuple(packet.packet_id for packet in cec),
    )


def test_retained_collapsed_protected_implies_active_obstruction() -> None:
    problem = _problem()
    pair = ("s0", "s1")
    assert zero_rel_r(problem, pair)
    difference = profile_difference(problem, pair)
    assert difference.is_zero
    obstruction = active_obstruction_of_components(problem, pair)
    assert type(obstruction) is ActiveObstructionV1
    assert obstruction.pair == pair
    assert obstruction.profile_difference == difference
    assert obstruction.authority_effect == "None"
    with pytest.raises(BridgeError):
        replace(obstruction, authority_effect="Minted")


def test_collapsed_unprotected_pair_is_not_an_obstruction() -> None:
    problem = _problem(protected=())
    assert zero_rel_r(problem, ("s0", "s1"))
    assert active_obstruction_of_components(problem, ("s0", "s1")) is None
    assert active_obstructions(problem) == ()


def test_all_pairs_is_an_external_closure_policy_not_a_collapse_theorem() -> None:
    explicit = _problem(protected=())
    external = _problem(protected=(), closure_policy=ClosurePolicy.EXTERNAL_ALL_PAIRS)
    assert active_obstructions(explicit) == ()
    obstruction = active_obstruction_of_components(external, ("s0", "s1"))
    assert obstruction is not None
    assert obstruction.protected_by == "external-all-pairs-closure-policy"


def test_retention_is_independent_and_required() -> None:
    problem = _problem(retained=())
    assert zero_rel_r(problem, ("s0", "s1"))
    assert ("s0", "s1") in problem.observer.protected_pairs
    assert active_obstruction_of_components(problem, ("s0", "s1")) is None


def test_same_level_repair_cannot_change_carrier_or_signature() -> None:
    problem = _problem()
    candidate = _same_level(problem)
    orbits = demand_orbits(problem)
    assert validate_same_level_repair(problem, candidate, orbits)
    assert not validate_same_level_repair(
        problem, replace(candidate, carrier_id="carrier:forged"), orbits
    )
    assert not validate_same_level_repair(
        problem, replace(candidate, signature_id="signature:forged"), orbits
    )


def test_same_level_repair_must_resolve_the_whole_orbit() -> None:
    problem = _problem()
    candidate = _same_level(problem)
    assert not validate_same_level_repair(
        problem,
        replace(candidate, profiles=problem.observer.profiles),
        demand_orbits(problem),
    )


def test_cec_child_packet_accepts_new_structure_and_replays() -> None:
    packet = _cec_packet(_problem())
    receipt = evaluate_cec_child_packet(packet)
    assert receipt.accepted
    assert all(value for _, value in receipt.checks)
    assert replay_cec_child_packet(packet, receipt)


def test_signature_only_cec_is_a_real_extension_not_a_same_level_move() -> None:
    problem = _problem()
    orbits = demand_orbits(problem)
    child_observer = ObserverPresentationV1(
        primitive_id=problem.primitive.primitive_id,
        signature_id="signature:child",
        signature=("new:mark", "old:constant"),
        profiles=(
            ProfileRowV1("s0", ("old:constant",)),
            ProfileRowV1("s1", ("new:mark", "old:constant")),
            ProfileRowV1("s2", ("old:constant",)),
        ),
        transitions=_identity_transitions(
            ("new:mark", "old:constant"), ("s0", "s1", "s2")
        ),
        protected_pairs=problem.observer.protected_pairs,
    )
    proposal = ConservativeExtensionProposalV1(
        parent_problem_id=problem.problem_id,
        child_primitive=problem.primitive,
        child_observer=child_observer,
        state_embedding=tuple(
            StateMapRowV1(state, state) for state in problem.primitive.states
        ),
        state_retraction=tuple(
            RetractionRowV1(state, state) for state in problem.primitive.states
        ),
        signature_embedding=(SignatureMapRowV1("old:constant", "old:constant"),),
        signature_retraction=(
            RetractionRowV1("new:mark", "old:constant"),
            RetractionRowV1("old:constant", "old:constant"),
        ),
        resolved_orbit_ids=tuple(orbit.orbit_id for orbit in orbits),
        producer_id="fixture:signature-only-cec",
    )
    packet = CECChildPacketV1(problem, orbits, proposal)
    receipt = evaluate_cec_child_packet(packet)
    assert receipt.accepted
    checks = dict(receipt.checks)
    assert checks["new_ids"]
    assert checks["genuinely_new_structure"]


def test_cec_refuses_missing_retention_or_profile_preservation() -> None:
    no_retention = _cec_packet(_problem(), preserve_retained=False)
    no_profile = _cec_packet(_problem(), preserve_profile=False)
    assert not evaluate_cec_child_packet(no_retention).accepted
    assert not evaluate_cec_child_packet(no_profile).accepted


def test_cec_refuses_a_noncommuting_old_transition() -> None:
    packet = _cec_packet(_problem())
    rows = list(packet.proposal.child_observer.transitions)
    index = rows.index(TransitionRowV1("old:constant", "n0", "n0"))
    rows[index] = TransitionRowV1("old:constant", "n0", "n1")
    observer = replace(packet.proposal.child_observer, transitions=tuple(rows))
    proposal = replace(packet.proposal, child_observer=observer)
    receipt = evaluate_cec_child_packet(replace(packet, proposal=proposal))
    assert not receipt.accepted
    assert dict(receipt.checks)["old_transitions_commute"] is False


def test_cec_preserves_external_all_pairs_policy_demands() -> None:
    problem = _problem(protected=(), closure_policy=ClosurePolicy.EXTERNAL_ALL_PAIRS)
    packet = _cec_packet(problem)
    receipt = evaluate_cec_child_packet(packet)
    assert not receipt.accepted
    assert dict(receipt.checks)["protected_preserved"] is False


def test_cec_requires_genuinely_new_structure_and_new_level_ids() -> None:
    packet = _cec_packet(_problem())
    proposal = packet.proposal
    no_new_state = replace(
        proposal.child_primitive,
        states=("n0", "n1", "n2"),
    )
    no_new_observer = replace(
        proposal.child_observer,
        primitive_id=no_new_state.primitive_id,
        profiles=(
            ProfileRowV1("n0", ("old:constant",)),
            ProfileRowV1("n1", ("old:constant",)),
            ProfileRowV1("n2", ("old:constant",)),
        ),
        signature=("old:constant",),
        transitions=_identity_transitions(("old:constant",), ("n0", "n1", "n2")),
    )
    no_new = replace(
        proposal,
        child_primitive=no_new_state,
        child_observer=no_new_observer,
        state_retraction=proposal.state_retraction[:3],
        signature_retraction=(RetractionRowV1("old:constant", "old:constant"),),
    )
    assert not evaluate_cec_child_packet(replace(packet, proposal=no_new)).accepted
    same_ids = replace(
        proposal,
        child_primitive=replace(
            proposal.child_primitive, carrier_id=packet.parent.primitive.carrier_id
        ),
    )
    same_ids = replace(
        same_ids,
        child_observer=replace(
            same_ids.child_observer,
            primitive_id=same_ids.child_primitive.primitive_id,
            signature_id=packet.parent.observer.signature_id,
        ),
    )
    assert not evaluate_cec_child_packet(replace(packet, proposal=same_ids)).accepted


def test_cec_receipt_tampering_fails_replay() -> None:
    packet = _cec_packet(_problem())
    receipt = evaluate_cec_child_packet(packet)
    object.__setattr__(receipt, "accepted", False)
    assert not replay_cec_child_packet(packet, receipt)


def test_nested_container_mutation_is_a_replayed_refusal() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    packet = _cec_packet(_problem())
    object.__setattr__(
        packet.proposal,
        "state_embedding",
        list(packet.proposal.state_embedding),
    )
    receipt = evaluate_cec_child_packet(packet)
    assert receipt.accepted is False
    assert dict(receipt.checks)["packet_reconstructs"] is False
    assert replay_cec_child_packet(packet, receipt)
    original = bridge._cec_checks
    try:
        bridge._cec_checks = bridge._oracle_cec_checks
        result = terminalize_declared_search(
            packet.parent,
            (),
            (packet,),
            _complete(cec=(packet,)),
        )
        assert type(result) is TypedRefusal
        assert result.code is RefusalCode.NO_ADMISSIBLE_RESPONSE
    finally:
        bridge._cec_checks = original


def test_nested_authority_mutation_is_a_replayed_refusal() -> None:
    packet = _cec_packet(_problem())
    object.__setattr__(packet.proposal.child_primitive, "authority_effect", "Minted")
    object.__setattr__(
        packet.proposal.child_observer,
        "primitive_id",
        packet.proposal.child_primitive.primitive_id,
    )
    object.__setattr__(packet.proposal.child_observer, "authority_effect", "Minted")
    receipt = evaluate_cec_child_packet(packet)
    assert receipt.accepted is False
    assert dict(receipt.checks)["packet_reconstructs"] is False
    assert dict(receipt.checks)["authority_none"] is False
    assert replay_cec_child_packet(packet, receipt)


def test_shared_producer_checker_substitution_cannot_forge_replay() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    packet = _cec_packet(_problem())
    original = bridge._cec_checks
    try:
        bridge._cec_checks = lambda _: (("forged", True),)
        receipt = evaluate_cec_child_packet(packet)
        assert receipt.accepted
        assert not replay_cec_child_packet(packet, receipt)
    finally:
        bridge._cec_checks = original


def test_shared_producer_checker_substitution_cannot_forge_terminal_cec() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    problem = _problem()
    packet = _cec_packet(problem)
    original = bridge._cec_checks
    try:
        bridge._cec_checks = lambda _: (("forged", True),)
        result = terminalize_declared_search(
            problem, (), (packet,), _complete(cec=(packet,))
        )
        assert type(result) is TypedRefusal
        assert result.code is RefusalCode.NO_ADMISSIBLE_RESPONSE
    finally:
        bridge._cec_checks = original


def test_shared_profile_helper_substitution_cannot_forge_cec() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    problem = _problem()
    packet = _cec_packet(problem, preserve_profile=False)
    original = bridge._profiles_by_state

    def forged(rows: tuple[ProfileRowV1, ...]) -> dict[str, tuple[str, ...]]:
        if rows and rows[0].state.startswith("s"):
            return {
                "s0": (),
                "s1": ("old:constant",),
                "s2": (),
            }
        return original(rows)

    try:
        bridge._profiles_by_state = forged
        receipt = evaluate_cec_child_packet(packet)
        assert receipt.accepted
        assert not replay_cec_child_packet(packet, receipt)
        result = terminalize_declared_search(
            problem, (), (packet,), _complete(cec=(packet,))
        )
        assert type(result) is TypedRefusal
        assert result.code is RefusalCode.NO_ADMISSIBLE_RESPONSE
    finally:
        bridge._profiles_by_state = original


def test_shared_profile_helper_substitution_cannot_forge_same_level() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    problem = _problem()
    candidate = replace(
        _same_level(problem),
        profiles=(
            ProfileRowV1("s0", ("old:constant",)),
            ProfileRowV1("s1", ("old:constant",)),
            ProfileRowV1("s2", ()),
        ),
    )
    original = bridge._profiles_by_state

    def forged(rows: tuple[ProfileRowV1, ...]) -> dict[str, tuple[str, ...]]:
        if rows is candidate.profiles:
            return {"s0": (), "s1": ("old:constant",), "s2": ()}
        return original(rows)

    try:
        bridge._profiles_by_state = forged
        assert validate_same_level_repair(problem, candidate, demand_orbits(problem))
        result = terminalize_declared_search(
            problem,
            (candidate,),
            (),
            _complete((candidate,)),
        )
        assert type(result) is TypedRefusal
        assert result.code is RefusalCode.NO_ADMISSIBLE_RESPONSE
    finally:
        bridge._profiles_by_state = original


def test_same_level_producer_failure_is_a_typed_refusal() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    problem = _problem()
    candidate = _same_level(problem)
    original = bridge._profiles_by_state
    try:
        bridge._profiles_by_state = lambda _: (_ for _ in ()).throw(
            RuntimeError("helper unavailable")
        )
        result = terminalize_declared_search(
            problem,
            (candidate,),
            (),
            _complete((candidate,)),
        )
        assert type(result) is TypedRefusal
        assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE
    finally:
        bridge._profiles_by_state = original


def test_cec_cannot_omit_a_canonical_demand_orbit() -> None:
    packet = _cec_packet(_problem())
    forged = replace(
        packet,
        demand_orbits=(),
        proposal=replace(packet.proposal, resolved_orbit_ids=()),
    )
    receipt = evaluate_cec_child_packet(forged)
    assert not receipt.accepted
    assert dict(receipt.checks)["demand_orbits_canonical"] is False


def test_live_orbit_helper_substitution_cannot_make_omission_canonical() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    packet = _cec_packet(_problem())
    forged = replace(
        packet,
        demand_orbits=(),
        proposal=replace(packet.proposal, resolved_orbit_ids=()),
    )
    original = bridge.demand_orbits
    try:
        bridge.demand_orbits = lambda _: ()
        receipt = evaluate_cec_child_packet(forged)
        assert receipt.accepted
        assert not replay_cec_child_packet(forged, receipt)
    finally:
        bridge.demand_orbits = original


def test_orbit_transport_preserves_policy_and_replays_renaming() -> None:
    source = _problem(closure_policy=ClosurePolicy.EXPLICIT_PROTECTED_ONLY)
    target = _problem(closure_policy=ClosurePolicy.EXTERNAL_ALL_PAIRS)
    renaming = StateRenamingV1(
        source.problem_id,
        target.problem_id,
        source.primitive.states,
        target.primitive.states,
        target.primitive.states,
    )
    assert orbit_transition_congruent(source, target, renaming) is False

    identity = StateRenamingV1(
        source.problem_id,
        source.problem_id,
        source.primitive.states,
        source.primitive.states,
        source.primitive.states,
    )
    assert orbit_transition_congruent(source, source, identity)
    object.__setattr__(identity, "image", list(identity.image))
    assert orbit_transition_congruent(source, source, identity) is False


def test_inner_automorphism_substitution_cannot_split_a_demand_orbit() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    problem = _problem(
        protected=(),
        retained=(
            RetainedDiffV1("s0", "s1", "retained:w01"),
            RetainedDiffV1("s0", "s2", "retained:w02"),
            RetainedDiffV1("s1", "s2", "retained:w12"),
        ),
        closure_policy=ClosurePolicy.EXTERNAL_ALL_PAIRS,
    )
    assert tuple(len(orbit.members) for orbit in demand_orbits(problem)) == (3,)
    original = bridge._automorphisms
    try:
        bridge._automorphisms = lambda value: (value.primitive.states,)
        forged_orbits = demand_orbits(problem)
        assert tuple(len(orbit.members) for orbit in forged_orbits) == (1, 1, 1)
        base = _cec_packet(problem)
        proposal = replace(
            base.proposal,
            resolved_orbit_ids=tuple(orbit.orbit_id for orbit in forged_orbits),
        )
        packet = replace(base, demand_orbits=forged_orbits, proposal=proposal)
        receipt = evaluate_cec_child_packet(packet)
        assert receipt.accepted is False
        assert replay_cec_child_packet(packet, receipt) is False
        result = terminalize_declared_search(
            problem,
            (),
            (packet,),
            _complete(cec=(packet,)),
        )
        assert type(result) is TypedRefusal
        assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE
    finally:
        bridge._automorphisms = original


def test_terminal_trichotomy_same_level_branch() -> None:
    problem = _problem()
    repair = _same_level(problem)
    result = terminalize_declared_search(problem, (repair,), (), _complete((repair,)))
    assert type(result) is SameLevelRepair
    assert terminal_kind(result) is TerminalKind.SAME_LEVEL_REPAIR


def test_duplicate_same_level_declarations_deduplicate_total_result() -> None:
    problem = _problem()
    repair = _same_level(problem)
    result = terminalize_declared_search(
        problem,
        (repair, repair),
        (),
        SearchExhaustionV1(False, False, (), ()),
    )
    assert type(result) is SameLevelRepair
    assert result.candidate_ids == (repair.candidate_id,)


def test_terminal_trichotomy_cec_branch_retains_nonunique_lifts() -> None:
    problem = _problem()
    first = _cec_packet(problem, mark_s2=False)
    second = _cec_packet(problem, mark_s2=True)
    result = terminalize_declared_search(
        problem, (), (first, second), _complete(cec=(first, second))
    )
    assert type(result) is ConservativeExtensionProposal
    assert terminal_kind(result) is TerminalKind.CONSERVATIVE_EXTENSION_PROPOSAL
    assert len(result.evaluations) == 2


def test_digest_and_terminal_type_substitution_cannot_change_controller_result() -> (
    None
):
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    original_digest = bridge.domain_digest
    original_same = bridge.SameLevelRepair
    original_refusal = bridge.TypedRefusal
    original_cec = bridge.ConservativeExtensionProposal
    original_code = bridge.RefusalCode
    original_kind = bridge.TerminalKind
    try:
        bridge.domain_digest = lambda *args: "x"
        bridge.SameLevelRepair = lambda ids: ("forged-same", ids)
        bridge.TypedRefusal = lambda code, detail: ("forged-refusal", code, detail)
        bridge.ConservativeExtensionProposal = lambda rows: ("forged-cec", rows)

        class FakeCode:
            NO_ACTIVE_OBSTRUCTION = object()
            INCOMPLETE_SEARCH_EVIDENCE = object()
            NO_ADMISSIBLE_RESPONSE = object()

        bridge.RefusalCode = FakeCode
        bridge.TerminalKind = FakeCode
        problem = _problem()
        first = _cec_packet(problem, mark_s2=False)
        second = _cec_packet(problem, mark_s2=True)
        cec_result = terminalize_declared_search(
            problem,
            (),
            (first, second),
            SearchExhaustionV1(True, False, (), ()),
        )
        assert type(cec_result) is ConservativeExtensionProposal
        assert len(cec_result.evaluations) == 2
        refusal = terminalize_declared_search(problem, [], (), _complete())
        assert type(refusal) is TypedRefusal
        assert type(refusal.code) is RefusalCode
    finally:
        bridge.domain_digest = original_digest
        bridge.SameLevelRepair = original_same
        bridge.TypedRefusal = original_refusal
        bridge.ConservativeExtensionProposal = original_cec
        bridge.RefusalCode = original_code
        bridge.TerminalKind = original_kind
    assert first.proposal.proposal_id != second.proposal.proposal_id


def test_duplicate_cec_packets_do_not_inflate_terminal_branches() -> None:
    problem = _problem()
    packet = _cec_packet(problem)
    result = terminalize_declared_search(
        problem,
        (),
        (packet, packet),
        SearchExhaustionV1(True, False, (), ()),
    )
    assert type(result) is ConservativeExtensionProposal
    assert len(result.evaluations) == 1
    assert result.evaluations[0].proposal_id == packet.proposal.proposal_id


def test_cec_cannot_bypass_same_level_exhaustion() -> None:
    problem = _problem()
    packet = _cec_packet(problem)
    incomplete = SearchExhaustionV1(
        same_level_declared_complete=False,
        cec_declared_complete=False,
        same_level_candidate_ids=(),
        cec_packet_ids=(),
    )
    result = terminalize_declared_search(problem, (), (packet,), incomplete)
    assert type(result) is TypedRefusal
    assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE


def test_same_level_replays_parent_authority_and_candidate_containers() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    problem = _problem()
    candidate = _same_level(problem)
    object.__setattr__(problem.primitive, "authority_effect", "Minted")
    object.__setattr__(
        problem.observer,
        "primitive_id",
        problem.primitive.primitive_id,
    )
    object.__setattr__(candidate, "problem_id", problem.problem_id)
    original = bridge._authority_is_none
    try:
        bridge._authority_is_none = lambda _: True
        result = terminalize_declared_search(
            problem,
            (candidate,),
            (),
            _complete((candidate,)),
        )
        assert type(result) is TypedRefusal
        assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE
    finally:
        bridge._authority_is_none = original

    canonical_problem = _problem()
    malformed_candidate = _same_level(canonical_problem)
    object.__setattr__(
        malformed_candidate,
        "resolved_orbit_ids",
        list(malformed_candidate.resolved_orbit_ids),
    )
    result = terminalize_declared_search(
        canonical_problem,
        (malformed_candidate,),
        (),
        _complete((malformed_candidate,)),
    )
    assert type(result) is TypedRefusal
    assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE

    canonical_candidate = _same_level(canonical_problem)
    canonical_exhaustion = _complete((canonical_candidate,))
    malformed_row_candidate = _same_level(canonical_problem)
    object.__setattr__(malformed_row_candidate, "profiles", (object(),))
    result = terminalize_declared_search(
        canonical_problem,
        (malformed_row_candidate,),
        (),
        canonical_exhaustion,
    )
    assert type(result) is TypedRefusal
    assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE


def test_terminalizer_replays_exhaustion_and_malformed_cec_parent() -> None:
    problem = _problem()
    packet = _cec_packet(problem)
    exhaustion = _complete(cec=(packet,))
    object.__setattr__(
        exhaustion,
        "cec_packet_ids",
        list(exhaustion.cec_packet_ids),
    )
    result = terminalize_declared_search(problem, (), (packet,), exhaustion)
    assert type(result) is TypedRefusal
    assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE

    malformed = _cec_packet(problem)
    object.__setattr__(malformed, "parent", object())
    with pytest.raises(BridgeError):
        evaluate_cec_child_packet(malformed)
    result = terminalize_declared_search(
        problem,
        (),
        (malformed,),
        _complete(cec=(packet,)),
    )
    assert type(result) is TypedRefusal
    assert result.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE


def test_terminal_trichotomy_refusal_branches() -> None:
    problem = _problem()
    complete = terminalize_declared_search(problem, (), (), _complete())
    assert type(complete) is TypedRefusal
    assert complete.code is RefusalCode.NO_ADMISSIBLE_RESPONSE
    incomplete = terminalize_declared_search(
        problem,
        (),
        (),
        SearchExhaustionV1(False, False, (), ()),
    )
    assert type(incomplete) is TypedRefusal
    assert incomplete.code is RefusalCode.INCOMPLETE_SEARCH_EVIDENCE
    no_demand = terminalize_declared_search(_problem(protected=()), (), (), _complete())
    assert type(no_demand) is TypedRefusal
    assert no_demand.code is RefusalCode.NO_ACTIVE_OBSTRUCTION


def test_terminal_eliminator_rejects_lookalikes() -> None:
    with pytest.raises(BridgeError):
        SameLevelRepair(())
    with pytest.raises(BridgeError):
        terminal_kind(("SameLevelRepair",))


def test_public_replay_and_terminalizer_expose_no_truth_function_hooks() -> None:
    assert tuple(signature(replay_cec_child_packet).parameters) == (
        "packet",
        "receipt",
    )
    assert tuple(signature(terminalize_declared_search).parameters) == (
        "problem",
        "same_level",
        "cec_packets",
        "exhaustion",
    )
    problem = _problem()
    packet = _cec_packet(problem)
    receipt = evaluate_cec_child_packet(packet)
    with pytest.raises(TypeError):
        replay_cec_child_packet(
            packet, receipt, _admission_oracle=lambda _: (("forged", True),)
        )
    with pytest.raises(TypeError):
        terminalize_declared_search(
            problem,
            (),
            (packet,),
            _complete(cec=(packet,)),
            _cec_replay=lambda *_: True,
        )


def _pr2_fixture(*, renamed: bool) -> BridgeProblemV1:
    states = ("0", "1", "2", "3")
    primitive = PrimitiveCarrierV1(
        "carrier:pr2",
        states,
        (
            RetainedDiffV1("0", "1", "retained:01"),
            RetainedDiffV1("2", "3", "retained:23"),
        ),
    )
    marked = {"0", "1"} if renamed else {"2", "3"}
    observer = ObserverPresentationV1(
        primitive.primitive_id,
        "signature:pr2",
        ("marked",),
        tuple(
            ProfileRowV1(state, ("marked",) if state in marked else ())
            for state in states
        ),
        _identity_transitions(("marked",), states),
        (),
        ClosurePolicy.EXTERNAL_ALL_PAIRS,
    )
    return BridgeProblemV1(primitive, observer)


def test_demand_orbits_transport_under_pr2_renaming_fixture() -> None:
    source = _pr2_fixture(renamed=False)
    target = _pr2_fixture(renamed=True)
    renaming = StateRenamingV1(
        source.problem_id,
        target.problem_id,
        source.primitive.states,
        target.primitive.states,
        ("2", "3", "0", "1"),
    )
    assert orbit_transition_congruent(source, target, renaming)
    assert {orbit.members for orbit in demand_orbits(source)} == {
        (("0", "1"),),
        (("2", "3"),),
    }
    source_least = min(obstruction.pair for obstruction in active_obstructions(source))
    target_least = min(obstruction.pair for obstruction in active_obstructions(target))
    assert source_least == target_least == ("0", "1")
    assert source.observer.profile("0") == ()
    assert target.observer.profile("0") == ("marked",)


def test_orbit_transport_requires_transition_commutation() -> None:
    source = _pr2_fixture(renamed=False)
    target = _pr2_fixture(renamed=True)
    rows = list(target.observer.transitions)
    index = rows.index(TransitionRowV1("marked", "0", "0"))
    rows[index] = TransitionRowV1("marked", "0", "1")
    target = BridgeProblemV1(
        target.primitive,
        replace(target.observer, transitions=tuple(rows)),
    )
    renaming = StateRenamingV1(
        source.problem_id,
        target.problem_id,
        source.primitive.states,
        target.primitive.states,
        ("2", "3", "0", "1"),
    )
    assert not orbit_transition_congruent(source, target, renaming)


def test_orbit_transport_requires_exact_retained_set_transport() -> None:
    source = _problem(protected=(), retained=())
    target = _problem(protected=())
    renaming = StateRenamingV1(
        source.problem_id,
        target.problem_id,
        source.primitive.states,
        target.primitive.states,
        source.primitive.states,
    )
    assert not orbit_transition_congruent(source, target, renaming)


def test_orbit_api_returns_full_classes_not_representatives() -> None:
    problem = _problem(
        protected=(),
        retained=(
            RetainedDiffV1("s0", "s1", "retained:w01"),
            RetainedDiffV1("s0", "s2", "retained:w02"),
            RetainedDiffV1("s1", "s2", "retained:w12"),
        ),
        closure_policy=ClosurePolicy.EXTERNAL_ALL_PAIRS,
    )
    orbits = demand_orbits(problem)
    assert len(orbits) == 1
    assert orbits[0].members == (("s0", "s1"), ("s0", "s2"), ("s1", "s2"))


def test_exact_runtime_types_and_authority_are_enforced() -> None:
    class StringAlias(str):
        pass

    with pytest.raises(BridgeError):
        PrimitiveCarrierV1("carrier", ("s0", "s1"), (), authority_effect="Minted")
    with pytest.raises(BridgeError):
        PrimitiveCarrierV1(
            "carrier",
            ("s0", "s1"),
            (),
            authority_effect=StringAlias("None"),
        )
    with pytest.raises(BridgeError):
        SearchExhaustionV1(1, True, (), ())
    with pytest.raises(BridgeError):
        RetainedDiffV1("s1", "s0", "wrong-order")


def test_universal_module_has_no_cochain_or_physics_surface() -> None:
    import omega_engine_pfp.infrastructure.adapters.retained_profile_cec_bridge as bridge

    source = open(bridge.__file__, encoding="utf-8").read().lower()
    for forbidden_import in (
        "import cochain",
        "import homology",
        "import physics",
        "import riemann",
        "import zeta",
    ):
        assert forbidden_import not in source
