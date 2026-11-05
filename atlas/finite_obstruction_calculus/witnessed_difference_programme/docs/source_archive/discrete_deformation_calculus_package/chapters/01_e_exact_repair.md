# Chapter 1 — Letter E: exact repair {#chapter-1}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

E removes a defect that lies in the image of $d_0$. It is the *exact* part of
the Hodge split, not the co-exact part; the first draft of this chapter had
the two reversed.

## 1.1 Definition

Let $K = (V, E, F)$ be a finite oriented 2-complex with

$$(d_0 \varphi)(u \to v) = \varphi(v) - \varphi(u), \qquad
(d_1 x)(f) = \sum_{e \in \partial f} [f : e]\, x(e),$$

where $[f : e] \in \{-1, 1\}$ is the orientation of $e$ in the boundary of $f$.
A defect $x \in C^1(K; \mathbb{Q})$ is *exact-repairable* when
$x \in \operatorname{im} d_0$, equivalently $\Phi_1(x) = 0$.

**Proposition 1.1** (DDC-E-01). An exact defect has a potential $\varphi$
with $d_0 \varphi = x$, unique up to adding one constant on each connected
component. `ExactRepairSolver` finds it by breadth-first integration from one
gauge vertex per component.

*Proof.* Two potentials of the same defect differ by $\psi$ with
$d_0 \psi = 0$, that is, $\psi$ is constant along every edge and hence on every
component. $\square$

The repair is $x \mapsto x - d_0 \varphi = 0$.

## 1.2 Step law

E keeps the carrier, starts from an exact class, and leaves
$\Phi_1 = \Gamma_2 = 0$ and a zero defect with an adequate detector. The
historical comparison model's `verify_step` checks the carrier and the exact class after the step
(`ExactRepairLeftResidual`); the class before the step, the zero defect and
the detector are checked only by this package (residual R-DDC-02).

## 1.3 Receipt

`ExactRepairReceipt` records `success`, `input_norm`, `residual_norm`,
`gauge_vertex`, `potential`, the repaired defect (`repaired`, all zeros on
success), `error` and `authority_effect = "None"`.

## 1.4 Results

**Theorem 1.2** (DDC-E-02). If $d_0 \varphi = x$ then $x - d_0 \varphi = 0$.
Lean: `Ddc.E_gauge_repair_discharges`.

**Theorem 1.3** (DDC-E-03). A gauge move $x \mapsto x - d_0 \varphi$ changes
neither $d_1 x$ nor whether $x$ is exact. Consequently no gauge repair can
cross a class: a defect that is closed but not exact, or open, stays so.
Lean: `Ddc.E_gauge_preserves_closure`, `Ddc.E_gauge_preserves_exactness`,
over an abstract complex with additive $d_0, d_1$ and $d_1 d_0 = 0$.

**Theorem 1.4** (DDC-E-04). A defect with non-zero circulation around any
cycle of the declared 1-skeleton is not in $\operatorname{im} d_0$, and E
refuses it with `REFUSED_NON_ZERO_CURL`. The name is kept for wire
compatibility; its meaning is exactly "not in $\operatorname{im} d_0$". Lean
example: `Ddc.E_triangle_open_not_exact` (every edge of a filled triangle
carries 1). Tests: `test_exact_repair.py::test_exact_repair_refusal_non_zero_curl`,
`test_letter_modules.py::test_exact_repair_refuses_any_cycle_with_circulation`.

**Theorem 1.5** (DDC-E-05). Exact repair is idempotent: repairing the
repaired (zero) defect again changes nothing. Lean: `Ddc.E_repair_idempotent`.

The orthogonality of the exact part to the harmonic part is Theorem 3.3 of the
spine.

## 1.5 Falsifiers

- Demo 1 applies `E` to an open defect; the step is refused because the class
  before `E` is not exact (`ExactRepairFromNonExactClass`).
- A class-crossing edit (an open state rewritten to zero) passes the historical comparison model
  but not the paper (`test_automaton.py::test_engine_checks_less_than_the_paper`).

## 1.6 Nonclaims

```text
E does not claim semantic truth or the correctness of external code or models.
E is a local algebraic gauge adjustment on a declared carrier.
No authorization is conferred.
```
