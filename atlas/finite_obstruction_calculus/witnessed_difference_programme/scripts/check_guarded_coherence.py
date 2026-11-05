"""Replay P.18 guarded-history coherence certificates against an explicit owner.

A ``wdp-guarded-coherence-v1`` certificate is a proposal produced elsewhere; it
is never trusted. From the separately supplied problem file this checker
recomputes the legal/refused partition of every linear extension, the
legal-swap graph with its square and hexagon faces and components, kind
compatibility, and each component's rational H1 rank by exact elimination. A
submitted star base is checked; when none is submitted, the checker confirms
that no legal order is one. It replays every submitted local 3-witness and any
separating cocycle with exact rationals.

Legality comes from a supplied oracle. The command line builds that oracle
only from the configured native owner (explicit binary, build receipt and
source root); there is no discovery and no Python transition fallback.
AuthorityEffect: None.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections.abc import Callable
from fractions import Fraction
from itertools import permutations
from math import gcd
from pathlib import Path

if __package__:
    from .check_causal_execution import (
        CertificateRefusal,
        NativeOwner,
        admit_problem,
        arguments,
        descriptors,
        digest,
        encoded,
        execute_order,
        fields,
        natural,
        read_json,
        require,
        same,
        schedules,
    )
    from .check_causal_three_cells import replacement_kind
else:  # Direct standalone invocation from the scripts directory.
    from check_causal_execution import (
        CertificateRefusal,
        NativeOwner,
        admit_problem,
        arguments,
        descriptors,
        digest,
        encoded,
        execute_order,
        fields,
        natural,
        read_json,
        require,
        same,
        schedules,
    )
    from check_causal_three_cells import replacement_kind

SCHEMA = "wdp-guarded-coherence-v1"
CERTIFICATE_FIELDS = {
    "schema", "authority_effect", "problem_file_sha256", "event_count", "linear_extensions",
    "legal_orders", "refused_orders", "edges", "squares", "hexagons", "components",
    "kind_compatible", "star_base", "coherence_witnesses", "separating_cocycle",
}
COCYCLE_FIELDS = {"component", "root_order", "target_order", "word_a", "word_b", "edge_values",
                  "value_a", "value_b"}
WITNESS_FIELDS = {"source_order", "target_order", "source_word", "target_word", "replacements"}
KIND_RANK = {"add_term": 0, "add_assertion": 1, "fill": 1, "identify": 2, "remove": 3}
WORD_BOUND = 1000
# Per-witness replacement budget; equals MAX_REPLACEMENTS in omega_wdp::genesis_guarded_history.
REPLACEMENT_BOUND = 250_000
WITNESS_BOUND = 1000
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?")
_HEX = re.compile(r"[0-9a-f]{64}")
_NATIVE_SCHEMA = "wdp-source25-native-v1"

Order = tuple[int, ...]
Edge = tuple[Order, int]
Face = tuple[str, Order, list[int]]
Legality = Callable[[Order], "str | None"]
EdgeCheck = Callable[[Order, int], None]


def swap(order: Order, position: int) -> Order:
    items = list(order)
    items[position], items[position + 1] = items[position + 1], items[position]
    return tuple(items)


def order_of(value: object, n: int, where: str) -> Order:
    require(type(value) is list and len(value) == n and all(type(e) is int for e in value),
            f"{where}: expected an order of {n} event indices")
    require(sorted(value) == list(range(n)), f"{where}: not a permutation of the events")
    return tuple(value)


def rational(value: object, where: str) -> Fraction:
    """Exact rational from canonical "p" or reduced "p/q" with q > 1."""
    require(type(value) is str and len(value) <= 1000 and _RATIONAL.fullmatch(value) is not None,
            f"{where}: expected exact rational string p or p/q")
    numerator, _, denominator = value.partition("/")
    require(numerator != "-0", f"{where}: negative zero")
    p = int(numerator)
    if not denominator:
        return Fraction(p)
    q = int(denominator)
    require(q > 1 and gcd(abs(p), q) == 1,
            f"{where}: rational not reduced with denominator above one")
    return Fraction(p, q)


def replay_legal(source: Order, word: object, legal: set[Order], where: str) -> Order:
    """Apply adjacent swaps; every intermediate order must be legal."""
    require(type(word) is list and len(word) <= WORD_BOUND,
            f"{where}: swap word must be an array within bound")
    require(source in legal, f"{where}: source order {list(source)} is not legal")
    current = source
    for step, position in enumerate(word):
        natural(position, f"{where}: swap position")
        require(position + 1 < len(current), f"{where}: swap position {position} outside history")
        current = swap(current, position)
        require(current in legal,
                f"{where}: intermediate order {list(current)} after step {step} is not legal")
    return current


def cochain_value(values: dict[Edge, Fraction], start: Order, word: list[int]) -> Fraction:
    """phi along a word; edge (h,p) is keyed by its lexicographically smaller end."""
    total, current = Fraction(0), start
    for position in word:
        target = swap(current, position)
        if current < target:
            total += values.get((current, position), Fraction(0))
        else:
            total -= values.get((target, position), Fraction(0))
        current = target
    return total


def legal_complex(legal_orders: list[Order],
                  n: int) -> tuple[list[Edge], dict[frozenset[Order], Face]]:
    """Realized swap edges and vertex-set-deduplicated faces with one boundary word."""
    legal = set(legal_orders)
    edges: list[Edge] = []
    faces: dict[frozenset[Order], Face] = {}
    for h in legal_orders:
        for p in range(n - 1):
            g = swap(h, p)
            if g in legal and h < g:
                edges.append((h, p))
        for i in range(n - 1):
            hi = swap(h, i)
            for j in range(i + 2, n - 1):
                square = frozenset((h, hi, swap(h, j), swap(hi, j)))
                if square <= legal:
                    faces.setdefault(square, ("square", h, [i, j, i, j]))
        for i in range(n - 2):
            hexagon = frozenset(h[:i] + perm + h[i + 3:] for perm in permutations(h[i:i + 3]))
            if hexagon <= legal:
                faces.setdefault(hexagon, ("hexagon", h, [i, i + 1] * 3))
    return edges, faces


def face_boundary(start: Order, word: list[int]) -> dict[Edge, int]:
    """Signed edge incidences of a face boundary, edges keyed as in cochain_value."""
    boundary: dict[Edge, int] = {}
    current = start
    for position in word:
        target = swap(current, position)
        key, sign = ((current, position), 1) if current < target else ((target, position), -1)
        boundary[key] = boundary.get(key, 0) + sign
        current = target
    return {edge: sign for edge, sign in boundary.items() if sign}


def rational_rank(rows: list[dict[Edge, int]]) -> int:
    """Rank over Q of sparse integer rows by exact Gaussian elimination."""
    pivots: dict[Edge, dict[Edge, Fraction]] = {}
    rank = 0
    for row in rows:
        vector = {key: Fraction(value) for key, value in row.items()}
        while vector:
            lead = min(vector)
            pivot = pivots.get(lead)
            if pivot is None:
                pivots[lead] = vector
                rank += 1
                break
            factor = vector[lead] / pivot[lead]
            for key, value in pivot.items():
                updated = vector.get(key, Fraction(0)) - factor * value
                if updated:
                    vector[key] = updated
                else:
                    vector.pop(key, None)
    return rank


def components_of(legal_orders: list[Order], edges: list[Edge]) -> list[frozenset[int]]:
    index = {h: k for k, h in enumerate(legal_orders)}
    parent = list(range(len(legal_orders)))

    def root(k: int) -> int:
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    for h, p in edges:
        a, b = root(index[h]), root(index[swap(h, p)])
        if a != b:
            parent[max(a, b)] = min(a, b)
    groups: dict[int, set[int]] = {}
    for k in range(len(legal_orders)):
        groups.setdefault(root(k), set()).add(k)
    return [frozenset(group) for group in groups.values()]


def _partition(certificate: dict, orders: list[Order], legality: Legality,
               n: int) -> list[Order]:
    verdict: dict[Order, str | None] = {}
    for order in orders:
        reason = legality(order)
        require(reason is None or (type(reason) is str and bool(reason)),
                "legality oracle returned neither None nor a refusal reason")
        verdict[order] = reason
    require(any(reason is None for reason in verdict.values()), "no legal complete execution")
    listed = certificate["legal_orders"]
    require(type(listed) is list and len(listed) <= len(orders),
            "legal_orders must be a bounded array")
    legal_orders = [order_of(value, n, "legal order") for value in listed]
    require(legal_orders == sorted(set(legal_orders)),
            "legal_orders not lexicographically sorted and duplicate-free")
    for order in legal_orders:
        require(order in verdict, f"legal order {list(order)} is not a linear extension")
    refused = certificate["refused_orders"]
    require(type(refused) is list and len(refused) <= len(orders),
            "refused_orders must be a bounded array")
    seen: set[Order] = set()
    for item in refused:
        fields(item, {"order", "reason"}, "refused order")
        order = order_of(item["order"], n, "refused order")
        require(order in verdict, f"refused order {list(order)} is not a linear extension")
        require(order not in seen, f"refused order {list(order)} listed twice")
        seen.add(order)
        require(verdict[order] is not None, f"legal order {list(order)} listed as refused")
        require(type(item["reason"]) is str and item["reason"] == verdict[order],
                f"refusal reason for {list(order)} differs from the owner")
    for order in legal_orders:
        require(verdict[order] is None,
                f"order {list(order)} listed legal but refused: {verdict[order]}")
    listed_legal = set(legal_orders)
    for order, reason in verdict.items():
        if reason is None:
            require(order in listed_legal, f"legal order {list(order)} omitted")
        else:
            require(order in seen, f"refused order {list(order)} omitted")
    return legal_orders


def _components(certificate: dict, legal_orders: list[Order], edges: list[Edge],
                faces: dict[frozenset[Order], Face]) -> list[frozenset[int]]:
    index = {h: k for k, h in enumerate(legal_orders)}
    actual = components_of(legal_orders, edges)
    owner = {k: c for c, members in enumerate(actual) for k in members}
    edge_counts, face_counts = [0] * len(actual), [0] * len(actual)
    boundaries: list[list[dict[Edge, int]]] = [[] for _ in actual]
    for h, _ in edges:
        edge_counts[owner[index[h]]] += 1
    for vertices, (_, start, word) in faces.items():
        c = owner[index[next(iter(vertices))]]
        face_counts[c] += 1
        boundaries[c].append(face_boundary(start, word))
    listed = certificate["components"]
    require(type(listed) is list and 0 < len(listed) <= len(legal_orders),
            "components must be a bounded array")
    declared: list[frozenset[int]] = []
    for item in listed:
        fields(item, {"vertices", "edges", "faces", "h1_rank"}, "component")
        vertices = item["vertices"]
        require(type(vertices) is list and bool(vertices),
                "component vertices must be a nonempty array")
        for k in vertices:
            natural(k, "component vertex")
            require(k < len(legal_orders), "component vertex outside legal_orders")
        require(len(set(vertices)) == len(vertices), "component vertex listed twice")
        declared.append(frozenset(vertices))
    require(sum(len(c) for c in declared) == len(legal_orders) and set(declared) == set(actual),
            "component vertex sets differ from the legal-swap graph")
    for item, vertices in zip(listed, declared):
        c = actual.index(vertices)
        require(natural(item["edges"], "component edges") == edge_counts[c],
                "component edge count mismatch")
        require(natural(item["faces"], "component faces") == face_counts[c],
                "component face count mismatch")
        rank = natural(item["h1_rank"], "component h1_rank")
        cycles = edge_counts[c] - len(vertices) + 1
        require(max(0, cycles - face_counts[c]) <= rank <= cycles,
                "component h1_rank outside cycle-rank bounds")
        # dim H1 = dim Z1 - rank of the face boundary map; Z1 has dimension E - V + 1.
        require(rank == cycles - rational_rank(boundaries[c]),
                "component h1_rank differs from the exact rational rank")
    return declared


def _replace(current: list[int], replacement: dict, step: str) -> list[int]:
    fields(replacement, {"kind", "offset", "before", "after"}, step)
    offset = natural(replacement["offset"], f"{step} offset")
    before, after = replacement["before"], replacement["after"]
    try:
        kind = replacement_kind(before, after)
    except ValueError as exc:
        raise CertificateRefusal(f"{step}: {exc}") from exc
    require(kind == replacement["kind"], f"{step}: replacement kind mismatch")
    require(offset + len(before) <= len(current), f"{step}: replacement offset outside word")
    require(same(current[offset:offset + len(before)], before),
            f"{step}: replacement offset does not match submitted side")
    return current[:offset] + after + current[offset + len(before):]


def _witnesses(certificate: dict, legal: set[Order], n: int) -> int:
    witnesses = certificate["coherence_witnesses"]
    require(type(witnesses) is list and len(witnesses) <= WITNESS_BOUND,
            "coherence_witnesses must be a bounded array")
    total = 0
    for w, witness in enumerate(witnesses):
        where = f"coherence witness {w}"
        fields(witness, WITNESS_FIELDS, where)
        source = order_of(witness["source_order"], n, f"{where} source")
        target = order_of(witness["target_order"], n, f"{where} target")
        for side in ("source_word", "target_word"):
            require(replay_legal(source, witness[side], legal, f"{where} {side}") == target,
                    f"{where}: {side} misses target order")
        replacements = witness["replacements"]
        require(type(replacements) is list and len(replacements) <= REPLACEMENT_BOUND,
                f"{where}: replacement bound")
        current = list(witness["source_word"])
        for r, replacement in enumerate(replacements):
            step = f"{where} replacement {r}"
            current = _replace(current, replacement, step)
            require(replay_legal(source, current, legal, step) == target,
                    f"{step}: replacement changes target order")
            total += 1
        require(same(current, witness["target_word"]),
                f"{where}: replacement sequence misses target word")
    return total


def _cocycle(certificate: dict, legal_orders: list[Order], declared: list[frozenset[int]],
             faces: dict[frozenset[Order], Face], n: int) -> bool:
    cocycle = certificate["separating_cocycle"]
    if cocycle is None:
        return False
    fields(cocycle, COCYCLE_FIELDS, "separating_cocycle")
    legal = set(legal_orders)
    index = {h: k for k, h in enumerate(legal_orders)}
    k = natural(cocycle["component"], "cocycle component")
    require(k < len(declared), "cocycle component outside components")
    require(certificate["components"][k]["h1_rank"] > 0,
            "separating cocycle on a component with zero h1_rank")
    root = order_of(cocycle["root_order"], n, "cocycle root")
    target = order_of(cocycle["target_order"], n, "cocycle target")
    require(root in legal and index[root] in declared[k], "cocycle root outside declared component")
    items = cocycle["edge_values"]
    require(type(items) is list and len(items) <= max(1, len(legal_orders) * n),
            "edge_values must be a bounded array")
    values: dict[Edge, Fraction] = {}
    for item in items:
        fields(item, {"order", "position", "value"}, "cocycle edge value")
        h = order_of(item["order"], n, "cocycle edge order")
        p = natural(item["position"], "cocycle edge position")
        require(p + 1 < n, "cocycle edge position outside history")
        g = swap(h, p)
        require(h in legal and g in legal, f"cocycle value on non-edge {list(h)} position {p}")
        require(h < g, f"cocycle edge key {list(h)} is not the lexicographically smaller endpoint")
        require((h, p) not in values, f"cocycle edge {list(h)} position {p} listed twice")
        require(index[h] in declared[k], "cocycle edge outside declared component")
        values[(h, p)] = rational(item["value"], "cocycle edge value")
    for kind, start, word in faces.values():
        require(cochain_value(values, start, word) == 0,
                f"cocycle not closed on {kind} at {list(start)} word {word}")
    for side in ("word_a", "word_b"):
        require(replay_legal(root, cocycle[side], legal, f"cocycle {side}") == target,
                f"cocycle {side} misses target order")
    value_a = rational(cocycle["value_a"], "value_a")
    value_b = rational(cocycle["value_b"], "value_b")
    require(cochain_value(values, root, cocycle["word_a"]) == value_a,
            "phi(word_a) differs from value_a")
    require(cochain_value(values, root, cocycle["word_b"]) == value_b,
            "phi(word_b) differs from value_b")
    require(value_a != value_b, "cocycle values do not separate the two words")
    return True


def _lower_cover_failure(e0: Order, legal_orders: list[Order], legal: set[Order],
                         n: int) -> tuple[Order, int] | None:
    """First legal (h, p) whose lower cover relative to e0 is refused, or None for a star base."""
    position = {e: k for k, e in enumerate(e0)}
    for h in legal_orders:
        for p in range(n - 1):
            if position[h[p]] > position[h[p + 1]] and swap(h, p) not in legal:
                return h, p
    return None


def _star_base(base: object, legal_orders: list[Order], n: int) -> None:
    legal = set(legal_orders)
    if base is None:
        for e0 in legal_orders:
            require(_lower_cover_failure(e0, legal_orders, legal, n) is not None,
                    f"star_base omitted although legal order {list(e0)} is a star base")
        return
    e0 = order_of(base, n, "star_base")
    require(e0 in legal, "star_base is not a legal order")
    failure = _lower_cover_failure(e0, legal_orders, legal, n)
    if failure is not None:
        h, p = failure
        raise CertificateRefusal(f"star_base lower-cover fails at {list(h)} position {p}")


def verify_guarded(problem: dict, problem_bytes: bytes, certificate: dict, legality: Legality,
                   edge_frames: EdgeCheck | None = None) -> dict:
    """Recompute the guarded certificate; never repair or trust submitted data."""
    fields(certificate, CERTIFICATE_FIELDS, "certificate")
    require(certificate["schema"] == SCHEMA, "unknown guarded certificate")
    require(certificate["authority_effect"] == "None", "certificate authority")
    require(type(problem_bytes) is bytes, "problem file bytes required")
    declared_sha = certificate["problem_file_sha256"]
    require(type(declared_sha) is str and _HEX.fullmatch(declared_sha) is not None,
            "problem_file_sha256 not lowercase hex")
    require(hashlib.sha256(problem_bytes).hexdigest() == declared_sha,
            "problem file bytes differ from certificate")
    try:
        bound = same(json.loads(problem_bytes), problem)
    except ValueError as exc:
        raise CertificateRefusal(f"problem file bytes are not JSON: {exc}") from exc
    require(bound, "supplied problem differs from the problem file bytes")
    events, before = admit_problem(problem)
    n = len(events)
    require(natural(certificate["event_count"], "event_count") == n, "event_count mismatch")
    orders = [tuple(order) for order in schedules(before)]
    require(natural(certificate["linear_extensions"], "linear_extensions") == len(orders),
            "linear extension count mismatch")
    legal_orders = _partition(certificate, orders, legality, n)
    edges, faces = legal_complex(legal_orders, n)
    squares = sum(kind == "square" for kind, _, _ in faces.values())
    hexagons = len(faces) - squares
    require(natural(certificate["edges"], "edges") == len(edges), "edge count mismatch")
    require(natural(certificate["squares"], "squares") == squares, "square count mismatch")
    require(natural(certificate["hexagons"], "hexagons") == hexagons, "hexagon count mismatch")
    declared = _components(certificate, legal_orders, edges, faces)
    compatible = all(KIND_RANK[events[p]["kind"]] <= KIND_RANK[events[e]["kind"]]
                     for e in range(n) for p in range(n) if before[e] >> p & 1)
    require(type(certificate["kind_compatible"]) is bool
            and certificate["kind_compatible"] == compatible,
            "kind_compatible differs from the precedence closure")
    base = certificate["star_base"]
    _star_base(base, legal_orders, n)
    if edge_frames is not None:
        for h, p in edges:
            edge_frames(h, p)
    replacements = _witnesses(certificate, set(legal_orders), n)
    separated = _cocycle(certificate, legal_orders, declared, faces, n)
    return {"schema": "wdp-guarded-coherence-receipt-v1", "status": "PASS",
            "authority_effect": "None", "certificate_sha256": digest(certificate),
            "problem_file_sha256": declared_sha, "event_count": n,
            "linear_extensions": len(orders), "legal_orders": len(legal_orders),
            "refused_orders": len(orders) - len(legal_orders), "edges": len(edges),
            "squares": squares, "hexagons": hexagons, "components": len(declared),
            "kind_compatible": compatible, "star_base_checked": True,
            "star_base_absence_checked": base is None,
            "coherence_witnesses": len(certificate["coherence_witnesses"]),
            "replacements_checked": replacements, "separating_cocycle_checked": separated,
            "h1_rank_recomputed": True,
            "framed_edges_checked": len(edges) if edge_frames is not None else 0,
            "fresh_native_replay": False,
            "scope": "every linear extension of this supplied finite event family; "
                     "rational H1 rank recomputed per component"}


def try_replay(owner: NativeOwner, initial: dict,
               changes: list[dict]) -> tuple[dict | None, str | None]:
    """NativeOwner.replay protocol, returning a native refusal reason instead of raising."""
    owner.calls += 1
    request = encoded({"initial": initial, "changes": changes})
    try:
        process = subprocess.run([str(owner.binary)], input=request, check=False,
                                 capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CertificateRefusal(f"native transport unavailable: {exc}") from exc
    try:
        output = json.loads(process.stdout)
    except ValueError as exc:
        raise CertificateRefusal("native response is not JSON") from exc
    require(type(output) is dict and output.get("schema") == _NATIVE_SCHEMA
            and output.get("authority_effect") == "None", "native response protocol mismatch")
    if output.get("status") == "REFUSE":
        require(process.returncode == 2
                and set(output) == {"schema", "status", "authority_effect", "reason"},
                "native refusal protocol mismatch")
        reason = output["reason"]
        require(type(reason) is str and bool(reason), "native refusal lacks a reason")
        return None, reason
    require(process.returncode == 0 and output.get("status") == "PASS",
            "native response status mismatch")
    run = output.get("run")
    require(type(run) is dict and same(run.get("changes"), changes),
            "native descriptor binding mismatch")
    require(type(run.get("states")) is list and len(run["states"]) == len(changes) + 1,
            "native states omitted")
    return run, None


class NativeLegality:
    """Legality oracle and framed histories backed only by the configured native owner."""

    def __init__(self, problem: dict, owner: NativeOwner):
        self.problem, self.owner = problem, owner
        self.runs: dict[Order, dict] = {}
        self.histories: dict[Order, dict] = {}

    def __call__(self, order: Order) -> str | None:
        changes, _ = descriptors(self.problem, list(order))
        run, reason = try_replay(self.owner, self.problem["initial"], changes)
        if run is not None:
            self.runs[order] = run
        return reason

    def history(self, order: Order) -> dict:
        if order not in self.histories:
            require(order in self.runs, f"legal order {list(order)} lacks a native run")
            history = execute_order(self.problem, list(order), self.owner)
            require(same(history["native"], self.runs[order]),
                    "native replay is not deterministic")
            self.histories[order] = history
        return self.histories[order]

    def edge_frames(self, order: Order, position: int) -> None:
        old, new = self.history(order), self.history(swap(order, position))
        for offset, side in ((0, "source"), (2, "target")):
            require(same(old["frames"][position + offset]["boundary"],
                         new["frames"][position + offset]["boundary"]),
                    f"swap {side} frame changed at {list(order)} position {position}")


def verify_native(problem: dict, problem_bytes: bytes, certificate: dict,
                  owner: NativeOwner) -> dict:
    owner.verify_custody()
    calls = owner.calls
    oracle = NativeLegality(problem, owner)
    receipt = verify_guarded(problem, problem_bytes, certificate, oracle,
                             edge_frames=oracle.edge_frames)
    owner.verify_custody()
    receipt.update(fresh_native_replay=True, native_binding=owner.binding,
                   native_calls=owner.calls - calls)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("check",))
    parser.add_argument("problem", type=Path)
    parser.add_argument("certificate", type=Path)
    arguments(parser)
    args = parser.parse_args(argv)
    try:
        owner = NativeOwner(args.native_bin, args.native_build_receipt, args.source_root)
        receipt = verify_native(read_json(args.problem), args.problem.read_bytes(),
                                read_json(args.certificate), owner)
    except CertificateRefusal as exc:
        print(encoded({"status": "REFUSE", "authority_effect": "None", "reason": str(exc)}))
        return 2
    print(encoded(receipt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
