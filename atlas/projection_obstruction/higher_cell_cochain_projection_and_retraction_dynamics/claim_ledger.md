# PO-034 claim ledger

Technical preprint v0.1 (0.1.0), dated 2026-10-10. Authority effect: None.

A finite autonomous Hermitian dilation uses one fixed finite-dimensional
carrier, one fixed time-independent Hermitian Hamiltonian, and one fixed
initial total state to reproduce the entire trajectory for all t>=0.
The no-go claims do not address time-by-time or unrestricted time-dependent
dilations. Thirteen ledger claims include six written-only lemmas; the seven
stored conditional abstract Lean declarations cover only C1 and C2.

## **PO034-C1**: Product projector idempotence and marginals

**Type:** Theorem

On traceless Hermitian directions at a normalized product reference, P is idempotent, preserves single-site marginals, and projects onto the algebraic product tangent space. Full-rank densities permit the usual interior manifold interpretation.

**Scope:** Boundary feasibility is separate. The full-space software map is the derivative of the homogeneous extension.

**Numerical evidence:** `coda_higher_cell.k_cell_retraction.k_cell_tangent_projector`, `coda_higher_cell.k_cell_retraction.k_cell_normal_projector`, `coda_higher_cell.k_cell_retraction.verify_marginal_preservation`.

**Regression examples:**

- `code/tests/test_k_cell_retraction.py::test_tangent_projector_idempotence_and_marginals`
- `code/tests/test_k_cell_retraction.py::test_full_space_extension_derivative_and_tiny_trace_linearity`
- `code/tests/test_holonomy_defect_bridge.py::test_single_site_hamiltonian_has_zero_defect_velocity`
- `code/tests/test_holonomy_defect_bridge.py::test_two_site_interaction_defect_and_marginal_annihilation`
- `code/tests/test_holonomy_defect_bridge.py::test_3simplex_cochain_mapping_and_face_holonomies`

### **PO034-C1-NS**: Product projector marginal preservation and no-signalling holonomy bridge

The product tangent projector \(P\) preserves local single-site marginals (\(\operatorname{Tr}_{\setminus j}[P(Z)] = \operatorname{Tr}_{\setminus j}[Z]\)) while the normal defect projector \(Q\) has vanishing single-site marginal traces (\(\operatorname{Tr}_{\setminus j}[Q(Z)] = 0\)). Under two-site entangling Hamiltonian interactions on a simplicial cell, defect speed \(\nu = \|Q[H, \rho]\|_1 > 0\) accumulates boundary edge cochains and face holonomies without perturbing local marginals, matching Cycle 007 formal no-signalling (`LT-NS`), continuous \(U(1)\) torsion exclusion (`LT-U1`), and discrete rotation generators (`LT-A`). Mechanized formal completions are stored in `lean4/quantum_mechanics/` (`NoSignalling.lean`, `RotationGroups.lean`, `H011Circle.lean`).

**Lean scope:** Conditional abstract additive identities; trace/embedding laws are structure fields. No concrete matrix instantiation. Formal completions for LT-A, LT-U1, and LT-NS reside in lean4/quantum_mechanics (RotationGroups.lean, H011Circle.lean, NoSignalling.lean). Stored census only; no fresh build in this review.

## **PO034-C2**: One-site isolation and a distinct highest-order projector

**Type:** Theorem and counterexample

Q annihilates one-site Hamiltonian variations. Proper multi-site support need not be tangent: X1 X2 I3 at |000> has QL=L with trace norm 2. A separate projector R_k=product_j(I-E_j) annihilates reference-factorized proper-support variations.

**Scope:** Q is not R_k for k>2. Neither full support nor a nonzero component alone establishes genuine multipartite entanglement.

**Numerical evidence:** `coda_higher_cell.k_cell_retraction.verify_generalized_tangent_isolation`, `coda_higher_cell.k_cell_retraction.verify_1local_tangent_isolation`, `coda_higher_cell.k_cell_retraction.highest_order_correlation_projector`, `coda_higher_cell.k_cell_retraction.k_cell_boundary_face_projector`.

**Regression examples:**

