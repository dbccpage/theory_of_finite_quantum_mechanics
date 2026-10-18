"""
Subgap R6 (Sporadic Literature Classes / Conjecture 2 Slices Reduction) Receipt Generator.

Firewall: stated region only; mints no authority
AuthorityEffect: None

This script does not recompute Conjecture 2. main() refuses to overwrite
`mub_subgap_r6_closure_receipt.json`. The committed receipt status is
NOT_A_CERTIFICATE. The in-memory dict below is not a certificate.
"""

from __future__ import annotations

from typing import Any

FIREWALL = "stated region only; mints no authority"


def generate_subgap_r6_receipt() -> dict[str, Any]:
    """Return a non-certificate description. This function does not recompute counts."""
    receipt = {
        "schema_version": "omega.mub6.subgap_r6_closure_receipt.v1",
        "project": "MUB(6)",
        "firewall": FIREWALL,
        "authority_effect": "None",
        "subgap_id": "R6",
        "name": "Sporadic Literature CHM Classes & Conjecture 2 Slices Reduction",
        "status": "NOT_A_CERTIFICATE",
        "verified": False,
        "arithmetic": "not recomputed by this script",
        "lean4_module": "lean4/research_programs/mub6/Conjecture2GeneralMechanization.lean",
        "formalization": {
            "conjecture_2a_tensor_product_proved": False,
            "conjecture_2b_slice_reduction_formalized": False,
            "proposition_4_2_mechanized": False,
        },
        "claim_hygiene": {
            "what_it_supports": (
                "Nothing beyond the separate odd-parity identity and the 2-circulant "
                "SymPy and Rust witnesses. This dict does not recompute them."
            ),
            "what_it_does_not_support": (
                "Does not prove Conjecture 2, Proposition 4.2, MUB(6)=3, or MUB(6)<=3."
            ),
            "narrowest_defensible_claim": (
                "This generator is not a certificate and must not overwrite the committed receipt."
            ),
            "next_test_needed": (
                "A matrix-level recomputation of Conjecture 2 and Proposition 4.2."
            ),
        },
    }
    return receipt


def main() -> None:
    raise SystemExit(
        "REFUSED: compute_subgap_r6_closure_receipt.py does not recompute Conjecture 2 "
        "and will not overwrite mub_subgap_r6_closure_receipt.json."
    )


if __name__ == "__main__":
    main()
