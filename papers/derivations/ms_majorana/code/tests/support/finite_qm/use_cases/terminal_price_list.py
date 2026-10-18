"""Terminal Price List & Final Quantum Mechanics Claim Architecture.

Campaign C250 Block 10: The Price List and the Terminal Claim.
AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations
from pathlib import Path as _Path

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Declaration:
    """A declared primitive assumption on the finite QM price list."""
    index: int
    name: str
    label: str
    description: str
    is_primitive: bool
    status: str


@dataclass(frozen=True)
class FormalRefusal:
    """An explicit mathematical refusal recorded in the campaign ledger."""
    index: int
    name: str
    obstruction_type: str
    description: str


DECLARATIONS: list[Declaration] = [
    Declaration(
        index=1,
        name="effect_domain",
        label="Effect Domain of Probability",
        description=(
            "Admission of the effect algebra domain (POVMs) supporting cyclic "
            "path transport and Bargmann 3-loop trace invariants tr(E_A E_B E_C)."
        ),
        is_primitive=True,
        status="DECLARED",
    ),
    Declaration(
        index=2,
        name="real_embedding",
        label="Single Real Embedding",
        description=(
            "Selection of one real embedding into R fixing positive branch "
            "orientations for algebraic roots and sign conventions."
        ),
        is_primitive=True,
        status="DECLARED",
    ),
    Declaration(
        index=3,
        name="tensor_product_composition",
        label="Tensor Product Composition",
        description=(
            "Combining axioms and composition rule combining subsystems into composite "
            "tensor products while preserving local discrete holonomies."
        ),
        is_primitive=True,
        status="DECLARED",
    ),
    Declaration(
        index=4,
        name="dynamics_generator_lift",
        label="Dynamics Generator Lift",
        description=(
            "Generator lift mapping discrete periodic unitary steps Q/Z to a "
            "continuous time flow parameter."
        ),
        is_primitive=True,
        status="DECLARED",
    ),
    Declaration(
        index=5,
        name="branch_weighting_beyond_rational",
        label="Branch Weighting Beyond Rational Sector",
        description=(
            "Fine-graining or weighting of branches beyond the rational sector "
            "where integer branch counting admits no exact solution."
        ),
        is_primitive=True,
        status="DECLARED",
    ),
    Declaration(
        index=6,
        name="conductor_escalation_purification",
        label="Conductor Escalation for Purification",
        description=(
            "Acceptance of unbounded conductor escalation for purification in "
            "the directed union tower Q^ab."
        ),
        is_primitive=True,
        status="DECLARED",
    ),
]

FORMAL_REFUSALS: list[FormalRefusal] = [
    FormalRefusal(
        index=1,
        name="irrational_sector_branch_counting_refusal",
        obstruction_type="ALGEBRAIC_INTEGER_COUNTING_OBSTRUCTION",
        description=(
            "Equal-weight integer branch counting admits no finite representation "
            "for irrational Born weights without remainder."
        ),
    ),
    FormalRefusal(
        index=2,
        name="unconditioned_d2_projective_frame_functions_refusal",
        obstruction_type="TOPOLOGICAL_DISCONNECTEDNESS_OBSTRUCTION",
        description=(
            "Dimension d=2 projective measurements admit non-Bornian frame "
            "assignments unless extended to the effect domain."
        ),
    ),
    FormalRefusal(
        index=3,
        name="single_finite_conductor_carrier_refusal",
        obstruction_type="CYCLOTOMIC_FIELD_DEGREE_OBSTRUCTION",
        description=(
            "No single finite cyclotomic field Q(zeta_n) can host all prime-qudit "
            "MUB families, refusing bounded conductor escalation."
        ),
    ),
]

BORN_STATUS: str = "CONDITIONAL_EFFECT_MODELS_GENERAL_BRIDGE_OPEN"
DYNAMICS_STATUS: str = "FINITE_PERIODIC_AND_APERIODIC_MODELS_TOPOLOGY_DECLARED"
CONTINUUM_STATUS: str = "COMPLETION_AND_EMBEDDING_REQUIRE_ASSUMPTIONS"
TERMINAL_CLAIM: str = 'Finite algebraic models and conditional obstructions are established in their stated scopes; effect-domain representation, dynamics, and continuum bridges require their recorded hypotheses. The six declarations form a chosen inventory; their independence and exhaustiveness are open.'


def get_declarations() -> list[Declaration]:
    """Return the declared primitive price list."""
    return list(DECLARATIONS)


def get_declaration_count() -> int:
    """Return the count of entries in the chosen declaration inventory."""
    return len(DECLARATIONS)


def any_declaration_named_born_rule() -> bool:
    """Check whether any declaration is named the Born rule."""
    forbidden_names = {"born_rule", "the_born_rule", "born", "born_postulate"}
    for d in DECLARATIONS:
        if d.name.lower() in forbidden_names or "born rule" in d.label.lower():
            return True
    return False


def get_formal_refusals() -> list[FormalRefusal]:
    """Return the list of formal mathematical refusals."""
    return list(FORMAL_REFUSALS)


def get_refusal_count() -> int:
    """Return the count of formal mathematical refusals."""
    return len(FORMAL_REFUSALS)


def compile_block_10_payload() -> dict[str, Any]:
    """Compile the complete Block 10 evaluation payload."""
    decl_list = [asdict(d) for d in DECLARATIONS]
    refusal_list = [asdict(r) for r in FORMAL_REFUSALS]
    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "block_id": "block_10",
        "declaration_count": get_declaration_count(),
        "any_declaration_named_born_rule": any_declaration_named_born_rule(),
        "born_status": BORN_STATUS,
        "dynamics_status": DYNAMICS_STATUS,
        "continuum_status": CONTINUUM_STATUS,
        "standing_bets_scored": False,
        "terminal_claim_verified": False,
        "declarations_independent": None,
        "declarations_exhaustive": None,
        "refusal_count": get_refusal_count(),
        "terminal_claim": TERMINAL_CLAIM,
        "declarations": decl_list,
        "refusals": refusal_list,
    }


def emit_receipt(output_path: str | Path | None = None) -> Path:
    """Emit a JSON report; writing it does not verify its mathematical claims."""
    if output_path is None:
        output_path = (_Path(__file__).resolve().parents[4] / "apps" / "finite_qm") / "evidence" / "c250_block10_terminal_price_list.json"
    else:
        output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = compile_block_10_payload()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return output_path


if __name__ == "__main__":
    receipt = emit_receipt()
    print(f"Emitted receipt to {receipt}")

__all__ = ['BORN_STATUS', 'CONTINUUM_STATUS', 'DECLARATIONS', 'DYNAMICS_STATUS', 'Declaration', 'FORMAL_REFUSALS', 'FormalRefusal', 'TERMINAL_CLAIM', 'any_declaration_named_born_rule', 'compile_block_10_payload', 'emit_receipt', 'get_declaration_count', 'get_declarations', 'get_formal_refusals', 'get_refusal_count']
