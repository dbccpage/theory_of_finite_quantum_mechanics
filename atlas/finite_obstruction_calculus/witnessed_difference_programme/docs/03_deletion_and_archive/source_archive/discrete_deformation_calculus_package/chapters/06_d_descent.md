# Chapter 6 — Letter D: descent {#chapter-6}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

Moving to a coarser carrier discards distinctions. D does not claim that the
coarse state is faithful; it books exactly what was lost.

## 6.1 Definition

With $\pi : \mathbb{Q}^{n+k} \to \mathbb{Q}^n$ keeping the first $n$
coordinates and $\iota$ the zero-padding inclusion, the loss vector is
$x - \iota(\pi(x))$ (the dropped tail) and the loss scalar is its $\ell^1$ norm
$L(x) = \sum_{i > n} \lvert x_i \rvert$.

## 6.2 Step law

D changes the carrier and carries a loss ledger (Law 6). The historical comparison model checks the
carrier change; the ledger clause is paper-only (residual R-DDC-05). D is one
of the two letters that may lower $\Phi_1$ or $\Gamma_2$ (spine,
Theorem 11.6), which is why its loss must be booked.

## 6.3 Receipt

`DescentReceipt` records the source and target dimensions, the coarse vector,
the loss vector, the loss scalar, `is_lossless`, the status (`LOSSLESS_DESCENT`
or `DESCENT_WITH_LOSS`) and `authority_effect = "None"`. `ledger_entry` is the
ledger a D step carries.

## 6.4 Results

**Proposition 6.1** (DDC-D-01). The loss is non-negative (a sum of absolute
values; in Lean a natural number).

**Theorem 6.2** (DDC-D-02). The descent is lossless exactly when every
dropped coordinate is zero, that is, when $x \in \iota(\mathbb{Q}^n)$. Lean:
`Ddc.D_lossless_iff`, `Ddc.l1_eq_zero_iff`.

**Theorem 6.3** (DDC-D-03). Projecting twice is projecting once. Lean:
`Ddc.D_projection_idempotent`.

**Proposition 6.4** (DDC-D-04). A non-zero loss can never produce a
`LOSSLESS_DESCENT` receipt, and a lawful D carries its ledger. Lean:
`Ddc.D_needs_ledger`; tests: `test_descent.py::test_descent_with_positive_loss`,
`test_letter_modules.py::test_descent_books_its_ledger`.

## 6.5 Falsifiers

- Demo 5 without a ledger: `D` is refused (`MissingLossLedger`), and the
  lawful record is `M·T` with `REFUSED_MISSING_LOSS_LEDGER`.
- CREDIT without a ledger at D is not lawful (spine, Theorem 11.8).

## 6.6 Nonclaims

```text
D does not claim lossless projection unless the loss is zero.
D does not permit unrecorded loss of distinctions. No authorization is conferred.
```
