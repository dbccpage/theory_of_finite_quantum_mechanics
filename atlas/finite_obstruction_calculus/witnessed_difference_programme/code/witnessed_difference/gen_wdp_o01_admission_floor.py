"""Explicit admission of the primitive-to-witness floor for GEN-WDP-O01.

The carrier, signature, irreflexivity law, and no-form challenge floor are
the inputs named by the programme sources. This module checks those named
finite cuts and cover fixtures. It does not prove a stronger floor, a cost
theorem, or a challenge generator for every regime. AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
from itertools import product

SCHEMA = "wdp.gen_wdp_o01_admission_floor.v1"
WITNESS_ID = "gen-wdp-o01-admission-floor"

SOURCE_ANCHORS = (
    "docs/genesis_bridge_register.md | GEN-WDP-O01",
    "docs/primitive_admission_and_transport.md ## The primitive floor",
    "docs/primitive_execution_refinement.md ## All-arity floor with persistent requirements",
    "docs/source_replay_and_remaining_derivations.md ## 2. The initial challenge floor and its alternatives",
    "lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean",
)


def canonical_payload(witness: dict[str, object]) -> str:
    return json.dumps(witness, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def problem_sha256(witness: dict[str, object]) -> str:
    return hashlib.sha256(canonical_payload(witness).encode("utf-8")).hexdigest()


def _covers(mentioned: set[int], edges: tuple[tuple[int, int], ...]) -> bool:
    return all(left in mentioned or right in mentioned for left, right in edges)


def _vertex_cover_size(size: int, edges: tuple[tuple[int, int], ...]) -> int:
    best = size
    for mask in range(1 << size):
        mentioned = {index for index in range(size) if mask & (1 << index)}
        if _covers(mentioned, edges):
            best = min(best, len(mentioned))
    return best


def _complete_edges(size: int) -> tuple[tuple[int, int], ...]:
    return tuple((left, right) for left in range(size) for right in range(left + 1, size))


def _contexts(arity: int, data_count: int) -> tuple[tuple[int | None, ...], ...]:
    slots: tuple[int | None, ...] = (None, *range(data_count))
    return tuple(
        word
        for word in product(slots, repeat=arity)
        if any(slot is None for slot in word)
    )


def _plug(word: tuple[int | None, ...], datum: int) -> tuple[int, ...]:
    return tuple(datum if slot is None else slot for slot in word)


def _profile(
    arity: int,
    instance: tuple[int, ...] | None,
    datum: int,
    data_count: int,
    uniform_rule: bool,
) -> frozenset[tuple[int | None, ...]]:
    recognized = []
    for word in _contexts(arity, data_count):
        plugged = _plug(word, datum)
        if uniform_rule or (instance is not None and plugged == instance):
            recognized.append(word)
    return frozenset(recognized)


def _profiles_differ(
    arity: int,
    instance: tuple[int, ...],
    data_count: int,
    left: int = 0,
    right: int = 1,
) -> bool:
    return _profile(arity, instance, left, data_count, False) != _profile(
        arity, instance, right, data_count, False
    )


def _common_arity(rows: list[dict[str, object]]) -> int:
    arities = {int(row["arity"]) for row in rows}
    if len(arities) != 1:
        raise RuntimeError(f"minimum responses did not share one arity: {sorted(arities)}")
    return arities.pop()


def _covering_instances(
    data_count: int,
    edges: tuple[tuple[int, int], ...],
    max_arity: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cover_size = _vertex_cover_size(data_count, edges)
    for arity in range(1, max_arity + 1):
        for word in product(range(data_count), repeat=arity):
            mentioned = set(word)
            if not _covers(mentioned, edges):
                continue
            rows.append(
                {
                    "arity": arity,
                    "instance": list(word),
                    "mentioned": sorted(mentioned),
                    "profiles_differ": _profiles_differ(arity, word, data_count),
                    "diagonal": len(mentioned) == 1 and arity > 1,
                    "exact_minimum_cover": len(word) == cover_size and len(mentioned) == cover_size,
                }
            )
    return rows


def _relation_holds(pairs: frozenset[tuple[int, int]], left: int, right: int) -> bool:
    return (left, right) in pairs


def _irreflexive(pairs: frozenset[tuple[int, int]], carrier: tuple[int, ...]) -> bool:
    return all(not _relation_holds(pairs, point, point) for point in carrier)


def _cut_record(name: str, pairs: frozenset[tuple[int, int]], first: int, second: int) -> dict[str, object]:
    carrier = (0, 1)
    return {
        "name": name,
        "carrier": list(carrier),
        "signature": "binary-relation-R",
        "law": "forall x, not R(x, x)",
        "instance": [first, second],
        "instance_holds": _relation_holds(pairs, first, second),
        "law_holds": _irreflexive(pairs, carrier),
        "endpoints_apart": first != second,
    }


def _inscription_supplies_no_floor() -> dict[str, object]:
    """Supply leaves the admitted components unchanged; dedup does not split a token."""
    data: list[str] = []
    forms: list[int] = []
    supplied = list(data)
    if "<>" not in data:
        data.append("<>")
    if "<>" not in data:
        data.append("<>")
    return {
        "glyph": "<>",
        "supply_leaves_components_unchanged": supplied == [],
        "dedup_datum_count": len(data),
        "form_count": len(forms),
        "law_present": False,
        "orientation_present": False,
    }


def admission_floor_witness() -> dict[str, object]:
    """Admit the named floor and check its source-stated finite fixtures."""
    forward_pairs = frozenset({(0, 1)})
    reverse_pairs = frozenset({(1, 0)})
    forward = _cut_record("forward", forward_pairs, 0, 1)
    reverse = _cut_record("reverse", reverse_pairs, 1, 0)
    if not (forward["instance_holds"] and forward["law_holds"] and forward["endpoints_apart"]):
        raise RuntimeError("forward cut failed its admitted hypotheses")
    if not (reverse["instance_holds"] and reverse["law_holds"] and reverse["endpoints_apart"]):
        raise RuntimeError("reverse cut failed its admitted hypotheses")
    if forward["instance"] == reverse["instance"]:
        raise RuntimeError("the two Bool orientations were not both retained")

    singleton = (0,)
    full_singleton = frozenset({(0, 0)})
    empty_singleton: frozenset[tuple[int, int]] = frozenset()
    singleton_instance_without_law = _relation_holds(full_singleton, 0, 0) and not _irreflexive(
        full_singleton, singleton
    )
    singleton_law_without_instance = _irreflexive(empty_singleton, singleton) and not _relation_holds(
        empty_singleton, 0, 0
    )
    full_is_cut = _relation_holds(full_singleton, 0, 0) and _irreflexive(full_singleton, singleton)
    empty_is_cut = _relation_holds(empty_singleton, 0, 0) and _irreflexive(empty_singleton, singleton)
    # The instance R(0,1) is sent to one image point, so preservation demands a diagonal.
    collapsed_requires_diagonal = _relation_holds(forward_pairs, 0, 1)
    forced_image = frozenset({(0, 0)}) if collapsed_requires_diagonal else frozenset()
    image_law_with_preservation = collapsed_requires_diagonal and _irreflexive(forced_image, singleton)
    identity_preserves = bool(
        forward["instance_holds"] and forward["law_holds"] and forward["endpoints_apart"]
    )

    pair_edges = _complete_edges(2)
    triangle_edges = _complete_edges(3)
    tetra_edges = _complete_edges(4)
    pair_rows = _covering_instances(2, pair_edges, 2)
    triangle_rows = _covering_instances(3, triangle_edges, 2)
    tetra_arity_two = _covering_instances(4, tetra_edges, 2)
    tetra_arity_three = _covering_instances(4, tetra_edges, 3)
    if not all(row["profiles_differ"] for row in pair_rows + triangle_rows + tetra_arity_three):
        raise RuntimeError("a covering instance failed to separate the target pair")

    pair_mu1 = pair_rows
    pair_mu2 = [row for row in pair_rows if row["exact_minimum_cover"]]
    triangle_mu2 = [row for row in triangle_rows if row["exact_minimum_cover"]]
    tetra_mu2 = [row for row in tetra_arity_three if row["exact_minimum_cover"]]
    expected_counts = (len(pair_mu1), len(pair_mu2), len(triangle_mu2), len(tetra_mu2))
    if expected_counts != (6, 2, 6, 24):
        raise RuntimeError(f"named fixture counts were {expected_counts}, not (6, 2, 6, 24)")
    if tetra_arity_two:
        raise RuntimeError("arity 2 separated the six-edge requirement graph")
    if any(row["arity"] == 1 for row in triangle_mu2):
        raise RuntimeError("a unary tuple was retained for the triangle")

    uniform_left = _profile(1, None, 0, 2, True)
    uniform_right = _profile(1, None, 1, 2, True)
    empty_left = _profile(1, None, 0, 2, False)
    empty_right = _profile(1, None, 1, 2, False)
    no_form_left: frozenset[tuple[int | None, ...]] = frozenset()
    no_form_right: frozenset[tuple[int | None, ...]] = frozenset()
    datum_without_form_separates = no_form_left != no_form_right
    inscription = _inscription_supplies_no_floor()
    if inscription["dedup_datum_count"] != 1 or inscription["law_present"] or inscription["form_count"] != 0:
        raise RuntimeError("the opaque inscription supplied a floor")

    form_and_instance = ("form", "instance")
    unary_arity = _common_arity(pair_mu2)
    binary_rows = [row for row in pair_mu1 if int(row["arity"]) != unary_arity]
    binary_link = {
        "name": "binary-link",
        "item_cost": len(form_and_instance),
        "arity_cost": _common_arity(binary_rows),
    }
    unary_mark = {
        "name": "unary-mark",
        "item_cost": len(form_and_instance),
        "arity_cost": unary_arity,
    }
    return {
        "schema": SCHEMA,
        "witness_id": WITNESS_ID,
        "authority_effect": "none",
        "admitted_object": "primitive-to-witness-admission-floor",
        "admitted": [
            "carrier",
            "signature",
            "irreflexivity-law",
            "no-form-challenge-generation-floor",
        ],
        "source_anchors": list(SOURCE_ANCHORS),
        "register_row_remains_open": True,
        "stronger_floor_proved": False,
        "stronger_floor_has_theorem_and_falsifier": False,
        "genesis_cost_floor_proved": False,
        "declared_responses_exhaust_every_language": False,
        "all_regime_challenge_refinement_proved": False,
        "irreflexivity_chosen_by_observational_floor": False,
        "program_refinement_proved": False,
        "generated_token_freshness_proved": False,
        "forward_cut": forward,
        "reverse_cut": reverse,
        "law_selects_one_orientation": not (
            bool(forward["instance_holds"] and forward["law_holds"])
            and bool(reverse["instance_holds"] and reverse["law_holds"])
        ),
        "orientations_retained": 2,
        "singleton_instance_without_law": singleton_instance_without_law,
        "singleton_law_without_instance": singleton_law_without_instance,
        "subsingleton_cut_refused": not full_is_cut and not empty_is_cut,
        "collapsed_endpoints_force_diagonal": collapsed_requires_diagonal,
        "collapsed_image_obeys_instance_and_law": image_law_with_preservation,
        "identity_transport_preserves_separation": identity_preserves,
        "inscription": inscription,
        "declared_price_responses": [unary_mark, binary_link],
        "raw_item_costs_tie": unary_mark["item_cost"] == binary_link["item_cost"],
        "declared_arity_selects_unary": unary_mark["arity_cost"] < binary_link["arity_cost"],
        "declared_prices_are_not_a_cost_theorem": True,
        "datum_without_form_separates": datum_without_form_separates,
        "form_without_instance_separates": empty_left != empty_right,
        "uniform_rule_separates": uniform_left != uniform_right,
        "pair_cover_size": _vertex_cover_size(2, pair_edges),
        "pair_mu1_count": len(pair_mu1),
        "pair_mu1_item_cost": len(form_and_instance),
        "pair_mu2_count": len(pair_mu2),
        "pair_mu2_arity": _common_arity(pair_mu2),
        "pair_mu1": pair_mu1,
        "diagonal_instances_retained": any(row["diagonal"] for row in pair_mu1),
        "triangle_cover_size": _vertex_cover_size(3, triangle_edges),
        "triangle_mu2_count": len(triangle_mu2),
        "triangle_mu2_arity": _common_arity(triangle_mu2),
        "triangle_mu2": triangle_mu2,
        "tetrahedron_cover_size": _vertex_cover_size(4, tetra_edges),
        "tetrahedron_arity_2_count": len(tetra_arity_two),
        "tetrahedron_mu2_count": len(tetra_mu2),
        "tetrahedron_mu2_arity": _common_arity(tetra_mu2),
        "tetrahedron_mu2": tetra_mu2,
    }
