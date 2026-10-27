Status: AI-drafted, awaiting human review.

# FSP-LATTICE-WESS-ZUMINO-SUSY

AuthorityEffect: None.

The node `FSP-LATTICE-WESS-ZUMINO-SUSY` (`TFQ-1204`) remains `OPEN` (`Narrowed`), while its finite-dimensional graded linear-algebraic core and lattice subalgebra obstruction—exact nilpotency $Q(A)^2 = 0$, the Clifford-SUSY relations $\{Q_a, Q_b\} = 2 \delta_{ab} H(A, A^\dagger)$ for the two Hermitian supercharges $Q_1, Q_2$, positive semidefiniteness of the bosonic and fermionic blocks $A^T A$ and $A A^T$, exact supertrace vanishing $\operatorname{Tr}(\Gamma_F H) = 0$, exact boson–fermion partner mapping on nonzero-energy eigenstates, the explicit 2-site lattice Wess–Zumino operator `wz2SiteBlock`, and the discrete cubic Leibniz rule defect witness (`leibnizCubicDefect3_witness`)—is formalized in `lean4/FermionSignLatticeWessZuminoSusy.lean` and checked in `checks/independent/fsp-lattice-wess-zumino-susy.py`.

## Setting

1. **$\mathbb{Z}_2$-Graded Supercharge Algebra (`supercharge_sq_zero`, `hermSupercharge1_sq`, `hermSupercharge2_sq`, `hermSupercharge_anticomm`)**:
   On a finite $\mathbb{Z}_2$-graded Hilbert space $n_B \oplus n_F$ with fermion parity involution $\Gamma_F = \operatorname{diag}(I_{n_B}, -I_{n_F})$, any odd forward supercharge $Q(A) = \begin{pmatrix} 0 & 0 \\ A & 0 \end{pmatrix}$ and backward partner $Q^\dagger(B) = \begin{pmatrix} 0 & B \\ 0 & 0 \end{pmatrix}$ satisfy $Q(A)^2 = 0$, $Q^\dagger(B)^2 = 0$, and $\{\Gamma_F, Q\} = 0$. The supersymmetric Hamiltonian $H(A, B) = \{Q(A), Q^\dagger(B)\} = \operatorname{diag}(B A, A B)$ commutes with $\Gamma_F$, $Q(A)$, and $Q^\dagger(B)$. Over $\mathbb{C}$ with $B = A^\dagger$, the two Hermitian combinations $Q_1(A) = Q(A) + Q(A)^\dagger$ and $Q_2(A) = -i(Q(A) - Q(A)^\dagger)$ satisfy
   $$Q_1(A)^2 = H(A, A^\dagger), \qquad Q_2(A)^2 = H(A, A^\dagger), \qquad Q_1(A) Q_2(A) + Q_2(A) Q_1(A) = 0.$$

2. **Positive Semidefiniteness, Supertrace Cancellation, & Boson–Fermion Partner Pairing (`bosonBlock_quadForm_nonneg`, `supertrace_susyHamiltonian_eq_zero`, `boson_to_fermion_eigenstate`, `boson_partner_ne_zero`)**:
   - For any real operator block $A \in M_{n_F \times n_B}(\mathbb{R})$ and vector $v \in \mathbb{R}^{n_B}$, $\langle v, (A^T A) v \rangle = \sum_{x} ((A v)_x)^2 \ge 0$, and similarly $\langle w, (A A^T) w \rangle \ge 0$.
   - The supertrace $\operatorname{Tr}(\Gamma_F H(A, B)) = \operatorname{Tr}(B A) - \operatorname{Tr}(A B) = 0$ vanishes identically.
   - If $(B A) v_B = E v_B$, then $(A B)(A v_B) = E (A v_B)$, and when $E \neq 0$ and $v_B \neq 0$ over a field, $A v_B \neq 0$.

3. **Explicit 2-Site Lattice Wess–Zumino Block & Discrete Leibniz Defect Obstruction (`wz2SiteBlock_boson_eq_fermion`, `leibnizCubicDefect3_witness`, `brokenSupercharge_sq_ne_zero`)**:
   - The 2-site lattice Wess–Zumino block $A_{\text{WZ}}(m, w) = \begin{pmatrix} m & -w \\ w & m \end{pmatrix}$ yields $A_{\text{WZ}}^T A_{\text{WZ}} = A_{\text{WZ}} A_{\text{WZ}}^T = (m^2 + w^2) I_2$ and $\det A_{\text{WZ}}(m, w) = m^2 + w^2 \ge 0$.
   - On the 3-site periodic ring $\text{Fin } 3$, the discrete cubic Leibniz integral $\sum_{x \in \text{Fin } 3} \phi_x^2 (\phi_{x+1} - \phi_{x-1})$ evaluates to $-2 \neq 0$ at $\phi = (0, 1, 2)$, showing why naive finite-difference discretizations of interacting superpotentials break the continuum Leibniz rule and preserve at most the nilpotent subalgebra $Q(A)^2 = 0$.

## Lean 4 Declarations (`lean4/FermionSignLatticeWessZuminoSusy.lean`)

