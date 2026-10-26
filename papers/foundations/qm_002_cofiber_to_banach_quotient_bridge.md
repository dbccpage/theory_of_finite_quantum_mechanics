# QM_002 — Redirect Stub (Absorbed into Shared Finite-Obstruction Treatment)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-10-17 packaging merge).

## Live Destination

The standalone manuscript is retired. Its surviving mathematical content is merged into the shared finite-obstruction quotient treatment alongside QM-000:

- **Canonical Monograph:** [`../finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md#chapter-04`](../finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md#chapter-04) (Chapter 4, §4.2.1 and §4.3).
- **Source Notes:** [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md#113-a-finite-banach-quotient-model-of-repair-qm-002-merged-and-retired`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md#113-a-finite-banach-quotient-model-of-repair-qm-002-merged-and-retired) (§11.3).
- **Lean 4 Mechanization:** [`lean4/CofiberBanachQuotient.lean`](../../lean4/CofiberBanachQuotient.lean) (`phi1_eq_quotient_norm`, `quotient_norm_eq_zero_iff_exact_repair`).
- **Certified Rust Solvers:** `omega_engine/crates_rs/omega_solvers/src/data_repair_packet.rs` (`RepairPacket::quotient_norm`).
- **Integration Tests:** `omega_engine/crates_rs/tests/omega_quantum_physics/foundations/repair_cofiber_banach_shadow.rs`.
- **Consolidated Claims:** [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (IDs `002:QM-002-C1` through `002:QM-002-C10`).

## Retained Mathematical Formulation

**Proposition (Finite Banach repair cokernel and quotient norm).**  
For any finite-dimensional linear repair map $d_0: C^0 \to C^1$ between finite-dimensional normed spaces with repair subspace $M = \operatorname{im} d_0$, the repair-distance functional equals the quotient norm of the finite Banach cokernel:

$$
\Phi_1([x]) = \inf_{\alpha \in C^0} \|x - d_0 \alpha\|_{1,w} = \inf_{m \in M} \|x - m\|_{1,w} = \|x + M\|_{C^1/M}.
$$

**Proof.** The repair image $M = \operatorname{im} d_0$ is a subspace of the finite-dimensional space $C^1$. Every element $m \in M$ has the form $d_0 \alpha$ for some $\alpha \in C^0$. Hence the infimum of the distance over all declared repairs $\alpha \in C^0$ is identically the infimum over elements $m \in M$, which defines the quotient norm $\|x + M\|_{C^1/M}$ on the algebraic quotient space. Finite dimensionality ensures that $M$ is closed, which establishes Hausdorff separation of the quotient space ($\|[x]\|_{\mathrm{quot}} = 0 \iff x \in M$). $\square$

### Key Mathematical Boundaries & Corrections

1. **Role of Closedness in Normed Quotients:**  
   Finite-dimensional closedness is *not* required for the distance infimum identity itself: for any subspace $M$ of a normed space,
   $$
   \operatorname{dist}(x, M) = \operatorname{dist}(x, \overline{M})
   $$
   holds universally (`Metric.infDist_closure`). What closedness establishes is the separation property
   $$
   \operatorname{dist}(x, M) = 0 \implies x \in M,
   $$
   ensuring that $C^1/M$ is a genuine normed space rather than merely a seminormed space. This distinguishes exact repair from limiting repair approximation. For example, the operator $T: \ell^1 \to \ell^1$ with $(Ta)_n = a_n/n$ has a dense range containing all finitely supported sequences, but $x_n = 1/n^2 \notin \operatorname{ran} T$. Here $\inf_a \|x - Ta\|_1 = \operatorname{dist}(x, M) = \operatorname{dist}(x, \overline{M}) = 0$, so distance to the range is zero and matches the norm in the separated completion, yet $x$ cannot be exactly repaired. Finite dimensionality ensures $\Phi_1([x]) = 0 \iff x \in \operatorname{im} d_0$.

2. **Categorical Language as a Chosen Finite Model:**  
   The statement "A finite linear repair map has an ordinary Banach cokernel whose quotient norm is the repair-distance functional" describes a chosen finite model in $\operatorname{Arr}(\mathsf{FinBan}_{\mathbb{R}})$. An unrestricted categorical realization remains an open research question: supplying a functor does not automatically establish that it preserves universal cofibers without an explicit universal comparison, nor do general Banach isomorphisms preserve numerical norms without isometric compatibility or bounded distortion.

3. **Closed Quotient Norm Formula:**  
   For the canonical map $d_0(\alpha) = (\alpha, -\alpha, 0)$ in $\mathbb{R}^3$ with unit weights, the quotient norm is exactly:
   $$
   \Phi_1([x_1, x_2, x_3]) = \inf_{\alpha \in \mathbb{R}} (|x_1 - \alpha| + |x_2 + \alpha| + |x_3|) = |x_1 + x_2| + |x_3|.
   $$
   The lower bound follows from the triangle inequality $|x_1 - \alpha| + |x_2 + \alpha| \ge |(x_1 - \alpha) + (x_2 + \alpha)| = |x_1 + x_2|$, attained at $\alpha = x_1$. This evaluates to $1$ on $(0,0,1)$ and $0$ on $(1,-1,0)$.

4. **Representative Selection vs. Quotient Descent:**  
   Coordinatewise absolute values $|x|$ and normalized densities $\operatorname{diag}(|x|/\|x\|_1)$ do not descend to quotient classes $C^1/M$. For $M = \operatorname{span}\{(1,-1)\}$, the class $[(1,0)] = [(0,1)]$ contains two norm-minimizing representatives whose normalized densities $\operatorname{diag}(1,0)$ and $\operatorname{diag}(0,1)$ are orthogonal. Density construction is a diagnostic of a declared representative, not a quotient class invariant.

## What This Folder Retains

- Historical claim ledger mapping for bijection packaging (`002:QM-002-C1`..`C10`).
- Sibling files preserved for backward provenance; no new standalone papers or active claims are minted here.
