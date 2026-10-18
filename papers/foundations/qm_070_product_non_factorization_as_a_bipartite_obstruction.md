# QM_070 — Redirect Stub (Absorbed into Consolidated Correlation & Separability Account)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone draft is retired. Its surviving mathematical core (classical independence diagnostic, stochastic map contraction, and observation-loss boundary) is merged directly into:

- **Consolidated Account:** [`qm_071_entanglement_as_a_separability_obstruction.md`](qm_071_entanglement_as_a_separability_obstruction.md) (Section 1: Classical Independence and the Observation-Loss Boundary).
- **Source Notes:** [`../006_finite_qm/finite_quantum_mechanics_source_notes.md#1130-product-non-factorization-in-bipartite-systems-qm-070-merged-and-retired`](../006_finite_qm/finite_quantum_mechanics_source_notes.md#1130-product-non-factorization-in-bipartite-systems-qm-070-merged-and-retired) (§11.30).
- **Certified Rust Implementation:** `omega_engine/crates_rs/omega_finite_probability/src/joint_table.rs` (`JointTable::{product_defect, product_defect_mass, apply_local_maps, has_vanishing_minors}`).
- **Integration & Property Tests:** `omega_engine/crates_rs/tests/omega_quantum_physics/entanglement/product_non_factorization.rs`.
- **Claims & Provenance:** Replayed in [`qm_071_entanglement_as_a_separability_obstruction.md`](qm_071_entanglement_as_a_separability_obstruction.md) (Section 1) and source notes [`../006_finite_qm/finite_quantum_mechanics_source_notes.md#1130-product-non-factorization-in-bipartite-systems-qm-070-merged-and-retired`](../006_finite_qm/finite_quantum_mechanics_source_notes.md#1130-product-non-factorization-in-bipartite-systems-qm-070-merged-and-retired) (§11.30).

---

## Retained Mathematical Formulation

### 1. Classical Independence Residual
For a nonnegative joint weight table $w$ over finite index sets $A \times B$ with total mass $W = \sum_{a,b} w(a,b) > 0$, marginals are $w_A(a) = \sum_b w(a,b)$ and $w_B(b) = \sum_a w(a,b)$. The **product defect** and its $\ell^1$ norm are:

$$
\delta_{\mathrm{prod}}(w) = w - \frac{w_A \otimes w_B}{W}, \qquad \Phi(w) = \|\delta_{\mathrm{prod}}(w)\|_1 = \sum_{a,b} \left|w(a,b) - \frac{w_A(a)\,w_B(b)}{W}\right|.
$$

**Theorem (Exact Classical Independence).**
$$
\Phi(w) = 0 \quad\Longleftrightarrow\quad w = \frac{w_A \otimes w_B}{W}.
$$

### 2. Scale-Independent Total-Variation Distance
For the normalized probability distribution $p = w / W$:

$$
\frac{\Phi(w)}{W} = \|p - p_A \otimes p_B\|_1.
$$

Thus $\frac{\Phi(w)}{2W} = \frac{1}{2}\|p - p_A \otimes p_B\|_1$ is the exact total-variation distance from $p$ to its own marginal product. (In general, this is not the minimum distance to the full manifold of all product distributions).

### 3. Contraction Under Independent Stochastic Maps
For independent column-stochastic maps $K_A, K_B$:

$$
\delta_{\mathrm{prod}}((K_A \otimes K_B)w) = (K_A \otimes K_B)\delta_{\mathrm{prod}}(w).
$$

Because a column-stochastic map is a non-expansion on the $\ell^1$ norm ($\|K v\|_1 \le \|v\|_1$ for all vectors $v$ with zero column-sum or general vectors):

$$
\Phi((K_A \otimes K_B)w) \le \Phi(w).
$$

The hypothesis of *independent* stochastic maps is mandatory. A shared random variable (mixture of local maps) can prepare correlated outcomes like $(0,0)$ and $(1,1)$ from a product state, creating classical correlation with $\Phi > 0$ without entanglement.

### 4. Information-Loss Boundary: A Single Table Cannot Certify Entanglement
Every product-basis probability table $p_{ab}$ admits the explicitly separable diagonal quantum realization:

$$
\rho_{\mathrm{diag}} = \sum_{a,b} p_{ab} |a\rangle\langle a| \otimes |b\rangle\langle b|.
$$

Consequently, observation of a single classical joint table alone is fundamentally compatible with a separable state:
- **Collision:** The maximally entangled Bell state $\rho_B = |\Phi^+\rangle\langle\Phi^+|$ and the classical separable mixture $\rho_C = \frac{1}{2}|00\rangle\langle00| + \frac{1}{2}|11\rangle\langle11|$ yield the exact same computational-basis table $p = (1/2, 0, 0, 1/2)$ and identical defect mass $\Phi = 1$.
- **Converse Failure:** The pure state $|\psi\rangle = \frac{1}{2}(|00\rangle + |01\rangle + |10\rangle - |11\rangle)$ is entangled (its coefficient matrix has rank 2), yet its computational-basis table is uniform $p = (1/4, 1/4, 1/4, 1/4)$, yielding $\Phi = 0$.

Thus $\Phi(w)$ evaluates the statistical independence of the observed table, not the productness or entanglement of the underlying quantum carrier.