- `code/tests/test_k_cell_retraction.py::test_one_site_tangent_isolation`
- `code/tests/test_k_cell_retraction.py::test_two_body_counterexample_and_highest_order_isolation`
- `code/tests/test_k_cell_retraction.py::test_full_support_can_commute`

**Lean scope:** One-site embedding identities and vectors explicitly assumed in im(P). No all-proper-support commutator theorem and no R_k formalization.

## **PO034-C3**: Finite-Hamiltonian short-time nonfactorization bound

**Type:** Analytic theorem

For a finite closed system, product initial state, and ||H||_infinity <= g for the whole Hamiltonian, D(t) >= nu*t - 2*(1+k^2)*g^2*t^2 >= nu*t - 6*k^2*g^2*t^2. For nu>0, t<=nu/(12*k^2*g^2) gives D(t)>=nu*t/2.

**Scope:** The code evaluates the weaker formula and compares actual analytic states numerically. Lemma 4.3a (PO034-C3a) is the closed-system site-budget refinement. Lemma 4.3b (PO034-C3b) is the finite-dilation extension. Lemma 4.3d (PO034-C3d) is the finite-jump coefficient with no Hamiltonian. Lemma 4.3e (PO034-C3e) places a bounded Hamiltonian beside that family. The code does not evaluate these lemmas. The mixed quadratic coefficient is \(2(1+k^2)(g+G)^2\). A strictly smaller mixed coefficient is not certified. Lemma 4.3f (PO034-C3f) shows that the state-acceleration bound cannot replace \((g+G)^2\) by \(g^2+G^2\). That lemma does not change the defect coefficient. Zero initial speed does not imply future factorization.

**Numerical evidence:** `coda_higher_cell.defect_bounds.short_time_k_party_defect_lower_bound`, `coda_higher_cell.defect_bounds.evaluate_k_party_trace_defect`.

**Regression examples:**

- `code/tests/test_defect_bounds.py::test_short_time_bound_against_analytic_ghz_state`
- `code/tests/test_defect_bounds.py::test_zero_initial_speed_does_not_imply_future_factorization`
- `code/tests/test_defect_bounds.py::test_classical_separable_state_has_defect_one`

**Lean scope:** Not mechanized in this deposit.

## **PO034-C3a**: Closed-system site-budget refinement of the short-time bound

**Type:** Lemma

For \(H=\sum_\alpha h_\alpha\) on a closed finite system, with each Hermitian \(h_\alpha\) supported on a declared subset \(X_\alpha\), \(g\ge\|H\|_\infty\), and \(g_j=\sum_{\alpha:j\in X_\alpha}\|h_\alpha\|_\infty\), set \(\Gamma=g^2+g\sum_j g_j+\sum_{i\ne j}g_ig_j\). Then \(D(t)\ge\nu t-2\Gamma t^2\). If \(\nu>0\) and \(t\le\nu/(4\Gamma)\), then \(D(t)\ge\nu t/2\). The one-term decomposition \(h_1=H\) with declared support \(X_1=\sigma\) and \(g=\|H\|_\infty\) recovers \(\Gamma=(1+k^2)g^2\).

**Scope:** Package version remains 0.1.0. The global factor \(g\) stays in \(\Gamma\). A redundant decomposition can make \(\Gamma\) larger than the Theorem 4.3 coefficient. Removing \(g\) is not claimed. The reduced-subsystem statement is Lemma 4.3b, not this lemma.

**Witness:** Example 4.3a. For \(k=3\), \(H=X\otimes X\otimes I\), \(g=1\), support \(\{1,2\}\), one has \(g_1=g_2=1\), \(g_3=0\), \(\sum_j g_j=2\), \(\sum_{i\ne j}g_ig_j=2\), \(\Gamma=5\), and \(2\Gamma=10\), against \(2(1+k^2)g^2=20\). Counterexample 4.2a gives \(\nu=2\), so \(D(t)\ge2t-10t^2\) and \(D(t)\ge t\) on \(0\le t\le1/10\). The weaker Theorem 4.3 window is \(0\le t\le1/54\). The site-3 velocity has trace norm \(0\). The site-1 velocity has trace norm \(2|\sin(2t)|\), equal to \(2g_1\) at \(t=\pi/4\). The witness does not evaluate \(D(t)\). It is not a Python test.

