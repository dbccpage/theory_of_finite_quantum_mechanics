"""Build and replay the finite certificate refinement at explicit runtime paths.

The output directory retains exact generated obligations and command logs. PASS
means the scoped checks below ran on the bound inputs, not full crate, compiler,
serializer, solver-semantics or publication certification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import replace
from itertools import product
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
ROOT = next(p for p in PAPER.parents if (p / "lean4/lakefile.lean").is_file())
sys.path.insert(0, str(PAPER / "code"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(items):
    return [tuple(x for x, keep in zip(items, mask) if keep)
            for mask in product((False, True), repeat=len(items))]


def verify(lake: Path, rustc: Path, out: Path) -> dict:
    if not __debug__:
        raise RuntimeError("optimized Python is not supported for verification")

    from witnessed_difference.reasoning import (
        Proof,
        ProofStep,
        Rule,
        Theory,
        graph_theory,
        solve,
    )
    from witnessed_difference.reasoning_refinement import (
        graph_module,
        proof_module,
        replay_in_lean,
    )

    if sys.version_info[:2] != (3, 12):
        raise RuntimeError("paper verification requires Python 3.12")
    out.mkdir(parents=True, exist_ok=True)
    lean = ROOT / "lean4"
    native = ROOT / "omega_engine/crates_rs"
    sources = [Path(__file__), PAPER / "code/witnessed_difference/reasoning.py",
               PAPER / "code/witnessed_difference/reasoning_refinement.py",
               lean / "lakefile.lean", lean / "lean-toolchain",
               *sorted((lean / "research_programs/wdp_reasoning").glob("*.lean")),
               native / "omega_wdp/src/witnessed_reasoning.rs",
               native / "omega_wdp/src/witnessed_reasoning_replay.rs",
               native / "omega_wdp/src/examples/witnessed_reasoning_replay.rs",
               native / "tests/omega_wdp/witnessed_reasoning.rs",
               native / "tests/omega_wdp/witnessed_reasoning_replay.rs"]
    bindings = {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in sources}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    env["PATH"] = str(lake.parent) + os.pathsep + env["PATH"]
    env["LEAN_PATH"] = str(lean / ".lake/build/lib/lean")
    lean_binary = lake.parent / ("lean.exe" if os.name == "nt" else "lean")
    checks = []

    def run(label, command, *, cwd=ROOT, reject=False, timeout=300):
        result = subprocess.run([str(x) for x in command], cwd=cwd, env=env,
                                capture_output=True, text=True, encoding="utf-8", timeout=timeout)
        output = result.stdout + result.stderr
        log = out / (label + ".log")
        log.write_bytes(output.encode("utf-8"))
        checks.append({"id": label, "command": [str(x) for x in command],
                       "cwd": str(cwd), "exit_code": result.returncode,
                       "expected_rejection": reject, "output_sha256": sha(log)})
        print(label, result.returncode, flush=True)
        if reject:
            assert result.returncode != 0 and "decide" in output and "error:" in output, output
        else:
            assert result.returncode == 0 and "warning:" not in output, output[-5000:]
        return output

    def kernel(label, source, *, reject=False, expected=1):
        path = out / (label + ".lean")
        path.write_bytes(source.encode("utf-8"))
        output = run(label, [lean_binary, path], cwd=lean, reject=reject)
        if not reject:
            rows = re.findall(r"'[^']+\.result' (?:does not depend on any axioms|depends on axioms: \[([^]]*)\])", output)
            assert len(rows) == expected, (label, len(rows), expected, output[-1000:])
            assert all(not row or set(row.split(", ")) <= {"propext", "Quot.sound"} for row in rows)
        checks[-1]["source_sha256"] = sha(path)
        checks[-1]["theorems_checked"] = 0 if reject else expected

    run("lean-version", [lean_binary, "--version"])
    run("lean-build", [lake, "build", "WdpReasoning"], cwd=lean)
    audit = run("axioms", [lake, "env", "lean", "research_programs/wdp_reasoning/RefinementAxioms.lean"], cwd=lean)
    rows = re.findall(r"depends on axioms: \[([^]]*)\]", audit)
    assert len(rows) == 17 and all(set(row.split(", ")) <= {"propext", "Quot.sound"} for row in rows)

    corpus = []
    all_rules = tuple(Rule(p, q) for p in subsets((0, 1)) for q in (0, 1))
    cases = 0
    for rules in subsets(all_rules):
        for facts in subsets((0, 1)):
            task = Theory(("a", "b"), frozenset(facts), rules)
            models = [v for v in product((False, True), repeat=2)
                      if all(v[a] for a in facts) and
                      all(not all(v[a] for a in r.premises) or v[r.conclusion] for r in rules)]
            for goal in (0, 1):
                result = solve(task, goal)
                assert isinstance(result, Proof) == all(v[goal] for v in models)
                corpus.append(proof_module(task, goal, result, case_index=cases).split("\n", 1)[1])
                cases += 1
    assert cases == 2048
    for start in range(0, cases, 128):
        batch = corpus[start:start + 128]
        kernel("python-two-atom-" + str(start), "import ExecutableReasoning\n" +
               "\n".join(batch), expected=len(batch))

    graphs = ["import ExecutableReasoning\n"]
    graph_cases = 0
    for edges in subsets(tuple(product((0, 1), repeat=2))):
        for start, goal in product((0, 1), repeat=2):
            nodes = ("a", "b")
            result = solve(graph_theory(nodes, edges, start), goal)
            graphs.append(graph_module(nodes, edges, start, goal, result,
                                       case_index=graph_cases).split("\n", 1)[1])
            graph_cases += 1
    assert graph_cases == 64
    kernel("python-all-two-vertex-graphs", "\n".join(graphs), expected=graph_cases)

    task = Theory(('<>\n#eval panic! "data" λ🦀', "b", "c"), frozenset({0}), (Rule((0,), 1),))
    proof = solve(task, 1)
    model = solve(task, 2)
    kernel("python-unicode", proof_module(task, 1, proof))
    mutations = {
        "forward": (task, 1, replace(proof, steps=(proof.steps[0], ProofStep(1, 0, (1,))))),
        "missing-premise": (task, 1, replace(proof, steps=(proof.steps[0], ProofStep(1, 0, ())))),
        "forged-fact": (task, 1, replace(proof, steps=(ProofStep(1, None),))),
        "empty": (task, 1, replace(proof, steps=())),
        "rule-index": (task, 1, replace(proof, steps=(proof.steps[0], ProofStep(1, 99, (0,))))),
        "wrong-goal": (task, 2, proof),
        "carrier": (task, 1, replace(proof, steps=(ProofStep(99, None),))),
        "closure": (task, 2, replace(model, true_atoms=frozenset({0}))),
        "model-goal": (task, 2, replace(model, true_atoms=frozenset({0, 1, 2}))),
        "model-facts": (task, 2, replace(model, true_atoms=frozenset())),
    }
    for label, (t, goal, result) in mutations.items():
        kernel("python-reject-" + label, proof_module(t, goal, result), reject=True)
    live = replay_in_lean(task, 1, proof, lean_binary=lean_binary, lean_root=lean, temp_parent=out)
    assert live.status == "KERNEL_ACCEPTED" and live.judgment == "derivable", live
    live_log = out / "python-live-adapter.log"
    live_log.write_bytes(live.output.encode("utf-8"))
    checks.append({"id": "python-live-adapter", "status": live.status,
                   "judgment": live.judgment, "source_sha256": live.source_sha256,
                   "theory_digest": live.theory_digest, "goal": live.goal,
                   "output_sha256": sha(live_log)})

    run("rust-version", [rustc, "--version"])
    wrapper = out / "selected_native.rs"
    wrapper.write_bytes((
        '#[path = '+json.dumps(str(native / "omega_wdp/src/witnessed_reasoning.rs"))+']\n'
        'pub mod witnessed_reasoning;\n'
        '#[path = '+json.dumps(str(native / "omega_wdp/src/witnessed_reasoning_replay.rs"))+']\n'
        'pub mod witnessed_reasoning_replay;\n').encode("utf-8"))
    run("rust-module", [rustc, "--edition=2021", "--crate-type=lib", "--crate-name=omega_wdp",
                        wrapper, "--out-dir", out])
    extern = "omega_wdp=" + str(out / "libomega_wdp.rlib")
    suffix = ".exe" if os.name == "nt" else ""
    for target in ("witnessed_reasoning", "witnessed_reasoning_replay"):
        binary = out / (target + "_tests" + suffix)
        run("rust-build-" + target, [rustc, "--edition=2021", "--test",
            native / ("tests/omega_wdp/" + target + ".rs"), "--extern", extern, "-o", binary])
        output = run("rust-test-" + target, [binary])
        assert "2 passed; 0 failed" in output
    emitter = out / ("native_replay" + suffix)
    run("rust-emitter-build", [rustc, "--edition=2021",
        native / "omega_wdp/src/examples/witnessed_reasoning_replay.rs", "--extern", extern, "-o", emitter])
    native_out = out / "native-corpus"
    native_out.mkdir(exist_ok=True)
    run("rust-emitter", [emitter, native_out])
    native_cases = sorted(native_out.glob("*.lean"))
    assert len(native_cases) == 11
    for path in native_cases:
        kernel("native-" + path.stem, path.read_text(encoding="utf-8"), reject=path.stem.startswith("reject_"))
    assert bindings == {p: sha(ROOT / p) for p in bindings}, "source changed during verification"
    receipt = {"schema": "wdp-executable-refinement-v1", "authority_effect": "None",
               "status": "SCOPED_PASS", "base_commit": subprocess.check_output(
                   ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "python": {"executable": sys.executable, "version": sys.version},
               "input_bindings": bindings, "checks": checks,
               "python_kernel_cases": cases, "graph_kernel_cases": graph_cases,
               "python_mutation_refusals": len(mutations), "native_kernel_cases": len(native_cases),
               "formal_declarations": 17,
               "limits": ["Lean executable checker refinement is proved for arbitrary finite inputs",
                          "Python/Rust serializers and source semantics are tested, not formally verified",
                          "Foreign solver termination and completeness are not formally refined here",
                          "Selected Rust modules only; no full crate or historical Mathlib build",
                          "Toolchain/runtime and compiler trust remain explicit; no publication or authority claim"]}
    (out / "refinement-verification.json").write_bytes((json.dumps(receipt, indent=2)+"\n").encode("utf-8"))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lake", required=True, type=Path)
    parser.add_argument("--rustc", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = verify(args.lake.resolve(), args.rustc.resolve(), args.output.resolve())
    print(result["status"], "17 formal declarations; 2048 Horn and 64 graph kernel cases; 11 native cases")


if __name__ == "__main__":
    main()
