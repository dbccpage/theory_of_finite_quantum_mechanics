# -*- coding: utf-8 -*-
"""
generate_figures.py: Pedagogy schematic for CODA-CS (NOT empirical evidence).

Plots:
1. 8-step BridgeAdmissible gate pipeline and query-relative authority (CS-T5).
   Y-axis is explicitly labeled as assigned diagnostic score (convention), not a measured physical residual.
2. Section 0 Worked Example: discrete left quadrature sum Q(X) = 7/8 on grid {0, 1/4, 2/4, 3/4, 1}.
   Endpoint t=1 has zero weight in the left sum.
3. Four Dots, Two Shadows: Boolean fibre collision in 2 x 2 (CS-T3 & CS-T4).

Caption requirement:
"Schematic of continuum finite-shadow tower, left quadrature, and Boolean fiber collision — not empirical evidence and not a physical law. AuthorityEffect: None."

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from coda_cs_core import (
    ContinuumQuery,
    ContinuumSignal,
    ProfileMap,
    ShadowSlice,
    ShadowTower,
    evaluate_query_authority,
    reproduce_worked_example,
)
from sympy import Matrix, Rational

matplotlib.use("Agg")
_pkg_root = Path(__file__).resolve().parent.parent


def generate_fig1() -> Path:
    """Generate pedagogical figure illustrating CODA-CS query authority, quadrature, and fiber collision."""
    val1, val2, _admissible = reproduce_worked_example()

    # Test cases for admission pipeline
    pts = (Rational(0, 4), Rational(1, 4), Rational(2, 4), Rational(3, 4))
    prof = ProfileMap(profile_id="Grid_4", sample_points=pts)
    samples = {p: Rational(p) for p in pts}
    sig = ContinuumSignal(signal_id="LinearSig", samples=samples)
    q_good = ContinuumQuery(query_id="Energy", degree_bound=2, evaluator=lambda s: Rational(1, 2))

    tower_good = ShadowTower(
        tower_id="GoodTower",
        slices=(ShadowSlice("S1", 4, True),),
        is_cofinal=True,
    )
    res_good = evaluate_query_authority(
        signal=sig,
        query=q_good,
        tower=tower_good,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 2),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )

    q_unbounded = ContinuumQuery(query_id="HighDeg", degree_bound=10, evaluator=lambda s: Rational(1, 2))
    res_deg = evaluate_query_authority(
        signal=sig,
        query=q_unbounded,
        tower=tower_good,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 2),
    )

    tower_non_cofinal = ShadowTower(
        tower_id="BadTower",
        slices=(ShadowSlice("S1", 4, True),),
        is_cofinal=False,
    )
    res_cofinal = evaluate_query_authority(
        signal=sig,
        query=q_good,
        tower=tower_non_cofinal,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 2),
    )

    tower_no_shadow = ShadowTower(
        tower_id="UnauthTower",
        slices=(ShadowSlice("S1", 4, False),),
        is_cofinal=True,
    )
    res_shadow = evaluate_query_authority(
        signal=sig,
        query=q_good,
        tower=tower_no_shadow,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 2),
    )

    res_no_term = evaluate_query_authority(
        signal=sig,
        query=q_good,
        tower=tower_good,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 2),
        has_terminalizer=False,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )

    # 3-Panel Plot
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 5.2))

    # Panel 1: Admissibility Gates & Assigned Diagnostic Scores
    labels = [
        "Admissible\nQuery",
        "Unbounded\nDegree (>4)",
        "Non-Cofinal\nTower",
        "Unauthorized\nShadow",
        "Missing\nTerminalizer",
    ]
    scores = [
        float(res_good.residual_mass),
        float(res_deg.residual_mass),
        float(res_cofinal.residual_mass),
        float(res_shadow.residual_mass),
        float(res_no_term.residual_mass),
    ]
    colors = ["#27ae60", "#e74c3c", "#d35400", "#c0392b", "#8e44ad"]

    bars = ax1.bar(labels, scores, color=colors, width=0.55, edgecolor="black", linewidth=1.2)
    ax1.set_ylabel("Assigned Diagnostic Score (Convention)", fontsize=10, fontweight="semibold")
    ax1.set_title("Bridge Admissibility & Authority (CS-T5)\n[Assigned Diagnostic Convention]", fontsize=11, fontweight="bold")
    ax1.set_ylim(0, 2.0)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    verdicts = [
        "CERTIFIED\n0.0",
        "REFUSED\n1.0",
        "REFUSED\n1.0",
        "REFUSED\n1.0",
        "REFUSED\n0.25",
    ]
    for bar, v, s_val in zip(bars, verdicts, scores):
        h = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.03,
            v,
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
        )

    refusal_table = (
        "Refusal Code Key:\n"
        "• Unbounded: R_unbounded_degree\n"
        "• Non-Cofinal: NoCofinalAuthorizedShadow\n"
        "• Unauthorized: NoFiniteShadow\n"
        "• No Terminal: NoTerminal"
    )
    ax1.text(
        0.03,
        0.96,
        refusal_table,
        transform=ax1.transAxes,
        fontsize=7.5,
        va="top",
        bbox={"boxstyle": "round,pad=0.4", "facecolor": "#ffffff", "edgecolor": "#bdc3c7", "alpha": 0.92},
    )

    # Panel 2: Section 0 Worked Example - Left Quadrature Sum = 7/8
    t_nodes = [0.0, 0.25, 0.5, 0.75, 1.0]
    x_nodes = [0.0, 0.5, 1.0, 1.5, 2.0]
    ax2.plot(t_nodes, x_nodes, marker="o", color="#2980b9", linewidth=2.2, markersize=7, label="Signal X(t)=2t")

    # Draw left quadrature step rectangles (t_k, X(t_k)^2 * 0.25)
    rect_x = [0.0, 0.25, 0.5, 0.75]
    rect_y = [(2 * t) ** 2 * 0.25 for t in rect_x]
    ax2.bar(
        [t + 0.125 for t in rect_x],
        rect_y,
        width=0.22,
        color="#3498db",
        alpha=0.35,
        edgecolor="#2980b9",
        linewidth=1.2,
        label=r"Left Quadrature Terms $X(t_k)^2 \cdot \frac{1}{4}$",
    )

    ax2.set_xlabel("Domain Node t", fontsize=10)
    ax2.set_ylabel("Signal / Quadrature Weight", fontsize=10, fontweight="semibold")
    ax2.set_title("Worked Example: Left Quadrature\n" + r"$Q(X) = \frac{1}{4}\sum_{k=0}^3 X(k/4)^2 = \frac{7}{8}$", fontsize=11, fontweight="bold")
    ax2.set_ylim(-0.15, 2.35)
    ax2.set_xlim(-0.05, 1.08)
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend(loc="upper left", fontsize=8)

    ax2.text(
        0.04,
        0.58,
        f"Discrete Left Sum = {val1}\n"
        f"Terms: 0 + 1/16 + 1/4 + 9/16 = 7/8\n"
        r"Endpoint $t=1$ has 0 weight in left sum." "\n"
        f"Fiber Constancy: q(Sig1)=q(Sig2)={val2}",
        transform=ax2.transAxes,
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "#f8f9fa", "edgecolor": "#bdc3c7"},
    )

    # Panel 3: Four Dots, Two Shadows (CS-T3 & CS-T4)
    # 4 points in 2 x 2: (0,0), (0,1), (1,0), (1,1)
    points = [(0, 0), (0, 1), (1, 0), (1, 1)]
    labels_pts = ["(F, F)\nq=F", "(F, T)\nq=T", "(T, F)\nq=F", "(T, T)\nq=T"]
    colors_pts = ["#2980b9", "#e74c3c", "#2980b9", "#e74c3c"]

    for (px, py), plab, pcol in zip(points, labels_pts, colors_pts):
        ax3.scatter(px, py, s=160, color=pcol, zorder=5, edgecolor="black", linewidth=1.2)
        offset_y = 0.12 if py == 0 else -0.16
        ax3.text(px, py + offset_y, plab, ha="center", va="center", fontsize=9, fontweight="bold")

    # Draw fibers of first coordinate
    ax3.axvline(x=0, color="#8e44ad", linestyle="--", linewidth=1.8, alpha=0.7, label=r"Fibre 1: $x.1=\mathsf{false}$ (splits q)")
    ax3.axvline(x=1, color="#27ae60", linestyle="--", linewidth=1.8, alpha=0.7, label=r"Fibre 2: $x.1=\mathsf{true}$ (splits q)")

    # Connect colliding points in fibre 0
    ax3.annotate(
        "Collision: same first,\ndifferent second (q)",
        xy=(0, 0.5),
        xytext=(-0.35, 0.5),
        arrowprops={"arrowstyle": "->", "color": "#c0392b", "lw": 1.5},
        ha="right",
        va="center",
        fontsize=8.5,
        fontweight="semibold",
        color="#c0392b",
    )

    ax3.set_xticks([0, 1])
    ax3.set_xticklabels([r"$\mathsf{false}$ (0)", r"$\mathsf{true}$ (1)"], fontsize=9.5)
    ax3.set_yticks([0, 1])
    ax3.set_yticklabels([r"$\mathsf{false}$ (0)", r"$\mathsf{true}$ (1)"], fontsize=9.5)
    ax3.set_xlabel("First Coordinate (Coarse Shadow p)", fontsize=10, fontweight="semibold")
    ax3.set_ylabel("Second Coordinate (Query q)", fontsize=10, fontweight="semibold")
    ax3.set_title("Four Dots, Two Shadows (CS-T3 / CS-T4)\n" + r"$\neg\mathsf{Factors}(x.1, x.2)$ — Fibre Collision", fontsize=11, fontweight="bold")
    ax3.set_xlim(-0.75, 1.45)
    ax3.set_ylim(-0.35, 1.35)
    ax3.grid(True, linestyle=":", alpha=0.4)
    ax3.legend(loc="lower right", fontsize=7.5)

    fig.suptitle(
        "CODA-CS: Continuum Finite-Shadow Tower (Omega_kappa)\n"
        "Schematic of continuum finite-shadow tower, left quadrature, and Boolean fiber collision — not empirical evidence and not a physical law. AuthorityEffect: None.",
        fontsize=10.5,
        fontstyle="italic",
        y=1.03,
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
