# -*- coding: utf-8 -*-
r"""
generate_figures.py: Generates publication-quality figure for CODA-GTLA.
Emits public_export/fig1_authority_descent.png with non-overlapping bounding boxes
and exact mathematical notation.

AuthorityEffect: None.
"""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

if hasattr(matplotlib, "use"):
    try:
        matplotlib.use("Agg")
    except Exception:
        pass

import os

os.environ.setdefault("MPLBACKEND", "Agg")
import matplotlib.pyplot as plt


def generate_gtla_figure(output: Path | None = None) -> Path:
    """Generate the non-overlapping CODA-GTLA architecture figure."""
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)

    # Header / Title Box
    ax.text(
        0.5,
        0.94,
        "CODA-GTLA: Finite declared evaluator\n"
        r"$\Pi^\sharp = \tau^\sharp \circ \mathrm{FOC}^\sharp \circ D^\sharp \circ \rho^\sharp \circ R^\sharp$",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.5", fc="#f7fafc", ec="#4a5568", lw=1.2),
    )

    # Five Finite Stages (Horizontal Sequence)
    stages = [
        (r"$R^\sharp$" + "\nCandidate sieve\nEmpty set refuses", 0.10, "#fed7d7"),
        (r"$\rho^\sharp$" + "\nProfile check\nCoarse / fine", 0.30, "#e2e8f0"),
        (r"$D^\sharp$" + "\nCoordinate gluing\nAll intersections", 0.50, "#bee3f8"),
        (
            r"$\mathrm{FOC}^\sharp$" + "\nExact distances\nQuotient LP & dual",
            0.70,
            "#e9d8fd",
        ),
        (r"$\tau^\sharp$" + "\nOrdered routing\nTerminal label", 0.90, "#feebc8"),
    ]

    for label, x, col in stages:
        ax.text(
            x,
            0.75,
            label,
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc=col, ec="#4a5568", lw=1.0),
        )

    # Arrows between stages
    arrow_xs = [(0.17, 0.23), (0.37, 0.43), (0.57, 0.63), (0.77, 0.83)]
    for x1, x2 in arrow_xs:
        ax.annotate(
            "",
            xy=(x2, 0.75),
            xytext=(x1, 0.75),
            arrowprops=dict(arrowstyle="->", lw=1.5, color="#2d3748"),
        )

    # Diagnostic Evidence Banner
    ax.text(
        0.5,
        0.60,
        r"Diagnostic Evidence: $[\delta_b] \in Q^1 = C^1 / \mathrm{im}(d_0), \quad \Phi_1([\delta_b]) \geq 0, \quad \Gamma_2([d_1 \delta_b]) \geq 0$",
        ha="center",
        va="center",
        fontsize=9,
        style="italic",
        bbox=dict(boxstyle="round,pad=0.3", fc="#edf2f7", ec="#a0aec0"),
    )

    # Central Non-Promotion Firewall
    ax.axhline(y=0.48, xmin=0.06, xmax=0.94, color="#e53e3e", linestyle="--", lw=2.2)
    ax.text(
        0.5,
        0.48,
        r"DECLARED MODEL: A quotient class does not authenticate a licence"
        "\n"
        r"Full-input replay checks consistency of the local outcome",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#c53030",
        bbox=dict(boxstyle="round,pad=0.35", fc="#fff5f5", ec="#e53e3e", lw=1.2),
    )

    # Three Disjoint Terminal Outlets - carefully spaced to eliminate bounding box collisions
    terminals = [
        (
            r"$\mathbb{T}_{\mathrm{auth}}$: Declared authorized branch"
            "\n"
            r"($\Phi_1 = 0 \ \wedge \ \Gamma_2 = 0 \ \wedge \ \mathrm{AuthToken}$)"
            "\n"
            "Declared license in this model",
            0.17,
            "#c6f6d5",
            "#276749",
        ),
        (
            r"$\mathbb{T}_{\mathrm{res}}$: Closed Residual (Anomalon)"
            "\n"
            r"($\Phi_1 > 0 \ \wedge \ \Gamma_2 = 0$)"
            "\n"
            r"Verified Dual Witness $y^* \in \mathrm{ker}(d_0^T)$",
            0.50,
            "#feebc8",
            "#9c4221",
        ),
        (
            r"$\mathbb{F}_{\mathrm{term}}$: Refusal Terminal"
            "\n"
            r"(earlier stage fails, or $\Gamma_2>0$, or zero/unlicensed)"
            "\n"
            "Refusal in this evaluation",
            0.83,
            "#fed7d7",
            "#9b2c2c",
        ),
    ]

    for label, x, bg_col, text_col in terminals:
        ax.text(
            x,
            0.25,
            label,
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            color=text_col,
            bbox=dict(boxstyle="round,pad=0.4", fc=bg_col, ec=text_col, lw=1.1),
        )
        ax.annotate(
            "",
            xy=(x, 0.34),
            xytext=(x, 0.43),
            arrowprops=dict(arrowstyle="->", lw=1.5, color=text_col),
        )

    # Bottom caption
    ax.text(
        0.5,
        0.08,
        r"Disjoint Partition: $\mathbb{T}_{\mathrm{auth}} \sqcup \mathbb{T}_{\mathrm{res}} \sqcup \mathbb{F}_{\mathrm{term}}$ uses ordered routing after earlier checks."
        "\n"
        r"First check sieve, refinement and gluing. Then classify; extension and tie enumeration remain open.",
        ha="center",
        va="center",
        fontsize=8,
        style="italic",
        color="#4a5568",
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    out_dir = Path(__file__).resolve().parent.parent / "public_export"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = output if output is not None else out_dir / "fig1_authority_descent.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    return out_path


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    path = generate_gtla_figure(parser.parse_args().output)
    print(f"Generated figure at {path}")
