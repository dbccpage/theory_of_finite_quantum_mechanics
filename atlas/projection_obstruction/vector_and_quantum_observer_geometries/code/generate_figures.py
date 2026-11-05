"""
Generates publication figures for vector_and_quantum_observer_geometries.
Paper: GS-003 (vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from cochain_complex import GraphComplex, Cochain
from quantum_geometry import HermitianOperator, QuantumQuotientSolver
from cptp_channels import KrausChannel, CochainMorphism


def generate_figure() -> None:
    """Generate multi-panel publication figure illustrating observer geometry principles."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: 3-Cycle Directed Graph with circulation
    ax1 = axes[0]
    # Triangle coordinates: 0: (0, 0), 1: (1, 0), 2: (0.5, np.sqrt(3)/2)
    coords = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])
    ax1.scatter(coords[:, 0], coords[:, 1], color="#2b5c8f", s=300, zorder=5)
    for i, (x, y) in enumerate(coords):
        ax1.text(x, y + 0.06, f"v_{i}", fontsize=12, fontweight="bold", ha="center")

    # Directed edges
    edge_labels = [
        r"$\omega_{01} = (1, 0)$",
        r"$\omega_{12} = (0, 1)$",
        r"$\omega_{20} = (0, 0)$",
    ]
    edges = [(0, 1), (1, 2), (2, 0)]
    for e_idx, (u, v) in enumerate(edges):
        p_u = coords[u]
        p_v = coords[v]
        dx, dy = p_v - p_u
        ax1.annotate(
            "",
            xy=(p_v[0] - 0.08 * dx, p_v[1] - 0.08 * dy),
            xytext=(p_u[0] + 0.08 * dx, p_u[1] + 0.08 * dy),
            arrowprops=dict(arrowstyle="->", color="#c0392b", lw=2.5),
        )
        mid = 0.5 * (p_u + p_v)
        offset = 0.08 * np.array([-dy, dx]) / np.hypot(dx, dy)
        ax1.text(
            mid[0] + offset[0],
            mid[1] + offset[1],
            edge_labels[e_idx],
            fontsize=9,
            ha="center",
        )

    ax1.text(
        0.5,
        0.28,
        r"$\mathbf{c} = \sum_e \omega_e = (1, 1)$",
        fontsize=11,
        ha="center",
        color="#8e44ad",
        fontweight="bold",
    )
    ax1.set_title(
        r"(a) 3-Cycle Gauge Circulation $\mathbf{c}$", fontsize=12, fontweight="bold"
    )
    ax1.set_xlim(-0.3, 1.3)
    ax1.set_ylim(-0.2, 1.1)
    ax1.set_aspect("equal")
    ax1.axis("off")

    # Panel 2: Unit Balls l^1 vs l^2 and Quotient Extrema
    ax2 = axes[1]
    theta = np.linspace(0, 2 * np.pi, 200)
    # L2 unit ball
    ax2.plot(
        np.cos(theta),
        np.sin(theta),
        color="#27ae60",
        lw=2.5,
        label=r"$\ell^2$ Ball ($r=1$, $\Phi_{2,1} = \sqrt{2}$)",
    )
    # L1 unit ball
    t_l1 = np.linspace(-1, 1, 100)
    ax2.plot(
        np.concatenate([t_l1, t_l1[::-1]]),
        np.concatenate([1 - np.abs(t_l1), -(1 - np.abs(t_l1))]),
        color="#e67e22",
        lw=2.5,
        ls="--",
        label=r"$\ell^1$ Ball ($\Phi_{1,1} = 2$)",
    )
    # Circulation point (1, 1)
    ax2.scatter(
        [1.0],
        [1.0],
        color="#8e44ad",
        s=100,
        zorder=6,
        label=r"Circulation $\mathbf{c} = (1, 1)$",
    )
    ax2.annotate(
        r"$\mathbf{c} = (1, 1)$",
        xy=(1.0, 1.0),
        xytext=(0.55, 1.15),
        arrowprops=dict(arrowstyle="->", color="#8e44ad"),
    )

    ax2.set_title(
        r"(b) Observer Geometry Unit Balls in $\mathbb{R}^2$",
        fontsize=12,
        fontweight="bold",
    )
    ax2.set_xlabel(r"$x_1$")
    ax2.set_ylabel(r"$x_2$")
    ax2.set_xlim(-1.4, 1.4)
    ax2.set_ylim(-1.4, 1.4)
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="lower left", fontsize=8)

    # Panel 3: CPTP Monotonicity Curve under Depolarizing Noise
    ax3 = axes[2]
    p_vals = np.linspace(0.0, 1.0, 11)
    comp = GraphComplex.triangle_complex()
    solver = QuantumQuotientSolver(comp, tol=1e-4)
    a_mat = 0.5 * HermitianOperator.SIGMA_Z
    delta = Cochain(np.array([a_mat, a_mat, a_mat], dtype=complex), degree=1)

    phi_vals = []
    for p in p_vals:
        ch = KrausChannel.depolarizing(d=2, p=float(p))
        morph = CochainMorphism.uniform(comp, ch)
        delta_p = morph.apply_to_cochain(delta)
        cert = solver.solve(delta_p)
        phi_vals.append(cert.primal_value)

    ax3.plot(
        p_vals,
        phi_vals,
        "o-",
        color="#2980b9",
        lw=2,
        markersize=6,
        label=r"Observed $\Phi_Q([\mathcal{E}_p \delta])$",
    )
    ax3.plot(
        p_vals,
        1.5 * (1.0 - p_vals),
        "r--",
        lw=1.5,
        label=r"Theoretical Bound $(1-p)\Phi_Q$",
    )
    ax3.set_title(
        r"(c) CPTP Quotient Monotonicity under Depolarizing Noise",
        fontsize=11,
        fontweight="bold",
    )
    ax3.set_xlabel(r"Depolarizing Parameter $p$")
    ax3.set_ylabel(r"Quotient Obstruction $\Phi_Q$")
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc="upper right", fontsize=9)

    plt.tight_layout()

    export_dir = Path(__file__).resolve().parents[1] / "public_export"
    export_dir.mkdir(parents=True, exist_ok=True)
    out_path = (
        export_dir / "fig1_006_vector_and_quantum_observer_geometries_readout.png"
    )
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated publication figure at {out_path}")


if __name__ == "__main__":
    generate_figure()
