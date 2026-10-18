r"""
Claim vs Reality Visualization Engine (GR-002 / PO-012).
Delegates to claim_vs_reality_plots modular functions for clean visualization generation.
"""

import matplotlib.pyplot as plt
from claim_vs_reality_plots import (
    plot_higgs_potential_comparison,
    plot_ewsb_scale_comparison,
    plot_free_parameters_comparison,
    plot_quantum_numbers_comparison
)


def generate_claim_vs_reality_plots():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Standard Model Derivation Claims vs Reality - Diagnostic Results',
                 fontsize=18, fontweight='bold', y=0.98)

    plot_higgs_potential_comparison(axes[0, 0])
    plot_ewsb_scale_comparison(axes[0, 1])
    plot_free_parameters_comparison(axes[1, 0])
    plot_quantum_numbers_comparison(axes[1, 1])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.text(0.5, 0.01,
             'DOCUMENTED ASSESSMENT: Standard Model parameters and scales are manually injected rather than emergent',
             ha='center', fontsize=13, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='red', alpha=0.3, edgecolor='darkred', linewidth=3))

    plt.savefig('claim_vs_reality_comparison.png', dpi=150, bbox_inches='tight')
    print("Claim vs Reality comparison saved to: claim_vs_reality_comparison.png")
    plt.close()


if __name__ == "__main__":
    generate_claim_vs_reality_plots()
