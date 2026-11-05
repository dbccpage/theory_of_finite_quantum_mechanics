# -*- coding: utf-8 -*-
"""
generate_figures.py: Pedagogy schematic for CODA-OR (NOT empirical evidence).

Plots:
1. 4-case diagram square defect classification under enriched comparison environment (OR-D2 / Section 2).
2. Comparison envelope non-creation firewall & support sieve audit (OR-D3 / OR-T5–T6).

Caption requirement:
"Pedagogical schematic of comparison envelope and 4-case diagram defect classification — not empirical evidence and not a physical law. AuthorityEffect: None."

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from coda_or_core import (
    ComparisonObject,
    SupportArrow,
    SupportSieve,
    evaluate_comparison_authority,
    reproduce_section_6a_worked_example,
)

_pkg_root = Path(__file__).resolve().parent.parent

def generate_fig1() -> Path:
    """Generate pedagogical figure illustrating CODA-OR square defects and anti-laundering firewall."""
    # 1. Replay the four-case worked example
    results = reproduce_section_6a_worked_example()

    # 2. Run Comparison Authority test cases with strictly bound targets
    sieve_empty = SupportSieve(target_object_id="X_empty", arrows=())
    obj_empty = ComparisonObject(
        object_id="X_empty",
        weight_class="finite_bilimit",
        support_sieve=sieve_empty,
    )
    auth_res_empty = evaluate_comparison_authority(obj_empty)

    sieve_no_term = SupportSieve(
        target_object_id="X_no_term",
        arrows=(
            SupportArrow(
                source_regime_id="Reg_A1",
                target_object_id="X_no_term",
                source_has_authority=True,
                certificate_id="chi_A1",
            ),
        ),
    )
    obj_no_term = ComparisonObject(
        object_id="X_no_term",
        weight_class="finite_bilimit",
        support_sieve=sieve_no_term,
        terminalizer_tau=None,
    )
    auth_res_no_term = evaluate_comparison_authority(obj_no_term)

    sieve_cert = SupportSieve(
        target_object_id="X_cert",
        arrows=(
            SupportArrow(
                source_regime_id="Reg_A1",
                target_object_id="X_cert",
                source_has_authority=True,
                certificate_id="chi_A1",
            ),
        ),
    )
    obj_certified = ComparisonObject(
        object_id="X_cert",
        weight_class="finite_bilimit",
        support_sieve=sieve_cert,
        descent_d="D_X",
        verifier_v="V_X",
        terminalizer_tau="tau_X",
    )
    auth_res_certified = evaluate_comparison_authority(obj_certified)

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Panel 1: 4-Case Square Defect Classification
    cases = ["Square 1\nStrict", "Square 2\nExact Repair", "Square 3\nH^1 Tear", "Square 4\nOpen Defect"]
    quotient_distances = [float(r.quotient_distance) for r in results]
    colors = ["#2ecc71", "#3498db", "#e67e22", "#e74c3c"]

    bars = ax1.bar(cases, quotient_distances, color=colors, width=0.55, edgecolor="black", linewidth=1.2)
    ax1.set_ylabel(r"Quotient Distance $\Phi([\delta])$ (exact $L_1$)", fontsize=11)
    ax1.set_title("OR-D2: 4-Case Square Defect Classification\n(Worked example replay)", fontsize=12, fontweight="bold")
    ax1.set_ylim(0, 4)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    for bar, r in zip(bars, results):
        h = bar.get_height()
        status_label = {"StrictCommute": "Strict", "WeakCommuteCertified": "Exact repair",
                        "H^1DiagramTear": "Closed tear",
                        "OpenDiagramObstruction": "Open defect"}.get(r.status.value, r.status.value)
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.15, f"{status_label}\n(dist={h:.1f})",
                 ha="center", va="bottom", fontsize=8, fontweight="semibold")

    # Panel 2: Comparison Envelope Non-Creation Firewall
    auth_labels = ["Empty Support Sieve\n(Supp_Auth = ∅)", "Missing Terminalizer\n(No D, V, τ)", "Certified\nComparison"]
    residuals = [
        float(auth_res_empty.residual_mass),
        float(auth_res_no_term.residual_mass),
        float(auth_res_certified.residual_mass),
    ]
    auth_colors = ["#c0392b", "#d35400", "#27ae60"]

    bars2 = ax2.bar(auth_labels, residuals, color=auth_colors, width=0.5, edgecolor="black", linewidth=1.2)
    ax2.set_ylabel("Residual Mass", fontsize=11)
    ax2.set_title("OR-T6: Completion Non-Creation Firewall\n(X in Comp(Reg) does NOT imply Auth(X))", fontsize=12, fontweight="bold")
    ax2.set_ylim(0, 1.3)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    verdicts = [
        f"REFUSAL\n{auth_res_empty.refusal_code}",
        f"REFUSAL\n{auth_res_no_term.refusal_code}",
        "CERTIFIED\nlocal terminal",
    ]
    for bar, v, r_val in zip(bars2, verdicts, residuals):
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.05, f"{v}\n(res={r_val:.2f})",
                 ha="center", va="bottom", fontsize=8, fontweight="semibold")

    fig.suptitle(
        "CODA-OR: Omniversal Re-Presentation (Comparison Envelope)\n"
        "Pedagogical schematic — not empirical evidence and not a physical law. AuthorityEffect: None.",
        fontsize=11,
        fontstyle="italic",
        y=1.02,
    )

    plt.tight_layout()

    out_dir = _pkg_root / "public_export"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "fig1_authority_descent.png"
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Generated {out_path}")
    return out_path


if __name__ == "__main__":
    generate_fig1()
