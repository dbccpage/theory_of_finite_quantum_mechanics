Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `FSP-SU2-ADJOINT-REAL-DET` (`TFQ-1200`)

**Date:** 2026-10-23  
**Campaign Node:** `FSP-SU2-ADJOINT-REAL-DET` (`TFQ-1200`, source ID `FSP-DERIV-036`, stage `FERMION_SIGN`)  
**Outcome:** `Narrowed` (`IMPORTED_ASSUMPTION` preserved; finite algebraic and lattice Wilson–Dirac reality core formalized in Lean 4 and checked by an independent Python script)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Historical Fixture Replacement (`NonAbelianGaugeSigns.lean`)**:
   - The legacy file `lean4/Imported/Fsp/NonAbelianGaugeSigns.lean` did not contain `su2_adjoint_fermion_real_determinant`; its declarations `adjoint_matter_zero_n_ality` and `adjoint_flux_tube_curvature_vanishes` were `rfl` on a constant lookup table (withdrawn in `GIN-C12`).
   - `lean4/CampaignFspSu2AdjointRealDet.lean` replaces that table lookup with the explicit $3 \times 3$ polynomial matrix `su2AdjointMatrix a b c d` on `Fin 3`, establishing `su2AdjointMatrix_center_blind` ($R(-a,-b,-c,-d) = R(a,b,c,d)$), `su2AdjointMatrix_transpose_mul_self` ($R^T R = I_3$ on the unit sphere), and `su2AdjointMatrix_det_eq_norm_cube` ($\det R = (a^2+b^2+c^2+d^2)^3$).

2. **Antiunitary Intertwining & 4D Lattice Adjoint Wilson–Dirac Reality**:
   - `antiunitary_intertwiner_det_conj` and `antiunitary_intertwiner_det_im_zero` show that any complex matrix $D$ intertwined with its entrywise complex conjugate $\overline{D}$ by an invertible matrix $C$ ($\det C \neq 0$, $C \overline{D} = D C$) satisfies $\overline{\det D} = \det D$ and $\text{Im}(\det D) = 0$.
   - `wilsonDiracAdjoint4_intertwined` and `wilsonDiracAdjoint4_det_im_zero` instantiate this for the 4D Euclidean lattice Wilson–Dirac operator coupled to arbitrary real adjoint gauge kernels $U^\pm_\mu : \text{Matrix } (\text{Site} \times \text{Fin } 3)\;(\text{Site} \times \text{Fin } 3)\;\mathbb{R}$, using the symplectic spinor intertwiner `chargeConj4` ($C_4^2 = -I_4$, $\det C_4 = 1$).

3. **Reality vs. Positivity & Majorana Pfaffian Sign Flips**:
   - `reality_not_positivity_witness` exhibits a $3 \times 3$ antiunitarily intertwined operator $D = -I_3$ with $\text{Im}(\det D) = 0$ and $\text{Re}(\det D) = -1 < 0$.
   - `skew2_det_eq_pfaffian2_sq`, `skew4_det_eq_pfaffian4_sq`, `majorana_pfaffian2_sign_flip`, and `majorana_pfaffian4_sign_flip` formalize the $2 \times 2$ and $4 \times 4$ skew-symmetric Pfaffian identities $\det M = (\text{Pf } M)^2$ and exhibit configuration pairs with $\text{Pf}(M_+) = +1$ and $\text{Pf}(M_-) = -1$ at identical positive determinant $\det M_+ = \det M_- = 1$.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignFspSu2AdjointRealDet.lean` (`L4D`), the $3 \times 3$ real adjoint representation of unit quaternions lies in $SO(3)$ and is invariant under $(a,b,c,d) \mapsto (-a,-b,-c,-d)$; any complex matrix $D$ satisfying $C \overline{D} = D C$ with $\det C \neq 0$ has $\text{Im}(\det D) = 0$; the 4D lattice Wilson–Dirac operator coupled to real adjoint link kernels satisfies this intertwining relation and has real determinant; and explicit witnesses show $\det D < 0$ and opposite-sign Majorana Pfaffians $\text{Pf} = \pm 1$ at $\det = 1$.
   - In `checks/independent/fsp-su2-adjoint-real-det.py` (`L4D`), 546 exact symbolic and rational checks pass with 2 negative-determinant witnesses and 3 $6 \times 6$ $SU(2)$ adjoint Majorana Pfaffian sign-flip pairs.
2. **What it does not support**:
   - Full continuum 4D $SU(2)$ Yang–Mills path-integral construction, general $2n \times 2n$ Berezin Grassmann integration in Lean 4, or positivity of the single-Majorana path-integral weight.
3. **Narrowest defensible claim**:
   - Antiunitary intertwining $C \overline{D} = D C$ with $\det C \neq 0$ forces $\text{Im}(\det D) = 0$ (including for 4D lattice Wilson–Dirac operators coupled to real $SU(2)$ adjoint link kernels), while leaving the sign of $\det D$ and the sign of the Majorana Pfaffian $\text{Pf}(M)$ unfixed.
4. **Next test needed**:
   - Proceed to the next available derivation in `dag/pfp/campaign/derivation_queue.json`.