**Numerical evidence:** None. The Theorem 4.3 code path is unchanged.

**Lean scope:** Not mechanized in this deposit.

## **PO034-C3b**: Reduced site-budget bound on a finite dilation

**Type:** Lemma

For a finite dilation on \(\sigma\sqcup\varepsilon\) with \(k=|\sigma|\ge 2\), Hermitian decomposition of the dilated Hamiltonian, \(g\ge\|H\|_\infty\), and system site budgets \(g_j\), the same \(\Gamma=g^2+g\sum_{j\in\sigma}g_j+\sum_{i\ne j}g_ig_j\) gives \(D_\sigma(t)\ge\nu_\sigma t-2\Gamma t^2\). If \(\nu_\sigma>0\) and \(t\le\nu_\sigma/(4\Gamma)\), then \(D_\sigma(t)\ge\nu_\sigma t/2\). If \(H=H_\sigma\otimes I+I\otimes H_\varepsilon\), the reduced trajectory is the unitary orbit of \(H_\sigma\) and \(\|H_\varepsilon\|_\infty\) does not enter it.

**Scope:** Package version remains 0.1.0. The global factor \(g\) stays in \(\Gamma\). Replacement by \(\max_j g_j\) is not claimed. A Lindblad generator without a finite autonomous Hermitian dilation is not covered. An environment-only summand can inflate \(g\). Example 4.3b is an exact symbolic witness, not a Python test.

**Witness:** Example 4.3b. \(\sigma=\{1,2,3\}\), \(\varepsilon=\{4\}\), \(H=(X\otimes X\otimes I)\otimes|0\rangle\langle0|\), \(g=1\), support \(\{1,2,4\}\), \(g_1=g_2=1\), \(g_3=0\), \(\Gamma=5\), and \(2\Gamma=10\), against the closed three-site leading coefficient \(20\). Initial vector \((|0000\rangle+|0001\rangle)/\sqrt{2}\). Exact reduced defect \(D_\sigma(t)=2ab+2\max(ab,|w|)\) with \(a=(1+\cos^2 t)/2\), \(b=\sin^2 t/2\), \(w=i\cos t\sin t/2\), \(ab=\sin^2 t(1+\cos^2 t)/4\), and \(|w|=|\cos t\sin t|/2\). Then \(\nu_\sigma=1\), so \(D_\sigma(t)\ge t-10t^2\) and \(D_\sigma(t)\ge t/2\) on \(0\le t\le 1/20\). Nonzero eigenvalues \((1\pm\cos t)/2\) on \([0,\pi/2]\) are not constant, so the reduced trajectory is not a unitary orbit. At \(t=\pi/2\), purity is \(1/2\) and \(D_\sigma=1\).

**Numerical evidence:** None. The Theorem 4.3 code path is unchanged.

**Lean scope:** Not mechanized in this deposit.

## **PO034-C3c**: Jump trajectory with no finite autonomous Hermitian dilation

**Type:** Lemma

For the two-qubit jump generator \(\mathcal L(\rho)=K\rho K^\dagger-\frac12\{K^\dagger K,\rho\}\) with \(K=|00\rangle\langle11|\) and \(\rho(0)=|11\rangle\langle11|\), one has \(\rho(t)=(1-e^{-t})|00\rangle\langle00|+e^{-t}|11\rangle\langle11|\), \(D(t)=4e^{-t}(1-e^{-t})\), and \(\nu=4\). Thus \(D(t)\ge 4t-6t^2\), and \(D(t)\ge 2t\) on \(0\le t\le 1/3\). The population \(e^{-t}\) is not a finite sum of characters \(e^{-i\omega t}\), so the trajectory is not the reduction of any fixed finite-dimensional autonomous Hermitian evolution with a fixed initial total state for every t>=0.

**Scope:** Package version remains 0.1.0. This is one generator. The finite-jump coefficient with no Hamiltonian is Lemma 4.3d, and it does not recover the coefficient \(6\). A bounded Hamiltonian beside a finite jump family is Lemma 4.3e, and its coefficient does not recover \(6\). Lemma 4.3b's norm \(g\) and site budgets are unavailable. Replacing \(g\) by \(\max_j g_j\) is not claimed. The witness is exact and symbolic, not a Python test.

