# Pre-Commit Claim Hygiene & Scope Review: `FSP-XCUBE-FRACTON-MODEL` (`TFQ-1217`)

AuthorityEffect: None.

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-xcube-fracton-model`
- **Target Node**: `FSP-XCUBE-FRACTON-MODEL` (`TFQ-1217` / `FSP-DERIV-053`, stage `FERMION_SIGN`, grade `E1 -> E3`)

## 1. What This Artifact Supports
- Formalizes in [`lean4/CampaignFspXcubeFractonModel.lean`](../../../lean4/CampaignFspXcubeFractonModel.lean) (10 theorems, 0 `sorry`) and checks via exact $\mathbb{F}_2$ Gaussian elimination in [`checks/independent/fsp-xcube-fracton-model.py`](../../../checks/independent/fsp-xcube-fracton-model.py) (`checks=74061 failures=0`):
  1. Periodic cubic lattice $\mathbb{T}^3(L_x, L_y, L_z)$ cell and edge-qubit counts $N_e = 3 L_x L_y L_z$ (`xcube_torus_cell_and_qubit_counts`).
  2. Pairwise commutativity $[A_v^{(\mu\nu)}, B_c] = 0$ via even edge overlap $2 \equiv 0 \pmod 2$ at every cube corner (`xcube_vertex_cross_cube_intersection_even`).
  3. Local vertex triple syzygy $A_v^{(xy)} A_v^{(yz)} A_v^{(zx)} = I$, global planar syzygy rank subtraction, logical qubit count $k = 2 L_x + 2 L_y + 2 L_z - 3$, and ground-state degeneracy $\text{GSD} = 2^{2 L_x + 2 L_y + 2 L_z - 3}$ (`xcube_local_vertex_triple_syzygy`, `xcube_stabilizer_rank_and_logical_qubit_identity`, `xcube_explicit_torus_degeneracy_table`, `xcube_subextensive_linear_scaling_vs_toric_code`).
  4. Exact $\mathbb{F}_2$ parity-check rank verification $\operatorname{rank}_{\mathbb{F}_2}(H_X) = V - (L_x + L_y + L_z - 2)$ and $\operatorname{rank}_{\mathbb{F}_2}(H_Z) = 2V - (L_x + L_y + L_z - 1)$ across all $27$ periodic cubic lattices $(L_x, L_y, L_z) \in \{2, 3, 4\}^3$.

## 2. What This Artifact Does Not Support
- Does not claim that the bosonic X-cube CSS stabilizer model resolves fermionic exchange sign problems (`xcube_css_bosonic_stoquasticity_fence`).
- Does not claim that non-abelian 2-gauge hinge intersections are sign-free (`nonabelian_hinge_holonomy_negative_trace_fence`).

## 3. Narrowest Defensible Claim
- On a finite periodic cubic lattice $\mathbb{T}^3(L_x, L_y, L_z)$ ($L_x, L_y, L_z \ge 2$), the 4-edge planar vertex crosses $A_v^{(\mu\nu)}$ and 12-edge cube operators $B_c$ share $0$ or $2$ edges, satisfy $H_X H_Z^T \equiv 0 \pmod 2$, and leave $k = 2L_x + 2L_y + 2L_z - 3$ logical qubits ($\text{GSD} = 2^{2L_x + 2L_y + 2L_z - 3}$) as checked by exact $\mathbb{F}_2$ Gaussian elimination for $(L_x, L_y, L_z) \in \{2, 3, 4\}^3$, while carrying no fermionic sign consequence by itself.

## 4. Next Test Needed
- Formalize Rank 63 `FSP-FRACTON-MOBILITY` (`TFQ-1218`) covering the sub-dimensional excitation syndrome and mobility laws for isolated fractons (0D), lineon dipoles (1D), and planon dipoles (2D).
