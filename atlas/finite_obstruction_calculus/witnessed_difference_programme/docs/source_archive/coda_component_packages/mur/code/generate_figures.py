# -*- coding: utf-8 -*-
"""
generate_figures.py: Pedagogy schematic for CODA-MUR (NOT empirical evidence).

Plots the 5-stage representation transport ladder and target terminalization firewall.
Caption requirement: "Schematic of representation transport ladder — not empirical evidence and not a physical law."

"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from coda_mur_core import (
    DescentSquareCertificate,
    LossLedger,
    MorphismKind,
    TerminalRegime,
    evaluate_transport_authority,
)
from sympy import Rational


def _figure_certificate(**kwargs):
    return DescentSquareCertificate(**kwargs, carrier=("art_01",),
        state_map=lambda x: "obj_x", observation_map=lambda x: 0,
        source_look=lambda x: 0, target_look=lambda x: 0)


def generate_fig1() -> Path:
    """
    Generate pedagogical figure illustrating the representation transport gate ladder.
    """
    # 1. Target regime with configurable terminalizer and auth
    regime_ok = TerminalRegime(
        regime_id="regime_B",
        terminalize=lambda x: f"term_{x}",
        is_auth=lambda t: True,
    )
    regime_no_term = TerminalRegime(
        regime_id="regime_B_noterm",
        terminalize=lambda x: None,
        is_auth=lambda t: True,
    )
    regime_unauth = TerminalRegime(
        regime_id="regime_B_unauth",
        terminalize=lambda x: f"term_{x}",
        is_auth=lambda t: False,
    )

    steps = [
        # Step 0: No certificate
        ("No cert", regime_ok, None),
        # Step 1: Lossy quotient without loss ledger
        (
            "Lossy no ledger",
            regime_ok,
            _figure_certificate(
                source_regime="A",
                target_regime="regime_B",
                morphism_name="F_quot",
                morphism_kind=MorphismKind.QUOTIENT,
                chi_certified=True,
                commutes=True,
                loss_ledger=None,
            ),
        ),
        # Step 2: Lossy with ledger, but target terminal absent (GTMUR-L02)
        (
            "No terminal",
            regime_no_term,
            _figure_certificate(
                source_regime="A",
                target_regime="regime_B_noterm",
                morphism_name="F_quot",
                morphism_kind=MorphismKind.QUOTIENT,
                chi_certified=True,
                commutes=True,
                loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 10)),
            ),
        ),
        # Step 3: Target terminalized but target unauthenticated
        (
            "Target unauth",
            regime_unauth,
            _figure_certificate(
                source_regime="A",
                target_regime="regime_B_unauth",
                morphism_name="F_quot",
                morphism_kind=MorphismKind.QUOTIENT,
                chi_certified=True,
                commutes=True,
                loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 10)),
            ),
        ),
        # Step 4: Fully certified, loss-ledgered, target terminalized and authenticated
        (
            "Certified auth",
            regime_ok,
            _figure_certificate(
                source_regime="A",
                target_regime="regime_B",
                morphism_name="F_quot",
                morphism_kind=MorphismKind.QUOTIENT,
                chi_certified=True,
                commutes=True,
                loss_ledger=LossLedger(e=True, loss_mass=Rational(1, 10)),
            ),
        ),
    ]

    xs = list(range(len(steps)))
    residuals = []
    inhabited = []

    for label, reg, cert in steps:
        res = evaluate_transport_authority("art_01", reg, "obj_x", cert)
        residuals.append(float(res.residual_mass))
        inhabited.append(1.0 if res.inhabited else 0.0)

    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
    width = 0.35
    x_indices = [x - width / 2 for x in xs]
    x_inhabited = [x + width / 2 for x in xs]

    # Discrete labeled bars for policy diagnostic constants (not continuous line)
    bars = ax.bar(
        x_indices,
        residuals,
        width,
        color="#d62728",
        alpha=0.75,
        edgecolor="#8b0000",
        linewidth=1.2,
        label="Policy diagnostic code (exact rational)",
    )
    # Binary authority inhabitation markers
    ax.scatter(
        x_inhabited,
        inhabited,
        color="#2ca02c",
        s=90,
        marker="s",
        edgecolor="#006400",
        linewidth=1.5,
        zorder=5,
        label="Target authority inhabited (0/1)",
    )

    # Annotate discrete diagnostic rational values above bars
    rational_labels = ["1", "3/4", "1/2", "1/4", "0"]
    for bar, r_lbl in zip(bars, rational_labels):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.03,
            r_lbl,
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#8b0000",
        )

    ax.set_title(
        "CODA-MUR Representation Transport Ladder (Schematic)",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_xlabel("Transport gate step", fontsize=11)
    ax.set_ylabel("Policy diagnostic code / Inhabitation flag", fontsize=11)
    ax.set_xticks(xs)
    ax.set_xticklabels([s[0] for s in steps], rotation=15)
    ax.set_ylim(0, 1.2)
    ax.grid(True, linestyle=":", alpha=0.6, axis="y")
    ax.legend(loc="upper center", bbox_to_anchor=(0.52, 1.0), frameon=True)
    ax.text(
        0.02,
        -0.25,
        "Schematic only — discrete policy diagnostic codes, not empirical convergence",
        transform=ax.transAxes,
        fontsize=8,
        color="#444444",
    )

    export_dir = Path(__file__).resolve().parents[1] / "public_export"
    export_dir.mkdir(parents=True, exist_ok=True)
    out_path = export_dir / "fig1_authority_descent.png"
    plt.tight_layout(rect=(0, 0.06, 1, 1))
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Generated figure: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_fig1()
