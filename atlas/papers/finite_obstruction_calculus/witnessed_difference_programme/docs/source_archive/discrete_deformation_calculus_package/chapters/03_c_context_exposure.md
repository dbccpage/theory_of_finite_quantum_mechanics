# Chapter 3 — Letter C: context exposure {#chapter-3}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

Evaluations are local. C restricts the ambient carrier to a window and
exposes every edge that straddles it, so that external dependencies become
declared boundary conditions instead of hidden entanglement.

## 3.1 Definition

For a finite graph $K = (V, E)$ and a window $V_W \subseteq V$, the internal
edges are those with both ends in $V_W$. The boundary interface
$\partial_E W$ is the set of edges with exactly one end in $V_W$. C maps a
cochain $c$ to $(c|_W, c|_{\partial_E W})$.

## 3.2 Step law

C changes the carrier and never lowers $\Phi_1$ or $\Gamma_2$ (Law 8). The
historical comparison model checks the carrier change (`CarrierUnchangedUnderRestructure`); the
monotonicity clause is paper-only (residual R-DDC-04). Hiding an obstruction
by choosing a smaller window is scope laundering; it has to be priced as a
descent with a loss ledger or a licensed lift.

## 3.3 Receipt

`ContextExposureReceipt` records the window, the internal and boundary edges,
both restricted cochains, the status `CONTEXT_EXPOSED` and
`authority_effect = "None"`.

## 3.4 Results

**Proposition 3.1** (DDC-C-01). The internal edges, the boundary edges and
the remaining edges partition $E$. Test:
`test_context_exposure.py::test_context_window_disjoint_partition`.

**Proposition 3.2** (DDC-C-02). An edit supported on the internal edges
leaves the boundary cochain unchanged. Test:
`test_letter_modules.py::test_exposure_is_read_only_and_internal_edits_keep_the_boundary`.

**Proposition 3.3** (DDC-C-03). Two exposures that agree on every shared edge
glue to a unique cochain on the union of their exposed edges; `glue` refuses
when a shared edge disagrees. Test:
`test_letter_modules.py::test_context_exposure_glues_agreeing_windows_uniquely`.

**Proposition 3.4** (DDC-C-04). Exposure is read-only: it returns
restrictions and never alters the ambient cochain. Test as for DDC-C-02.

**Theorem 3.5** (DDC-C-05). The boundary of an intersection of windows lies
in the union of their boundaries. Lean: `Ddc.C_boundary_of_intersection`;
test: `test_letter_modules.py::test_boundary_of_an_intersection_lies_in_the_union_of_boundaries`.

**Theorem 3.6** (DDC-C-06). A lawful C step changes the carrier and never
lowers $\Phi_1$ or $\Gamma_2$. Lean: `Ddc.C_is_not_repair`,
`Ddc.C_changes_carrier`.

## 3.5 Falsifiers

- A C step that lowers $\Gamma_2$ is refused (`ContextExposureLoweredObstruction`).
- A C step that leaves the carrier unchanged is refused by paper and historical comparison model.

## 3.6 Nonclaims

```text
C does not claim that a window is complete or that unexposed values are trivial.
C is not repair. No authorization is conferred.
```
