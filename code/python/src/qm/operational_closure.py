"""Unresolved evidence inventory for the original C500 FQMC-1 contract.

The ten clauses are copied from campaigns/c500/README.md. Candidate source
names are review leads, not verified evidence bindings. This kernel does not
establish the launch-frozen class, replay dependencies, or certify closure.
AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import json
from typing import Any

_CLAUSE_DEFINITIONS = (
    ("Finite carrier and scalar domain", ["weyl_ccr_residual.py"]),
    ("Normalized states, effects, and their probability pairing", ["busch_effects.py"]),
    ("Transformations and measurement instruments", ["cptp_channels_stinespring.py"]),
    ("Composition rule and subsystem interface", ["refinement_subsystem_tower.py"]),
    ("Reversible and irreversible dynamics with explicit time semantics", ["dynamics_dichotomy.py", "continuous_time_locality_limit.py"]),
    ("Contextual and multipartite correlation semantics", ["contextuality_thresholds.py", "tensor_commuting_correlation_frontier.py"]),
    ("Terminating algorithms for every computational claim", []),
    ("Theorem, countermodel, or explicit OPEN status for every structural claim", []),
    ("Named metric and error bound for every finite-to-infinite comparison", ["norm_approximation_frontier.py", "tower_topological_completion.py"]),
    ("Price/refusal ledger naming every imported structure", ["terminal_price_list.py"]),
)


def fqmc1_clauses_inventory() -> list[dict[str, Any]]:
    """List the original ten obligations, without promoting candidate evidence."""
    return [
        {
            "clause_id": f"FQMC-1-C{index:02d}",
            "name": name,
            "status": "OPEN_UNVERIFIED",
            "evidence_class": "OPEN",
            "candidate_evidence_modules": modules.copy(),
            "evidence_binding_status": "NOT_VERIFIED_BY_KERNEL",
        }
        for index, (name, modules) in enumerate(_CLAUSE_DEFINITIONS, start=1)
    ]


def fqmc1_refusal_register() -> list[dict[str, str]]:
    """Record scoped refusal descriptions; these labels are not new proofs."""
    return [
        {
            "refusal_id": "REFUSAL-C500-01",
            "title": "Direct Non-Zero CCR in Finite Dimension",
            "mathematical_obstruction": "Tr([Q, P]) = 0 precludes [Q, P] = i*hbar*I for positive finite dimension and nonzero hbar",
            "retained_alternative": "Finite Weyl relations",
        },
        {
            "refusal_id": "REFUSAL-C500-02",
            "title": "Topology-Free Continuum Limits",
            "mathematical_obstruction": "An algebraic union alone does not supply a topology, completion, or convergence proof",
            "retained_alternative": "Explicit topology and comparison obligations",
        },
        {
            "refusal_id": "REFUSAL-C500-03",
            "title": "Unrestricted Uniform Correlation Decision Algorithm",
            "mathematical_obstruction": "MIP* = RE is a cited guardrail; not a locally formalized separation theorem",
            "retained_alternative": "Bounded computations and conditional interval certificates",
        },
        {
            "refusal_id": "REFUSAL-C500-04",
            "title": "Unpriced Continuum Field Limits",
            "mathematical_obstruction": "Finite benchmarks do not establish volume, truncation, or spacing limits",
            "retained_alternative": "Finite lattice data with open scaling obligations",
        },
    ]


def decide_fqmc1_terminal(untyped_count: int, open_count: int, *, global_refusal: bool = False) -> str:
    """Bookkeeping rule; the input counts need an independent evidence audit."""
    if type(untyped_count) is not int or type(open_count) is not int or min(untyped_count, open_count) < 0:
        raise ValueError("obligation counts must be nonnegative integers")
    if type(global_refusal) is not bool:
        raise ValueError("global_refusal must be a Boolean decision")
    if global_refusal:
        return "FQMC1_REFUSED_AS_GLOBAL_FINITE_REPLACEMENT"
    if untyped_count or open_count:
        return "FQMC1_OPEN_INTERNAL_GAPS"
    return "FQMC1_CLOSED_AT_DECLARED_CLASS"


def evaluate_fqmc1_terminal() -> dict[str, Any]:
    """Report unresolved obligations. Claimed status fields cannot certify them.

    There is no evidence validator in this kernel. A caller replacing a row's
    status or supplying a path/hash string still has not discharged the original
    class-wide clause. The launch-class identity is an additional unresolved
    internal dependency; it is not inferred from the existence of sample files.
    """
    candidates = fqmc1_clauses_inventory()
    clauses = [dict(row, status="OPEN_UNVERIFIED", evidence_class="OPEN",
                    evidence_binding_status="NOT_VERIFIED_BY_KERNEL") for row in candidates]
    expected_ids = {f"FQMC-1-C{index:02d}" for index in range(1, 11)}
    actual_ids = {row.get("clause_id") for row in clauses}
    missing = sorted(expected_ids - actual_ids)
    untyped_count = 1 + len(missing) + len(actual_ids - expected_ids)
    obligations = [{"obligation_id": row.get("clause_id"), "description": row.get("name"),
                    "category": "UNVERIFIED_CONTRACT_CLAUSE"} for row in clauses]
    return {
        "contract": "FQMC-1",
        "contract_source": "apps/finite_qm/campaigns/c500/README.md",
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "fqmc1_obligation_count": len(clauses),
        "untyped_internal_obligation_count": untyped_count,
        "open_internal_obligation_count": len(obligations),
        "class_binding_status": "NOT_ESTABLISHED",
        "class_identity_obligation": "Original nonempty launch-frozen class and its immutable binding are unresolved",
        "missing_clause_ids": missing,
        "terminal": decide_fqmc1_terminal(untyped_count, len(obligations)),
        "unqualified_complete_claim_count": None,
        "claim_scan_status": "NOT_VERIFIED_BY_KERNEL",
        "direct_ccr_refusal_retained": any(row["refusal_id"] == "REFUSAL-C500-01" for row in fqmc1_refusal_register()),
        "all_block_bets_scored": None,
        "bet_scoring_status": "NOT_VERIFIED_BY_KERNEL",
        "internal_open_obligations": obligations,
        "clauses": clauses,
        "refusals": fqmc1_refusal_register(),
    }


def generate_canonical_block10_receipt() -> dict[str, Any]:
    """Generate the bounded evidence-inventory receipt, with unknowns retained."""
    result = evaluate_fqmc1_terminal()
    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_10",
        "global_targets": "C500-T526..C500-T550",
        "terminal_outcome": result["terminal"],
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "closure_audit": result,
        "machine_bet_clauses": {name: result[name] for name in (
            "fqmc1_obligation_count", "untyped_internal_obligation_count",
            "open_internal_obligation_count", "terminal", "unqualified_complete_claim_count",
            "direct_ccr_refusal_retained", "all_block_bets_scored")},
        "standing_bet_clauses": {
            "finite_weyl_residual_retained": None,
            "direct_nonzero_ccr_in_finite_dimension": False,
            "at_least_one_operational_selection_axiom_is_declared": None,
            "every_limit_claim_names_topology_and_error_mode": None,
            "unrestricted_correlation_solver_claimed": False,
            "fqmc1_terminal": result["terminal"],
            "empirical_adequacy_claimed": False,
            "predecessor_and_all_block_inputs_are_exactly_pinned": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(generate_canonical_block10_receipt(), indent=2))

__all__ = ['decide_fqmc1_terminal', 'evaluate_fqmc1_terminal', 'fqmc1_clauses_inventory', 'fqmc1_refusal_register', 'generate_canonical_block10_receipt']
