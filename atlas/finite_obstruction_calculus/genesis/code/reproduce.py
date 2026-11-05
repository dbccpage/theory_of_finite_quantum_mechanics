"""Cold mathematical replay with the frozen Python model and native Rust.

No monorepo imports. The full mode compares every context observation and
portable key, rather than accepting a native program's self-reported PASS.
"""
from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

from derivation.candidates import (
    Bounds,
    NewDatum,
    NewForm,
    NewInst,
    apply_delta,
    min_responses,
    response_valid_naive,
)
from derivation.iso import canonical
from derivation.model import EMPTY, AdmitDatum, AdmitRuleAll, Regime, step
from derivation.observe import contexts, derivable, plug, profiles, satisfies
from portable_key import (
    PREFIX,
    U64_MAX,
    PortableKeyError,
    decode_portable_key_v1,
    encode_structural_key_v1,
    portable_key_v1,
    structural_words,
)
from verify_sources import check_sources

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    """Keep replay checks active when Python runs with optimization enabled."""
    if not condition:
        raise RuntimeError(message)


def population():
    """All instance subsets and uniform-rule choices on one binary form, n≤3;
    plus two-form unary populations. Requirement stores protect existing
    separations. No random sampling or silent truncation.
    """
    for n in range(4):
        data = tuple(f"d{i}" for i in range(n))
        for forms in [(), (1,), (2,), (1, 1)]:
            possible = [(f, args) for f, a in enumerate(forms)
                        for args in itertools.product(range(n), repeat=a)]
            for bits in range(2 ** len(possible)):
                insts = frozenset(i for k, i in enumerate(possible) if bits & (1 << k))
                for rule_bits in range(2 ** len(forms)):
                    rules = frozenset(f for f in range(len(forms)) if rule_bits & (1 << f))
                    r = Regime(data, forms, insts, rules, frozenset())
                    ps = profiles(r)
                    reqs = frozenset((i, j) for i in range(n) for j in range(i + 1, n)
                                     if ps[i] != ps[j])
                    yield Regime(data, forms, insts, rules, reqs)


def encode(r):
    return "|".join([str(r.n_data()), ",".join(map(str, r.forms)),
                     ";".join(f"{f}:" + ",".join(map(str, args)) for f, args in sorted(r.insts)),
                     ",".join(map(str, sorted(r.rules))),
                     ";".join(f"{i}:{j}" for i, j in sorted(r.reqs))])


def observations(r):
    cs = contexts(r)
    bits = ["".join("1" if derivable(r, plug(c, d)) else "0" for c in cs)
            for d in range(r.n_data())]
    return f"{portable_key_v1(r).hex()}|{len(cs)}|" + ",".join(bits)


def wire_probes():
    """Boundary vectors and deliberately malformed layouts, independent of search."""
    def raw(words):
        return PREFIX + b"".join(w.to_bytes(8, "big") for w in words)

    valid = [encode_structural_key_v1(key) for key in [
        (0, (), (), (), ()),
        (U64_MAX, (U64_MAX,), (), (), ()),
        (2, (1, 2), ((0, (1,)), (1, (0, 1))), (0, 1), ((0, 1),)),
    ]]
    empty = valid[0]
    invalid = [empty[:n] for n in range(len(empty))]
    invalid += [PREFIX[:-1] + b"\x02" + empty[len(PREFIX):], empty + bytes(8),
                raw([0, U64_MAX, 0, 0, 0]),
                raw([0, 0, U64_MAX, 0, 0]), raw([0, 0, 0, 0, U64_MAX]),
                raw([0, 1, 0, 0, 0, 0]),
                raw([1, 1, 1, 1, 1, 1, 0, 0, 0]),
                raw([1, 1, 1, 1, 0, 0, 0, 0]),
                raw([1, 1, 1, 1, 0, 1, 1, 0, 0]),
                raw([0, 0, 0, 1, 0, 0]),
                raw([2, 0, 0, 0, 1, 1, 0]),
                raw([2, 0, 0, 0, 1, 0, 2]),
                raw([1, 1, 1, 2, 0, 1, 0, 0, 1, 0, 0, 0]),
                raw([1, 1, 1, 0, 2, 0, 0, 0]),
                raw([3, 0, 0, 0, 2, 1, 2, 0, 1]),
                raw([2, 0, 0, 0, 2, 0, 1, 0, 1])]
    return [(value, value.hex()) for value in valid] + [(value, "REJECT") for value in invalid]


