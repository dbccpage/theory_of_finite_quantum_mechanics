# Chapter 8 — Letter T: terminalization {#chapter-8}

**Part of:** [Discrete Deformation Calculus v1.0.3](../discrete_deformation_calculus.md)

A recursive evaluation needs a halting law that prevents infinite expansion
and self-certification. T closes a tape on a routing terminal when the
declared terminal policy allows it, subject to the sealing conditions below.

## 8.1 Definition

`CanContinue_n` is the conjunction of the nine conjuncts named by the historical comparison model
(`omega_discrete_deformation_calculus::oeprmalg2::CONTINUATION_CONJUNCTS`):

1. an outstanding obligation exists;
2. a higher obligation witness exceeds it;
3. the next carrier is declared;
4. the adapter is sound (its loss ledger is booked);
5. the detector is adequate;
6. any lift is minimal and licensed;
7. the old skeleton is preserved;
8. budget is available;
9. no GTLA continuation refusal was issued.

The first draft's three-condition form (positive budget, unresolved residual,
strict progress) is a weakening. It is conjuncts 8 and 1, plus the progress
guard of spine Theorem 11.6.

## 8.2 Step law

T leaves the state unchanged, requires $\Gamma_2 = 0$, and requires an
adequate detector. The historical comparison model checks the unchanged state and $\Gamma_2 = 0$
(`TerminalizedOpenResidual`); the detector clause is paper-only (residual
R-DDC-05). After T nothing is admitted.

## 8.3 Verdicts

The abstract Lean T law does not include `CanContinue_n`; its theorem
concerns only the conjunction itself. `TerminalizationEvaluator.evaluate`
accepts optional `continuation_facts`. After the open/blind-state guards, if all nine hold it returns
`CAN_CONTINUE`; if one fails, an open or blind state still cannot seal, and
a closed positive residual receives `HALTED_CONTINUATION_POLICY`. These
booleans are supplied assumptions, not independently verified facts.

Without `continuation_facts`, the separate residual/budget/lookback policy
returns one of the following. Its simple-policy tests do not establish
the nine-fact policy for a deployed system:

| Verdict | When | Routing |
|---|---|---|
| `SEAL_REFUSED_OPEN_OBSTRUCTION` | $\Gamma_2 > 0$ | not terminal; the tape ends in M |
| `SEAL_REFUSED_DETECTOR_INADEQUATE` | blind detector | not terminal; the tape ends in M |
| `LOCAL_GREEN_FOR_SCOPE` | zero residual | `CheckPassed` inside the declared scope |
| `HALTED_OUT_OF_BUDGET` | closed residual, budget spent | residual terminal |
| `HALTED_STAGNANT_PROGRESS` | no progress over the lookback window | residual terminal |

Every receipt records `authority_terminal = "F_term:REFUSED"`. A local green
licenses nothing: refusal on the authorization axis is an explicit package
policy, not an inferred external theorem. The first draft emitted a terminal verdict for an out-of-budget
open obstruction; that verdict now routes to M (`REFUSED_OPEN_OBSTRUCTION`).

## 8.4 Results

**Proposition 8.1** (DDC-T-01). If every charged step costs at least
$\varepsilon > 0$ from an initial budget $B_0$, at most
$\lfloor B_0 / \varepsilon \rfloor$ charged steps occur. This is a conditional
theorem with a one-line proof: the budget is non-negative and falls by
$\varepsilon$ per step.

**Proposition 8.2** (DDC-T-02). Under the simple policy, a zero residual with $\Gamma_2 = 0$ and an
adequate detector yields `LOCAL_GREEN_FOR_SCOPE` and records the unlicensed
authority terminal.
Tests: `test_terminalization.py::test_terminal_local_green`,
`test_letter_modules.py::test_terminal_evaluator_refuses_to_seal_open_or_blind_states`.

**Proposition 8.3** (DDC-T-03). A non-decreasing residual over the lookback
window halts with `HALTED_STAGNANT_PROGRESS`. Test:
`test_terminalization.py::test_terminal_stagnant_progress`.

**Theorem 8.4** (DDC-T-04). T seals: the control becomes `Terminalized` and
admits nothing. Lean: `Ddc.T_seals`, `Ddc.terminal_absorbing`.

**Theorem 8.5** (DDC-T-05). A lawful T leaves the state unchanged, has
$\Gamma_2 = 0$ and an adequate detector, and lands on the exact or the closed
class. Lean: `Ddc.T_never_seals_open`, `Ddc.T_routing`.

**Theorem 8.6** (DDC-T-06). `CanContinue_n` holds exactly when all nine
conjuncts hold, and each conjunct is a strict boolean, never an integer. Lean:
`Ddc.canContinue_iff`; test:
`test_letter_modules.py::test_can_continue_is_the_conjunction_of_the_nine_named_conjuncts`.

## 8.5 Falsifiers

- Demo 2 appends `T` to an open refusal: refused (`TerminalizedOpenResidual`).
- Demo 4 appends `T` under a blind detector: refused (`BlindDetector`).

## 8.6 Nonclaims

T does not mint global authority and never emits an unscoped green verdict.
A terminal receipt records a conditional terminal-policy decision. No
authorization is conferred.
