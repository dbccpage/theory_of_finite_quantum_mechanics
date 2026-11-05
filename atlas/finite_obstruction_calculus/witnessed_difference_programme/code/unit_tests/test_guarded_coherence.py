"""P.18 guarded coherence certificates: hand-written oracles and native replay.

The pure tests use tiny problems in the real problem schema, legality oracles
written here by hand and certificates whose counts were derived by hand (see
the comments on each case). Native tests need the explicitly configured owner.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from itertools import permutations
from pathlib import Path
from types import SimpleNamespace

import pytest

PAPER = next(p for p in Path(__file__).resolve().parents
             if (p / "witnessed_difference_programme.md").exists())
sys.path.insert(0, str(PAPER))
from scripts import check_causal_execution as causal  # noqa: E402
from scripts import check_guarded_coherence as guarded  # noqa: E402

CERTIFICATES = PAPER / "code/causal_certificates"
NATIVE_ENV = ("WDP_CAUSAL_NATIVE_BIN", "WDP_CAUSAL_BUILD_RECEIPT", "WDP_CAUSAL_SOURCE_ROOT")
ZERO = "zero-count remove"
GUARD = "hand-declared guard"


def assertion(tag: str, predecessors: tuple[str, ...] = ()) -> dict:
    return {"tag": tag, "kind": "add_assertion", "relation": "r", "tokens": ["origin", "origin"],
            "predecessors": list(predecessors)}


def removal(tag: str, predecessors: tuple[str, ...] = ()) -> dict:
    return {"tag": tag, "kind": "remove", "relation": "r", "tokens": ["origin", "origin"],
            "predecessors": list(predecessors)}


def birth(token: str) -> dict:
    return {"tag": f"birth-{token}", "kind": "add_term", "birth": token, "predecessors": []}


def problem_of(events: list[dict], count: int) -> dict:
    return {"schema": "wdp-causal-problem-v1",
            "initial": {"terms": ["t0"], "r": [str(count)], "s": ["0"], "filled": []},
            "initial_tokens": ["origin"], "events": events,
            "protected_prices": ["assertion_additions"]}


def file_bytes(problem: dict) -> bytes:
    return (json.dumps(problem, indent=2) + "\n").encode()


def count_guard(problem: dict):
    """Hand-written stand-in for the positive-count Remove guard of P.18."""
    events, start = problem["events"], int(problem["initial"]["r"][0])

    def legality(order):
        count = start
        for e in order:
            if events[e]["kind"] == "add_assertion":
                count += 1
            elif events[e]["kind"] == "remove":
                if count == 0:
                    return f"{ZERO}: {events[e]['tag']}"
                count -= 1
        return None

    return legality


def skeleton(problem: dict, extensions: int, legal: list[list[int]], refused: list[dict]) -> dict:
    return {"schema": "wdp-guarded-coherence-v1", "authority_effect": "None",
            "problem_file_sha256": hashlib.sha256(file_bytes(problem)).hexdigest(),
            "event_count": len(problem["events"]), "linear_extensions": extensions,
            "legal_orders": legal, "refused_orders": refused, "coherence_witnesses": [],
            "star_base": None, "separating_cocycle": None}


def path_case():
    """a=Add, x=Remove, b=birth; count 0. Legal iff a before x: a 3-vertex path."""
    problem = problem_of([assertion("assert-a"), removal("remove-x"), birth("b")], 0)
    reason = f"{ZERO}: remove-x"
    cert = skeleton(problem, 6, [[0, 1, 2], [0, 2, 1], [2, 0, 1]],
                    [{"order": o, "reason": reason} for o in ([1, 0, 2], [1, 2, 0], [2, 1, 0])])
    cert.update(edges=2, squares=0, hexagons=0, kind_compatible=True, star_base=[2, 0, 1],
                components=[{"vertices": [0, 1, 2], "edges": 2, "faces": 0, "h1_rank": 0}],
                coherence_witnesses=[{
                    "source_order": [0, 1, 2], "target_order": [0, 1, 2],
                    "source_word": [], "target_word": [1, 1],
                    "replacements": [{"kind": "backtrack", "offset": 0, "before": [],
                                      "after": [1, 1]}]}])
    return problem, cert, count_guard(problem)


def isolated_case():
    """Four-event P.18-style counterexample: x<a, y<b, count 1; two isolated histories."""
    problem = problem_of([removal("remove-x"), assertion("assert-a", ("remove-x",)),
                          removal("remove-y"), assertion("assert-b", ("remove-y",))], 1)
    refused = [{"order": [0, 2, 1, 3], "reason": f"{ZERO}: remove-y"},
               {"order": [0, 2, 3, 1], "reason": f"{ZERO}: remove-y"},
               {"order": [2, 0, 1, 3], "reason": f"{ZERO}: remove-x"},
               {"order": [2, 0, 3, 1], "reason": f"{ZERO}: remove-x"}]
    cert = skeleton(problem, 6, [[0, 1, 2, 3], [2, 3, 0, 1]], refused)
    cert.update(edges=0, squares=0, hexagons=0, kind_compatible=False,
                components=[{"vertices": [0], "edges": 0, "faces": 0, "h1_rank": 0},
                            {"vertices": [1], "edges": 0, "faces": 0, "h1_rank": 0}])
    return problem, cert, count_guard(problem)


def annulus_case():
    """Four births with 0123 and 3210 refused: the S4 permutohedron minus two antipodes.

    36-6=30 edges, 6-2=4 squares, 8-4=4 hexagons, one component, Euler
    characteristic 0, H1 rank 1. The cocycle is dual to the face path
    H(last=3) - Q{0,2} - H(last=1) - H(first=3) between the two holes.
    """
    problem = problem_of([birth("b"), birth("c"), birth("d"), birth("e")], 0)
    refused = {(0, 1, 2, 3), (3, 2, 1, 0)}
    legal = [list(o) for o in permutations(range(4)) if o not in refused]
    cert = skeleton(problem, 24, legal, [{"order": [0, 1, 2, 3], "reason": GUARD},
                                         {"order": [3, 2, 1, 0], "reason": GUARD}])
    cert.update(edges=30, squares=4, hexagons=4, kind_compatible=True,
                components=[{"vertices": list(range(22)), "edges": 30, "faces": 8, "h1_rank": 1}],
                coherence_witnesses=[
                    {"source_order": [0, 2, 3, 1], "target_order": [3, 2, 0, 1],
                     "source_word": [0, 1, 0], "target_word": [1, 0, 1],
                     "replacements": [{"kind": "braid", "offset": 0, "before": [0, 1, 0],
                                       "after": [1, 0, 1]}]},
                    {"source_order": [0, 2, 1, 3], "target_order": [2, 3, 0, 1],
                     "source_word": [0, 2, 1], "target_word": [2, 0, 1],
                     "replacements": [{"kind": "square", "offset": 0, "before": [0, 2],
                                       "after": [2, 0]}]}],
                separating_cocycle={
                    "component": 0, "root_order": [0, 2, 1, 3], "target_order": [2, 0, 1, 3],
                    "word_a": [0], "word_b": [2, 1, 2, 1, 0, 2, 1, 0, 1],
                    "edge_values": [{"order": [0, 2, 1, 3], "position": 0, "value": "1"},
                                    {"order": [0, 2, 3, 1], "position": 0, "value": "1"},
                                    {"order": [3, 0, 2, 1], "position": 1, "value": "1"}],
                    "value_a": "1", "value_b": "0"})
    return problem, cert, (lambda order: GUARD if order in refused else None)


CASES = {"path": path_case, "isolated": isolated_case, "annulus": annulus_case}


def check(problem: dict, cert: dict, oracle, data: bytes | None = None) -> dict:
    return guarded.verify_guarded(problem, file_bytes(problem) if data is None else data,
                                  cert, oracle)


@pytest.mark.parametrize("name,expected", [
    ("path", {"legal_orders": 3, "refused_orders": 3, "edges": 2, "squares": 0, "hexagons": 0,
              "components": 1, "star_base_checked": True, "replacements_checked": 1}),
    ("isolated", {"legal_orders": 2, "refused_orders": 4, "edges": 0, "components": 2,
                  "kind_compatible": False, "separating_cocycle_checked": False}),
    ("annulus", {"legal_orders": 22, "edges": 30, "squares": 4, "hexagons": 4, "components": 1,
                 "replacements_checked": 2, "separating_cocycle_checked": True}),
])
def test_hand_built_certificates_pass(name, expected):
    problem, cert, oracle = CASES[name]()
    before = causal.encoded(cert)
    receipt = check(problem, cert, oracle)
    assert receipt["status"] == "PASS" and receipt["authority_effect"] == "None"
    assert receipt["fresh_native_replay"] is False and receipt["h1_rank_recomputed"] is True
    assert {key: receipt[key] for key in expected} == expected
    assert causal.encoded(cert) == before


@pytest.mark.parametrize("name", sorted(CASES))
def test_oracle_consulted_on_every_schedule(name):
    problem, cert, oracle = CASES[name]()
    seen = []

    def counting(order):
        seen.append(order)
        return oracle(order)

    check(problem, cert, counting)
    assert len(seen) == len(set(seen)) == cert["linear_extensions"]


def test_changed_problem_bytes_refuse():
    problem, cert, oracle = path_case()
    with pytest.raises(causal.CertificateRefusal, match="bytes differ"):
        check(problem, cert, oracle, file_bytes(problem) + b" ")
    changed = copy.deepcopy(problem)
    changed["events"][2]["birth"] = "renamed"
    with pytest.raises(causal.CertificateRefusal, match="differs from the problem file bytes"):
        check(changed, cert, oracle, file_bytes(problem))
    cert["problem_file_sha256"] = hashlib.sha256(b"not json").hexdigest()
    with pytest.raises(causal.CertificateRefusal, match="not JSON"):
        check(problem, cert, oracle, b"not json")


def legal_as_refused(cert):
    cert["legal_orders"].remove([0, 2, 1])
    cert["refused_orders"].append({"order": [0, 2, 1], "reason": f"{ZERO}: remove-x"})


def merged_components(cert):
    cert["components"] = [{"vertices": [0, 1], "edges": 0, "faces": 0, "h1_rank": 0}]


def braid_through_refused(cert):
    # 0213 -s1-> 0123 is refused, so the braid's alternate route is illegal.
    cert["coherence_witnesses"] = [{
        "source_order": [0, 2, 1, 3], "target_order": [1, 2, 0, 3],
        "source_word": [0, 1, 0], "target_word": [1, 0, 1],
        "replacements": [{"kind": "braid", "offset": 0, "before": [0, 1, 0], "after": [1, 0, 1]}]}]


def backtrack_through_refused(cert):
    witness = cert["coherence_witnesses"][0]
    witness["target_word"] = [0, 0]
    witness["replacements"][0]["after"] = [0, 0]


def cocycle_on_path(cert):
    cert["separating_cocycle"] = {
        "component": 0, "root_order": [0, 1, 2], "target_order": [0, 2, 1], "word_a": [1],
        "word_b": [1], "edge_values": [], "value_a": "0", "value_b": "1"}


def set_in(path, value):
    def mutate(cert):
        target = cert
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    return mutate


COCYCLE = ("separating_cocycle",)
EDGE = COCYCLE + ("edge_values",)
WITNESS = ("coherence_witnesses",)


@pytest.mark.parametrize("name,mutate,match", [
    ("path", set_in(("authority_effect",), "Grant"), "authority"),
    ("path", set_in(("schema",), "wdp-guarded-coherence-v0"), "unknown guarded"),
    ("path", set_in(("event_count",), 4), "event_count"),
    ("path", set_in(("linear_extensions",), 5), "linear extension"),
    ("path", set_in(("extra",), 1), "field mismatch"),
    ("path", legal_as_refused, "listed as refused"),
    ("path", set_in(("refused_orders", 0, "reason"), "other reason"), "refusal reason"),
    ("path", lambda c: c["refused_orders"].pop(), "omitted"),
    ("path", lambda c: c["legal_orders"].reverse(), "sorted"),
    ("path", set_in(("legal_orders", 0), [True, 1, 2]), "event indices"),
    ("isolated", merged_components, "component vertex sets"),
    ("annulus", set_in(("edges",), 31), "edge count mismatch"),
    ("annulus", set_in(("squares",), 5), "square count"),
    ("annulus", set_in(("hexagons",), 3), "hexagon count"),
    ("annulus", set_in(("components", 0, "edges"), 29), "component edge count"),
    ("annulus", set_in(("components", 0, "faces"), 7), "component face count"),
    ("path", set_in(("components", 0, "h1_rank"), 1), "cycle-rank"),
    # Inside the cycle-rank bounds [1, 9] but not the exact rank 1.
    ("annulus", set_in(("components", 0, "h1_rank"), 9), "exact rational rank"),
    ("annulus", set_in(("components", 0, "h1_rank"), 2), "exact rational rank"),
    ("annulus", set_in(WITNESS + (1, "replacements", 0, "offset"), 1), "offset"),
    ("annulus", set_in(WITNESS + (0, "replacements", 0, "offset"), True), "natural"),
    ("annulus", set_in(WITNESS + (0, "replacements", 0, "kind"), "square"), "kind mismatch"),
    ("annulus", set_in(WITNESS + (1, "replacements", 0, "after"), [0, 2]), "local relation"),
    ("annulus", set_in(WITNESS + (0, "source_order"), [0, 1, 2, 3]), "not legal"),
    ("annulus", set_in(WITNESS + (1, "target_order"), [2, 0, 3, 1]), "misses target"),
    ("annulus", braid_through_refused, "not legal"),
    ("path", backtrack_through_refused, "not legal"),
    ("annulus", set_in(EDGE + (2, "value"), "2"), "not closed on hexagon"),
    ("annulus", set_in(EDGE + (1, "value"), "2"), "not closed on square"),
    ("annulus", set_in(EDGE + (0,), {"order": [2, 0, 1, 3], "position": 0, "value": "-1"}),
     "lexicographically smaller"),
    ("annulus", set_in(EDGE + (0,), {"order": [0, 1, 2, 3], "position": 0, "value": "1"}),
     "non-edge"),
    ("annulus", set_in(COCYCLE + ("value_b",), "1/2"), "differs from value_b"),
    ("annulus", set_in(COCYCLE + ("component",), 1), "outside components"),
    ("annulus", set_in(COCYCLE + ("word_b",), [2, 1, 2, 1, 0, 2, 1, 0]), "misses target"),
    ("path", cocycle_on_path, "zero h1_rank"),
    ("isolated", set_in(("star_base",), [0, 1, 2, 3]), "lower-cover"),
    ("path", set_in(("star_base",), None), "star_base omitted"),
    ("annulus", set_in(("star_base",), [0, 2, 1, 3]), "lower-cover"),
    ("annulus", set_in(("star_base",), [0, 1, 2, 3]), "not a legal order"),
    ("path", set_in(("kind_compatible",), False), "kind_compatible"),
    ("isolated", set_in(("kind_compatible",), True), "kind_compatible"),
    ("annulus", set_in(("kind_compatible",), 1), "kind_compatible"),
])
def test_altered_certificate_refuses(name, mutate, match):
    problem, cert, oracle = CASES[name]()
    mutate(cert)
    before = causal.encoded(cert)
    with pytest.raises(causal.CertificateRefusal, match=match):
        check(problem, cert, oracle)
    assert causal.encoded(cert) == before


def test_equal_cocycle_values_do_not_separate():
    problem, cert, oracle = annulus_case()
    cert["separating_cocycle"].update(word_b=[0], value_b="1")
    with pytest.raises(causal.CertificateRefusal, match="do not separate"):
        check(problem, cert, oracle)


@pytest.mark.parametrize("value", [1.0, 1, True, "1.0", "1/1", "2/2", "0/3", "-0", "01", "+1"])
@pytest.mark.parametrize("slot", ["edge", "value_a"])
def test_cocycle_values_must_be_exact_rational_strings(value, slot):
    problem, cert, oracle = annulus_case()
    if slot == "edge":
        cert["separating_cocycle"]["edge_values"][0]["value"] = value
    else:
        cert["separating_cocycle"]["value_a"] = value
    with pytest.raises(causal.CertificateRefusal, match="rational|negative zero"):
        check(problem, cert, oracle)


def test_fractional_cocycle_is_exact():
    problem, cert, oracle = annulus_case()
    for item in cert["separating_cocycle"]["edge_values"]:
        item["value"] = "-2/3"
    cert["separating_cocycle"]["value_a"] = "-2/3"
    assert check(problem, cert, oracle)["separating_cocycle_checked"] is True


def test_oracle_must_return_reason_or_none():
    problem, cert, _ = path_case()
    with pytest.raises(causal.CertificateRefusal, match="legality oracle"):
        check(problem, cert, lambda order: False)


def stand_in(monkeypatch, stdout: str, returncode: int):
    def run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0] if args else kwargs.get("args"), returncode,
                                           stdout=stdout, stderr="")
    monkeypatch.setattr(guarded.subprocess, "run", run)
    return SimpleNamespace(binary=Path("native-stand-in"), calls=0)


def native_output(**fields) -> str:
    return json.dumps({"schema": "wdp-source25-native-v1", "authority_effect": "None", **fields})


CHANGES = [{"kind": "add_term"}]


def test_try_replay_returns_native_refusal_reason(monkeypatch):
    owner = stand_in(monkeypatch, native_output(status="REFUSE", reason="guard refused"), 2)
    assert guarded.try_replay(owner, {}, CHANGES) == (None, "guard refused")
    assert owner.calls == 1


def test_try_replay_returns_bound_run(monkeypatch):
    run = {"changes": CHANGES, "states": [{}, {}]}
    owner = stand_in(monkeypatch, native_output(status="PASS", run=run), 0)
    assert guarded.try_replay(owner, {}, CHANGES) == (run, None)


@pytest.mark.parametrize("stdout,code,match", [
    (native_output(status="REFUSE", reason="x"), 0, "refusal protocol"),
    (native_output(status="REFUSE", reason="x", extra=1), 2, "refusal protocol"),
    (native_output(status="REFUSE", reason=""), 2, "lacks a reason"),
    (native_output(status="PASS", run={"changes": [], "states": [{}, {}]}), 0, "binding"),
    (native_output(status="PASS", run={"changes": CHANGES, "states": [{}]}), 0, "states omitted"),
    (native_output(status="PASS", run={"changes": CHANGES, "states": [{}, {}]}), 2, "status"),
    (json.dumps({"schema": "wdp-source25-native-v1", "authority_effect": "Grant",
                 "status": "PASS"}), 0, "protocol mismatch"),
    ("not json", 0, "not JSON"),
])
def test_try_replay_refuses_protocol_violations(monkeypatch, stdout, code, match):
    owner = stand_in(monkeypatch, stdout, code)
    with pytest.raises(causal.CertificateRefusal, match=match):
        guarded.try_replay(owner, {}, CHANGES)


def test_try_replay_transport_failure_refuses(monkeypatch):
    def run(*args, **kwargs):
        raise OSError("absent")
    monkeypatch.setattr(guarded.subprocess, "run", run)
    with pytest.raises(causal.CertificateRefusal, match="transport unavailable"):
        guarded.try_replay(SimpleNamespace(binary=Path("absent"), calls=0), {}, CHANGES)


def test_command_line_requires_explicit_native_owner(capsys):
    with pytest.raises(SystemExit) as exit_info:
        guarded.main(["check", "problem.json", "certificate.json"])
    assert exit_info.value.code == 2
    assert "--native-bin" in capsys.readouterr().err


@pytest.fixture(scope="module")
def native():
    if not all(os.environ.get(n) for n in NATIVE_ENV):
        pytest.skip("fresh native integration requires explicit binary, build receipt "
                    "and source root")
    return causal.NativeOwner(*(Path(os.environ[n]) for n in NATIVE_ENV))


def retained_pairs() -> list:
    cases = []
    for problem in sorted(CERTIFICATES.glob("guarded_*_problem.json")):
        certificate = problem.with_name(problem.name.removesuffix("_problem.json")
                                        + "_certificate.json")
        absent = pytest.mark.skip(reason=f"{certificate.name} absent")
        marks = () if certificate.exists() else absent
        cases.append(pytest.param(problem, certificate, id=problem.stem, marks=marks))
    return cases or [pytest.param(None, None, id="none-retained", marks=pytest.mark.skip(
        reason="no retained guarded_*_problem.json with a matching guarded_*_certificate.json"))]


@pytest.mark.monorepo
@pytest.mark.parametrize("problem_path,certificate_path", retained_pairs())
def test_native_retained_guarded_certificate(problem_path, certificate_path, native):
    problem, certificate = causal.read_json(problem_path), causal.read_json(certificate_path)
    receipt = guarded.verify_native(problem, problem_path.read_bytes(), certificate, native)
    assert receipt["status"] == "PASS" and receipt["fresh_native_replay"] is True
    assert receipt["native_calls"] >= receipt["linear_extensions"]
    assert receipt["framed_edges_checked"] == receipt["edges"]
    moved = copy.deepcopy(certificate)
    order = moved["legal_orders"].pop(0)
    moved["refused_orders"].append({"order": order, "reason": "forged refusal"})
    with pytest.raises(causal.CertificateRefusal, match="listed as refused"):
        guarded.verify_native(problem, problem_path.read_bytes(), moved, native)


@pytest.mark.monorepo
def test_native_p18_counterexample_has_two_isolated_histories(native):
    # P.18 table: p, x, a<x, y, b<y on one term with zero R count.
    problem = problem_of([assertion("p"), removal("x"), assertion("a", ("x",)), removal("y"),
                          assertion("b", ("y",))], 0)
    oracle = guarded.NativeLegality(problem, native)
    _, before = causal.admit_problem(problem)
    verdict = {tuple(o): oracle(tuple(o)) for o in causal.schedules(before)}
    assert len(verdict) == 30
    assert {o for o, reason in verdict.items() if reason is None} == {(0, 1, 2, 3, 4),
                                                                      (0, 3, 4, 1, 2)}
    refused = [{"order": list(o), "reason": r} for o, r in sorted(verdict.items()) if r]
    cert = skeleton(problem, 30, [[0, 1, 2, 3, 4], [0, 3, 4, 1, 2]], refused)
    cert.update(edges=0, squares=0, hexagons=0, kind_compatible=False,
                components=[{"vertices": [0], "edges": 0, "faces": 0, "h1_rank": 0},
                            {"vertices": [1], "edges": 0, "faces": 0, "h1_rank": 0}])
    receipt = guarded.verify_native(problem, file_bytes(problem), cert, native)
    assert receipt["components"] == 2 and receipt["fresh_native_replay"] is True


@pytest.mark.monorepo
def test_native_all_order_legal_antichain_frames_every_edge(native):
    # Four independent events: the full S4 permutohedron, 36 edges, 6 squares, 8 hexagons.
    path = CERTIFICATES / "antichain_problem.json"
    problem = causal.read_json(path)
    cert = {"schema": "wdp-guarded-coherence-v1", "authority_effect": "None",
            "problem_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "event_count": 4, "linear_extensions": 24,
            "legal_orders": [list(o) for o in permutations(range(4))], "refused_orders": [],
            "edges": 36, "squares": 6, "hexagons": 8,
            "components": [{"vertices": list(range(24)), "edges": 36, "faces": 14, "h1_rank": 0}],
            "kind_compatible": True, "star_base": [0, 1, 2, 3], "separating_cocycle": None,
            "coherence_witnesses": [{"source_order": [0, 1, 2, 3], "target_order": [2, 1, 0, 3],
                                     "source_word": [0, 1, 0], "target_word": [1, 0, 1],
                                     "replacements": [{"kind": "braid", "offset": 0,
                                                       "before": [0, 1, 0], "after": [1, 0, 1]}]}]}
    receipt = guarded.verify_native(problem, path.read_bytes(), cert, native)
    assert receipt["framed_edges_checked"] == 36 and receipt["fresh_native_replay"] is True