Built via `cd lean4 && lake build FermionSignLatticeWessZuminoSusy` using only standard axioms (`propext`, `Classical.choice`, `Quot.sound`):
- `FermionSignLatticeWessZuminoSusy.fermionParity_sq`
- `FermionSignLatticeWessZuminoSusy.supercharge_sq_zero`
- `FermionSignLatticeWessZuminoSusy.superchargeAdj_sq_zero`
- `FermionSignLatticeWessZuminoSusy.supercharge_anticommutes_parity`
- `FermionSignLatticeWessZuminoSusy.superchargeAdj_anticommutes_parity`
- `FermionSignLatticeWessZuminoSusy.susyHamiltonian_eq_fromBlocks`
- `FermionSignLatticeWessZuminoSusy.susyHamiltonian_commutes_parity`
- `FermionSignLatticeWessZuminoSusy.supercharge_commutes_susyHamiltonian`
- `FermionSignLatticeWessZuminoSusy.superchargeAdj_commutes_susyHamiltonian`
- `FermionSignLatticeWessZuminoSusy.hermSupercharge1_hermitian`
- `FermionSignLatticeWessZuminoSusy.hermSupercharge2_hermitian`
- `FermionSignLatticeWessZuminoSusy.hermSupercharge1_sq`
- `FermionSignLatticeWessZuminoSusy.hermSupercharge2_sq`
- `FermionSignLatticeWessZuminoSusy.hermSupercharge_anticomm`
- `FermionSignLatticeWessZuminoSusy.bosonBlock_quadForm_eq_sum_sq`
- `FermionSignLatticeWessZuminoSusy.bosonBlock_quadForm_nonneg`
- `FermionSignLatticeWessZuminoSusy.fermionBlock_quadForm_nonneg`
- `FermionSignLatticeWessZuminoSusy.boson_eq_fermion_trace`
- `FermionSignLatticeWessZuminoSusy.supertrace_susyHamiltonian_eq_zero`
- `FermionSignLatticeWessZuminoSusy.boson_to_fermion_eigenstate`
- `FermionSignLatticeWessZuminoSusy.fermion_to_boson_eigenstate`
- `FermionSignLatticeWessZuminoSusy.boson_partner_ne_zero`
- `FermionSignLatticeWessZuminoSusy.wz2SiteBlock_boson_eq_fermion`
- `FermionSignLatticeWessZuminoSusy.wz2SiteBlock_det`
- `FermionSignLatticeWessZuminoSusy.leibnizCubicDefect3_witness`
- `FermionSignLatticeWessZuminoSusy.brokenSupercharge_sq_ne_zero`

## Independent Check (`checks/independent/fsp-lattice-wess-zumino-susy.py`)

Imports no repository code. Uses Python `fractions.Fraction` and SymPy to check:
- Symbolic and exact rational $\mathbb{Z}_2$-graded supercharge relations ($Q^2 = 0$, $\{Q_a, Q_b\} = 2 \delta_{ab} H$, $\operatorname{Str}(H^k) = 0$, and characteristic polynomial pairing $\lambda^{n_F}\det(\lambda I_{n_B} - A^\dagger A) = \lambda^{n_B}\det(\lambda I_{n_F} - A A^\dagger)$) across square and rectangular blocks.
- Exact 2-site, 3-site 1D ring, and rectangular ($n_B = 3, n_F = 2$) finite-lattice Wess–Zumino models, confirming positive semidefiniteness and explicit nonzero eigenstate pairing $v_F = A v_B$.
- Vanishing of the discrete Leibniz sum for linear $W'(\phi) = m \phi + c$ on periodic rings $L=3, 4, 5$ contrasted with nonzero cubic Leibniz defects for $W'(\phi) = \phi^2$ (including $-2 \neq 0$ at $\phi = (0, 1, 2)$ on $L=3$).

## Scope Fence (What Is Not Claimed)

1. **What it supports**: The exact finite-dimensional graded supercharge algebra ($Q(A)^2 = 0$, $Q_1^2 = Q_2^2 = H(A, A^\dagger)$, $\{Q_1, Q_2\} = 0$), quadratic-form nonnegativity of $A^T A$ and $A A^T$, supertrace vanishing $\operatorname{Tr}(\Gamma_F H) = 0$, exact nonzero-eigenvalue partner mapping between bosonic and fermionic sectors, the 2-site lattice Wess–Zumino block, and the 3-site discrete cubic Leibniz defect witness.
2. **What it does not support**: A full interacting 2D continuum or infinite-volume lattice Wess–Zumino Fock-space construction preserving the full 2D super-Poincaré algebra without fine-tuning, or nonperturbative continuum limit restoration of broken lattice supercharges.
3. **Narrowest defensible claim**: In Lean 4 (`FermionSignLatticeWessZuminoSusy`), any odd block supercharge $Q(A)$ on a finite $\mathbb{Z}_2$-graded space satisfies $Q(A)^2 = 0$, generates two Hermitian supercharges obeying $Q_1^2 = Q_2^2 = H(A, A^\dagger)$ and $\{Q_1, Q_2\} = 0$ with nonnegative quadratic form, zero supertrace, and exact boson–fermion eigenstate pairing at $E \neq 0$, while the discrete cubic Leibniz sum on $\text{Fin } 3$ evaluates to $-2 \neq 0$ at $\phi = (0, 1, 2)$.
