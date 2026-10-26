# -*- coding: utf-8 -*-
"""
generate_figures.py: Pedagogy schematic for CODA-FOC (NOT empirical evidence).

Figure 1 illustrates three separate finite obstruction packets matching the prose:
- ExactRepair: M1 = span(e1), x = (1, 0), repair d0 f = (-1, 0), residual r = 0, Phi1 = 0.
- CoherentResidual: M1 = span(e1), x = (0, 1), d1 = 0, Phi1 = 1, Gamma2 = 0.
- NonclosedDefect: M1 = span(e1), x = (0, 1), d1(a, b) = b, M2 = {0}, Phi1 = 1, Gamma2 = 1.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

_fig_dir = Path(__file__).resolve().parent
_pkg_root = _fig_dir.parent

if str(_fig_dir) not in sys.path:
    sys.path.insert(0, str(_fig_dir))

FIGURE_COORDINATES: dict[str, dict[str, Any]] = {
    "ExactRepair": {
        "x": (1, 0),
        "d0_f": (-1, 0),
        "r": (0, 0),
        "phi1": 0,
        "gamma2": 0,
    },
    "CoherentResidual": {
        "x": (0, 1),
        "d0_f": (0, 0),
        "r": (0, 1),
        "phi1": 1,
        "gamma2": 0,
    },
    "NonclosedDefect": {
        "x": (0, 1),
        "d0_f": (0, 0),
        "r": (0, 1),
        "d1_r": 1,
        "phi1": 1,
        "gamma2": 1,
    },
}


def generate_figure_1(out_path: Path | None = None) -> tuple[Path, dict[str, dict[str, Any]]]:
    """Generate 3-panel pedagogical schematic for CODA-FOC and return coordinates."""
    if out_path is None:
        out_path = _pkg_root / "public_export" / "fig1_authority_descent.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.4), dpi=150)

    # Common styling helper
    for ax in (ax1, ax2, ax3):
        ax.axhline(0, color="gray", linestyle="--", alpha=0.5, lw=1)
        ax.axvline(0, color="gray", linestyle="--", alpha=0.5, lw=1)
        ax.set_xlim(-1.5, 1.8)
        ax.set_ylim(-1.5, 1.8)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle=":", alpha=0.4)
        ax.set_xlabel("Axis 1 (Repair Subspace $M_1$)", fontsize=9)
        ax.set_ylabel("Axis 2", fontsize=9)

    # Panel 1: ExactRepair
    # M1 = span(e1), x = (1, 0), d0 f = (-1, 0), r = (0, 0)
    ax1.plot([-1.4, 1.6], [0, 0], color="tab:blue", lw=3.5, alpha=0.35, label=r"$M_1 = \operatorname{span}(e_1)$")
    ax1.annotate("", xy=(1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="purple", lw=2.2))
    ax1.plot([1], [0], "mo", markersize=6, label=r"Defect $x = (1, 0)$")
    ax1.annotate("", xy=(0, 0), xytext=(1, 0), arrowprops=dict(arrowstyle="->", color="tab:blue", lw=2.0, ls="--"))
    ax1.plot([0], [0], "go", markersize=8, label=r"Residual $r = 0$ ($\Phi_1=0$)")
    ax1.set_title("Panel A: ExactRepair\n" r"$x=(1,0), d_0 f=(-1,0), r=0 \Rightarrow \Phi_1=0$", fontsize=9.5)
    ax1.legend(loc="upper left", fontsize=8)

    # Panel 2: CoherentResidual
    # M1 = span(e1), x = (0, 1), best d0 f = (0, 0), r = (0, 1), d1 = 0
    ax2.plot([-1.4, 1.6], [0, 0], color="tab:blue", lw=3.5, alpha=0.35, label=r"$M_1 = \operatorname{span}(e_1)$")
    ax2.annotate("", xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="purple", lw=2.2))
    ax2.plot([0], [1], "mo", markersize=6, label=r"Defect $x = (0, 1)$")
    ax2.annotate("", xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="red", lw=1.8, ls=":"))
    ax2.plot([0], [1], "ro", markersize=5, label=r"Residual $r = (0, 1)$ ($\Phi_1=1$)")
    ax2.set_title("Panel B: CoherentResidual\n" r"$x=(0,1), d_1=0 \Rightarrow \Phi_1=1, \Gamma_2=0$", fontsize=9.5)
    ax2.legend(loc="upper left", fontsize=8)

    # Panel 3: NonclosedDefect
    # M1 = span(e1), x = (0, 1), r = (0, 1), d1(a,b) = b, M2 = {0}
    ax3.plot([-1.4, 1.6], [0, 0], color="tab:blue", lw=3.5, alpha=0.35, label=r"$M_1 = \operatorname{span}(e_1)$")
    ax3.annotate("", xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="purple", lw=2.2))
    ax3.plot([0], [1], "mo", markersize=6, label=r"Defect $x = (0, 1)$")
    ax3.plot([0], [1], "ro", markersize=5, label=r"Residual $r = (0, 1)$")
    ax3.text(0.1, 1.05, r"$d_1 r = 1 \notin M_2=\{0\}$" "\n" r"$\Phi_1=1, \Gamma_2=1$", color="darkred", fontsize=8.5,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="mistyrose", edgecolor="red", alpha=0.7))
    ax3.set_title("Panel C: NonclosedDefect\n" r"$x=(0,1), d_1(a,b)=b \Rightarrow \Phi_1=1, \Gamma_2=1$", fontsize=9.5)
    ax3.legend(loc="upper left", fontsize=8)

    fig.suptitle("Three separate finite obstruction packets illustrating ExactRepair, CoherentResidual, and NonclosedDefect\n(Pedagogical schematics, not empirical evidence)", fontsize=11, y=1.02)
    plt.tight_layout()
    fig.savefig(str(out_path), dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path, FIGURE_COORDINATES


if __name__ == "__main__":
    p, coords = generate_figure_1()
    print(f"Generated figure at: {p}")

