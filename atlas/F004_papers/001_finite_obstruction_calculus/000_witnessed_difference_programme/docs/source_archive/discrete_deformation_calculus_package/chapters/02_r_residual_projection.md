# Chapter 2 — Letter R: residual projection {#chapter-2}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

Not every defect can or should be removed. R records what remains, keeping
its class, so that an unrepaired residual is never silently discarded or
averaged away.

## 2.1 Definition

Over $\mathbb{Q}$ with the standard inner product the 1-cochains split as
$C^1 = \operatorname{im} d_0 \oplus \operatorname{im} d_1^{\top} \oplus
\mathcal{H}^1$ (spine, Theorem 3.3).

**Proposition 2.1** (DDC-R-01). Every defect splits uniquely into exact,
co-exact and harmonic parts. The first draft named only two parts, which is
correct only when there are no faces. Evidence: spine Theorem 3.3,
`cochain.hodge_split`, `test_cochain.py::test_hodge_split_is_orthogonal_and_matches_the_classes`.

R's canonical representative subtracts the coboundary of the potential that
matches the defect on a spanning forest. What remains is supported on the
edges outside the forest: one value per independent cycle.

**Proposition 2.2** (DDC-R-06). The register has $b_1 = |E| - |V| + c$
coordinates for a graph with $c$ components. They are the circulations of the
defect around the fundamental cycles, and all of them vanish exactly when the
defect is exact. The first draft handled a single cycle only.
`GraphResidualProjector` covers any finite graph, and `ResidualProjector`
keeps the single-cycle case. Tests:
`test_letter_modules.py::test_graph_projector_keeps_one_coordinate_per_independent_cycle`,
`test_cochain.py::test_a_hollow_cycle_carries_a_closed_residual`.

## 2.2 Step law

R keeps the carrier, $\Phi_1$ and $\Gamma_2$, with an adequate detector. The
historical comparison model checks the carrier and $\Phi_1$ (`ResidualProjectionChangedMass`); the
$\Gamma_2$ clause is paper-only (residual R-DDC-03).

## 2.3 Receipt

`ResidualProjectionReceipt` records the raw, exact and residual norms, both
components, the status (`RESIDUAL_RETAINED` or `EXACT_TENSION_ONLY`), the
cycle coordinates and `authority_effect = "None"`.

These norms are unweighted $\ell^1$ norms of the recorded vectors, rather
than certificates of $\Phi_1$. A fixed forest representative may have norm
strictly greater than the quotient minimum. For example, on the increasingly
oriented complete graph with vertices $a<b<c<d$ and value $-1$ on all six
edges, the forest rooted at $a$ retains $(-1,-1,-1)$ on $bc,bd,cd$. Its norm
is 3; the potential $(0,-1,-1,-2)$ attains objective 2 and a dual witness
certifies $\Phi_1=2$. Test:
`test_publication_regressions.py::test_forest_register_norm_is_not_the_quotient_minimum`.
R preserves the quotient distance because its difference is exact, regardless
of whether its representative attains the minimum.

`evaluate_xi_tie_break` compares a secondary exact score only after equal
primary diagnostics. It checks the supplied diagnostic values and makes no
claim to authenticate or remeasure the candidates.

## 2.4 Results

**Theorem 2.3** (DDC-R-02). The canonical R move is a gauge move, so it keeps
$\Gamma_2$ and exactness; a lawful R step keeps the class. Lean:
`Ddc.R_gauge_move_is_lawful`, `Ddc.R_keeps_diagnostics`, `Ddc.R_keeps_class`.

**Proposition 2.4** (DDC-R-03). The defect is conserved edge by edge: the
exact component plus the residual component equals the raw defect. Test:
`test_letter_modules.py::test_projection_conserves_the_defect`.

**Proposition 2.5** (DDC-R-04). Projecting the representative again returns
it unchanged. Test:
`test_letter_modules.py::test_graph_projector_keeps_one_coordinate_per_independent_cycle`.

**Proposition 2.6** (DDC-R-05). Terminalizing an unchanged non-exact state never yields
`CheckPassed`. A closed residual is sealed only on the residual terminal, and
an open one not at all (spine, Theorem 11.7). Test:
`test_automaton.py::test_run_tape_stops_at_the_first_unlawful_step_and_chains_receipts`.

## 2.5 Falsifiers

- An R step that lowers $\Gamma_2$ is refused (`ResidualProjectionChangedClosure`).
- An R step that moves $\Phi_1$ is refused by the paper and the historical comparison model
  (`ResidualProjectionChangedMass`).

The abstract step law compares diagnostics only. Equal norms do not identify
quotient classes: on a hollow triangle, (1,0,0) and (−1,0,0) have equal
diagnostics but different circulation. `GraphResidualProjector` subtracts an
actual coboundary; `run_tape(..., carriers=...)` checks that stronger condition.
A booked descent can subsequently change a non-exact state into an exact one.

## 2.6 Nonclaims

```text
R does not resolve the defect and does not claim that a retained residual will vanish.
R binds unresolved residual mass into the tape. No authorization is conferred.
```
