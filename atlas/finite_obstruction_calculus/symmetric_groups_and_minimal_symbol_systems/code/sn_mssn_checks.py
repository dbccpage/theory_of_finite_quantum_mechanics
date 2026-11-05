"""Finite checks for WDP Paper 001.

Each function is the shipped checker for one manuscript statement.
Tests and the reproduction entry call these functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import re

PAPER_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[6]
_local_ebnf = PAPER_DIR / "code" / "grammar" / "mssn.ebnf"
_canonical_ebnf = (
    REPO_ROOT
    / "omega_engine_education"
    / "documentation"
    / "003_oemssn"
    / "grammar"
    / "mssn.ebnf"
)
EBNF_PATH = _local_ebnf if _local_ebnf.is_file() else _canonical_ebnf
PAPER_PATH = PAPER_DIR / "paper.md"
LEDGER_PATH = PAPER_DIR / "paper_claim_ledger.md"

STATUSES = ("definition", "proved", "negative boundary", "withdrawn")
PROVED_IDS = (
    "WDP-P001-002",
    "WDP-P001-004",
    "WDP-P001-005",
    "WDP-P001-007",
    "WDP-P001-008",
    "WDP-P001-009",
    "WDP-P001-011",
    "WDP-P001-012",
    "WDP-P001-018",
)
WITHDRAWN_NAMES = (
    "univalence_from_two_sided_inverse",
    "automatic_postnikov_tower",
    "selected_chsh_detects_all_contextuality",
    "involution_proves_pentagon",
    "sql_and_lean_prove_bisimulation",
    "fixtures_certify_physical_theory",
)


class DemandHypothesisError(ValueError):
    """Discharged subset or disjoint-birth hypothesis failed."""


class RecoveryHypothesisError(ValueError):
    """Old-image recovery hypothesis failed."""


class ChainHypothesisError(ValueError):
    """Chain-map retraction hypothesis failed."""


@dataclass(frozen=True)
class DemandAccount:
    previous: frozenset[str]
    discharged: frozenset[str]
    born: frozenset[str]
    remaining: frozenset[str]
    nxt: frozenset[str]
    s: int
    d: int
    b: int
    s_next: int


def demand_account(
    previous: set[str] | frozenset[str],
    discharged: set[str] | frozenset[str],
    born: set[str] | frozenset[str],
) -> DemandAccount:
    """Cardinality of W minus D disjoint-union B."""
    prev = frozenset(previous)
    gone = frozenset(discharged)
    births = frozenset(born)
    if not gone <= prev:
        raise DemandHypothesisError("discharged demands are not a subset of the register")
    remaining = prev - gone
    if births & remaining:
        raise DemandHypothesisError("births meet the undischarged register")
    nxt = remaining | births
    return DemandAccount(
        previous=prev,
        discharged=gone,
        born=births,
        remaining=remaining,
        nxt=nxt,
        s=len(prev),
        d=len(gone),
        b=len(births),
        s_next=len(nxt),
    )


def supplied_tag_separates(
    report: dict[str, str], tag: dict[str, int], left: str, right: str
) -> dict[str, object]:
    """A supplied tag separates one pair and the first component recovers the report."""
    refined = {point: (report[point], tag[point]) for point in report}
    return {
        "separated": refined[left] != refined[right],
        "recovered_left": refined[left][0] == report[left],
        "recovered_right": refined[right][0] == report[right],
        "refined": refined,
    }


def _as_map(mapping: dict[str, str]) -> dict[str, str]:
    return dict(mapping)


def old_image_injective(lift: dict[str, str], recover: dict[str, tuple[str, str]]) -> bool:
    """True when the old-image law holds and the lift is injective on its keys."""
    for source, image in lift.items():
        outcome = recover[image]
        if outcome != ("inl", source):
            raise RecoveryHypothesisError("old-image law failed")
    images = list(lift.values())
    return len(images) == len(set(images))


def recovery_counterexamples() -> dict[str, dict[str, object]]:
    """Three finite maps where old-image recovery holds and a stronger claim fails."""
    off_lift = {"a": "a"}
    off_recover = {"a": ("inl", "a"), "extra": ("inl", "a")}
    observation_lift = {"a1": "a1", "a2": "a2"}
    observation_recover = {"a1": ("inl", "a1"), "a2": ("inl", "a2")}
    old_observation = {"a1": "o", "a2": "o"}
    new_observation = {"a1": "o", "a2": "o2"}
    repair_lift = {"a": "a"}
    repair_recover = {"a": ("inl", "a")}
    obstruction = {"a": True}
    return {
        "off_image": {
            "injective": old_image_injective(off_lift, off_recover),
            "rejects_off_image": off_recover["extra"] == ("inr", "NON_DESCENT"),
            "off_image_outcome": off_recover["extra"],
        },
        "observation": {
            "injective": old_image_injective(observation_lift, observation_recover),
            "preserves_observation": all(
                new_observation[observation_lift[source]] == old_observation[source]
                for source in observation_lift
            ),
        },
        "repair": {
            "injective": old_image_injective(repair_lift, repair_recover),
            "obstruction_before": obstruction["a"],
            "obstruction_after": obstruction[repair_lift["a"]],
        },
    }


def indecomposable_words(alphabet: tuple[str, ...], max_length: int = 2) -> tuple[tuple[str, ...], ...]:
    """Words that are not a concatenation of two nonempty words, up to max_length."""
    found: list[tuple[str, ...]] = []
    for length in range(1, max_length + 1):
        for word in product(alphabet, repeat=length):
            if word and not any(
                word[:split] and word[split:] for split in range(1, len(word))
            ):
                found.append(word)
    return tuple(found)


def free_monoids_nonisomorphic(left: tuple[str, ...], right: tuple[str, ...]) -> dict[str, object]:
    """Compare indecomposable counts of two finite alphabets."""
    left_words = indecomposable_words(left)
    right_words = indecomposable_words(right)
    return {
        "left_count": len(left_words),
        "right_count": len(right_words),
        "nonisomorphic": len(left_words) != len(right_words),
        "left_words": left_words,
        "right_words": right_words,
    }


def discrete_categories_inequivalent(left_objects: int, right_objects: int) -> dict[str, object]:
    """Discrete categories are inequivalent exactly when object counts differ."""
    if left_objects < 0 or right_objects < 0:
        raise ValueError("object counts are cardinalities")
    return {
        "left_objects": left_objects,
        "right_objects": right_objects,
        "left_iso_classes": left_objects,
        "right_iso_classes": right_objects,
        "inequivalent": left_objects != right_objects,
    }


def language_restriction(language: frozenset[str], old_alphabet: frozenset[str]) -> frozenset[str]:
    return frozenset(word for word in language if set(word) <= old_alphabet)


def refuse_word(word: str, old_alphabet: frozenset[str]) -> tuple[str, str]:
    if set(word) <= old_alphabet:
        return ("word", word)
    return ("NON_DESCENT", "")


def erase_word(word: str, old_alphabet: frozenset[str]) -> str:
    return "".join(char for char in word if char in old_alphabet)


def three_recovery_contracts() -> dict[str, object]:
    """Language restriction, typed refusal, and erasure disagree on a new letter."""
    old = frozenset("a")
    language = frozenset({"a", "ab"})
    restricted = language_restriction(language, old)
    refused = refuse_word("ab", old)
    erased = erase_word("ab", old)
    old_refused = refuse_word("a", old)
    old_erased = erase_word("a", old)
    return {
        "restricted": tuple(sorted(restricted)),
        "refused_new": refused,
        "erased_new": erased,
        "old_word_refused": old_refused,
        "old_word_erased": old_erased,
        "contracts_differ": refused != ("word", erased),
    }


def encode_collapse(word: str) -> str:
    """a maps to 0 and b maps to 00."""
    table = {"a": "0", "b": "00"}
    return "".join(table[char] for char in word)


def code_collapse_witness() -> dict[str, object]:
    aa = encode_collapse("aa")
    bee = encode_collapse("b")
    return {"aa": aa, "b": bee, "collapsed": aa == bee and aa == "00"}


def edge_directions(inscription: str) -> tuple[tuple[str, str], ...]:
    """Read declared directed-edge syntax into ordered endpoint pairs."""
    edges: list[tuple[str, str]] = []
    for index, mark in enumerate(inscription):
        if mark in {">", "<"}:
            left = inscription[index - 1]
            right = inscription[index + 1]
            if mark == ">":
                edges.append((left, right))
            else:
                edges.append((right, left))
    return tuple(edges)


def component_count(vertices: tuple[str, ...], edges: tuple[tuple[str, str], ...]) -> int:
    """Undirected components. A loop does not join distinct vertices."""
    parent = {vertex: vertex for vertex in vertices}

    def find(vertex: str) -> str:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    def unite(left: str, right: str) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for src, tgt in edges:
        if src != tgt:
            unite(src, tgt)
    return len({find(vertex) for vertex in vertices})


def graph_component_report() -> dict[str, object]:
    vertices = ("a", "b")
    empty = component_count(vertices, ())
    loop = component_count(vertices, (("a", "a"),))
    edge = component_count(vertices, (("a", "b"),))
    triangle = component_count(("a", "b", "c"), (("a", "b"), ("b", "c"), ("c", "a")))
    return {
        "empty": empty,
        "loop": loop,
        "edge": edge,
        "triangle": triangle,
        "reduced_empty": empty - 1,
        "reduced_edge": edge - 1,
        "loop_preserves_count": loop == empty,
        "edge_lowers_count": edge == empty - 1,
    }


def edge_boundary(src: int, tgt: int, vertices: int) -> tuple[int, ...]:
    boundary = [0] * vertices
    boundary[src] -= 1
    boundary[tgt] += 1
    return tuple(boundary)


def retraction_recovers_cycle(
    cycle: tuple[int, ...],
    included: tuple[int, ...],
    boundary_of_primitive: tuple[int, ...],
    retracted_included: tuple[int, ...],
    retracted_boundary: tuple[int, ...],
    boundary_of_retracted: tuple[int, ...],
) -> tuple[int, ...]:
    """Return the recovered boundary when section and chain-map laws hold."""
    if included != boundary_of_primitive:
        raise ChainHypothesisError("included cycle is not the claimed boundary")
    if retracted_included != cycle:
        raise ChainHypothesisError("section law failed")
    if retracted_boundary != boundary_of_retracted:
        raise ChainHypothesisError("retraction is not a chain map")
    return boundary_of_retracted


def two_point_obstruction() -> dict[str, object]:
    boundary = edge_boundary(0, 1, 2)
    required = tuple(0 for _ in boundary)
    return {
        "boundary": boundary,
        "required": required,
        "admits_retraction": boundary == required,
    }


def triangle_boundary(coeffs: tuple[int, int, int]) -> tuple[int, int, int]:
    x_ab, y_bc, w_ca = coeffs
    return (-x_ab + w_ca, x_ab - y_bc, y_bc - w_ca)


def triangle_obstruction() -> dict[str, object]:
    cycle = (1, 1, 1)
    cycle_boundary = triangle_boundary(cycle)
    return {
        "cycle": cycle,
        "cycle_boundary": cycle_boundary,
        "face_boundary": cycle,
        "admits_retraction": cycle == (0, 0, 0),
    }


def identity_retraction_recovers() -> tuple[int, ...]:
    cycle = (2, -2)
    return retraction_recovers_cycle(cycle, cycle, cycle, cycle, cycle, cycle)


def fiber_descent(report: dict[str, str], answer: dict[str, str]) -> dict[str, object]:
    """A question descends to the realized report image exactly on constant fibers."""
    constant = all(
        answer[left] == answer[right]
        for left in report
        for right in report
        if report[left] == report[right]
    )
    descended: dict[str, str] = {}
    if constant:
        for point, image in report.items():
            descended[image] = answer[point]
    return {
        "constant_on_fibers": constant,
        "descended": descended if constant else None,
        "image": tuple(sorted(set(report.values()))),
    }


def chsh_missed_orientation() -> dict[str, object]:
    e00, e01, e10, e11 = 1, 1, -1, 1
    selected = e00 + e01 + e10 - e11
    other = e00 + e01 - e10 + e11
    required_product = e00 * e01 * e10 * e11
    assignment_products = {
        (a0 * b0) * (a0 * b1) * (a1 * b0) * (a1 * b1)
        for a0 in (1, -1)
        for a1 in (1, -1)
        for b0 in (1, -1)
        for b1 in (1, -1)
    }
    return {
        "selected": selected,
        "other": other,
        "required_product": required_product,
        "assignment_products": tuple(sorted(assignment_products)),
        "global_assignment_impossible": required_product not in assignment_products,
    }


def _normalize_ebnf(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\\|", "|")).strip()


def grammar_productions(ebnf_text: str) -> dict[str, str]:
    productions: dict[str, str] = {}
    for line in ebnf_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("(*"):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*);\s*$", stripped)
        if match:
            productions[match.group(1)] = _normalize_ebnf(match.group(2))
    return productions


def appendix_inventory(paper_text: str) -> tuple[tuple[str, str, str], ...]:
    rows: list[tuple[str, str, str]] = []
    for line in paper_text.splitlines():
        match = re.match(
            r"^\|\s*\*\*(\d+)\*\*\s*\|\s*`([^`]+)`\s*\|\s*`([^`]*)`\s*\|",
            line,
        )
        if match:
            rows.append((match.group(1), match.group(2), _normalize_ebnf(match.group(3))))
    return tuple(rows)


def grammar_inventory_matches(
    ebnf_text: str | None = None, paper_text: str | None = None
) -> dict[str, object]:
    ebnf_source = EBNF_PATH.read_text(encoding="utf-8") if ebnf_text is None else ebnf_text
    paper_source = PAPER_PATH.read_text(encoding="utf-8") if paper_text is None else paper_text
    productions = grammar_productions(ebnf_source)
    rows = appendix_inventory(paper_source)
    mismatches = []
    for number, name, rhs in rows:
        actual = productions.get(name)
        if actual != rhs:
            mismatches.append({"number": number, "name": name, "appendix": rhs, "grammar": actual})
    return {
        "count": len(rows),
        "names": tuple(name for _, name, _ in rows),
        "matches": len(rows) == 22 and not mismatches and rows[0][1] == "raw_glyphs" and rows[-1][1] == "rewrite_rule",
        "mismatches": tuple(mismatches),
    }


def ledger_rows(ledger_text: str | None = None) -> tuple[tuple[str, str], ...]:
    source = LEDGER_PATH.read_text(encoding="utf-8") if ledger_text is None else ledger_text
    rows = []
    for line in source.splitlines():
        match = re.match(r"^\|\s*(WDP-P001-\d+)\s*\|\s*([^|]+?)\s*\|", line)
        if match:
            rows.append((match.group(1), match.group(2).strip()))
    return tuple(rows)


def ledger_status_report(ledger_text: str | None = None) -> dict[str, object]:
    rows = ledger_rows(ledger_text)
    proved = tuple(row_id for row_id, status in rows if status == "proved")
    return {
        "count": len(rows),
        "statuses_closed": all(status in STATUSES for _, status in rows) and len(rows) == 19,
        "proved": proved,
        "proved_matches_coverage": proved == PROVED_IDS,
        "withdrawn_present": any(status == "withdrawn" for _, status in rows),
    }


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def manuscript_boundaries(paper_text: str | None = None) -> dict[str, bool]:
    source = _flat(PAPER_PATH.read_text(encoding="utf-8") if paper_text is None else paper_text)
    return {
        "survivor_not_theorem": "not a universal native survivor sequence" in source
        and "(0,1,1,1,0,1,1)" in source,
        "physics_withdrawn": "withdrawn claims must not re-enter" in source
        and "chiral-superconductor" in source
        and "does not claim a fresh rerun" in source,
        "archive_historical": "source archive" in source and "not competing" in source,
    }


def edge_multiset_witness() -> dict[str, object]:
    forward = edge_directions("a>b>c")
    reversed_walk = edge_directions("c<b<a")
    return {
        "forward": forward,
        "reversed": reversed_walk,
        "same_edge_multiset": sorted(forward) == sorted(reversed_walk),
        "same_traversal": forward == reversed_walk,
    }


def run_reproduction() -> dict[str, object]:
    """Evaluate every proved row and the named negative boundaries."""
    demand = demand_account({"w1", "w2", "w3"}, {"w2"}, {"b1"})
    tag = supplied_tag_separates({"a": "o", "b": "o"}, {"a": 0, "b": 1}, "a", "b")
    injective = old_image_injective({"a": "ua", "b": "ub"}, {"ua": ("inl", "a"), "ub": ("inl", "b")})
    counters = recovery_counterexamples()
    monoids = free_monoids_nonisomorphic(("0", "1"), tuple("0123456789"))
    same_monoids = free_monoids_nonisomorphic(("a", "b"), ("x", "y"))
    categories = discrete_categories_inequivalent(2, 26)
    same_categories = discrete_categories_inequivalent(4, 4)
    contracts = three_recovery_contracts()
    collapse = code_collapse_witness()
    graphs = graph_component_report()
    recovered = identity_retraction_recovers()
    two_point = two_point_obstruction()
    triangle = triangle_obstruction()
    descent = fiber_descent({"x": "y", "x2": "y"}, {"x": "z", "x2": "z"})
    blocked = fiber_descent({"x": "y", "x2": "y"}, {"x": "z", "x2": "z2"})
    chsh = chsh_missed_orientation()
    grammar = grammar_inventory_matches()
    ledger = ledger_status_report()
    bounds = manuscript_boundaries()
    edges = edge_multiset_witness()
    ok = all(
        (
            demand.s_next == demand.s - demand.d + demand.b,
            demand.nxt == frozenset({"w1", "w3", "b1"}),
            tag["separated"] is True and tag["recovered_left"] is True,
            injective is True,
            counters["off_image"]["injective"] is True and counters["off_image"]["rejects_off_image"] is False,
            counters["observation"]["injective"] is True and counters["observation"]["preserves_observation"] is False,
            counters["repair"]["injective"] is True and counters["repair"]["obstruction_after"] is True,
            monoids["nonisomorphic"] is True and same_monoids["nonisomorphic"] is False,
            monoids["left_count"] == 2 and monoids["right_count"] == 10,
            categories["inequivalent"] is True and same_categories["inequivalent"] is False,
            contracts["contracts_differ"] is True,
            collapse["collapsed"] is True,
            graphs["loop_preserves_count"] is True and graphs["edge_lowers_count"] is True,
            graphs["empty"] == 2 and graphs["triangle"] == 1 and graphs["reduced_empty"] == 1,
            recovered == (2, -2),
            two_point["admits_retraction"] is False,
            triangle["admits_retraction"] is False and all(item == 0 for item in triangle["cycle_boundary"]),
            descent["constant_on_fibers"] is True and descent["descended"] == {"y": "z"},
            blocked["constant_on_fibers"] is False and blocked["descended"] is None,
            chsh["selected"] == 0 and chsh["other"] == 4 and chsh["global_assignment_impossible"] is True,
            grammar["matches"] is True,
            ledger["proved_matches_coverage"] is True and ledger["statuses_closed"] is True,
            bounds["survivor_not_theorem"] is True and bounds["physics_withdrawn"] is True,
            edges["same_edge_multiset"] is True and edges["same_traversal"] is False,
        )
    )
    return {
        "ok": ok,
        "demand": {
            "s": demand.s,
            "d": demand.d,
            "b": demand.b,
            "s_next": demand.s_next,
            "next": tuple(sorted(demand.nxt)),
        },
        "tag_separated": tag["separated"],
        "injective": injective,
        "off_image_rejected": counters["off_image"]["rejects_off_image"],
        "observation_preserved": counters["observation"]["preserves_observation"],
        "obstruction_after_identity": counters["repair"]["obstruction_after"],
        "monoid_counts": (monoids["left_count"], monoids["right_count"]),
        "monoids_nonisomorphic": monoids["nonisomorphic"],
        "equal_monoids_nonisomorphic": same_monoids["nonisomorphic"],
        "categories_inequivalent": categories["inequivalent"],
        "equal_categories_inequivalent": same_categories["inequivalent"],
        "contracts_differ": contracts["contracts_differ"],
        "refused_new": contracts["refused_new"],
        "erased_new": contracts["erased_new"],
        "code_collapsed": collapse["collapsed"],
        "components": {
            "empty": graphs["empty"],
            "loop": graphs["loop"],
            "edge": graphs["edge"],
            "triangle": graphs["triangle"],
            "reduced_empty": graphs["reduced_empty"],
        },
        "recovered_cycle": recovered,
        "two_point_boundary": two_point["boundary"],
        "two_point_admits_retraction": two_point["admits_retraction"],
        "triangle_cycle_boundary": triangle["cycle_boundary"],
        "triangle_admits_retraction": triangle["admits_retraction"],
        "descent": descent["descended"],
        "blocked_descent": blocked["descended"],
        "chsh": {
            "selected": chsh["selected"],
            "other": chsh["other"],
            "required_product": chsh["required_product"],
            "assignment_products": chsh["assignment_products"],
        },
        "grammar_names": grammar["names"],
        "grammar_matches": grammar["matches"],
        "proved_ids": ledger["proved"],
        "withdrawn_names": WITHDRAWN_NAMES,
        "survivor_not_theorem": bounds["survivor_not_theorem"],
        "physics_withdrawn": bounds["physics_withdrawn"],
        "edge_multiset_same": edges["same_edge_multiset"],
        "traversal_same": edges["same_traversal"],
    }
