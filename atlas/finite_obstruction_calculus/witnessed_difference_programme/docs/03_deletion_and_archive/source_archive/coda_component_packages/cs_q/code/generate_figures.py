"""generate_figures.py: Generates publication-quality figures for CODA-CS-Q.

Emits public_export/fig1_authority_descent.png illustrating the genuine
conditional mathematical decision tree for finite profile factorization:
1. Fiber constancy test and collision witness extraction.
2. Factor construction on the sampled image Prof(D).
3. Optional extension data, outside the finite solver.
4. Admission only when all eight declared checks pass.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def generate_bridge_architecture_figure(out_path: Path | None = None) -> Path:
    """Renders the CSQ conditional decision tree and saves to public_export."""
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Styling helpers
    box_blue = {"boxstyle": "round,pad=0.4", "fc": "#ebf8ff", "ec": "#3182ce", "lw": 1.5}
    box_green = {"boxstyle": "round,pad=0.4", "fc": "#f0fff4", "ec": "#38a169", "lw": 1.5}
    box_red = {"boxstyle": "round,pad=0.4", "fc": "#fff5f5", "ec": "#e53e3e", "lw": 1.5}
    box_gray = {"boxstyle": "round,pad=0.4", "fc": "#f7fafc", "ec": "#718096", "lw": 1.2}

    # 1. Root Input Node
    ax.text(
        0.5, 0.92,
        "Input: Query Probe $q: X \\to Y$ and Shadow Tower $\\Lambda_0$\n"
        "Nonempty finite domain $D \\subseteq X$; fixed profile/query observations",
        ha="center", va="center", fontsize=10, fontweight="bold",
        bbox=box_blue,
    )

    # Arrow to Decision 1
    ax.annotate("", xy=(0.5, 0.77), xytext=(0.5, 0.84),
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#2b6cb0"})

    # 2. Decision Diamond 1: Fiber Constancy
    ax.text(
        0.5, 0.73,
        "Decision 1: Fiber Constancy Test\n"
        "$\\forall x, y \\in D,\\; \\mathrm{Prof}(x) = \\mathrm{Prof}(y) \\rightarrow q(x) = q(y)$?",
        ha="center", va="center", fontsize=9.5, fontweight="bold",
        bbox=box_gray,
    )

    # Branch 1A: NO -> Collision Witness & Halt
    ax.annotate("", xy=(0.18, 0.58), xytext=(0.38, 0.70),
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#e53e3e"})
    ax.text(0.24, 0.66, "NO (Violated)", ha="center", va="center", fontsize=8.5, color="#c53030", fontweight="bold")
    ax.text(
        0.18, 0.52,
        "Refusal: Non-Factorable Query\n"
        "Exhibit witness pair: $(x_1, x_2) \\in D^2$\n"
        "$\\mathrm{Prof}(x_1) = \\mathrm{Prof}(x_2),\\; q(x_1) \\ne q(x_2)$\n"
        "Record residual: $R_{\\mathrm{factor}}$ (Halt)",
        ha="center", va="center", fontsize=8.5,
        bbox=box_red,
    )

    # Branch 1B: YES -> Factor on Realized Image
    ax.annotate("", xy=(0.72, 0.58), xytext=(0.58, 0.70),
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#38a169"})
    ax.text(0.70, 0.66, "YES (Satisfied)", ha="center", va="center", fontsize=8.5, color="#276749", fontweight="bold")
    ax.text(
        0.72, 0.52,
        "Factorization on Sampled Image (CSQ-T1)\n"
        "Construct $\\bar{q}: \\mathrm{Prof}(D) \\to Y$\n"
        "$\\bar{q}(\\mathrm{Prof}(x)) := q(x)$ for all $x \\in D$",
        ha="center", va="center", fontsize=8.5, fontweight="bold",
        bbox=box_green,
    )

    # Arrow from 1B to Decision 2
    ax.annotate("", xy=(0.72, 0.40), xytext=(0.72, 0.45),
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#2b6cb0"})

    # 3. Decision Diamond 2: Total Profile Extension
    ax.text(
        0.72, 0.35,
        "Optional extension to $P=\\prod_{\\lambda\\in\\Lambda_0} A_\\lambda$\n"
        "Additional data; not decided by the finite solver",
        ha="center", va="center", fontsize=9, fontweight="bold",
        bbox=box_gray,
    )

    # Branch 2A: Partial Image Only
    ax.annotate("", xy=(0.48, 0.22), xytext=(0.62, 0.32),
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#718096"})
    ax.text(0.50, 0.28, "No extension supplied", ha="center", va="center", fontsize=8, color="#4a5568")
    ax.text(
        0.45, 0.17,
        "Partial Factor Carrier\n"
        "$\\bar{q}$ defined on $\\mathrm{Prof}(D)$;\n"
        "Unsampled profiles raise KeyError.\n"
        "Record residual: $R_{\\mathrm{domain}}$",
        ha="center", va="center", fontsize=8,
        bbox=box_gray,
    )

    # Branch 2B: Closed Extension
    ax.annotate("", xy=(0.85, 0.22), xytext=(0.78, 0.32),
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#38a169"})
    ax.text(0.85, 0.28, "Explicit extension supplied", ha="center", va="center", fontsize=8, color="#276749")
    ax.text(
        0.85, 0.17,
        "Total Factor Extension\n"
        "$\\tilde{q}: P \\to Y$\n"
        "$\\tilde{q}|_{\\mathrm{Prof}(D)} = \\bar{q}$",
        ha="center", va="center", fontsize=8,
        bbox=box_green,
    )

    # Arrow to Terminal Conservativity (Step 8)
    ax.annotate("", xy=(0.65, 0.08), xytext=(0.65, 0.11),
                arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#2b6cb0"})

    # Step 8 Summary
    ax.text(
        0.65, 0.05,
        "Admission: all eight checks, including $\\tau_q(x)=\\tau_{\\mathrm{CS}}(x)$ for $x\\in D$, must pass",
        ha="center", va="center", fontsize=8.5, fontweight="bold",
        bbox=box_blue,
    )

    # Footer
    ax.text(
        0.5, 0.005,
        "CODA-CS-Q Finite Profile Factorization Decision Procedure | 8-Step Admission Audit | AuthorityEffect: None",
        ha="center", va="center", fontsize=8, style="italic", color="#718096",
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.02, 1.0)
    ax.axis("off")

    if out_path is None:
        out_path = Path(__file__).resolve().parent.parent / "public_export" / "fig1_authority_descent.png"
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    return out_path


if __name__ == "__main__":
    generated = generate_bridge_architecture_figure()
    print(f"Generated figure at {generated}")
