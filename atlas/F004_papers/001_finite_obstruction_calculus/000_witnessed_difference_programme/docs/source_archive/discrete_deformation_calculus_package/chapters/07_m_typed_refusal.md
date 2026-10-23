# Chapter 7 — Letter M: typed refusal {#chapter-7}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

The ability to refuse is co-equal with the ability to deform. M is a lawful
refusal outcome: it leaves the state unchanged, names its reason and moves
control to `Refused`. It does not seal the tape; a later C, Λ or T still needs
its own law and control check.

## 7.1 Definition

A request is a letter, a locus, an alleged witness and a cost. Grounding is
checked at intake, before admission; witness and budget are checked on the
tape as M.

## 7.2 Step law

M leaves the state unchanged and carries a reason from the closed vocabulary
below. The historical comparison model checks the unchanged state (`InertOpMutatedState`). It
carries its reason as a free string
(`dda_alphabet::StepOutcome::RefusedToExecute`), so this vocabulary is owned by
the paper (residual R-DDC-05). After M, only `C`, `Λ` or `T` may follow
(spine, Theorem 11.3).

## 7.3 The refusal vocabulary

Intake refusals are recorded before admission and never enter the tape
(`enters_ddc_trace` is false):

| Code | Meaning |
|---|---|
| `REFUSED_UNTYPED` | the request or its defect is not typed on the declared carrier |
| `REFUSED_UNGROUNDED_LOCUS` | the locus is not in the declared carrier |
| `ADAPTER_INADEQUATE` | the adapter cannot represent the request |

In-trace reasons carried by M:

| Code | Raised when |
|---|---|
| `REFUSED_INVALID_WITNESS` | the witness is missing or does not verify |
| `REFUSED_BUDGET_EXHAUSTED` | the cost exceeds the remaining budget |
| `REFUSED_NON_ZERO_CURL` | E was requested for a defect not in $\operatorname{im} d_0$ |
| `REFUSED_UNLICENSED_LIFT` | Λ was requested without a licence |
| `REFUSED_LIFT_TRIGGER` | Λ was requested without a Law 4 trigger |
| `REFUSED_MISSING_LOSS_LEDGER` | D was requested without a loss ledger |
| `REFUSED_MISSING_RECEIPT` | I was requested without a receipt |
| `REFUSED_REQUIRES_LIFT` | a closed survivor needs a lift that is not licensed |
| `REFUSED_DETECTOR_INADEQUATE` | the detector cannot certify the diagnostics |
| `REFUSED_OPEN_OBSTRUCTION` | an open obstruction ($\Gamma_2 > 0$) cannot be sealed |

The first draft used both `MissingLossLedger` and SCREAMING_CASE codes, and
listed the ungrounded locus both as an intake refusal and as an M reason. It
is an intake refusal.

## 7.4 Results

**Theorem 7.1** (DDC-M-01). A lawful M leaves the state unchanged and names a
reason, and it moves the control to `Refused`. Lean: `Ddc.M_preserves_state`,
`Ddc.M_refuses`.

**Proposition 7.2** (DDC-M-02). An ungrounded locus is refused at intake and
never enters the tape. Test:
`test_letter_modules.py::test_ungrounded_locus_is_an_intake_refusal_that_never_enters_the_tape`.

**Proposition 7.3** (DDC-M-03). A missing or invalid witness yields
`REFUSED_INVALID_WITNESS`. Test: `test_typed_refusal.py::test_refusal_invalid_witness`.

**Proposition 7.4** (DDC-M-04). A cost above the remaining budget yields
`REFUSED_BUDGET_EXHAUSTED`. Test: `test_typed_refusal.py::test_refusal_budget_exhausted`.

## 7.5 Falsifiers

- An M step without a reason, or with a reason outside the vocabulary, is
  refused (`MissingRefusalReason`).
- An M step that alters the state is refused by paper and historical comparison model.

## 7.6 Nonclaims

```text
M is not a system failure. It is a typed, lawful refusal that preserves state.
No authorization is conferred.
```
