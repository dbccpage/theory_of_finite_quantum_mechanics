"""Generate the paper's two scientific figures from exact example values."""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from coda_core import affine_quadrature, coordinate_packet


def generate(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.hashsalt": "coda-paper-v2",
        }
    )
    blue, orange, green = "#245b78", "#b56032", "#2d775c"
    packets = [coordinate_packet(x) for x in ((2, 0, 0), (2, 3, 0), (2, 3, 5))]
    fig, ax = plt.subplots(figsize=(9.4, 4.4), layout="constrained")
    centers = list(range(3))
    bars1 = ax.bar(
        [x - 0.18 for x in centers],
        [float(p.phi) for p in packets],
        width=0.34,
        color=blue,
        label=r"First quotient $\Phi_1$",
    )
    bars2 = ax.bar(
        [x + 0.18 for x in centers],
        [float(p.gamma) for p in packets],
        width=0.34,
        color=orange,
        label=r"Next quotient $\Gamma_2$",
    )
    ax.bar_label(bars1, padding=4)
    ax.bar_label(bars2, padding=4)
    ax.set_xticks(
        centers,
        [
            "Exact repair\n(2, 0, 0)",
            "Coherent residual\n(2, 3, 0)",
            "Nonclosed defect\n(2, 3, 5)",
        ],
    )
    ax.set_ylim(0, 10)
    ax.set_ylabel("Exact diagnostic value")
    ax.set_title(
        "One declared linear packet, three outcomes", loc="left", weight="bold", pad=15
    )
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", alpha=0.17)
    ax.set_axisbelow(True)
    for ext in ("png", "svg"):
        path = output / f"coda_foc_outcomes.{ext}"
        fig.savefig(
            path,
            dpi=160,
            metadata={"Date": None} if ext == "svg" else {},
        )
        if ext == "svg":
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    plt.close(fig)

    counts = list(range(1, 21))
    values = [affine_quadrature(n) for n in counts]
    fig, (ax, error_ax) = plt.subplots(
        1,
        2,
        figsize=(11.0, 4.3),
        layout="constrained",
        gridspec_kw={"width_ratios": [1.7, 1]},
    )
    ax.plot(
        counts,
        [float(v["left"]) for v in values],
        "o-",
        color=blue,
        markersize=3,
        label="Left sum",
    )
    ax.plot(
        counts,
        [float(v["right"]) for v in values],
        "o-",
        color=orange,
        markersize=3,
        label="Right sum",
    )
    ax.plot(
        counts,
        [50] * len(counts),
        color=green,
        linewidth=2,
        label="Trapezoid = integral = 50",
    )
    ax.set_xlabel("Equal panels N")
    ax.set_ylabel("Area query for f(x) = x on [0, 10]")
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.legend(frameon=False, fontsize=9)
    ax.set_title(
        "Exact sums on an admitted affine model", loc="left", weight="bold", pad=15
    )
    error_ax.plot(
        counts, [float(v["error"]) for v in values], "o-", color=blue, markersize=3
    )
    error_ax.set_title("Left / right absolute error", loc="left", pad=15)
    error_ax.set_xlabel("Equal panels N")
    error_ax.set_ylabel("50 / N")
    error_ax.set_xticks([1, 5, 10, 15, 20])
    for panel in (ax, error_ax):
        panel.grid(alpha=0.17)
        panel.set_axisbelow(True)
    for ext in ("png", "svg"):
        path = output / f"coda_quadrature.{ext}"
        fig.savefig(
            path,
            dpi=160,
            metadata={"Date": None} if ext == "svg" else {},
        )
        if ext == "svg":
            path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    plt.close(fig)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "images",
    )
    generate(parser.parse_args().output_dir)
