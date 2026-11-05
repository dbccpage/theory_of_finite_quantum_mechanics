# PROD-P3-NEXT-2

Goal id: PROD-P3-NEXT-2

Selected scope for PROD-P3-NEXT-2 is recorded in this note.

## Selected scope

Verification (`PROD-P3-NEXT-2`) of the WDP Appendix Q.4 worked break-even example (`13` hits required for strict positive benefit) via `q4_worked_example_ledger` and `WdpGuardTransferChecker.price` (`omega_engine_applications/wdp_products/p3_guard_transfer/adapter.py` and `omega_engine_applications/tests/test_p3_p5_adapters.py`).

## Hypotheses

H1. On a declared target workload with $N$ candidate occurrences, $h$ early rejections, full verifier cost $v$, guard evaluation cost $g$, and one-time setup cost $C_0$, the exact saving is $\operatorname{saving}(h) = h v - N g - C_0$ (`BreakEven.saving()`, `antibody_transfer.checker.cost`, `GEN-WDP-48`).

H2. In the Appendix Q.4 worked example ($N = 10000$, $v = 1$, $g = 1/1000$, $C_0 = 2$), total overhead is $N g + C_0 = 10 + 2 = 12$.

H3. Strict positive benefit ($\operatorname{saving}(h) > 0$) holds for integer hit counts $h$ if and only if $h \ge 13$.

## Derivation

1. **Exact boundary at $h = 12$**:
   - `q4_worked_example_ledger(hits=12)` gives $\operatorname{saving}(12) = 12 \cdot 1 - 10000 \cdot (1/1000) - 2 = 0$ and `strict_benefit() is False`.

2. **Minimal integer strict benefit at $h = 13$**:
   - `q4_worked_example_ledger(hits=13)` gives $\operatorname{saving}(13) = 13 \cdot 1 - 10 - 2 = 1 > 0$ and `strict_benefit() is True`.
   - `WdpGuardTransferChecker().price(rule, q4_worked_example_ledger(hits=13))` equals `Fraction(1)`, matching `antibody_transfer.checker.cost`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim that Q.4's conditional formula on declared counts is an empirical hit-rate measurement.
