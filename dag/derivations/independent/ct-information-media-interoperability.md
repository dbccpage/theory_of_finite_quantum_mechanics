# Independent Derivation & Scope Narrowing: `CT-INFORMATION-MEDIA-INTEROPERABILITY` (`TFQ-2006`)

## 1. Node Identity and Epistemic Contract

- **Node ID**: `CT-INFORMATION-MEDIA-INTEROPERABILITY` (`TFQ-2006`)
- **Stage**: `CONSTRUCTOR_THEORY`
- **Status**: `IMPORTED_ASSUMPTION` (narrowed to exact finite/algebraic components and non-selection scope fences in Lean 4 and an independent exact-arithmetic Python verifier)
- **External Source**: D. Deutsch and C. Marletto, *"Constructor theory of information"*, Proc. R. Soc. A **471**, 20140540 (2015), `arXiv:1405.5563`, Sections 3–6, pp. 9–12.
- **Lean 4 Module**: [`lean4/CampaignCtInformationMediaInteroperability.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean) (`L4D`, 11 theorems, 0 `sorry`, standard Lean 4 axioms only, 6/6 semantic mutations killed)
- **Independent Python Verifier**: [`checks/independent/ct-information-media-interoperability.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/ct-information-media-interoperability.py)

---

## 2. Exact Finite Algebraic Formulation (Deutsch & Marletto 2015, Sections 3–6)

In Deutsch & Marletto (2015, Sections 3–6), information is defined in terms of constructor-theoretic task realizability on discrete attributes:

1. **Computation Variable and Permutation Threshold (Section 3, p. 9)**:
   - A computation medium is a substrate equipped with a variable $S$ of cardinality $|S| \ge 2$ for which all permutations $\pi \in \mathrm{Sym}(S)$ are realizable tasks.
   - In [`singleton_not_computation_variable_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L92-L103), we formalize that a 1-state variable $\mathrm{Fin}\ 1$ has no distinct attributes ($\forall x, y \in \mathrm{Fin}\ 1, x = y$) and trivial permutation group $|\mathrm{Perm}(\mathrm{Fin}\ 1)| = 1$, whereas every $\mathrm{Fin}(n+2)$ ($|S| \ge 2$) admits distinct attributes $0 \neq 1$ exchanged by $\mathrm{Equiv.swap}\ 0\ 1$.

2. **Clonable Variable, Reversible CNOT Cloning, and Distinguishability (Sections 4–5, pp. 10–11)**:
   - A variable $S$ is clonable if there exists a blank attribute $x_0 \in S$ such that the task $\{(x, x_0) \to (x, x)\}_{x \in S}$ is realizable on $S \times S$. An information variable is a clonable computation variable.
   - On $S = \mathbb{Z}_n$, reversible cloning is realized by the generalized CNOT / modular addition map
     $$\mathrm{cnotClone}_n(x, y) = (x, x + y \bmod n), \qquad \mathrm{cnotUnclone}_n(x, y) = (x, y - x \bmod n).$$
   - In [`cnotClone_bijective_and_clones_zero`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L65-L83) and [`cnotClone_zmod2_involutive`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L86-L89), we establish that $\mathrm{cnotClone}_n$ and $\mathrm{cnotUnclone}_n$ are two-sided inverses for every $n$, $\mathrm{cnotClone}_n$ is a bijection on $\mathbb{Z}_n \times \mathbb{Z}_n$ that clones every $x \in \mathbb{Z}_n$ when the target slot is prepared in the blank attribute $0$, and $\mathrm{cnotClone}_2$ is an involution on $\mathbb{Z}_2 \times \mathbb{Z}_2$.
   - In [`clonable_computation_implies_distinguishable`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L108-L120), any injective encoding $f : X \to \mathbb{Z}_n$ maps distinct source attributes $x \neq y$ to distinct cloned pairs $\mathrm{cnotClone}_n(f(x), 0) \neq \mathrm{cnotClone}_n(f(y), 0)$, whereas any non-injective collision $f(x) = f(y)$ cannot be separated by any downstream map $g$.

3. **Principle III: Interoperability of Information Media on Finite Sets (Section 6, p. 12)**:
   - Principle III postulates that the composite of two information media $M_1, M_2$ with information variables $S_1, S_2$ is an information medium with composite information variable $S_1 \times S_2$.
   - In [`principle_III_composite_cloning_and_cardinality`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L140-L154) and [`cross_medium_copy_transfer`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L163-L171), we establish that componentwise modular addition $\mathrm{compositeClone}_{n_1, n_2}((x_1, x_2), (y_1, y_2)) = ((x_1, x_2), (x_1 + y_1, x_2 + y_2))$ is a bijection on $(\mathbb{Z}_{n_1} \times \mathbb{Z}_{n_2})^2$ that clones every joint attribute $(x_1, x_2)$ from the composite blank $(0, 0)$, the composite attribute set $\mathrm{Fin}\ d_1 \times \mathrm{Fin}\ d_2$ has cardinality $d_1 d_2$, and cross-medium copy followed by any target permutation $\pi \in \mathrm{Perm}(\mathbb{Z}_n)$ realizes the recoded copy task $(x_1, 0) \mapsto (x_1, \pi(x_1))$.

---

## 3. Non-Equivalence and Non-Selection Scope Fences (`TFQ-2007` Bridge)

Why does Principle III (`CT-INFORMATION-MEDIA-INTEROPERABILITY`) not discharge `FQ-GAP-TENSOR-UNIQUENESS` (`TFQ-2007`)? We formalize four explicit mathematical fences in [`lean4/CampaignCtInformationMediaInteroperability.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean):

