#!/usr/bin/env python3
"""Build jupyter_notebooks/00_enter_po000.ipynb — primary Zenodo front door."""
from __future__ import annotations

import json
from pathlib import Path

import uuid

ROOT = Path(__file__).resolve().parents[1]
NB_PATH = ROOT / "jupyter_notebooks" / "00_enter_po000.ipynb"


def md(s: str) -> dict:
    lines = s.strip("\n").split("\n")
    return {
        "cell_type": "markdown",
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "source": [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else []),
    }


def code(s: str) -> dict:
    lines = s.strip("\n").split("\n")
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": uuid.uuid4().hex[:8],
        "metadata": {},
        "outputs": [],
        "source": [ln + "\n" for ln in lines[:-1]] + ([lines[-1] + "\n"] if lines else []),
    }


def main() -> int:
    cells: list[dict] = []

    cells.append(
        md(
            """# PO-000 — Enter the Paper

**Title:** Projection Obstruction for Factorized States  
**Package version:** `v6.3` (pre-print; this revision is not yet deposited)  
**Published predecessors:** v6.0 — version DOI [10.5281/zenodo.21752743](https://doi.org/10.5281/zenodo.21752743) under concept [10.5281/zenodo.18896776](https://doi.org/10.5281/zenodo.18896776); v5.6 — [10.5281/zenodo.20650922](https://doi.org/10.5281/zenodo.20650922)  
**AuthorityEffect:** `None`

This is the **primary** interactive front door for the paper.

Use it to:
1. See a short cartoon of **projection**, **retraction**, and **obstruction**
2. Run finite demos tied to named claim faces
3. Try to **break** hypotheses in the falsification room
4. Navigate ledger / Lean honesty in plain words

The monograph and claim ledger remain the paper's authoritative claim statements. Finite / instance / numerical checks here do **not** prove universal theorems. See the **Scope fences and nonclaims** section of the root `README.md`."""
        )
    )

    cells.append(
        md(
            """## 0. Setup (production library only)

Import from `code/` (bare imports; 2026-08-31 fix, the src/po000 layout never shipped). No reimplemented formulas in later cells."""
        )
    )

    cells.append(
        code(
            """import sys
from pathlib import Path

ROOT = Path("..").resolve()
sys.path.insert(0, str(ROOT / "code"))

import numpy as np

from inline_code_companion import (
    run_example_61_bell_state_leakage,
    run_example_62_tfim_normal_rate,
)
from falsification_sandbox import (
    TOL,
    bell_closed_form,
    short_time_lower_bound,
    control_signed_bell_both_signs,
    run_all_breaks,
)
from cochain_presentation import LinearRepairProblem
from retraction_geometry import GraphRetraction  # exact rail (floats rejected)

print(f"Imports OK. TOL={TOL}")
print(f"Package root: {ROOT}")
print(f"Production: {ROOT / 'code'}")"""
        )
    )

    cells.append(
        md(
            r"""## 1. Three-second thesis

Product-state **projection** compresses a full state toward factorized data.  
The product-of-marginals map is a **retraction** $\Pi_e$.  
What is left is a **normal residual** / obstruction face — e.g. raw two-site defect $D_e(t)$ — which is **not** interchangeable with a cochain tally or quotient $\Phi$ without declared maps.

For finite one- and two-local Hamiltonians the raw two-site defect obeys

$$D_e(t)\ge \nu_e t-24g^2 t^2$$

on a short-time window — finite carriers, finite time, no authority grant."""
        )
    )

    cells.append(
        md(
            r"""## 2. Cartoon — projection, retraction, residual

**What to see**

| Idea | Everyday picture | Paper face |
| --- | --- | --- |
| **Projection** | Looking at a 3D object from one angle; depth is lost | Compress full state toward product / chart data |
| **Retraction** | Snap every point back onto a chosen surface (product manifold) | $\Pi$ or graph retraction onto product / manifold $M$ |
| **Obstruction / residual** | After snapping, the gap that dynamics re-opens | $n_e$, $D_e(t)$, cochain vs $\Phi$ (distinct types) |

**Why a human might care (non-claiming):** mean-field, Hartree–Fock, product ansatz, and "ignore correlations" all do this compression. The paper isolates a **finite structural cost** of that move — not a verdict on "truth of QM", not governance, not entanglement from residual alone.

**Lean honesty:** Lean certifies algebraic RE hierarchy (D2/D5) and abstract defect transfer (E8). The short-time quantum bound is **paper-proved** with Python finite replays — modules `l002`/`l003` are **LEAN_TOY** residuals, not Thm 5.1."""
        )
    )

    cells.append(
        code(
            """# Cartoon widget: graph retraction Pi(x,y,z)=(x,y,x^2) + residual size
# Float cartoon of the exact GraphRetraction in code/retraction_geometry.py

try:
    import ipywidgets as widgets
    from IPython.display import display
    import matplotlib.pyplot as plt
    HAS_W = True
except Exception:
    HAS_W = False

def residual_of_point(x, y, z):
    \"\"\"Ambient point vs its retract; L1 residual in ambient coords.

    Float cartoon mirroring the exact Pi(x, y, z) = (x, y, x**2): the exact
    rail rejects binary floats by design, so this widget computes the same
    retraction directly in floats (2026-08-31 fix).
    \"\"\"
    rx, ry, rz = float(x), float(y), float(x) ** 2
    d = (float(x) - rx, float(y) - ry, float(z) - rz)
    return abs(d[0]) + abs(d[1]) + abs(d[2]), [rx, ry, rz]


def cartoon_panel(x=0.5, y=0.0, z=1.0):
    res, rp = residual_of_point(float(x), float(y), float(z))
    on_m = abs(float(z) - float(x) ** 2) < 1e-12
    print(f"ambient point  p = ({x:.3f}, {y:.3f}, {z:.3f})")
    print(f"retract Pi(p)  = ({rp[0]:.3f}, {rp[1]:.3f}, {rp[2]:.3f})  # on graph z=x^2")
    print(f"L1 residual    = {res:.6e}   on_manifold={on_m}")
    print(
        "Interpretation: projection/retraction snaps to product/manifold data; "
        "residual is the obstruction face."
    )
    if HAS_W:
        fig, ax = plt.subplots(figsize=(5, 3.2))
        xs = np.linspace(-1.2, 1.2, 80)
        ax.plot(xs, xs**2, "k-", lw=2, label="manifold M: z=x^2")
        ax.scatter([x], [z], c="C0", s=80, zorder=3, label="ambient p (y ignored in 2d slice)")
        ax.scatter([rp[0]], [rp[2]], c="C3", s=80, zorder=3, label="Pi(p)")
        ax.plot([x, rp[0]], [z, rp[2]], "C1--", lw=1.5, label="residual segment")
        ax.set_xlabel("x")
        ax.set_ylabel("z")
        ax.legend(fontsize=8)
        ax.set_title("Retraction cartoon (production GraphRetraction)")
        ax.grid(True, alpha=0.3)
        plt.show()
    return res


if HAS_W:
    widgets.interact(
        cartoon_panel,
        x=widgets.FloatSlider(value=0.5, min=-1.0, max=1.0, step=0.05, description="x"),
        y=widgets.FloatSlider(value=0.0, min=-1.0, max=1.0, step=0.05, description="y"),
        z=widgets.FloatSlider(value=1.0, min=-0.2, max=1.5, step=0.05, description="z"),
    )
else:
    cartoon_panel()
    print("(ipywidgets unavailable — static cartoon values only)")"""
        )
    )

    cells.append(
        md(
            r"""## [F1] Example 6.1 — Bell product-retraction defect

**Ledger:** PROVEN COMPUTATION · §6.1 · instance only  
**Expected:** $1/\sqrt{2}+1/4$ at $\theta=\pm\pi/8$ (both signs of $J$)

Use the slider to explore $\theta$; production closed form + eigenvalue sum must stay within $10^{-12}$ of each other."""
        )
    )

    cells.append(
        code(
            """EXPECTED_F1 = 1.0 / np.sqrt(2.0) + 0.25


def f1_panel(theta):
    num, formula = run_example_61_bell_state_leakage(theta=float(theta))
    closed = bell_closed_form(float(theta))
    r_nf = abs(num - formula)
    r_fc = abs(formula - closed)
    ok = r_nf <= TOL and r_fc <= TOL
    print(f"theta={theta:.6f}")
    print(f"numerical eig-sum = {num:.16f}")
    print(f"signed formula    = {formula:.16f}")
    print(f"closed helper     = {closed:.16f}")
    print(f"|num-formula|={r_nf:.3e}  |formula-closed|={r_fc:.3e}  ok={ok}")
    if abs(abs(theta) - np.pi / 8) < 1e-9:
        print(
            f"at ±pi/8: |value - expected| = {abs(num - EXPECTED_F1):.3e} "
            f"(expected {EXPECTED_F1:.16f})"
        )
    return ok


if HAS_W:
    w = widgets.FloatSlider(
        value=float(np.pi / 8),
        min=-float(np.pi / 2),
        max=float(np.pi / 2),
        step=0.01,
        description="theta",
    )
    widgets.interact(f1_panel, theta=w)
else:
    print("ipywidgets unavailable — static ±pi/8 control")
    pos, neg = control_signed_bell_both_signs()
    print(
        "CONTROL",
        pos,
        neg,
        "match",
        abs(pos - EXPECTED_F1) <= TOL and abs(neg - EXPECTED_F1) <= TOL,
    )"""
        )
    )

    cells.append(
        md(
            r"""## [E4] Theorem 5.1 face — short-time lower bound RHS

**Ledger:** PROVEN, CONDITIONAL (prose theorem) · Python = **numerical/instance face only**  
**Form:** $D_e(t)\ge \nu_e t - 24 g^2 t^2$ on a short-time window

This cell plots the **signed RHS** from production `short_time_lower_bound` — it does **not** Lean-prove the theorem."""
        )
    )

    cells.append(
        code(
            """def e4_panel(nu_e=2.0, g=1.0, t=0.05):
    rhs = short_time_lower_bound(float(nu_e), float(g), float(t))
    window_ok = float(t) <= float(nu_e) / (48.0 * float(g) * float(g) + 1e-30)
    print(f"nu_e={nu_e}, g={g}, t={t}")
    print(f"RHS short_time_lower_bound = {rhs:.16f}")
    print(f"inside crude window t <= nu/(48 g^2)? {window_ok}")
    print("Residual-honest: positive RHS is a bound face, not a universal proof.")
    if HAS_W:
        ts = np.linspace(0.001, 0.4, 200)
        rhss = [short_time_lower_bound(float(nu_e), float(g), float(tt)) for tt in ts]
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(ts, rhss, label="RHS nu t - 24 g^2 t^2")
        ax.axhline(0, color="k", lw=0.8)
        ax.axvline(t, color="C3", ls="--", label=f"current t={t}")
        ax.set_xlabel("t")
        ax.set_ylabel("RHS")
        ax.legend(fontsize=8)
        ax.set_title("E4 bound face (not a Lean quantum theorem)")
        ax.grid(True, alpha=0.3)
        plt.show()
    return rhs


if HAS_W:
    widgets.interact(
        e4_panel,
        nu_e=widgets.FloatSlider(value=2.0, min=0.1, max=5.0, step=0.1, description="nu_e"),
        g=widgets.FloatSlider(value=1.0, min=0.1, max=3.0, step=0.1, description="g"),
        t=widgets.FloatSlider(value=0.05, min=0.001, max=0.5, step=0.001, description="t", readout_format=".3f"),
    )
else:
    e4_panel()"""
        )
    )

    cells.append(
        md(
            r"""## [D8] Type distinction — raw tally vs repair/quotient face

**Ledger:** PROVEN TYPE DISTINCTION / FINITE CERTIFICATE · §4.3.1 / §7.2  
**Production:** `cochain_presentation.LinearRepairProblem`

A positive raw edge tally is **not** interchangeable with quotient obstruction $\Phi$."""
        )
    )

    cells.append(
        code(
            """print("LinearRepairProblem:", LinearRepairProblem)
print("D8 face: use cochain_presentation for I vs Phi certificates in unit tests.")
print("Open falsify room for FS breaks that trip when raw is confused with watched/quotient.")"""
        )
    )

    cells.append(
        md(
            """## Hub — where next?

| Path | Role |
| --- | --- |
| **Primary (this notebook)** | Enter + cartoon + F1/E4/D8 faces |
| `reviewer_projection_obstruction.ipynb` | Claim walkthrough |
| `projection_obstruction.md` | The monograph itself (deposit root) |
| `projection_obstruction_claim_ledger.md` | Claim types & residuals |
| `README.md` — **Scope fences and nonclaims** | Evidence ceilings |
| `lean4/README.md` | MECHANIZED vs LEAN_TOY map |

**Lean public sentence:** algebraic RE hierarchy + abstract transfer are Lean cores; short-time quantum bound is not a Lean quantum theorem."""
        )
    )

    cells.append(
        md(
            r"""## Optional: run all falsification breaks (production)

Residual for each deliberate break must exceed $10^{-12}$."""
        )
    )

    cells.append(
        code(
            """results = run_all_breaks()
for r in results:
    print(f"{r.name}: residual={r.residual:.3e} tripped={r.tripped} expected_fail={r.expected_failure}")
assert all(r.tripped for r in results if r.expected_failure), "expected breaks must trip"
print("All expected breaks tripped — falsify protocol OK")"""
        )
    )

    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }
    NB_PATH.write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",  # LF regardless of platform, matching the shipped tree
    )
    print(f"wrote {NB_PATH} cells={len(cells)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