def python_replay():
    rows = []
    for reading, data, target in [("L", ("a", "b"), (0, 1)),
                                   ("F", ("<>", "a", "b"), (1, 2))]:
        base = Regime(data, (), frozenset(), frozenset(), frozenset({target}))
        for measure in ["mu1", "mu2"]:
            minimum = min_responses(base, target, measure, Bounds())
            require(minimum is not None, "missing minimum response")
            require(all(response_valid_naive(base, target, d) for d in minimum.deltas),
                    "reported minimum contains an invalid response")
            classes = {canonical(apply_delta(base, d)) for d in minimum.deltas}
            rows.append([reading, measure, *minimum.cost, len(minimum.deltas), len(classes)])
    expected = [["L", "mu1", 2, -1, 6, 3], ["L", "mu2", 2, 1, 2, 1],
                ["F", "mu1", 2, -1, 10, 5], ["F", "mu2", 2, 1, 2, 1]]
    require(rows == expected, f"minimum census differs: {rows}")
    count_cases = 0
    for n in range(5):
        for arity in range(1, 8):
            r = Regime(tuple(map(str, range(n))), (arity,), frozenset(), frozenset(), frozenset())
            require(len(contexts(r)) == (n + 1) ** arity - n ** arity,
                    f"context count differs for n={n}, arity={arity}")
            count_cases += 1
    progress_targets = 0
    states = list(population())
    for r in states:
        require(satisfies(r), "generated regime violates protected requirements")
        for i, j in itertools.combinations(range(r.n_data()), 2):
            delta = (NewForm(1), NewInst(len(r.forms), (i,)))
            require(response_valid_naive(r, (i, j), delta),
                    f"fresh unary progress fails at {encode(r)} target {(i, j)}")
            progress_targets += 1
    collision = step(EMPTY, AdmitDatum("w1"))
    require(apply_delta(collision, (NewDatum(),)) == collision,
            "frozen datum naming collision was not reproduced")
    marked = Regime(("a", "b"), (1,), frozenset({(0, (0,))}), frozenset(), frozenset())
    require(profiles(marked)[0] != profiles(marked)[1], "unary mark did not separate")
    require(len(set(profiles(step(marked, AdmitRuleAll(0))))) == 1,
            "uniform-rule collapse counterexample was not reproduced")
    probes = wire_probes()
    for value, expected in probes:
        try:
            actual = encode_structural_key_v1(decode_portable_key_v1(value)).hex()
        except PortableKeyError:
            actual = "REJECT"
        require(actual == expected, "wire boundary or malformed-input check differs")
    return {"minima": rows, "context_count_cases": count_cases,
            "progress_regimes": len(states), "progress_targets": progress_targets,
            "frozen_name_collision_reproduced": True, "wire_protocol_cases": len(probes)}, states


def reproduce(rust=True, lean_wire=False):
    result, states = python_replay()
    result.update(check_sources())
    if rust:
        with tempfile.TemporaryDirectory(prefix="genesis-rust-") as directory:
            compare_rust(result, states, Path(directory))
        result["rust_python_exact_agreements"] = len(states)
    if lean_wire:
        result.update(compare_lean(states))
    result["scope"] = "Finite cross-language replay; universal statements are in lean4, not inferred from counts."
    return result