1. **Quantum Off-Diagonal Non-Clonability / Entanglement Fence** ([`unitary_cnot_clones_computational_basis_not_superposition_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L186-L198)):
   - On unnormalized two-qubit amplitude vectors $(a_{00}, a_{01}, a_{10}, a_{11}) \in \mathbb{Z}^4$, the unitary CNOT map $\mathrm{cnot4}(a_{00}, a_{01}, a_{10}, a_{11}) = (a_{00}, a_{01}, a_{11}, a_{10})$ clones the computational basis vectors $(1,0,0,0) \mapsto (1,0,0,0)$ and $(0,0,1,0) \mapsto (0,0,0,1)$, but maps the superposition $(1,0,1,0) = (|0\rangle + |1\rangle) \otimes |0\rangle$ to the entangled Bell state $(1,0,0,1)$ rather than the product clone $(1,1,1,1)$. Its Schmidt determinant $a_{00} a_{11} - a_{01} a_{10} = 1 \neq 0$, whereas every product vector $(u_0 v_0, u_0 v_1, u_1 v_0, u_1 v_1)$ has Schmidt determinant $0$.

2. **Composite State-Space Dimension Trichotomy Fence** ([`composite_state_space_dimension_trichotomy_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L219-L229)):
   - Fixing two binary information variables ($d_1 = 2, d_2 = 2$) with composite attribute cardinality $|\mathrm{Fin}\ 2 \times \mathrm{Fin}\ 2| = 4$, four distinct composite state-space dimension rules all share the exact same 4-element classical information variable:
     $$\dim_{\text{simplex}}(2,2) = 3 < \dim_{\text{real-local}}(2,2) = 9 < \dim_{\text{real-quantum}}(2,2) = 10 < \dim_{\text{complex-Hermitian}}(2,2) = 16.$$
   - Therefore, set-level Cartesian interoperability ($|S_1 \times S_2| = d_1 d_2$) does not select the complex Hermitian tensor-product state-space dimension $d_1^2 d_2^2$.

3. **Complex Local Tomography vs Real Holism Excess Fence** ([`real_vs_complex_bilinear_tomography_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L235-L243)):
   - Complex Hermitian dimension satisfies exact multiplicative local tomography $(d_1 d_2)^2 = d_1^2 d_2^2$ for all $d_1, d_2$, whereas real symmetric composite space satisfies the exact holism excess identity
     $$2 d_1 d_2 (d_1 d_2 + 1) - d_1(d_1+1) d_2(d_2+1) = d_1 d_2 (d_1 - 1)(d_2 - 1) > 0 \quad (d_1, d_2 \ge 2).$$

4. **PSD vs Partially-Transposed (PT) Cone Non-Selection Fence** ([`psd_vs_pt_cone_classical_interoperability_agreement_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L263-L266), [`psd_vs_pt_cone_bell_witness_separation_fence`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean#L289-L307)):
   - On $4 \times 4$ matrices over $\mathbb{Z}$, the subsystem-$B$ partial transpose $\mathrm{partialTranspose4}$ leaves every diagonal matrix $\mathrm{Matrix.diagonal}\ d$ invariant. Thus the standard quantum PSD cone and the Partially-Transposed (PT) cone share the exact same classical information subalgebra on $\{0,1\}^2$ and the exact same quadratic form $(u_0 v_0 + u_1 v_1)^2 \ge 0$ on all product vectors, yet are separated by the Bell matrix $\mathrm{bellState4}$ and its partial transpose $\mathrm{swapWitness4}$ on the singlet vector $(0, 1, -1, 0)$ ($0$ vs $-2$).

---

## 4. Summary of Claims (Claim Hygiene Compliance)

1. **What it supports**:
   - Formalizes in Lean 4 ([`lean4/CampaignCtInformationMediaInteroperability.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean)) and an independent exact-arithmetic Python verifier ([`checks/independent/ct-information-media-interoperability.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/ct-information-media-interoperability.py)) the finite deterministic core of Constructor Theory Principle III (reversible CNOT cloning on $\mathbb{Z}_n$, computation variable cardinality threshold $|S| \ge 2$, distinguishability via injective cloning, composite Cartesian cloning on $\mathbb{Z}_{n_1} \times \mathbb{Z}_{n_2}$ with cardinality $d_1 d_2$, and cross-medium copy/recoding) together with the dimension trichotomy ($3 < 9 < 10 < 16$) and PSD-vs-PT cone separation fences.
2. **What it does not support**:
   - Does not derive the complex Hilbert-space tensor product $\mathcal{H}_1 \otimes_{\mathbb{C}} \mathcal{H}_2$ or unique bipartite PSD cone selection from Principle III alone (`FQ-GAP-TENSOR-UNIQUENESS` remains an explicit open gap).
3. **Narrowest defensible claim**:
   - On finite deterministic substrates, Principle III induces the Cartesian composite attribute set $S_1 \times S_2$ of size $d_1 d_2$ with componentwise reversible cloning $\mathrm{compositeClone}_{n_1, n_2}$, which is shared by classical simplex, real quantum, complex quantum, and partially-transposed bipartite state spaces and therefore leaves `FQ-GAP-TENSOR-UNIQUENESS` open.
4. **Next test needed**:
   - Narrow `FSP-BF-2GROUP-SIGN-CLAIM` (`TFQ-1210`) and `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211`) in the fermion-sign frontier queue.
