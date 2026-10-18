# Exact Relational Mechanics and Certified Sign Boundaries of the Fermi-Hubbard Model

**Date:** 2026-10-02  
**Version:** 0.1.0  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0) / MIT (Code)  

This package assigns no authorization and changes no jurisdiction. It carries no operational authority or institutional standing.

## Overview

This repository package contains the manuscript, data, relational schemas, and reproducibility test suites for *Exact Relational Mechanics and Certified Sign Boundaries of the Fermi-Hubbard Model: Diagonal Sign Gauges, Auxiliary-Field Palindromic Symmetries, and Explicit Negative Witnesses*.

The investigation provides exact algebraic evaluations of the Fermi-Hubbard model on finite graphs using pure rational arithmetic ($\mathbb{Q} \times \mathbb{Q}$) in SQLite, with zero floating-point operations.

## Key Mathematical Results

1. **Exchange-Loop Obstructions on Physical Trees**: In the occupation basis, diagonal sign gauges cannot remove negative matrix elements on the 3-leaf star graph, demonstrating that the absence of spatial lattice loops does not prevent many-fermion exchange-loop sign obstructions.
2. **Palindromic Kinetic Symmetries**: The kinetic matrix $T$ is constructed as an exact second-order Suzuki product of bond exponentials, ensuring $\det(T) = 1$ and the particle-hole inversion relation $\eta T \eta = T^{-1}$ on bipartite lattices.
3. **Protected Determinant Sectors**:
   - *Repulsive Half-Filled Bipartite*: $\det(I + P_\downarrow) = \det(I + P_\uparrow) / \det(P_\uparrow)$, yielding non-negative weights $w(s) \ge 0$ for all field configurations.
   - *Attractive Arbitrary Geometries*: $P_\uparrow = P_\downarrow$, yielding non-negative squared weights $w(s) = h^{-\sum s} [\det(I + P_\uparrow)]^2 \ge 0$ across all geometries, including geometrically frustrated clusters.
4. **Explicit Negative Field Witnesses**: Rational existence witnesses record that breaking bipartiteness or half-filling introduces negative weights (Mask 15721 for doped 4-site ring; Mask 1281 for frustrated 3-site triangle).
5. **Non-Singular Observables via Dual Numbers**: Evaluates exact total particle number expectations without singular matrix inversions.

## Repository Layout

- `paper.md`: Main research paper manuscript.
- `paper_claim_ledger.md`: Formal claim ledger mapping all mathematical claims to test verifications.
- `paper_change_log.md`: Package changelog.
- `code/`:
  - `hubbard_exact_model.py`: Vendored exact Hubbard evaluator. It does not import the sibling `sign_sql` package at runtime.
  - `hubbard_schema.sql`: Relational schema for SQLite evaluation tables and determinant CTEs.
  - `deposit_paths.py`: Path safety and file walker utilities.
  - `tests/test_hubbard_paper_reproducibility.py`: Full reproducibility test suite.
- `docs/`: Component descriptions and literature references.
- `verify_deposit.py`: Canonical deposit verifier.

## Verification

To verify all claims and run the reproducibility tests:
```bash
py -3.12 -m pytest code/tests/test_hubbard_paper_reproducibility.py
py -3.12 verify_deposit.py
```
