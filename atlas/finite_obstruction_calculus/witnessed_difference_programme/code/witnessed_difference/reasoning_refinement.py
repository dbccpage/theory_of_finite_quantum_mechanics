"""Replay concrete Horn certificates as closed Lean kernel proof obligations.

The foreign solver proposes data. Lean checks a theorem about the fully rendered
task. The serializer and process boundary are tested bridges, not formally
verified Python semantics. A rejected or exhausted replay supplies no judgment.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .reasoning import Countermodel, Proof, ProofStep, Theory, graph_theory


def _nat(value: int) -> str:
    if type(value) is not int or value < 0:
        raise ValueError("Lean indices require nonnegative integers")
    return str(value)


def _list(values) -> str:
    return "[" + ", ".join(values) + "]"


def _string(value: str) -> str:
    if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        raise ValueError("atom names must contain Unicode scalar values")
    return "(String.ofList " + _list(f"(Char.ofNat {ord(c)})" for c in value) + ")"


def theory_term(theory: Theory) -> str:
    if type(theory) is not Theory:
        raise ValueError("expected a validated Theory")
    atoms = _list(_string(a) for a in theory.atoms)
    facts = _list(_nat(a) for a in sorted(theory.facts))
    rules = _list("⟨" + _list(_nat(a) for a in r.premises) + ", " +
                  _nat(r.conclusion) + "⟩" for r in theory.rules)
    return "⟨" + atoms + ", " + facts + ", " + rules + "⟩"


def certificate_term(theory: Theory, result: Proof | Countermodel) -> tuple[str, str]:
    """Check representation and source binding; leave semantic checking to Lean."""
    if type(result) not in (Proof, Countermodel) or result.theory_digest != theory.digest():
        raise ValueError("certificate must be bound to the supplied theory")
    goal = _nat(result.goal)
    if type(result) is Proof:
        if type(result.steps) is not tuple:
            raise ValueError("proof steps must be a tuple")
        steps = []
        for step in result.steps:
            if type(step) is not ProofStep or type(step.premises) is not tuple:
                raise ValueError("invalid proof step representation")
            rule = "none" if step.rule is None else "(some " + _nat(step.rule) + ")"
            steps.append("⟨" + _nat(step.conclusion) + ", " + rule + ", " +
                         _list(_nat(i) for i in step.premises) + "⟩")
        return "Proof", "⟨task, " + goal + ", " + _list(steps) + "⟩"
    if (type(result.true_atoms) is not frozenset or
            any(type(a) is not int or not 0 <= a < len(theory.atoms) for a in result.true_atoms)):
        raise ValueError("countermodel values must be in the source carrier")
    values = _list("true" if i in result.true_atoms else "false" for i in range(len(theory.atoms)))
    return "Model", "⟨task, " + goal + ", " + values + "⟩"


def proof_module(theory: Theory, goal: int, result: Proof | Countermodel,
                 *, case_index: int = 0) -> str:
    """Emit data constructors and a closed theorem; never interpolate Lean code."""
    task = theory_term(theory)
    requested = _nat(goal)
    kind, certificate = certificate_term(theory, result)
    namespace = "Replay" + _nat(case_index)
    checker = "checkProof" if kind == "Proof" else "checkCountermodel"
    judgment = "" if kind == "Proof" else "¬"
    parameter = "p" if kind == "Proof" else "m"
    return f"""import ExecutableReasoning
open WitnessedReasoning WitnessedReasoning.Executable
namespace {namespace}
def task : FiniteTheory := {task}
def certificate : {kind}Certificate := {certificate}
theorem result : {judgment}Derivable task.abstract {requested} :=
  {checker}_sound (T := task) (goal := {requested}) ({parameter} := certificate) (by decide)
#print axioms result
end {namespace}
"""


def graph_module(nodes: tuple[str, ...], edges: tuple[tuple[int, int], ...],
                 start: int, goal: int, result: Proof | Countermodel, *,
                 case_index: int = 0) -> str:
    theory = graph_theory(nodes, edges, start)
    kind, certificate = certificate_term(theory, result)
    namespace = "GraphReplay" + _nat(case_index)
    atom_term = _list(_string(a) for a in nodes)
    edge_term = _list("(" + _nat(a) + ", " + _nat(b) + ")" for a, b in edges)
    requested = _nat(goal)
    checker = "checked_graph_proof" if kind == "Proof" else "checked_graph_countermodel"
    judgment = "" if kind == "Proof" else "¬"
    parameter = "p" if kind == "Proof" else "m"
    return f"""import ExecutableReasoning
open WitnessedReasoning WitnessedReasoning.Executable
namespace {namespace}
def nodes : List String := {atom_term}
def edges : List (Nat × Nat) := {edge_term}
def task : FiniteTheory := graphTheory nodes edges {start}
def certificate : {kind}Certificate := {certificate}
theorem result : {judgment}Reachable edges {start} {requested} :=
  {checker} (atoms := nodes) (edges := edges) (start := {start})
    (goal := {requested}) ({parameter} := certificate) (by decide)
#print axioms result
end {namespace}
"""


@dataclass(frozen=True)
class ReplayResult:
    status: str
    source_sha256: str
    theory_digest: str
    goal: int
    judgment: str | None
    output: str


def replay_in_lean(theory: Theory, goal: int, result: Proof | Countermodel, *,
                   lean_binary: Path, lean_root: Path, timeout_seconds: float = 60,
                   temp_parent: Path | None = None) -> ReplayResult:
    source = proof_module(theory, goal, result)
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    judgment = "derivable" if type(result) is Proof else "not_derivable"
    env = dict(os.environ)
    env["LEAN_PATH"] = str(lean_root / ".lake/build/lib/lean")
    with tempfile.TemporaryDirectory(prefix="wdp-replay-", dir=temp_parent) as folder:
        path = Path(folder) / "Replay.lean"
        path.write_bytes(source.encode("utf-8"))
        try:
            run = subprocess.run([str(lean_binary), str(path)], cwd=lean_root, env=env,
                                 capture_output=True, text=True, encoding="utf-8",
                                 timeout=timeout_seconds, check=False)
        except subprocess.TimeoutExpired:
            return ReplayResult("RESOURCE_EXHAUSTED", digest, theory.digest(), goal, None, "timeout")
        except OSError as exc:
            return ReplayResult("TOOL_ERROR", digest, theory.digest(), goal, None, str(exc))
    output = run.stdout + run.stderr
    if run.returncode != 0:
        status = "KERNEL_REJECTED"
    elif "warning:" in output:
        status = "KERNEL_REJECTED"
    elif "'Replay0.result' does not depend on any axioms" in output:
        status = "KERNEL_ACCEPTED"
    else:
        match = re.search(r"'Replay0.result' depends on axioms: \[([^]]*)\]", output)
        allowed = {"propext", "Quot.sound", "Classical.choice"}
        status = ("KERNEL_ACCEPTED" if match and
                  set(match.group(1).split(", ")) <= allowed else "TOOL_ERROR")
    return ReplayResult(status, digest, theory.digest(), goal,
                        judgment if status == "KERNEL_ACCEPTED" else None, output)
