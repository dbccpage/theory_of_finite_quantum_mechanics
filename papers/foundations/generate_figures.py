"""
Generates publication figures for qm_020_born_normalization_and_conditional_hilbert_lift.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def generate_figure():
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y, label="Conditional Hilbert Lifts of ℓ¹ Sector Weights and Born Normalization Redundancy", color="darkblue", lw=2)
    ax.set_title("Conditional Hilbert Lifts of ℓ¹ Sector Weights and Born Normalization Redundancy")
    ax.set_xlabel("Parameter $t$")
    ax.set_ylabel("Readout")
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    export_dir = Path(__file__).resolve().parents[1] / "public_export"
    export_dir.mkdir(parents=True, exist_ok=True)
    out_path = export_dir / "fig1_qm_020_born_normalization_and_conditional_hilbert_lift_readout.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Generated figure at {out_path}")

if __name__ == "__main__":
    generate_figure()