# Pre-Commit Claim Hygiene & Scope Review: `FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` (`TFQ-1216`)

AuthorityEffect: None.

- **Date**: 2026-10-24
- **Branch**: `campaign/fsp-dirac-kahler-spinfoam-claim`
- **Target Node**: `FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` (`TFQ-1216` / `FSP-DERIV-052`, stage `FERMION_SIGN`, grade `E1 -> E3`)

## 1. What This Artifact Supports
- Formalizes in [`lean4/CampaignFspDiracKahlerSpinfoamClaim.lean`](../../../lean4/CampaignFspDiracKahlerSpinfoamClaim.lean) (10 theorems, 0 `sorry`) and checks in [`checks/independent/fsp-dirac-kahler-spinfoam-claim.py`](../../../checks/independent/fsp-dirac-kahler-spinfoam-claim.py) (`checks=16242 failures=0`):
  1. 4D exterior-algebra binomial taste decomposition $\sum_{p=0}^4 \binom{4}{p} = 1+4+6+4+1 = 16 = 4 \times 2^{4/2}$ and alternating Euler sum $0$ (`dirac_kahler_4d_exterior_taste_decomposition`).
  2. Orientifold involution $\omega(p) = (-1)^{p(p-1)/2}$ with $\omega(p)^2 = 1$, Hodge self-dual/anti-self-dual 2-form split $3(1) + 3(-1) = 0$, and minimal single-taste spinor projector idempotence $P^2 = P$ with $\operatorname{Tr}(P) = 4$ and $\operatorname{Tr}(I - P) = 12$ (`orientifold_involution_and_hodge_chirality_grading`, `minimal_spinor_projector_idempotent_and_trace_four`).
  3. Simplicial coboundary nilpotence $d_1 d_0 = 0$, flat vs curved Dirac-projector commutator $[D_{\text{curved}}(c), P_0] \ne 0$ for $c \ne 0$, and $S^4$ Euler-vs-$\hat{A}$ index mismatch $\chi(S^4) = 2 \ne 4 \hat{A}(S^4) = 0$ (`simplicial_coboundary_nilpotence_on_4simplex`, `dirac_kahler_projector_commutator_flat_vs_curved`, `kahler_dirac_euler_vs_spinor_ahat_mismatch_on_s4`).
  4. Finite spin-network boundary contraction sign dichotomy: mirror-glued two-vertex contractions $\langle \psi | V^T V | \psi \rangle \ge 0$ are nonnegative, whereas the single-vertex spin-$1$ tetrahedral Racah $6j$ recoupling kernel $W_{6j} = \begin{pmatrix} 1/6 & -1/3 \\ -1/3 & 1/6 \end{pmatrix}$ yields $-\frac{1}{3} < 0$ on $\psi_+ = (1, 1)^T$ and $+1 > 0$ on $\psi_- = (1, -1)^T$ (`finite_spin_network_boundary_contraction_sign_dichotomy`).

## 2. What This Artifact Does Not Support
- Does not claim that the 16-component taste count implies determinant or spinfoam weight positivity (`taste_count_carries_no_positivity_fence`).
- Does not claim that single-vertex EPRL-FK or Racah $6j$ spinfoam boundary contractions are universally nonnegative (`finite_spin_network_boundary_contraction_sign_dichotomy`), or that arbitrary boundary spins $k$ satisfy Euclidean EPRL half-integrality without sublattice restrictions (`eprl_simplicity_spin_embedding_sublattice_fence`).
- Does not eliminate odd-simplex Berezin orientation-reversal signs (`fermionic_cochain_orientation_reversal_sign_fence`).

## 3. Narrowest Defensible Claim
- In $D = 4$, the exterior algebra $\Lambda^*(\mathbb{Q}^4)$ decomposes into $\sum_{p=0}^4 \binom{4}{p} = 16 = 4 \times 4$ components with a rank-4 idempotent single-taste projector that commutes with the flat block Dirac operator but fails to commute under non-zero inter-taste curvature holonomy ($|[D, P]|_F^2 = 2c^2 > 0$) and exhibits index mismatch $\chi(S^4) = 2 \ne 4 \hat{A}(S^4) = 0$; on finite spin-network boundaries, mirror-glued contractions $W = V^T V$ are positive semidefinite while single-vertex spin-$1$ Racah $6j$ contractions take both negative ($-1/3$) and positive ($+1$) values.

## 4. Next Test Needed
- Formalize Rank 52 `FSP-XCUBE-FRACTON-MODEL` (`TFQ-1217`) covering the 3D X-cube stabilizer commutativity $[A_v, B_c^{\mu\nu}] = 0$ and sub-extensive ground-state degeneracy $2^{2L_x + 2L_y + 2L_z - 3}$ on finite periodic cubic lattices.
