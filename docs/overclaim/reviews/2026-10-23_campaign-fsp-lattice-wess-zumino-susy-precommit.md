Status: AI-drafted, awaiting human review.

# Pre-Commit Overclaim & Falsification Review: `FSP-LATTICE-WESS-ZUMINO-SUSY` (`TFQ-1204`)

**Date:** 2026-10-23  
**Campaign Node:** `FSP-LATTICE-WESS-ZUMINO-SUSY` (`TFQ-1204`, source ID `FSP-DERIV-040`, stage `FERMION_SIGN`)  
**Outcome:** `Narrowed` (`OPEN` status preserved; finite-dimensional $\mathbb{Z}_2$-graded supercharge algebra, positive semidefiniteness, nonzero-energy boson–fermion partner pairing, 2-site lattice Wess–Zumino block, and 3-site discrete cubic Leibniz defect witness formalized in Lean 4 and checked by an independent Python script)  
**AuthorityEffect:** `None`

---

## 1. Falsification & Boundary Audit

1. **Historical Fixture Replacement (`NonAbelianGaugeSigns.lean` and `regge_wdw_core.lean`)**:
   - The legacy citation `NonAbelianGaugeSigns.lean::susy_supercharge_positive_hamiltonian` did not exist, and `regge_wdw_core.lean::supercharge_is_nilpotent` was `rfl` on `0 = 0` while `susy_hamiltonian_nonnegative` was `E >= 0` for `E : Nat`.
   - `lean4/CampaignFspLatticeWessZuminoSusy.lean` replaces those placeholders with genuine block-matrix supercharges `supercharge A` and `superchargeAdj B` on `nB ⊕ nF`, establishing `supercharge_sq_zero`, `susyHamiltonian_eq_fromBlocks`, `hermSupercharge1_sq`, `hermSupercharge2_sq`, `hermSupercharge_anticomm`, `bosonBlock_quadForm_nonneg`, `supertrace_susyHamiltonian_eq_zero`, `boson_to_fermion_eigenstate`, and `boson_partner_ne_zero`.

2. **Explicit Lattice Wess–Zumino Block vs. Discrete Leibniz Obstruction**:
   - `wz2SiteBlock_boson_eq_fermion` and `wz2SiteBlock_det` formalize the 2-site lattice Wess–Zumino block $A_{\text{WZ}}(m, w) = \begin{pmatrix} m & -w \\ w & m \end{pmatrix}$ with $A_{\text{WZ}}^T A_{\text{WZ}} = A_{\text{WZ}} A_{\text{WZ}}^T = (m^2 + w^2) I_2 \ge 0$.
   - `leibnizCubicDefect3_witness` and `brokenSupercharge_sq_ne_zero` show that on the 3-site periodic ring $\text{Fin } 3$, the discrete cubic Leibniz integral $\sum_{x \in \text{Fin } 3} \phi_x^2 (\phi_{x+1} - \phi_{x-1})$ evaluates to $-2 \neq 0$ at $\phi = (0, 1, 2)$, and that populating both off-diagonal blocks breaks $Q^2 = 0$, explaining why lattice discretizations generally keep at most a nilpotent subalgebra exact.

---

## 2. Claim Hygiene Summary

1. **What it supports**:
   - In `lean4/CampaignFspLatticeWessZuminoSusy.lean` (`L4D`), any odd block supercharge $Q(A)$ on a finite $\mathbb{Z}_2$-graded space satisfies $Q(A)^2 = 0$, generates two Hermitian supercharges obeying $Q_1^2 = Q_2^2 = H(A, A^\dagger)$ and $\{Q_1, Q_2\} = 0$ with nonnegative quadratic form, zero supertrace, and exact boson–fermion eigenstate pairing at $E \neq 0$, while the discrete cubic Leibniz sum on $\text{Fin } 3$ evaluates to $-2 \neq 0$ at $\phi = (0, 1, 2)$.
   - In `checks/independent/fsp-lattice-wess-zumino-susy.py` (`L4D`), 113 symbolic and exact rational checks pass with 11 paired nonzero eigenmodes and 5 discrete Leibniz/nilpotency defect witnesses.
2. **What it does not support**:
   - A full interacting 2D continuum or infinite-volume lattice Wess–Zumino Fock-space construction preserving the full 2D super-Poincaré algebra without fine-tuning, or nonperturbative continuum limit restoration of broken lattice supercharges.
3. **Narrowest defensible claim**:
   - Finite $\mathbb{Z}_2$-graded odd block supercharges $Q(A)$ satisfy $Q(A)^2 = 0$, $\{Q_a, Q_b\} = 2 \delta_{ab} H(A, A^\dagger)$, $\langle v, A^T A v \rangle = \|A v\|^2 \ge 0$, $\operatorname{Tr}(\Gamma_F H) = 0$, and exact nonzero-energy boson–fermion eigenstate pairing, whereas on a periodic lattice the failure of the discrete Leibniz rule for nonlinear superpotentials (`leibnizCubicDefect3 ![0, 1, 2] = -2 ≠ 0`) obstructs full continuum SUSY closure.
4. **Next test needed**:
   - Proceed to the next available derivation in `dag/pfp/campaign/derivation_queue.json`.
