# -*- coding: utf-8 -*-
"""
generate_figures.py: Pedagogy schematic for CODA-FDA (NOT empirical evidence).

Captions and labels explicitly state:
"Schematic of toy authorization refusals under derived guards — not FOC Phi_1 residual geometry and not a physical law."

AuthorityEffect: None
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from coda_fda_core import (
    DescentPacket,
    GuardEvidence,
    evaluate_authorization,
)
from sympy import Rational


def _packet() -> DescentPacket:
    return DescentPacket(
        carrier_k="fig_carrier",
        evaluator_class_e=["e0", "e1"],
        verifier_v="v_fig",
        terminalizer_tau="tau_fig",
        discipline_lambda="L_fig",
    )


def _green(**overrides: Any) -> GuardEvidence:
    base = dict(
        pipeline_accepted=True,
        replay_deterministic=True,
        residual_mass=Rational(0, 1),
        residual_zero_tol=Rational(0, 1),
        skeleton_preserved=True,
        candidates_checked=2,
        candidates_declared=2,
        pending_lifts=0,
        active_refusal=False,
    )
    base.update(overrides)
    if "checked_candidate_ids" not in overrides:
        checked_n = base.get("candidates_checked", 0)
        base["checked_candidate_ids"] = tuple(f"e{i}" for i in range(checked_n))
    return GuardEvidence(**base)


_pkg_root = Path(__file__).resolve().parent.parent

def generate_fig1() -> Path:
    """
    Schematic: authorization residual diagnostic vs successive green steps.

    X-axis steps are cumulative green mutations toward full IsAuth, not a
    physical residual law. Values come from evaluate_authorization.
    """
    packet = _packet()
    ladder_evidence = [
        _green(
            pipeline_accepted=False,
            replay_deterministic=False,
            residual_mass=Rational(1, 1),
            skeleton_preserved=False,
            candidates_checked=0,
            candidates_declared=2,
            pending_lifts=1,
            active_refusal=True,
        ),
        _green(
            pipeline_accepted=True,
            replay_deterministic=False,
            residual_mass=Rational(1, 1),
            skeleton_preserved=False,
            candidates_checked=0,
            candidates_declared=2,
            pending_lifts=1,
            active_refusal=True,
        ),
        _green(
            pipeline_accepted=True,
            replay_deterministic=True,
            residual_mass=Rational(1, 1),
            skeleton_preserved=False,
            candidates_checked=0,
            candidates_declared=2,
            pending_lifts=1,
            active_refusal=True,
        ),
        _green(
            pipeline_accepted=True,
            replay_deterministic=True,
            residual_mass=Rational(0, 1),
            skeleton_preserved=False,
            candidates_checked=0,
            candidates_declared=2,
            pending_lifts=1,
            active_refusal=True,
        ),
        _green(
            pipeline_accepted=True,
            replay_deterministic=True,
            residual_mass=Rational(0, 1),
            skeleton_preserved=True,
            candidates_checked=0,
            candidates_declared=2,
            pending_lifts=1,
            active_refusal=True,
        ),
        _green(
            pipeline_accepted=True,
            replay_deterministic=True,
            residual_mass=Rational(0, 1),
            skeleton_preserved=True,
            candidates_checked=2,
            candidates_declared=2,
            pending_lifts=1,
            active_refusal=True,
        ),
        _green(
            pipeline_accepted=True,
            replay_deterministic=True,
            residual_mass=Rational(0, 1),
            skeleton_preserved=True,
            candidates_checked=2,
            candidates_declared=2,
            pending_lifts=0,
            active_refusal=True,
        ),
        _green(),  # full green
    ]

    xs = list(range(len(ladder_evidence)))
    residuals = []
    inhabited_flags = []
    for i, ev in enumerate(ladder_evidence):
        r = evaluate_authorization(f"step_{i}", packet, ev)
        # Convert exact Rational to float strictly for plotting display
        residuals.append(float(r.residual_mass))
        inhabited_flags.append(1.0 if r.inhabited else 0.0)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(
        xs,
        residuals,
        "o-",
        color="#1f77b4",
        linewidth=2.5,
        markersize=8,
        label="Toy refusal residual (gate diagnostic)",
    )
    ax.plot(
        xs,
        inhabited_flags,
        "s--",
        color="#2ca02c",
        linewidth=2.0,
        markersize=7,
        label="Standing inhabited (0/1)",
    )
    ax.set_title(
        "CODA-FDA toy authorization ladder (schematic, not FOC Phi_1)",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xlabel("Cumulative green-evidence step (pedagogy)", fontsize=11)
    ax.set_ylabel("Toy residual / inhabited flag", fontsize=11)
    ax.set_xticks(xs)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, 0.98), frameon=True)
    fig.text(
        0.5,
        0.025,
        "Schematic only — not empirical residual geometry",
        ha="center",
        fontsize=8,
        color="#444444",
    )

    export_dir = Path(__file__).resolve().parents[1] / "public_export"
    export_dir.mkdir(parents=True, exist_ok=True)
    out_path = export_dir / "fig1_authority_gate_descent.png"
    plt.tight_layout(rect=(0, 0.09, 1, 1))
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated figure: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_fig1()
