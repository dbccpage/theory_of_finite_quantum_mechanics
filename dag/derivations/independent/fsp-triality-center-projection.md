Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `FSP-TRIALITY-CENTER-PROJECTION` (`TFQ-1202` / `FSP-DERIV-038`)

AuthorityEffect: None.

## 1. What This Derivation Supports

1. **Canonical-Ensemble $\mathbb{Z}_3$ Center Projection in the Eisenstein-Cyclotomic Ring $\mathbb{Z}[\omega]$**:
   Representing elements $a + b\omega \in \mathbb{Z}[\omega]$ ($\omega = e^{i 2\pi / 3}$, $\omega^2 = -1 - \omega$, $\omega^3 = 1$, $1 + \omega + \omega^2 = 0$, `z3_roots_of_unity_group_law`), the unnormalized canonical-ensemble $\mathbb{Z}_3$ center projector
   $$\Pi_{\mathbb{Z}_3}(q) = \sum_{k=0}^2 \omega^{q k} \in \mathbb{Z}[\omega]$$
   equals $\langle 3, 0 \rangle$ whenever $q \equiv 0 \pmod 3$ (zero-triality color-singlet meson and baryon sectors) and vanishes identically ($\langle 0, 0 \rangle$) whenever $q \equiv 1, 2 \pmod 3$ (fractional-triality quark and diquark sectors, `canonical_z3_center_projection_identity`), satisfying the idempotence relation $\Pi_{\mathbb{Z}_3}(q)^2 = 3 \Pi_{\mathbb{Z}_3}(q)$ (`z3_center_projector_idempotence`).
2. **Which Signs $\mathbb{Z}_3$ Center Projection Removes vs Which Zero-Triality Baryon Signs Persist**:
   For a grand-canonical center-twisted partition function $Z(z_k) = Z_0 + \omega^k Z_1 + \omega^{2k} Z_2$, summing over $k \in \{0, 1, 2\}$ eliminates the fractional-triality amplitudes $Z_1, Z_2$ and isolates $3 Z_0$ (`canonical_z3_sector_fourier_isolation`). However, when the zero-triality baryon sector itself contains competing positive and negative configurations $Z_0 = w_{B,+} - w_{B,-}$ with $w_{B,-} > w_{B,+} > 0$, the center-projected partition sum $3(w_{B,+} - w_{B,-}) < 0$ remains strictly negative (`zero_triality_baryon_sector_sign_persistence`), showing that center projection removes fractional-triality phases without resolving sign oscillations inside the zero-triality baryon sector.
3. **Simplicial Y-Junction Nilpotence $d_1 \circ d_0 = 0$, $SU(3)$ Cartan Singlet Curvature, and Polyakov Action Shifts**:
   On the 4-vertex, 6-edge, 3-face simplicial Y-junction complex (`SU3SimplicialYJunction` in `code/python/src/fsp/su3_baryon_triality.py`), $d_1(d_0(v)) = (0, 0, 0)$ holds for every 0-cochain $v \in \mathbb{Z}^4$ (`y_junction_simplicial_nilpotence_d1_d0`). A uniform meson spoke cochain has zero 2-cochain curvature $d_1(s, s, s, 0, 0, 0) = (0, 0, 0)$, whereas the color-singlet 3-spoke baryon cochain $(2, 1, -3, 0, 0, 0)$ ($2 + 1 - 3 = 0$) has non-zero 2-cochain coboundary $(1, 4, -5)$ with L1 norm $10 > 0$ (`su3_cartan_singlet_y_junction_curvature`). Across the three Polyakov-loop sectors $k \in \{0, 1, 2\}$, $S_F(0) + S_F(1) + S_F(2) = 0$ and $S_F(1) - S_F(0) = 18 h P > 0$ (`polyakov_center_sector_action_sum_and_gap`).

## 2. What This Derivation Does Not Support (`GIN-C10` & `GIN-C11` Scope Fences)

1. **Historical `GIN-C10` and `GIN-C11` Fixture Fences**:
   As shown in `gin_c11_confined_sector_multiplicity_imbalance` and `gin_c10_c11_historical_fixture_scope_fence`, the finite Y-junction cochain curvature and the Polyakov-loop action gap $18 h P > 0$ are algebraic fixtures and do not establish a sign-free canonical-ensemble solver for dense lattice QCD (`OPEN` status preserved).

## 3. Narrowest Defensible Claim

In $\mathbb{Z}[\omega]$ ($\omega^2 + \omega + 1 = 0$), the canonical-ensemble $\mathbb{Z}_3$ center projector $\sum_{k=0}^2 \omega^{q k}$ isolates the zero-triality sector $q \equiv 0 \pmod 3$ and annihilates the fractional-triality sectors $q \equiv 1, 2 \pmod 3$, while leaving intra-sector baryon sign differences $w_{B,+} - w_{B,-}$ uncancelled; on the 4-vertex Y-junction complex, $d_1 \circ d_0 = 0$ holds identically and color-singlet 3-spoke fluxes carry non-zero 2-cochain coboundary, and the node remains `OPEN` under `GIN-C10` and `GIN-C11`.

## 4. Next Test Needed

Formulate an explicit canonical-ensemble determinant projection over $SU(3)$ temporal link variables on a finite $N_s^3 \times N_\tau$ lattice and measure the residual sign variance of the projected zero-triality canonical determinants $Z_B$ at non-zero baryon number $B \ge 1$.
