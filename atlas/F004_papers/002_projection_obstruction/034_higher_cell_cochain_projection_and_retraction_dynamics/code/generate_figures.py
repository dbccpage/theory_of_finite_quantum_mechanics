"""Render an analytic GHZ-family defect example, not empirical convergence."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from coda_higher_cell.defect_bounds import (
    evaluate_k_party_trace_defect,
    short_time_k_party_defect_lower_bound,
)


def generate_fig1() -> Path:
    times = np.linspace(0, 1 / 54, 101)
    defects, bounds = [], []
    for t in times:
        psi = np.zeros(8, dtype=complex)
        psi[0], psi[7] = np.cos(t), -1j * np.sin(t)
        defects.append(evaluate_k_party_trace_defect(np.outer(psi, psi.conj()), [2, 2, 2]))
        bounds.append(short_time_k_party_defect_lower_bound(2, 3, 1, float(t))[0])
    fig, ax = plt.subplots(figsize=(7.5, 4.2), constrained_layout=True)
    ax.plot(times, defects, label="Analytic state, numerical trace norm", color="#176b86")
    ax.plot(times, bounds, label="Proved lower bound: 2t - 54t²", color="#ba5a31")
    ax.set(
        xlabel="Time t (g=1)",
        ylabel="Distance to product of marginals",
        title="Three qubits on a degree-2 cell",
    )
    ax.legend()
    ax.grid(alpha=0.25)
    fig.text(
        0.5,
        -0.035,
        "Finite worked example; not a genuine multipartite entanglement test.",
        ha="center",
        fontsize=9,
    )
    out = Path(__file__).resolve().parents[1] / "public_export" / "fig1_overview.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        out, dpi=180, bbox_inches="tight", metadata={"Software": "PO-034 numerical example"}
    )
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(generate_fig1())
