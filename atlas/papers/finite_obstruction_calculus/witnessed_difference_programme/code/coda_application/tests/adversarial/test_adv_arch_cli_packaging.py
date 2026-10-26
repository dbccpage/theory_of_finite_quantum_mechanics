# -*- coding: utf-8 -*-
"""
Adversarial tests for architecture, CLI, packaging, the Rust bridge, and the
firewall audit use case.

Claims under attack: domain/__init__.py ("pure entities, value objects, and layer
boundary contracts with zero I/O dependencies"); `coda status` ("100% Inward
Dependency Isolation"); README ("connects cleanly to the high-performance Rust
crates"; the directory tree; `coda` console script); cmd_stress_test runtime
bound (< 3.0 s); audit_authority_firewall ("Asserts non-promotion discipline and
verifies that no spurious token is emitted").

AuthorityEffect: None.
"""

from __future__ import annotations

import ast
import re
import shutil
import time

import pytest
from sympy import Float, Matrix

from coda_application.infrastructure.rust_bridge import RustCrateBridge
from coda_application.presentation import cli
from coda_application.tests.adversarial._support import APP_ROOT, foc_phi1, make_problem, run_cli, run_python
from coda_application.application import audit_authority_firewall

LAYERS = ("domain", "use_cases", "infrastructure", "presentation")


def imports_of(path):
    """Every imported module name in a file, including function-local imports."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        elif isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
    return names


def layer_imports(layer):
    return {p.relative_to(APP_ROOT).as_posix(): imports_of(p) for p in (APP_ROOT / layer).rglob("*.py")}


def outward(layer, forbidden):
    return {
        f: sorted(m for m in mods if any(m.startswith(f"coda_application.{x}") for x in forbidden))
        for f, mods in layer_imports(layer).items()
        if any(m.startswith(f"coda_application.{x}") for x in forbidden for m in mods)
    }


# ------------------------------------------------------- architecture


# FIXED 2026-09-23 (was BREAK ARC-01: domain/layers/layer1_foc.py imports coda_application.infrastructure (function-local import))
def test_domain_does_not_import_outer_layers():
    assert outward("domain", ("infrastructure", "use_cases", "presentation")) == {}


# FIXED 2026-09-23 (was BREAK ARC-02: the 'zero I/O' domain reads wall clocks: budget.py imports time, anomalon_registry.py datetime)
def test_domain_has_no_clock_dependencies():
    clocks = {f: sorted(m & {"time", "datetime"}) for f, m in layer_imports("domain").items() if m & {"time", "datetime"}}
    assert clocks == {}


def test_use_cases_do_not_import_outer_layers():
    """HELD: use_cases never import infrastructure or presentation."""
    assert outward("use_cases", ("infrastructure", "presentation")) == {}


def test_infrastructure_does_not_import_presentation():
    """HELD: infrastructure never imports presentation."""
    assert outward("infrastructure", ("presentation", "use_cases")) == {}


# FIXED 2026-09-23 (was BREAK ARC-03: `coda status` prints '100% Inward Dependency Isolation' while ARC-01 exists)
def test_status_isolation_claim_is_true():
    out = run_cli("status").stdout
    assert "100% Inward Dependency Isolation" not in out or outward(
        "domain", ("infrastructure", "use_cases", "presentation")
    ) == {}


# FIXED 2026-09-23 (was BREAK ARC-04: tests import apps.alpha, which pyproject.toml does not declare)
def test_no_undeclared_cross_app_imports():
    foreign = {
        p.relative_to(APP_ROOT).as_posix(): sorted(m for m in imports_of(p) if m.startswith("apps.") and not m.startswith("coda_application"))
        for p in APP_ROOT.rglob("*.py")
        if "__pycache__" not in p.parts
    }
    assert {f: m for f, m in foreign.items() if m} == {}


# FIXED 2026-09-23 (was BREAK ARC-05: README's directory tree omits budget, contracts, firewall_engine, anomalon_registry and two test files)
def test_readme_crosswalk_links_every_runtime_layer():
    readme = (APP_ROOT / "README.md").read_text(encoding="utf-8")
    for paper in ("FOC", "MUR", "CS", "CS_Q", "Q", "A", "OR", "FDA", "GTLA"):
        assert re.search(rf"\|\s*\d+\s+{paper}\s*\|", readme)
    assert "does not construct the" in readme
    assert "do not construct standing" in readme


# ------------------------------------------------------------ packaging


# FIXED 2026-09-23 (was BREAK PKG-01: pyproject.toml cannot build: setuptools finds four flat top-level packages, so `coda` never installs)
def test_package_metadata_builds(tmp_path):
    pkg = tmp_path / "coda_pkg"
    shutil.copytree(APP_ROOT, pkg, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".ruff_cache"))
    (pkg / "meta").mkdir()
    proc = run_python(
        ["-c", f"import os; os.chdir({str(pkg)!r}); import setuptools.build_meta as b; b.prepare_metadata_for_build_wheel('meta')"],
        timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-400:]


# ------------------------------------------------------------------ CLI


# FIXED 2026-09-23 (was BREAK CLI-01: `coda evaluate --licensed` mints an AuthorityToken from a command-line flag)
def test_cli_flag_does_not_mint_authority():
    assert "Authority Token : PRESENT" not in run_cli("evaluate", "--licensed").stdout


def test_cli_obstructed_phi1_matches_oracle():
    """HELD: the CLI's canned obstructed instance reports the true Phi_1 = 1."""
    out = run_cli("evaluate", "--obstructed").stdout
    truth = foc_phi1(Matrix([[-1, 1], [1, -1]]), Matrix([1, 0]))
    assert f"Phi_1 Defect    : {truth}" in out