def compare_lean(states):
    """Execute the proved encoder and exhaustive search, with labelled inputs."""
    lean = ROOT / "lean4"
    build = subprocess.run(["lake", "build", "wireReplay", "searchReplay"], cwd=lean,
                           capture_output=True, text=True, encoding="utf-8", check=False)
    if build.returncode:
        raise RuntimeError(build.stdout + build.stderr)
    executable = lean / ".lake/build/bin/wireReplay"
    if not executable.is_file():
        executable = executable.with_suffix(".exe")
    encoded = [portable_key_v1(r) for r in states]
    encoded += [value for value, expected in wire_probes() if expected != "REJECT"]
    words = [structural_words(decode_portable_key_v1(value)) for value in encoded]
    run = subprocess.run([str(executable)], input="\n".join(
        ",".join(map(str, row)) for row in words) + "\n", capture_output=True,
        text=True, encoding="utf-8", check=False)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    require(run.stdout.splitlines() == [value.hex() for value in encoded],
            "native Lean wire encoding differs from Python")
    search_executable = lean / ".lake/build/bin/searchReplay"
    if not search_executable.is_file():
        search_executable = search_executable.with_suffix(".exe")
    # Keep original datum/form labels: passing already-canonical tuples would
    # exercise idempotence, rather than comparing the actual minimum searches.
    labelled = [(r.n_data(), r.forms, tuple(sorted(r.insts)),
                 tuple(sorted(r.rules)), tuple(sorted(r.reqs))) for r in states]
    inputs = [",".join(map(str, structural_words(key))) for key in labelled]
    minimum_run = subprocess.run([str(search_executable)], input="\n".join(inputs) + "\n",
                                 capture_output=True, text=True, encoding="utf-8", check=False)
    require(minimum_run.returncode == 0, minimum_run.stdout + minimum_run.stderr)
    require(minimum_run.stdout.splitlines() == [portable_key_v1(r).hex() for r in states],
            "native proved Lean canonical search differs from Python")
    mixed = Regime(("a", "b"), (1, 2), frozenset({(0, (1,)), (1, (1, 0))}),
                   frozenset({1}), frozenset({(0, 1)}))
    unsorted = Regime(("a", "b"), (1,), frozenset({(0, (0,)), (0, (1,))}),
                      frozenset(), frozenset({(0, 1)}))
    mixed_key = (2, mixed.forms, tuple(sorted(mixed.insts)), (1,), ((0, 1),))
    special_inputs = [",".join(map(str, structural_words(mixed_key))),
                      "2,1,1,2,0,1,1,0,1,0,0,1,0,1",  # Descending instance order.
                      "8,2,1,1,0,0,0"]  # 8! × 2! = 80,640 admitted candidates.
    special = subprocess.run([str(search_executable)], input="\n".join(special_inputs) + "\n",
                             capture_output=True, text=True, encoding="utf-8", check=False)
    require(special.returncode == 0 and special.stdout.splitlines() ==
            [portable_key_v1(r).hex() for r in (mixed, unsorted)] +
            [encode_structural_key_v1((8, (1, 1), (), (), ())).hex()],
            "Lean mixed-arity, unordered-list or maximum-budget search differs")
    rejected_words = [[], [0, 0], [0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0],
                      [1, 1, 1, 1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0],
                      [1, 1, 1, 1, 0, 1, 1, 0, 0], [1, 1, 1, 0, 1, 1, 0],
                      [2, 0, 0, 0, 1, 1, 0], [2, 0, 0, 0, 1, 0, 0],
                      [1, 1, 1, 2, 0, 1, 0, 0, 1, 0, 0, 0],
                      [1, 1, 1, 0, 2, 0, 0, 0], [2, 0, 0, 0, 2, 0, 1, 0, 1],
                      [-1, 0, 0, 0, 0], [U64_MAX + 1, 0, 0, 0, 0],
                      [9, 0, 0, 0, 0], [8, 3, 1, 1, 1, 0, 0, 0]]
    for row in rejected_words:
        rejected = subprocess.run([str(search_executable)], input=",".join(map(str, row)) + "\n",
                                  capture_output=True, text=True, encoding="utf-8", check=False)
        require(rejected.returncode == 1 and rejected.stderr and not rejected.stdout,
                f"native Lean search did not refuse invalid or over-budget input: {row}")
    return {"lean_python_wire_agreements": len(encoded),
            "lean_python_canonical_agreements": len(states), "lean_canonical_adversarial_cases": 2,
            "lean_search_rejection_cases": len(rejected_words), "lean_search_maximum_candidates": 80640}


def compare_rust(result, states, target_dir):
    """Use a disposable native build so replay cannot pollute the release tree."""
    manifest = ROOT / "code/rust/Cargo.toml"
    build = subprocess.run(["cargo", "build", "--offline", "--manifest-path", str(manifest),
                            "--target-dir", str(target_dir), "--bin", "genesis_replay"],
                           capture_output=True, text=True, check=False)
    if build.returncode:
        raise RuntimeError(build.stdout + build.stderr)
    exe = target_dir / "debug/genesis_replay"
    if not exe.is_file():
        exe = exe.with_suffix(".exe")
    probes = wire_probes()
    requests = ["minima", *map(encode, states), *("wire:" + value.hex() for value, _ in probes)]
    run = subprocess.run([str(exe)], input="\n".join(requests) + "\n",
                         capture_output=True, text=True, check=False)
    if run.returncode:
        raise RuntimeError(run.stderr)
    lines = run.stdout.splitlines()
    expected_minima = ";".join(",".join(map(str, row)) for row in result["minima"])
    require(len(lines) == len(requests), "native population mismatch")
    require(lines[0] == expected_minima, "native minima mismatch")
    for k, (r, observed) in enumerate(zip(states, lines[1:1 + len(states)])):
        require(observed == observations(r), f"native mismatch at regime {k}: {encode(r)}")
        require(decode_portable_key_v1(bytes.fromhex(observed.split("|", 1)[0])) ==
                decode_portable_key_v1(portable_key_v1(r)), "native key did not round-trip")
    for observed, (_, expected) in zip(lines[1 + len(states):], probes):
        require(observed == expected, "native wire acceptance or rejection differs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-only", action="store_true")
    parser.add_argument("--lean-wire", action="store_true",
                        help="Compile and compare the mechanized Lean encoder and canonical search")
    args = parser.parse_args()
    print(json.dumps(reproduce(rust=not args.python_only, lean_wire=args.lean_wire), indent=2))
