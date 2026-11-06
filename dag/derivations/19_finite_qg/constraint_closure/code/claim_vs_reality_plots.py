r"""
Claim vs Reality Visual Diagnostic Component Module (GR-002 / PO-012).
Modular plotting functions for Higgs, EWSB, parameters, quantum numbers, and scorecards.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_higgs_potential_comparison(ax):
    """Plots Higgs potential energy landscape fit comparison."""
    ax.set_title('Test 1: Higgs Potential Energy Landscape', fontsize=14, fontweight='bold')
    categories = ['Linear\nFit', 'Quadratic\nFit', 'Quartic\nFit\n(Mexican Hat)']
    claimed = [0.0, 0.0, 1.0]
    reality = [1.0, 1.0, 0.9856]

    x = np.arange(len(categories))
    width = 0.35

    ax.bar(x - width/2, claimed, width, label='Claimed', color='lightgreen', alpha=0.7, edgecolor='green', linewidth=2)
    bars2 = ax.bar(x + width/2, reality, width, label='Measured R²', color='lightcoral', alpha=0.7, edgecolor='red', linewidth=2)

    ax.set_ylabel('R² Score (1.0 = perfect fit)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim([0, 1.1])
    ax.axhline(1.0, color='black', linestyle='--', alpha=0.3, linewidth=1)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)

    for bar, val in zip(bars2, reality):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.text(0.5, 0.05, 'VERDICT: Energy along fixed ray is LINEAR (R²=1.0), not quartic\nQuartic double-well requires manual polynomial injection',
            transform=ax.transAxes, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))


def plot_ewsb_scale_comparison(ax):
    """Plots EWSB energy scale comparison."""
    ax.set_title('Test 2: Electroweak Symmetry Breaking Scale', fontsize=14, fontweight='bold')
    scales = ['Claimed VEV\n(Target)', 'Lattice Unit\n(Dimensionless)', 'Hardcoded\n(In Code)']
    values = [246.0, 1.0, 246.0]
    colors = ['lightgreen', 'lightcoral', 'yellow']
    edge_colors = ['green', 'red', 'orange']

    bars = ax.bar(scales, values, color=colors, alpha=0.7, edgecolor=edge_colors, linewidth=2)
    ax.set_ylabel('Scale (arbitrary unit / GeV)', fontsize=12)
    ax.set_yscale('log')
    ax.set_ylim([0.5, 500])
    ax.axhline(246.0, color='red', linestyle='--', alpha=0.5, linewidth=2, label='SM VEV (246 GeV)')
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, which='both')

    labels = ['246.0 GeV', '1.0 (arbitrary)', '246.0 GeV']
    for bar, lbl in zip(bars, labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height * 1.15,
                lbl, ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.text(0.5, 0.05, 'VERDICT: Physical scale not determined by dimensionless lattice\n246 GeV threshold manually injected',
            transform=ax.transAxes, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))


def plot_free_parameters_comparison(ax):
    """Plots free parameter count comparison."""
    ax.set_title('Test 3: Free Parameter Count', fontsize=14, fontweight='bold')
    param_categories = ['Claimed', 'Yukawa\nSector', 'Total\nMeasured', 'Standard\nModel']
    param_counts = [0, 9, 12, 19]
    colors = ['lightgreen', 'lightcoral', 'lightcoral', 'lightblue']
    edge_colors = ['green', 'red', 'red', 'blue']

    bars = ax.bar(param_categories, param_counts, color=colors, alpha=0.7, edgecolor=edge_colors, linewidth=2)
    ax.set_ylabel('Number of Free Parameters', fontsize=12)
    ax.set_ylim([0, 22])
    ax.grid(axis='y', alpha=0.3)

    for bar, val in zip(bars, param_counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{val}', ha='center', va='bottom', fontsize=14, fontweight='bold')

    ax.text(0.5, 0.05, 'VERDICT: 12+ free parameters (9 Yukawa + 3 other)\nClaim of "zero free parameters" is false',
            transform=ax.transAxes, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))


def plot_quantum_numbers_comparison(ax):
    """Plots fermion quantum numbers emergence vs hardcoded reality comparison."""
    ax.set_title('Test 4: Fermion Quantum Numbers Origin', fontsize=14, fontweight='bold')
    quantum_aspects = ['SU(3)\nColor', 'SU(2)\nWeak', 'Hyper-\ncharge', 'Lepton\nChirality', 'Three\nGens']
    claimed_status = [1, 1, 1, 1, 1]
    reality_status = [0, 0, 0, 0, 0]

    x = np.arange(len(quantum_aspects))
    width = 0.35

    bars1 = ax.bar(x - width/2, claimed_status, width, label='Claimed (Emergent)', color='lightgreen', alpha=0.7, edgecolor='green', linewidth=2)
    bars2 = ax.bar(x + width/2, reality_status, width, label='Reality (Hardcoded)', color='lightcoral', alpha=0.7, edgecolor='red', linewidth=2)

    ax.set_ylabel('Status (1=Emergent, 0=Hardcoded)', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(quantum_aspects)
    ax.set_ylim([-0.2, 1.5])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Hardcoded\n(Injected)', 'Emergent\n(Derived)'])
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2., 1.05, '✓ Claimed',
                ha='center', va='bottom', fontsize=9, color='green', fontweight='bold')
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2., -0.05, '✗ Hardcoded',
                ha='center', va='top', fontsize=9, color='red', fontweight='bold')

    ax.text(0.5, 0.25, 'VERDICT: All 5 quantum number types are INJECTED\nSM values hardcoded by convention (see code lines 64-85)',
            transform=ax.transAxes, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
