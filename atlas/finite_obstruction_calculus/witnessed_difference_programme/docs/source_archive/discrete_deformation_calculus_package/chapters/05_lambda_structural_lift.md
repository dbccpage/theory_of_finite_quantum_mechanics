# Chapter 5 — Letter Λ: structural lift {#chapter-5}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

When an obstruction cannot be handled on the current carrier, ad hoc
expansion would launder authority. Λ is licensed carrier expansion: it needs a
licence, and it needs a trigger that makes a lift the right move. A trigger is
not a licence.

## 5.1 Definition

The lift pads with zeros: $\iota : \mathbb{Q}^n \hookrightarrow
\mathbb{Q}^{n+k}$, $\iota(x)_i = x_i$ for $i \le n$ and $0$ otherwise.

## 5.2 Step law

Λ changes the carrier, carries a licence, and starts from a `ClosedResidual`
or from an inadequate detector (Law 4). The historical comparison model checks the carrier change;
the licence and the trigger are paper-only (residual R-DDC-05). The first
draft did not state the trigger.

## 5.3 Receipt

`LiftReceipt` records the initial and extended dimensions, the licence, the
lifted vector, the trigger, `success`, `error` (`REFUSED_UNLICENSED_LIFT`,
`REFUSED_LIFT_TRIGGER` or `INVALID_NEGATIVE_EXPANSION`) and
`authority_effect = "None"`.

The auxiliary `FiniteLambdaLedger` stores exact nonnegative diagnostic rows
and checks endpoint matching, adjacency, non-final `is_descent` flags and the
final `is_valid` flag. Both flags must be actual booleans; the row sequence is
snapshotted. They remain assumptions, rather than checked preservation or
licence certificates. This consistency gate does not execute the external
Rust `require_descent_step` or `require_valid` methods and establishes no
current contract conformance. It also does not impose a resolved final
endpoint on a nonempty ledger; that condition needs a separate policy.

## 5.4 Results

**Theorem 5.1** (DDC-L-01). Zero-padding preserves the $\ell^1$ norm, and
every inner product among old vectors. Lean: `Ddc.L_pad_preserves_l1`; test:
`test_letter_modules.py::test_lift_trigger_law_and_norm_preservation`.

**Proposition 5.2** (DDC-L-02). A lawful Λ carries a licence and a trigger.
Lean: `Ddc.L_needs_licence_and_trigger`.

**Proposition 5.3** (DDC-L-03). The new coordinates are orthogonal to the
image of $\iota$, since their supports are disjoint.

**Proposition 5.4** (DDC-L-04). An unlicensed or untriggered lift fails
closed and returns the original vector. Tests:
`test_structural_lift.py::test_unlicensed_lift_refusal`,
`test_letter_modules.py::test_lift_trigger_law_and_norm_preservation`.

**Theorem 5.5** (DDC-TAPE-09). Let
$K_0$ sit in $K_1$ with restriction maps that commute with $d_0$, and let
$x'$ on $K_1$ restrict to $x$ on $K_0$. If $x'$ is exact on $K_1$, then $x$
is exact on $K_0$. So a non-exact residual stays non-exact under every lift
that extends it. Lean: `Ddc.L_cannot_exactify`.

*Proof.* If $x' = d_0 \varphi$ then
$x = \rho_1(d_0 \varphi) = d_0(\rho_0 \varphi)$. $\square$

Demo 3 shows both halves. A lift that adds capacity away from the cycle keeps
$\Phi_1 = 1$, and the survivor is sealed on the residual terminal. A lift that
attaches a face bounding the cycle turns the survivor into an open defect
($\Gamma_2 = 1$) that `T` may not seal.

## 5.5 Falsifiers

- A lift without a licence is refused (`UnlicensedLift`).
- A lift from an exact or an open, adequately detected state is refused
  (`LiftWithoutTrigger`).

## 5.6 Nonclaims

```text
Λ does not grant unbounded or continuous expansion and does not resolve a survivor.
Λ requires an explicit discrete licence. No authorization is conferred.
```
