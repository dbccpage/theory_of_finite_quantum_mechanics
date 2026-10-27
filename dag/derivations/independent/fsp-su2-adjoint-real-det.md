Status: AI-drafted, awaiting human review.

# FSP-SU2-ADJOINT-REAL-DET

AuthorityEffect: None.

The node `FSP-SU2-ADJOINT-REAL-DET` (`TFQ-1200`) remains `IMPORTED_ASSUMPTION` (`Narrowed`), while its finite algebraic core—the explicit $3 \times 3$ real adjoint representation $R(a,b,c,d)$ of $SU(2)$ parameters, $\mathbb{Z}_2$ center blindness $R(-q) = R(q)$, the general antiunitary intertwiner determinant reality theorem, the 4D Euclidean charge-conjugation intertwiner $C_4$ and 4D lattice adjoint Wilson–Dirac reality theorem, reality-without-positivity witnesses ($\det < 0$), and the $2 \times 2$ and $4 \times 4$ skew-symmetric Majorana Pfaffian square identities and sign-flip pairs—is formalized in `lean4/FermionSignSu2AdjointRealDet.lean` and checked in `checks/independent/fsp-su2-adjoint-real-det.py`.

## Setting

1. **Real $SU(2) \to SO(3)$ Adjoint Matrix (`su2AdjointMatrix`)**:
   For real parameters $(a, b, c, d) \in \mathbb{R}^4$, define the $3 \times 3$ real matrix
   $$R(a,b,c,d) = \begin{pmatrix} a^2+b^2-c^2-d^2 & 2(bc-ad) & 2(bd+ac) \\ 2(bc+ad) & a^2-b^2+c^2-d^2 & 2(cd-ab) \\ 2(bd-ac) & 2(cd+ab) & a^2-b^2-c^2+d^2 \end{pmatrix}.$$
   When $a^2+b^2+c^2+d^2 = 1$, $U(a,b,c,d) = a I_2 - i(b \sigma_1 + c \sigma_2 + d \sigma_3) \in SU(2)$ acts by conjugation $U \sigma_k U^\dagger = \sum_{j=1}^3 R(a,b,c,d)_{j,k} \sigma_j$ on the Pauli basis.

2. **Antiunitary Intertwining (`antiunitary_intertwiner_det_conj`, `antiunitary_intertwiner_det_im_zero`)**:
   For a finite index type $n$ and matrices $D, C \in M_n(\mathbb{C})$ with $\det C \neq 0$, let $\text{matConj}(D) = \overline{D}$ be the entrywise complex conjugate of $D$. If $C \, \overline{D} = D \, C$, taking determinants gives
   $$\det(C) \, \overline{\det(D)} = \det(C \, \overline{D}) = \det(D \, C) = \det(D) \, \det(C),$$
   and cancelling $\det(C) \neq 0$ yields $\overline{\det(D)} = \det(D)$ and $\text{Im}(\det D) = 0$.

3. **4D Lattice Adjoint Wilson–Dirac Reality (`wilsonDiracAdjoint4_det_im_zero`)**:
   In the 4D Euclidean chiral basis $\gamma_\mu$ ($\mu \in \text{Fin } 4$) on $\text{Spin4} = \text{Fin } 2 \oplus \text{Fin } 2$, the symplectic block matrix $C_4 = \text{diag}(\varepsilon_2, \varepsilon_2)$ with $\varepsilon_2 = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$ satisfies $C_4^2 = -I_4$, $\det C_4 = 1$, and $C_4 \, \overline{\gamma_\mu} = \gamma_\mu \, C_4$ for all $\mu \in \text{Fin } 4$. Lifting $C_4$ to $C_{\text{full}} = C_4 \otimes I_{\text{Site} \times \text{Fin } 3}$ gives $C_{\text{full}}^2 = -I$, $\det C_{\text{full}} \neq 0$, and $C_{\text{full}} \, \overline{D_{\text{adj}}} = D_{\text{adj}} \, C_{\text{full}}$ for every 4D lattice Wilson–Dirac operator $D_{\text{adj}}(m_0, r, U^+, U^-)$ coupled to real adjoint gauge kernels $U^\pm_\mu$.

4. **Reality Is Not Positivity & Majorana Pfaffian Sign Flips**:
   - Reality of $\det D$ does not force $\det D \ge 0$: on $\text{Fin } 3$, $D = -I_3$ intertwined by $C = I_3$ has $\text{Im}(\det D) = 0$ and $\text{Re}(\det D) = -1 < 0$ (`reality_not_positivity_witness`).
   - For $2 \times 2$ and $4 \times 4$ skew-symmetric Majorana matrices $\text{skew2}(p)$ and $\text{skew4}(a,b,c,d,e,f)$, $\det M = (\text{Pf } M)^2$ (`skew2_det_eq_pfaffian2_sq`, `skew4_det_eq_pfaffian4_sq`), while explicit configuration pairs have $\text{Pf}(M_+) = +1$ and $\text{Pf}(M_-) = -1$ at identical positive determinant $\det M_+ = \det M_- = 1$ (`majorana_pfaffian2_sign_flip`, `majorana_pfaffian4_sign_flip`).

## Lean 4 Declarations (`lean4/FermionSignSu2AdjointRealDet.lean`)

