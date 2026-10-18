# QM_004 — Redirect Stub (Absorbed into Shared Finite-Obstruction Treatment)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone manuscript is retired. Its surviving mathematical content is merged into the shared finite-obstruction quotient treatment:

- **Canonical Monograph:** [`../001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md#chapter-04`](../001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md#chapter-04) (Chapter 4, §4.2.2).
- **Source Notes:** [`../006_finite_qm/finite_quantum_mechanics_source_notes.md#114-residual-density-across-the-l1l2-boundary-qm-003-and-qm-004-absorbed-and-retired`](../006_finite_qm/finite_quantum_mechanics_source_notes.md#114-residual-density-across-the-l1l2-boundary-qm-003-and-qm-004-absorbed-and-retired) (§11.4).
- **Native Rust Tests:** `006_finite_qm/native/tests/obstruction_management_firewall.rs` and `006_finite_qm/native/tests/residual_density_boundary.rs`.
- **Consolidated Claims:** [`../006_finite_qm/claims/claim_ledger.yaml`](../006_finite_qm/claims/claim_ledger.yaml) (IDs `004:QM-004-C1` through `004:QM-004-C24`).

## Retained Mathematical Formulation

### 1. Diagonal Density Presentation and Mass Ledger Scale Invariance

Given a finite vector of nonnegative masses $\mu = (\mu_1, \ldots, \mu_n) \in \mathbb{R}^n_{\ge 0}$ with positive total $\sum_{j=1}^n \mu_j > 0$, the normalized weights

$$
p_i = \frac{\mu_i}{\sum_{j=1}^n \mu_j}, \qquad \rho_{\mathrm{diag}} = \operatorname{diag}(p_1, \ldots, p_n)
$$

define a valid classical probability distribution presented as a diagonal density matrix ($\operatorname{Tr}(\rho_{\mathrm{diag}}) = 1$, $\rho_{\mathrm{diag}} \succeq 0$). Stochastic updates preserve this diagonal representation.

**Scale Invariance:** The correspondence is between mass ledgers modulo positive overall scaling $\mu \sim c\mu$ ($c > 0$) and diagonal density matrices. Ledgers $(3, 1)$ and $(6, 2)$ produce the identical diagonal density $\operatorname{diag}(3/4, 1/4)$. Normalization forgets total unnormalized mass. This result does not derive complex amplitudes, coherence, Born uniqueness, or physical quantum dynamics.

### 2. Observer Factorization Criterion

For an observation map $O: X \to Y$, a target readout or query $h: X \to Z$ can be recovered from the observation (there exists $\tilde{h}: Y \to Z$ such that $h = \tilde{h} \circ O$) if and only if

$$
O(x) = O(y) \implies h(x) = h(y) \qquad \forall x, y \in X.
$$

For multiple observers with maps $O_1, \ldots, O_k$, replace $O$ by their joint report $(O_1, \ldots, O_k)$. Statements regarding "locally green but globally red" fragments are direct instances of this fiber-separation criterion.

### 3. Exact-Repair Translation Commutativity and Quotient Defect Invariance

In a fixed linear repair complex with repair map $d_0: C^0 \to C^1$, an exact repair parametrized by $a \in C^0$ has the form

$$
R_a(x) = x + d_0 a.
$$

Fixed repair translations commute: $R_a \circ R_b = R_b \circ R_a = R_{a+b}$, and leave the quotient projection unchanged: $\pi(R_a(x)) = \pi(x)$. State-dependent representative changes may fail to commute, but every such change induces the identity on the repair quotient and preserves every quotient-defined readout.

**Counterexample (noncommuting state-dependent repairs):** Let $d_0 a = (a, 0)$, so the repair quotient remembers only $y$. Define
$$
R(x, y) = (x + y, y), \qquad S(x, y) = (2x, y).
$$
Both maps change the input only by an element of $\operatorname{im}(d_0)$. Nevertheless,
$$
R \circ S(x, y) = (2x + y, y), \qquad S \circ R(x, y) = (2x + 2y, y).
$$
They need not commute, even though both induce the identity on the quotient.

Thus, manipulating representatives in this way cannot create a new observable distinction at the quotient level. A proposed quantum operation must do something beyond changing representatives within a fixed repair class; every quotient-defined defect functional satisfies:

$$
\Phi_1([x + d_0 f(x)]) = \Phi_1([x]).
$$

## What This Folder Retains

- Historical claim ledger mapping for bijection packaging (`004:QM-004-C1`..`C24`).
- Standalone manuscript retired; Everett/MCTS analogies, branch-search framing, and repeated authority results are omitted.
