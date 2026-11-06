"""Exercise proposed Python containment changes in isolated scratch copies."""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import omega_engine.crates.mub_verify  # Initialize package before isolated module overrides.
PATCHED = ROOT / "scratch/audit_2026_09_22/patched/omega_engine/crates/mub_verify"


def load(name):
    key = "omega_engine.crates.mub_verify." + name
    spec = importlib.util.spec_from_file_location(key, PATCHED / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod


governor = load("l1_governor")
b1 = load("target_b1_continuous_chaining")
receipts = load("verify_all_receipts")
firewall = load("packet_firewall")
for value in (0.1, True):
    try:
        governor.Edge("a", "b", value)
    except TypeError:
        pass
    else:
        raise AssertionError("inexact/boolean weight admitted")
graph = governor.ConstraintGraph(("a", "b", "c"), tuple(governor.Edge(u, v) for u, v in (("a", "b"), ("b", "c"), ("c", "a"))))
host = governor.L1SymbolGameGovernor(graph)
for e in graph.edges:
    host.step_assert(e.u, e.v, Q(1))
assert host.primary_obstruction() == 3
assert not host.step_cut(proposed_claims={}).admitted
assert host.primary_obstruction() == 3
assert not b1.ContinuousChainingAuditor().audit_sample_chain(b1.build_dense_chain_sample())[0]
assert receipts.verify_all_receipts(ROOT / "artifacts")["all_passed"]
assert not receipts.verify_all_receipts(ROOT / "artifacts", ROOT / "scratch/audit_2026_09_22/duplicate_manifest.json")["all_passed"]
step = firewall.DerivationStep("UNDECLARED", 0, "missing", {}, "bad", "bad", "UNDECLARED invalid")
assert not firewall.PacketFirewallHost().verify_step(step).admitted
print("PROPOSED_PYTHON_GUARDS_PASS: inexact input rejected; claim erasure rejected; gapped chain rejected; duplicate receipts rejected; unlicensed carrier call rejected; original manifest still readable")
