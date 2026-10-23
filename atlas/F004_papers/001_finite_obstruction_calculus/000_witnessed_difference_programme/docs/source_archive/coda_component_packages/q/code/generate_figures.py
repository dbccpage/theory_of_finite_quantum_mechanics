# -*- coding: utf-8 -*-
"""Pedagogy schematic for CODA-Q (not empirical evidence)."""

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from coda_q_core import (
    enclosure_endpoint_sequence,
    nested_sqrt2_enclosures,
    two_signal_sample_collision,
)
from continuum import sqrt2_enclosure


def generate_fig1(out_path: Path | None = None) -> Path:
    """Nested √2 enclosures and a two-signal sample collision."""
    encs = nested_sqrt2_enclosures(6)
    collision = two_signal_sample_collision()
    lowers = enclosure_endpoint_sequence(6, "lower")
    uppers = enclosure_endpoint_sequence(6, "upper")
    mids = enclosure_endpoint_sequence(6, "midpoint")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for k, enc in enumerate(encs):
        ax1.hlines(
            k,
            float(enc.lower),
            float(enc.upper),
            colors="#1f77b4",
            linewidth=6 - 0.5 * k,
            alpha=0.85,
        )
        ax1.plot(float(enc.midpoint), k, "o", color="#d62728", markersize=5)
    ax1.set_yticks(range(len(encs)))
    ax1.set_yticklabels([f"n={k}" for k in range(len(encs))])
    ax1.set_xlabel("rational endpoints")
    ax1.set_title("Nested enclosures of √2\n(midpoint marked, not identified)")
    ax1.invert_yaxis()
    ax1.grid(True, axis="x", linestyle=":", alpha=0.6)

    nodes = [0.0, 0.5, 1.0]
    f_vals = [0.0, float(collision["query_f"]), 0.0]
    g_vals = [0.0, float(collision["query_g"]), 0.0]
    ax2.plot(nodes, f_vals, "o-", color="#2ca02c", label="f(t)=0")
    ax2.plot(nodes, g_vals, "s--", color="#ff7f0e", label="g(t)=t(t-1)")
    ax2.axvline(0.0, color="#7f7f7f", linestyle=":", alpha=0.5)
    ax2.axvline(1.0, color="#7f7f7f", linestyle=":", alpha=0.5)
    ax2.set_xlabel("t")
    ax2.set_ylabel("sample")
    ax2.set_title(
        f"Same samples on {{0,1}}, different value at 1/2\n(collision={collision['collides']})"
    )
    ax2.legend(loc="best")
    ax2.grid(True, linestyle=":", alpha=0.6)

    fig.suptitle(
        "CODA-Q: finite completion and enclosure — schematic, not a physical law.",
        fontsize=11,
    )
    plt.tight_layout()

    if out_path is None:
        out_path = Path(__file__).resolve().parent / "fig1_authority_descent.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    # Touch the endpoint sequences so the figure is driven by the companion.
    assert lowers.terms[0] == sqrt2_enclosure(0).lower
    assert uppers.terms[0] == sqrt2_enclosure(0).upper
    assert mids.terms[0] == sqrt2_enclosure(0).midpoint
    return out_path


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    generate_fig1(parser.parse_args().output)
