# WDP-APPX-REPORT-DOMAIN: Align Calibrated Model Admission and Bounded Raw Report Semantics

**AuthorityEffect**: `None`  
**Status**: `done`  
**Unblocks**: Appendix calibrated recovery contract alignment (`WDP-APPX-REPORT-DOMAIN`)

## 1. Scope & Problem Statement

In `calibrated_recovery/bridge.py`, `propose_cost(model)` and `verify_cost(model, certificate)` compute minimum fixed and adaptive observation budgets over the ideal calibrated interval product (`COST_DOMAIN = "ideal_calibrated_interval_product"`), whereas `evaluate(model, report, proposed_answer)` parses each raw reading via `parse_rational(raw_value)` subject to a 256-bit numerator/denominator cap (`abs(num) <= 2**256`, `1 <= den <= 2**256`).

Under the Review R1 witness (`gain = 1 / 2**255`, `offset = 0`, interval `[2**255, 2**255]`), `validate(model)` admits the model and `verify_cost` certifies `fixed_cost == "1"` and `adaptive_cost == "1"` in `ideal_calibrated_interval_product`. However, the unique raw reading for the high interval cell is:
$$
r = \frac{y - b}{a} = \frac{2^{255} - 0}{2^{-255}} = 2^{510} > 2^{256}
$$
which exceeds the 256-bit parser cap, causing `evaluate(model, report, "high")` to return `status == "INVALID_REPORT"`.

## 2. Scoped Contract Alignment

To align calibrated model admission and bounded raw report semantics without mutating the sealed paper package:
1. **Explicit Ideal Cost Scope**: `COST_DOMAIN = "ideal_calibrated_interval_product"` remains the declared scope of `propose_cost` and `verify_cost`.
2. **Executable Raw-Domain Admission Check (`check_executable_raw_domain`)**: For each channel $c$ with affine map $y = a_c r + b_c$ and each interval cell $[L, U]$, the pre-image interval in raw coordinates is $[r_{\min}, r_{\max}]$ with endpoints $(L - b_c)/a_c$ and $(U - b_c)/a_c$ (swapped when $a_c < 0$). A cell is executable under the 256-bit raw report cap if and only if $[r_{\min}, r_{\max}]$ contains at least one reduced rational $p/q$ with $|p| \le 2^{256}$, $1 \le q \le 2^{256}$, and canonical string length $\le 160$.
3. **Scoped Report Evaluation (`evaluate_scoped`)**: Separates ideal-product cost verification from executable raw-report feasibility, reporting `executable_raw_domain_admissible` alongside the `evaluate` result and surfacing `RAW_CAP_EXCEEDED_IN_MODEL` when an admitted ideal model contains cells unreachable under the 256-bit raw parser cap.