**Witness:** Lemma 4.3c. \(K=|00\rangle\langle11|\), \(\rho(0)=|11\rangle\langle11|\), \(D(t)=4e^{-t}(1-e^{-t})\), \(\nu=4\), coefficient \(6\), half-speed window \(0\le t\le 1/3\). Obstruction: linear independence of \(e^{-t}\) from \(\{e^{-i\omega t}\}\).

**Numerical evidence:** None. The Theorem 4.3 code path is unchanged.

**Lean scope:** Not mechanized in this deposit.

## **PO034-C3d**: Quadratic coefficient for a finite family of jumps

**Type:** Lemma

For \(k\ge 2\) and a finite jump family with no Hamiltonian,
\(\mathcal L(X)=\sum_\alpha\bigl(K_\alpha X K_\alpha^\dagger-\frac12\{K_\alpha^\dagger K_\alpha,X\}\bigr)\)
and \(G\ge\sum_\alpha\|K_\alpha\|_\infty^2\), product initial data gives
\(D(t)\ge\nu t-2(1+k^2)G^2 t^2\ge\nu t-6k^2 G^2 t^2\), where
\(\nu=\|f'(0)\|_1\). If \(\nu>0\) and \(0\le t\le\nu/(4(1+k^2)G^2)\), then
\(D(t)\ge\nu t/2\). On the Lemma 4.3c data, \(G=1\) and \(k=2\), so the
quadratic coefficient is \(10\) and the half-speed window is \(1/5\), not
the scalar coefficient \(6\) and the window \(1/3\).

**Scope:** Package version remains 0.1.0. No Hamiltonian term. No site budgets. The global factor \(g\) is not removed, and replacement by \(\max_j g_j\) is not claimed. No finite-dilation obstruction is claimed for a general jump family. The witness is the comparison with Lemma 4.3c, not a Python test.

**Witness:** Lemma 4.3c data inside Lemma 4.3d. \(m=1\), \(K=|00\rangle\langle11|\), \(G=1\), \(k=2\), \(\nu=4\), quadratic coefficient \(2(1+4)G^2=10\), half-speed window \(0\le t\le 1/5\). Lemma 4.3c gives coefficient \(6\) and window \(1/3\). At \(t=0\), \(\|\rho'(0)\|_1=2=2G\), so the first-derivative budget is achieved and the quadratic coefficient is not.

**Numerical evidence:** None. The Theorem 4.3 code path is unchanged.

**Lean scope:** Not mechanized in this deposit.

## **PO034-C3e**: Quadratic coefficient for a bounded Hamiltonian beside a finite jump family

**Type:** Lemma

For \(k\ge 2\), Hermitian \(H\) with \(g\ge\|H\|_\infty\), and a finite jump family with \(G\ge\sum_\alpha\|K_\alpha\|_\infty^2\), the generator
\(\mathcal L(X)=-i[H,X]+\sum_\alpha\bigl(K_\alpha X K_\alpha^\dagger-\frac12\{K_\alpha^\dagger K_\alpha,X\}\bigr)\)
and product initial data give
\(D(t)\ge\nu t-2(1+k^2)(g+G)^2 t^2\ge\nu t-6k^2(g+G)^2 t^2\),
where \(\nu=\|f'(0)\|_1\). If \(\nu>0\) and \(0\le t\le\nu/(4(1+k^2)(g+G)^2)\), then
\(D(t)\ge\nu t/2\). The case \(G=0\) recovers the leading coefficient of Theorem 4.3.
The case \(g=0\) recovers Lemma 4.3d. The square \((g+G)^2\) keeps the cross term \(2gG\).
On the commuting witness \(k=2\), \(g=1\), \(G=1\), the quadratic coefficient is \(40\) and the half-speed window is \(1/20\), not the scalar coefficient \(6\) and the window \(1/3\).

**Scope:** Package version remains 0.1.0. No site budgets. The global factor \(g\) is not removed, and replacement by \(\max_j g_j\) is not claimed. The cross term is not removed, and \((g+G)^2\) is not replaced by \(g^2+G^2\). Lemma 4.3f shows that the state-acceleration form of that replacement is false and does not change this defect coefficient. The scalar coefficient \(6\) and the window \(1/3\) are not recovered. No finite-dilation obstruction is claimed for a general mixed family. The witness is exact and symbolic, not a Python test.

**Witness:** \(k=2\), \(m=1\), \(K=|00\rangle\langle11|\), \(H=|00\rangle\langle00|-|11\rangle\langle11|\), \(\rho(0)=|11\rangle\langle11|\), \(g=1\), \(G=1\), \(\nu=4\). Quadratic coefficient \(2(1+4)(1+1)^2=40\). Half-speed window \(0\le t\le 1/20\). \(H\) commutes with the Lemma 4.3c trajectory, so \(D(t)=4e^{-t}(1-e^{-t})\) and Lemma 4.3c still gives coefficient \(6\) and window \(1/3\). At \(t=0\), \(\|\rho'(0)\|_1=2\), while \(2(g+G)=4\), so the first-derivative budget is not achieved and the quadratic coefficient is not sharp. This one trajectory still has no finite autonomous Hermitian dilation.

**Numerical evidence:** None. The Theorem 4.3 code path is unchanged.

**Lean scope:** Not mechanized in this deposit.

## **PO034-C3f**: The acceleration cross term does not drop

**Type:** Lemma

For two qubits, \(S=|0\rangle\langle0|+i|1\rangle\langle1|\), \(H=Z\otimes I\), \(K=S\otimes I\), and \(\rho(0)=|+\rangle\langle+|\otimes|0\rangle\langle0|\), one has \(g=1\), \(G=1\), and \(\|\rho''(0)\|_1=10\). Thus \(4(g^2+G^2)=8<\|\rho''(0)\|_1<16=4(g+G)^2\). The state-acceleration estimate \(\|\rho''(t)\|_1\le 4(g+G)^2\) cannot be replaced by \(\|\rho''(t)\|_1\le 4(g^2+G^2)\). The orbit is the product \(A(t)\otimes|0\rangle\langle0|\) with coherence \(c(t)=\tfrac12 e^{-(1+3i)t}\), so \(D(t)=0\) and \(\nu=0\).

**Scope:** Package version remains 0.1.0. No site budgets. The global factor \(g\) is not removed, and replacement by \(\max_j g_j\) is not claimed. The defect coefficient of Lemma 4.3e is not replaced by \(2(1+k^2)(g^2+G^2)\), and this witness does not establish that the defect replacement is false. The full cross contribution \(8gG\) inside \(4(g+G)^2\) is not achieved. The scalar coefficient \(6\) and the window \(1/3\) are not recovered. No finite-dilation obstruction is claimed for a general mixed family. The witness is exact and symbolic, not a Python test.

**Witness:** \(k=2\), \(m=1\), \(H=Z\otimes I\), \(K=S\otimes I\), \(\rho(0)=|+\rangle\langle+|\otimes|0\rangle\langle0|\), \(g=1\), \(G=1\). Coherence \(c(t)=\tfrac12\exp(-(1+3i)t)\). \(\|\rho'(0)\|_1=\sqrt{10}<4=2(g+G)\). \(\|\rho''(0)\|_1=10\). The gap above \(4(g^2+G^2)\) is \(2\). The acceleration budget \(16\) is not achieved. \(D(t)=0\) and \(\nu=0\). The factor \(e^{-t}\) is not a finite sum of characters, so this one trajectory has no finite autonomous Hermitian dilation.

**Numerical evidence:** None. The Theorem 4.3 code path is unchanged.

**Lean scope:** Not mechanized in this deposit.

## **PO034-C4**: Polar trace-norm duality without a tangent-annihilator claim

**Type:** Theorem and counterexample

A polar partial isometry W has operator norm at most one and pairs with the residual to its trace norm. A normal residual can have an optimal witness with nonzero tangent pairing.

**Scope:** Numerical SVD; singular-value cutoffs contribute to the returned full complex alignment error. No nearest-tangent or entanglement certificate.

**Numerical evidence:** `coda_higher_cell.defect_bounds.schatten1_dual_witness`.

**Regression examples:**

- `code/tests/test_defect_bounds.py::test_polar_witness_does_not_annihilate_tangents`
- `code/tests/test_defect_bounds.py::test_complex_polar_alignment`
- `code/tests/test_defect_bounds.py::test_zero_and_thresholded_witness`

**Lean scope:** Not mechanized in this deposit.

## **PO034-C5**: Finite scalar Hodge decomposition

**Type:** Standard finite theorem

Constant-coefficient scalar cochains decompose orthogonally into im(d_prev), im(d_next*), and ker(Delta). Components are unique; potentials need not be. The hollow triangle cycle disappears on filling.

**Scope:** Requires declared incidence, orientation, and coefficients. No general sheaf or protected-entanglement interpretation is supplied.

**Numerical evidence:** `coda_higher_cell.simplicial_complex.simplicial_laplacian`, `coda_higher_cell.simplicial_complex.hodge_decomposition`, `coda_higher_cell.simplicial_complex.simplicial_boundary_matrix`.

**Regression examples:**

- `code/tests/test_simplicial_laplacian.py::test_incidence_nilpotence`
- `code/tests/test_simplicial_laplacian.py::test_hollow_filled_triangle_and_complex_hodge`

**Lean scope:** Not mechanized in this deposit.

## **PO034-C6**: Graded-square sign and separate semigroup coefficient

**Type:** Finite algebra and analytic proposition

With C=dh(q+1)dv(p)-dv(p+1)dh(q) and D=dh+(-1)^p dv, D^2=dh^2+dv^2+(-1)^p C. Independently, a C^2 retraction gives mixed semigroup coefficient P A n + D^2Pi(Am,n), tangent under the genuine retraction hypotheses.

**Scope:** The example double complex has nilpotent vertical maps. A supplied Hessian vector is not certified as a retraction Hessian. No equality between square and semigroup defects or non-Abelian model is established.

**Numerical evidence:** `coda_higher_cell.bicomplex_ddc.bicomplex_curvature_tensor`, `coda_higher_cell.bicomplex_ddc.semigroup_defect_tensor`.

**Regression examples:**

- `code/tests/test_bicomplex_and_prime_triad.py::test_commuting_double_complex_is_nilpotent`
- `code/tests/test_bicomplex_and_prime_triad.py::test_noncommuting_square_and_totalized_sign`
- `code/tests/test_bicomplex_and_prime_triad.py::test_semigroup_coefficient_checks_tangency_and_inputs`

**Lean scope:** Not mechanized in this deposit.

## **PO034-C7**: Metadata, aligned adapter losses, and local policy scaffold

**Type:** Local protocol schema

Carrier degree equals simplex cardinality minus one. Adapter loss is the trace norm of an ambient defect minus a sum of supplied common-space lifts. Continuation applies local policies to declared evidence; the seven-label trace always reports receipt_verified=False.

**Scope:** No executed DDC, automatic gluing, external Prime algorithm, or authority. Scalar residual equality does not establish a cycle, and evidence identifiers do not replay their contents.

**Numerical evidence:** `coda_higher_cell.prime_triad_bridge.prime_triad_carrier_declaration`, `coda_higher_cell.prime_triad_bridge.adapter_loss_ledger`, `coda_higher_cell.prime_triad_bridge.can_continue_predicate`.

**Regression examples:**

- `code/tests/test_bicomplex_and_prime_triad.py::test_carrier_declaration_requires_evidence_identifiers`
- `code/tests/test_bicomplex_and_prime_triad.py::test_adapter_loss_requires_aligned_operators`
- `code/tests/test_bicomplex_and_prime_triad.py::test_cycle_requires_declared_complete_state_identity`

**Lean scope:** Not mechanized in this deposit.

The exact exercise runner checks only small finite algebra. The stored Lean report lists seven conditional declarations; it is not a fresh build receipt. See the review receipt for performed checks and unavailable replay gates.

**PO034-C8**: §4.3 gives the written density-state perturbation and observed-cochain bounds. The new supplemental census proves the normed factor-replacement and residual bounds under explicit path-step estimates; the concrete density-matrix instantiation remains a written proof. See `lean4/projection_axiom_census.json`. Scalar examples in `docs/residual_error_budget/` validate supplied-bound arithmetic only.
