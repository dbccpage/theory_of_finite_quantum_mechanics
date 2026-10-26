# -*- coding: utf-8 -*-
"""
generate_figures.py: Generates publication-quality figure for CODA-A.
Diagrams the linear projection decomposition V = im(C) ⊕ ker(C), residual map r = I - C,
and the canonical cokernel identification coker(C) ≅ ker(C).
Emits public_export/fig1_projection_cokernel.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def generate_projection_cokernel_figure(out_path: Path | None = None) -> Path:
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    # Title Banner
    ax.text(
        0.5, 0.93,
        "CODA-A: Projection Decomposition & Cokernel Section\n"
        r"$V = \mathrm{im}(C) \oplus \ker(C),\quad r = I - C,\quad \mathrm{coker}(C) \cong \ker(C)$",
        ha="center", va="center", fontsize=11, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.5", fc="#f7fafc", ec="#4a5568", lw=1.2)
    )

    # Ambient Space V
    ax.add_patch(Rectangle((0.08, 0.45), 0.22, 0.35, fc="#ebf8ff", ec="#3182ce", lw=1.5, ls="--"))
    ax.text(0.19, 0.76, r"Ambient Space $V$", ha="center", fontsize=11, fontweight="bold", color="#2b6cb0")
    ax.text(0.19, 0.65, r"Vector $x = (3, 4)^T$", ha="center", fontsize=10)
    ax.text(0.19, 0.52, r"$x = Cx + r(C, x)$", ha="center", fontsize=9, style="italic", color="#4a5568")

    # Image Subspace im(C)
    ax.add_patch(Rectangle((0.42, 0.62), 0.24, 0.18, fc="#feebc8", ec="#dd6b20", lw=1.5))
    ax.text(0.54, 0.74, r"$\mathrm{im}(C) = \mathrm{Fix}(C)$", ha="center", fontsize=11, fontweight="bold", color="#c05621")
    ax.text(0.54, 0.66, r"$Cx = (3, 0)^T$", ha="center", fontsize=10)

    # Kernel Subspace ker(C)
    ax.add_patch(Rectangle((0.42, 0.35), 0.24, 0.20, fc="#c6f6d5", ec="#38a169", lw=1.5))
    ax.text(0.54, 0.49, r"$\ker(C) = \mathrm{Leftovers}$", ha="center", fontsize=11, fontweight="bold", color="#276749")
    ax.text(0.54, 0.40, r"$r(C, x) = (0, 4)^T$", ha="center", fontsize=10)

    # Cokernel Quotient V / im(C)
    ax.add_patch(Rectangle((0.76, 0.45), 0.18, 0.35, fc="#e9d8fd", ec="#805ad5", lw=1.5))
    ax.text(0.85, 0.74, r"Cokernel", ha="center", fontsize=11, fontweight="bold", color="#6b46c1")
    ax.text(0.85, 0.66, r"$V / \mathrm{im}(C)$", ha="center", fontsize=11, fontweight="bold", color="#6b46c1")
    ax.text(0.85, 0.54, r"Class $[x]$", ha="center", fontsize=10)

    # Arrows
    # x -> Cx (Projection C)
    ax.annotate("", xy=(0.42, 0.71), xytext=(0.30, 0.67),
                arrowprops=dict(arrowstyle="->", lw=2, color="#dd6b20"))
    ax.text(0.35, 0.73, r"$C$", ha="center", fontsize=11, fontweight="bold", color="#dd6b20")

    # x -> r(C, x) (Residual r = I - C)
    ax.annotate("", xy=(0.42, 0.47), xytext=(0.30, 0.62),
                arrowprops=dict(arrowstyle="->", lw=2, color="#38a169"))
    ax.text(0.34, 0.51, r"$r = I - C$", ha="center", fontsize=11, fontweight="bold", color="#38a169")

    # V -> V / im(C) (Quotient map q : V -> V / im(C))
    ax.annotate("", xy=(0.78, 0.80), xytext=(0.25, 0.80),
                arrowprops=dict(arrowstyle="->", lw=2, color="#805ad5", connectionstyle="arc3,rad=-0.08"))
    ax.text(0.52, 0.835, r"Quotient $q : V \to V / \mathrm{im}(C)$", ha="center", fontsize=10, fontweight="bold", color="#6b46c1")

    # V / im(C) -> ker(C) (Induced section s)
    ax.annotate("", xy=(0.66, 0.45), xytext=(0.76, 0.52),
                arrowprops=dict(arrowstyle="->", lw=2, color="#2b6cb0", ls="-"))
    ax.text(0.71, 0.43, r"Section $s$", ha="center", fontsize=10, fontweight="bold", color="#2b6cb0")

    # ker(C) -> V (Inclusion i : ker(C) -> V)
    ax.annotate("", xy=(0.30, 0.50), xytext=(0.42, 0.44),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#276749", ls=":"))
    ax.text(0.35, 0.43, r"$\iota : \ker(C) \hookrightarrow V$", ha="center", fontsize=9, fontweight="bold", color="#276749")

    # Bottom Explanatory Banner
    ax.text(
        0.5, 0.12,
        r"Scope Fence A-S1: Leftover $r(C,x) = (0,4)^T$ is an algebraic vector in $\ker(C)$."
        "\nIt is not a decision, not an authorization, and not an origin story.",
        ha="center", va="center", fontsize=9.5, style="italic", color="#2d3748",
        bbox=dict(boxstyle="round,pad=0.4", fc="#edf2f7", ec="#cbd5e0")
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    if out_path is None:
        out_dir = Path(__file__).resolve().parent.parent / "public_export"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "fig1_projection_cokernel.png"
    else:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    return out_path

if __name__ == "__main__":
    generate_projection_cokernel_figure()
