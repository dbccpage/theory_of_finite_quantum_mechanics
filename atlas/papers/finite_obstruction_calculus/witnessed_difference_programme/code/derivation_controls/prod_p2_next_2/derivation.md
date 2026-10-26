# PROD-P2-NEXT-2

Goal id: PROD-P2-NEXT-2

Selected scope for PROD-P2-NEXT-2 is recorded in this note.

## Selected scope

Exhaustive single-step negative-control fixture matrix (`PROD-P2-NEXT-2`) for P2 `WdpOutputGate` (`omega_engine_applications/wdp_products/p2_output_gate/adapter.py` and `omega_engine_applications/tests/test_p1_p2_adapters.py`): for each of the twelve `G5Step` values (`G.5.1` through `G.5.12`), `mutate_for_g5_step(step)` constructs a candidate/policy fixture whose `WdpOutputGate.check` report fails exclusively that single step (`tuple(f.step for f in report.failures) == (step,)`).

## Hypotheses

H1. WDP Appendix G.5 specifies twelve independent verification steps (`G5Step.G5_1` through `G5Step.G5_12`) evaluated by `WdpOutputGate.check`.

H2. If two steps are coupled or shadowed, a single-step fault fixture would either pass silently or trigger collateral step failures, preventing localized fault diagnosis.

H3. Every step $s \in \{\text{G.5.1}, \dots, \text{G.5.12}\}$ admits a dedicated perturbation fixture $F_s$ such that `WdpOutputGate.check(F_s)` returns `admitted=False` and `failures` containing solely `StepFailure(step=s, ...)`.

## Derivation

1. **Baseline admission**:
   - `default_valid_candidate_and_policy()` satisfies all twelve steps (`report.admitted is True`, `report.failures == ()`).

2. **Twelve orthogonal single-step failure fixtures**:
   - Iterating over `step in G5Step`, `cand, pol = mutate_for_g5_step(step)` perturbs only the invariant checked at `step`.
   - Evaluating `report = WdpOutputGate().check(cand, pol)` yields `report.admitted is False` and `[f.step for f in report.failures] == [step]` for all twelve steps (`G.5.1`..`G.5.12`).

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim that multi-fault inputs cannot fail multiple G.5 steps simultaneously.