Built via `cd lean4 && lake build FermionSignSu2AdjointRealDet` using only standard axioms (`propext`, `Classical.choice`, `Quot.sound`):
- `FermionSignSu2AdjointRealDet.su2AdjointMatrix_one`
- `FermionSignSu2AdjointRealDet.su2AdjointMatrix_center_blind`
- `FermionSignSu2AdjointRealDet.su2AdjointMatrix_conj_eq_transpose`
- `FermionSignSu2AdjointRealDet.su2AdjointMatrix_transpose_mul_self`
- `FermionSignSu2AdjointRealDet.su2AdjointMatrix_mul_transpose_self`
- `FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_eq_norm_cube`
- `FermionSignSu2AdjointRealDet.su2AdjointMatrix_det_one`
- `FermionSignSu2AdjointRealDet.matConj_realToComplexMat`
- `FermionSignSu2AdjointRealDet.matConj_su2AdjointMatrix`
- `FermionSignSu2AdjointRealDet.matConj_det`
- `FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_conj`
- `FermionSignSu2AdjointRealDet.antiunitary_intertwiner_det_im_zero`
- `FermionSignSu2AdjointRealDet.antiunitary_intertwiner_two_flavor_nonneg`
- `FermionSignSu2AdjointRealDet.chargeConj4_sq`
- `FermionSignSu2AdjointRealDet.chargeConj4_det`
- `FermionSignSu2AdjointRealDet.chargeConj4_intertwines_gamma4d`
- `FermionSignSu2AdjointRealDet.chargeConj4_intertwines_gamma5Four`
- `FermionSignSu2AdjointRealDet.fullIntertwiner4_sq`
- `FermionSignSu2AdjointRealDet.fullIntertwiner4_det_ne_zero`
- `FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_intertwined`
- `FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_conj`
- `FermionSignSu2AdjointRealDet.wilsonDiracAdjoint4_det_im_zero`
- `FermionSignSu2AdjointRealDet.reality_not_positivity_witness`
- `FermionSignSu2AdjointRealDet.skew2_det_eq_pfaffian2_sq`
- `FermionSignSu2AdjointRealDet.majorana_pfaffian2_sign_flip`
- `FermionSignSu2AdjointRealDet.skew4_det_eq_pfaffian4_sq`
- `FermionSignSu2AdjointRealDet.majorana_pfaffian4_sign_flip`

## Independent Check (`checks/independent/fsp-su2-adjoint-real-det.py`)

Imports no repository code. Uses Python `fractions.Fraction` and SymPy to check:
- Symbolic polynomial identities for $R(a,b,c,d)$, $\mathbb{Z}_2$ center blindness, Pauli adjoint intertwining $U \sigma_k U^\dagger = \sum_j R_{j,k} \sigma_j$, quaternion homomorphism $R(q_1 q_2) = R(q_1) R(q_2)$, and 125 rational unit quaternions on $S^3(\mathbb{Q})$.
- Exact 4D Euclidean intertwining $C_4 \overline{\gamma_\mu} = \gamma_\mu C_4$ and $24 \times 24$ 4D Wilson–Dirac operators coupled to non-commuting rational $SO(3)$ links, confirming $C_{\text{full}} \overline{D_{\text{adj}}} = D_{\text{adj}} C_{\text{full}}$, $\text{Im}(\det D_{\text{adj}}) = 0$, and local $SO(3)$ gauge invariance of $\det D_{\text{adj}}$.
- Explicit real-intertwined adjoint operators with negative real determinants ($\det = -1$ and $\det = -3$).
- Symbolic $2 \times 2$, $4 \times 4$, and $6 \times 6$ skew-symmetric Pfaffian identities $\det M = (\text{Pf } M)^2$ and explicit $6 \times 6$ $SU(2)$ adjoint Majorana sign-flip pairs ($\text{Pf} = -1$ vs $\text{Pf} = +1$ with $\det = +1$).

## Scope Fence (What Is Not Claimed)

1. **What it supports**: The explicit $3 \times 3$ real adjoint representation of $SU(2)$ parameters, $\mathbb{Z}_2$ center blindness $R(-q) = R(q)$, determinant reality $\text{Im}(\det D) = 0$ for any complex matrix intertwined with its complex conjugate by an invertible matrix $C$, reality of $\det D_{\text{adj}}$ for the 4D lattice Wilson–Dirac operator coupled to real adjoint link kernels, negative-determinant witnesses showing reality is not positivity, and the $2 \times 2$ and $4 \times 4$ Majorana Pfaffian square identities and sign-flip witnesses.
2. **What it does not support**: Full continuum or thermodynamic-limit 4D $SU(2)$ Yang–Mills path-integral construction, general $2n \times 2n$ Grassmann Berezin-integral derivations of the Pfaffian measure for arbitrary lattice volumes, or absence of a sign problem for a single Majorana adjoint flavor.
3. **Narrowest defensible claim**: In Lean 4 (`FermionSignSu2AdjointRealDet`), every unit quadruple $(a,b,c,d)$ defines an $SO(3)$ matrix $R(a,b,c,d)$ invariant under $(a,b,c,d) \mapsto (-a,-b,-c,-d)$; every 4D lattice Wilson–Dirac operator `wilsonDiracAdjoint4` coupled to real adjoint link kernels is intertwined by `fullIntertwiner4` with its entrywise complex conjugate and has $\text{Im}(\det D_{\text{adj}}) = 0$; and explicit finite witnesses show $\det D < 0$ is compatible with antiunitary reality while $2 \times 2$ and $4 \times 4$ skew-symmetric Majorana matrices satisfy $\det M = (\text{Pf } M)^2$ with opposite-sign Pfaffians at $\det M = 1$.
