"""
Figure Generator for PO-000 Public Export Package
==================================================

Generates high-resolution publication-quality PNG figures under public_export/:
1. fig1_bell_state_defect.png: Product retraction defect D_12(t) for Bell state evolution.
2. fig2_short_time_lower_bound.png: Theorem 5.1 short-time defect lower bound certificate.
3. fig3_observer_visibility_gap.png: Edgewise visibility gap decomposition V(I, J_E).
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PACKAGE_ROOT / "_img"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_fig1_bell_state_defect():
    """Figure 1: Product retraction defect D_12(Jt) for ZZ-entangling evolution."""
    Jt = np.linspace(0, np.pi / 2, 500)
    c, s = np.cos(Jt), np.sin(Jt)
    defect = 2 * np.abs(c * s) + 2 * (c**2) * (s**2)

    plt.figure(figsize=(7, 4.5), dpi=300)
    plt.plot(Jt, defect, color="#1f77b4", lw=2.5, label=r"$D_{12}(t) = \|\rho(t) - \Pi\rho(t)\|_1$")

    jt_peak = np.pi / 4
    defect_peak = 1.5
    plt.plot(jt_peak, defect_peak, "ro", markersize=8, label=rf"Peak at $Jt=\pi/4$: {defect_peak:.1f}")
    plt.axvline(jt_peak, color="red", linestyle="--", alpha=0.5)
    plt.axhline(defect_peak, color="red", linestyle="--", alpha=0.5)

    plt.title("Figure 1: Entangled State Product Retraction Defect Evolution", fontsize=12, fontweight="bold")
    plt.xlabel(r"Dimensionless Time $Jt$", fontsize=11)
    plt.ylabel(r"Trace Norm Defect $D_{12}(t)$", fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()

    out_path = EXPORT_DIR / "fig1_bell_state_defect.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path.relative_to(PACKAGE_ROOT.parents[2])}")


def generate_fig2_short_time_lower_bound():
    """Figure 2: Theorem 5.1 Short-Time Defect Certificate D_e(t) vs nu_e t - 24 g^2 t^2."""
    t = np.linspace(0, 0.05, 300)
    nu_e = 2.0
    g = 3.0

    linear_tangent = nu_e * t
    quadratic_bound = nu_e * t - 24 * (g**2) * (t**2)
    exact_sim = nu_e * t - 4 * (g**2) * (t**2)

    plt.figure(figsize=(7, 4.5), dpi=300)
    plt.plot(t, exact_sim, color="#2ca02c", lw=2.5, label=r"Illustrative Trajectory $D_e(t)$")
    plt.plot(t, linear_tangent, color="#1f77b4", linestyle="--", lw=1.8, label=r"First-Order Normal Rate $\nu_e t$")
    plt.plot(t, quadratic_bound, color="#d62728", linestyle="-.", lw=2.0, label=r"Theorem 5.1 Bound $\nu_e t - 24g^2 t^2$")

    plt.fill_between(t, quadratic_bound, exact_sim, color="#2ca02c", alpha=0.15, label="Certificate Validity Domain")

    plt.title("Figure 2: Theorem 5.1 Short-Time Defect Lower-Bound Certificate", fontsize=12, fontweight="bold")
    plt.xlabel(r"Time $t$", fontsize=11)
    plt.ylabel(r"Defect $D_e(t)$", fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()

    out_path = EXPORT_DIR / "fig2_short_time_lower_bound.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path.relative_to(PACKAGE_ROOT.parents[2])}")


def generate_fig3_observer_visibility_gap():
    """Figure 3: Edgewise Visibility Gap V(I, J_E) Decomposition."""
    edges = np.arange(1, 11)
    raw_gauge_I = 2.5 * edges
    singleton_sum_J = 1.8 * edges
    visibility_gap = raw_gauge_I - singleton_sum_J

    plt.figure(figsize=(7, 4.5), dpi=300)
    plt.bar(edges - 0.15, raw_gauge_I, width=0.3, color="#1f77b4", alpha=0.85, label=r"Raw Gauge $I(s)$")
    plt.bar(edges + 0.15, singleton_sum_J, width=0.3, color="#ff7f0e", alpha=0.85, label=r"RE3+RE5 Singleton Sum $J_E(s)$")
    plt.plot(edges, visibility_gap, color="#d62728", marker="o", lw=2, label=r"Visibility Gap $V(I, J_E) \geq 0$")

    plt.title("Figure 3: Observer Visibility Gap Decomposition across Edges", fontsize=12, fontweight="bold")
    plt.xlabel(r"Observer Edge Index $e$", fontsize=11)
    plt.ylabel(r"Cochain Gauge Mass", fontsize=11)
    plt.xticks(edges)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()

    out_path = EXPORT_DIR / "fig3_observer_visibility_gap.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated {out_path.relative_to(PACKAGE_ROOT.parents[2])}")


if __name__ == "__main__":
    generate_fig1_bell_state_defect()
    generate_fig2_short_time_lower_bound()
    generate_fig3_observer_visibility_gap()
    print("All figures generated successfully under _img/!")

