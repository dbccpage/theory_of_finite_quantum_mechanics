# -*- coding: utf-8 -*-
"""
Adversarial tests of documentation and claim-ledger statements about apps/coda.

Targets: apps/coda/docs/test_catalog_and_failure_modes.md, apps/coda/README.md,
and the F005 claim ledgers that cite apps/coda tests as evidence (GTLA-06..11,
OR-T9/T10, A-T8) plus the FDA paper's halt-guard definition. A citation is
checked for existence and for whether the cited test actually exercises the
cited claim.

AuthorityEffect: None.
"""

from __future__ import annotations

import ast
import inspect
import re

from coda_application.domain.entities import MasterNormalFormOutcome
from coda_application.domain.firewall_engine import AuthorityFirewallEngine
from coda_application.tests.adversarial._support import APP_ROOT, REPO_ROOT

CATALOG = APP_ROOT / "docs" / "test_catalog_and_failure_modes.md"
F005 = APP_ROOT.parents[1] / "docs" / "source_archive" / "coda_component_packages"
LEDGERS = [
    F005 / "coda_gtla" / "coda_gtla_claim_ledger.md.txt",
    F005 / "or" / "coda_or_claim_ledger.md.txt",
    F005 / "a" / "coda_a_claim_ledger.md.txt",
]
NODE = re.compile(r"apps/coda/tests/(\w+)\.py::(test_\w+)")


def text(path):
    return path.read_text(encoding="utf-8")


def source_of_test(module, name):
    tree = ast.parse(text(APP_ROOT / "tests" / f"{module}.py"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(text(APP_ROOT / "tests" / f"{module}.py"), node)
    return None


def ledger_row(claim_id):
    for ledger in LEDGERS:
        for line in text(ledger).splitlines():
            cells = line.split("|")
            if len(cells) > 2 and re.sub(r"[*`\s]", "", cells[1]) == claim_id:
                return line
    raise LookupError(claim_id)


def _norm(s):
    return re.sub(r"[^a-z]", "", s.lower())


# FIXED 2026-09-23 (was BREAK DOC-01: catalog G1-G7 (Well-Formedness ... External License) and code GUARD_1-7 (Role ... Verification Limits) overlap only in the word 'cocycle')
def test_catalog_guards_match_code_guards():
    doc = re.findall(r"\*\*\$G_\d\$ \(([^)]+)\):\*\*", text(CATALOG))
    code = [v for k, v in vars(AuthorityFirewallEngine).items() if k.startswith("GUARD_")]
    assert len(doc) == 7
    assert sorted(map(_norm, doc)) == sorted(_norm(c.split("_", 2)[2]) for c in code)


# FIXED 2026-09-23 (was BREAK DOC-02: the catalog says 'all 23 automated tests'; the original suite has 29)
def test_catalog_test_count_is_current():
    count = sum(
        1
        for p in (APP_ROOT / "tests").glob("test_*.py")
        for node in ast.walk(ast.parse(text(p)))
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    )
    assert f"all {count} automated tests" in text(CATALOG)


def test_cited_apps_coda_test_nodes_exist():
    """Any still-active direct app test citation resolves to a real test."""
    cited = {m for ledger in LEDGERS for m in NODE.findall(text(ledger))}
    assert all(source_of_test(mod, name) for mod, name in cited)
    assert "former `apps/coda/tests/` prefix" in text(LEDGERS[0])


def test_catalog_reference_papers_exist():
    """HELD: the six F004 papers the catalog is keyed to exist on disk."""
    base = REPO_ROOT / "omega_engine_atlas" / "coda_atlas" / "F004_papers" / "001_finite_obstruction_calculus"
    for prefix in ("004", "005", "027", "028", "029", "030"):
        assert any(p.name.startswith(prefix + "_") for p in base.iterdir()), prefix


# FIXED 2026-09-23 (was BREAK DOC-03: OR-T10 is 'THEOREM / MECHANIZED' on test_high_dim_stress.py, which never exhausts a budget)
def test_or_t10_does_not_promote_budget_policy_to_a_mechanized_theorem():
    row = ledger_row("OR-T10")
    assert "DECLARED POLICY" in row
    assert "no package-local proof or runtime test" in row.lower()
    assert "MECHANIZED" not in row


# FIXED 2026-09-23 (was BREAK DOC-04: GTLA-09 (budget exhaustion forces refusal) cites a test that asserts CLOSED_RESIDUAL and a runtime)
def test_gtla_09_evidence_exercises_refusal():
    row = ledger_row("GTLA-09")
    assert "test_coda_gtla.py::test_master_normal_form_refusal_empty_sieve" in row
    source = text(F005 / "coda_gtla" / "code" / "tests" / "test_coda_gtla.py")
    assert "assert receipt.terminal_outcome.kind == TerminalKind.REFUSED" in source
    assert "WITHDRAWN" in row


# FIXED 2026-09-23 (was BREAK DOC-05: GTLA-10 ('locked into the Anomalon register') cites a pipeline test that never reads the register)
def test_gtla_10_does_not_claim_a_persistence_proof():
    row = ledger_row("GTLA-10")
    assert "not a current persistence proof" in row
    assert "test_master_normal_form_closed_residual_anomalon" in row
    source = text(F005 / "coda_gtla" / "code" / "tests" / "test_coda_gtla.py")
    assert "assert receipt.terminal_outcome.kind == TerminalKind.CLOSED_RESIDUAL" in source


# FIXED 2026-09-23 (was BREAK DOC-06: FDA paper: guards are 'derived from a finite evidence record, not supplied as unbound booleans'; two are bool arguments)
def test_halt_guards_are_not_unbound_booleans():
    assert "not supplied as unbound booleans" in text(F005 / "fda" / "coda_fda.md")
    params = inspect.signature(AuthorityFirewallEngine.evaluate_authority).parameters
    assert [n for n, p in params.items() if isinstance(p.default, bool)] == []


# FIXED 2026-09-23 (was BREAK DOC-07: README promises 'mechanical LP dual witnesses'; no LP is solved anywhere in the app)
def test_app_solves_an_lp():
    calls = set()
    for layer in ("domain", "infrastructure", "use_cases"):
        for p in (APP_ROOT / layer).rglob("*.py"):
            for node in ast.walk(ast.parse(text(p))):
                if isinstance(node, ast.Call):
                    f = node.func
                    calls.add(f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", ""))
    assert "unweighted coordinate L1 distance" in text(APP_ROOT / "README.md")
    assert "solve_l1_quotient" in calls


# FIXED 2026-09-23 (was BREAK DOC-08: ST-01 claims 'zero duality gap' but outcomes carry no primal repair, so no gap is certified)
def test_outcome_certifies_duality_gap():
    assert "zero duality gap" in text(CATALOG)
    fields = {f.name for f in MasterNormalFormOutcome.__dataclass_fields__.values()}
    assert fields & {"repair_witness", "primal_repair", "primal_residual"}