def test_cli_lists_nine_layers():
    """HELD: `coda layers` lists nine layers."""
    assert len(re.findall(r"^Layer \d\d ", run_cli("layers").stdout, flags=re.M)) == 9


def test_cli_unknown_subcommand_is_usage_error():
    """HELD: an unknown subcommand exits 2 via argparse."""
    assert run_cli("frobnicate").returncode == 2


# FIXED 2026-09-23 (was BREAK CLI-02: `coda` with no subcommand prints help and exits 0)
def test_cli_without_subcommand_exits_nonzero():
    assert run_cli().returncode != 0


# FIXED 2026-09-23 (was BREAK CLI-03: invalid --vertices is a Python traceback, not a usage error)
@pytest.mark.parametrize("vertices", ["5", "-3"])
def test_cli_rejects_small_graphs_cleanly(vertices):
    proc = run_cli("stress-test", "--vertices", vertices)
    assert "Traceback" not in proc.stderr


# FIXED 2026-09-23 (was BREAK CLI-04: --chord equal to --vertices makes self-loop rows, falls off the fast path; 400 vertices take ~9 s)
def test_cli_stress_certificate_survives_chord_choice():
    start = time.perf_counter()
    proc = run_cli("stress-test", "--vertices", "20", "--chord", "20", timeout=30)
    elapsed = time.perf_counter() - start
    assert proc.returncode == 0 and "dual_witness: PASS" in proc.stdout and "gamma2: PASS" in proc.stdout, f"{elapsed:.1f}s"


# FIXED 2026-09-23 (was BREAK CLI-05: stress-test prints the < 3.0 s bound as FAIL yet exits 0 (exit gate is 5.0 s))
def test_cli_fail_verdict_has_nonzero_exit(monkeypatch, capsys):
    ticks = iter([0.0, 0.1, 0.1, 4.0, 4.0])
    real = time.perf_counter

    def fake_clock():
        tick = next(ticks, None)
        return real() if tick is None else tick

    monkeypatch.setattr(time, "perf_counter", fake_clock)
    code = cli.cmd_stress_test(num_vertices=20, chord_interval=10)
    out = capsys.readouterr().out
    assert "FAIL" not in out or code != 0


# --------------------------------------------------------------- bridge


# FIXED 2026-09-23 (was BREAK BRG-01: solve_phi1_l1_via_rust never runs Rust: it returns a SCHEMA_READY payload and no Phi_1)
def test_rust_bridge_computes_phi1():
    res = RustCrateBridge().solve_phi1_l1_via_rust(Matrix([[-1, 1], [1, -1]]), Matrix([1, 0]))
    assert res is not None and "phi1" in res


# FIXED 2026-09-23 (was BREAK BRG-02: a Float boundary entry crashes payload serialisation with AttributeError (.p))
def test_rust_bridge_rejects_float_entries_cleanly():
    with pytest.raises((ValueError, TypeError)):
        RustCrateBridge().solve_phi1_l1_via_rust(Matrix([[Float(0.5)]]), Matrix([1]))


def test_rust_workspace_has_named_crates():
    """The bridge detects crates in a monorepo checkout; the native evaluator supplies functional results."""
    crates = RustCrateBridge().get_available_crates()
    assert {"omega_homology", "omega_pipelines"} <= set(crates)
    assert "omega_functional" in (APP_ROOT / "README.md").read_text(encoding="utf-8")


# FIXED 2026-09-23 (was BREAK BRG-03: chord_interval == num_vertices writes self-loop rows with a single +1: not an incidence matrix)
def test_generated_graph_is_an_incidence_matrix():
    p = RustCrateBridge.generate_high_dim_graph_instance(num_vertices=12, chord_interval=12)
    for r in range(p.d0.rows):
        assert sorted(x for x in p.d0.row(r) if x != 0) == [-1, 1], r


# ---------------------------------------------------------------- audit


# Outcomes can no longer be forged through their constructor (REG-15), so the breach is
# built with object.__new__, which skips validation: an AUTHORIZED outcome for an
# unlicensed problem, with Phi_1 = 5 and no token.
_BREACH = (
    "import coda_application.use_cases.audit_firewall as a\n"
    "from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator\n"
    "from coda_application.domain.entities import MasterNormalFormOutcome, ResidualPair, TerminalKind\n"
    "from coda_application.domain.value_objects import ExactRational, FirewallDecision\n"
    "from coda_application.tests.adversarial._support import make_problem\n"
    "breach = object.__new__(MasterNormalFormOutcome)\n"
    "for k, v in dict(problem_id='adv', terminal_kind=TerminalKind.AUTHORIZED,\n"
    "                 residual_pair=ResidualPair(ExactRational(5, 1), ExactRational(0, 1)), dual_witness=None,\n"
    "                 authority_token=None, layer_records=(), firewall_decision=FirewallDecision.PERMIT_AUTHORIZED,\n"
    "                 reason='forged', primal_repair=None, evidence_digest='').items():\n"
    "    object.__setattr__(breach, k, v)\n"
    "a.evaluate_coda_pipeline = lambda p, **kw: breach\n"
    "print(a.audit_authority_firewall(make_problem(), evaluator=NativeFunctionalEvaluator())['firewall_audit_passed'])\n"
)


def test_audit_catches_injected_breach():
    """HELD: the audit reports an injected unlicensed AUTHORIZED breach as failed (no crash)."""
    proc = run_python(["-c", _BREACH])
    assert proc.returncode == 0 and proc.stdout.strip() == "False", proc.stderr[-400:]


# FIXED 2026-09-23 (was BREAK AUD-01: the audit's checks are bare asserts: under `python -O` an injected breach reports passed=True)
def test_audit_survives_optimized_mode():
    proc = run_python(["-c", _BREACH], optimize=True)
    assert proc.stdout.strip() != "True"


# FIXED 2026-09-23 (was BREAK AUD-02: the audit re-runs the same solver: a false-zero obstruction (true Phi_1 = 5) passes it)
def test_audit_detects_false_zero():
    d0, c = Matrix.zeros(2, 1), Matrix([0, 5])
    report = audit_authority_firewall(make_problem(d0=d0, defect_cochain=c, fda_license_granted=True))
    assert foc_phi1(d0, c) == 0 or report["terminal_kind"] != "AUTHORIZED"


class AuditCrashed(Exception):
    pass


# FIXED 2026-09-23 (was BREAK AUD-03: a string license makes the audit raise AssertionError instead of returning a failed report)
def test_audit_reports_rather_than_crashes():
    try:
        report = audit_authority_firewall(make_problem(fda_license_granted="no"))
    except AssertionError as exc:
        raise AuditCrashed(str(exc)) from exc
    assert report["firewall_audit_passed"] is False
