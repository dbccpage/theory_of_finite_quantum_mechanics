
## Supplemental formalization: uncertainty and correction (23 October 2026)

The standalone supplemental build `python tools/replay_projection_bounds.py`
compiles `lean4/ProjectionBounds.lean` with Lean 4.35.0 and replays every named
theorem in `lean4/ProjectionCensus.lean`. The 20-theorem result and exact source
hashes are recorded in `lean4/projection_axiom_census.json`; the text axiom
output is `lean4/projection_axiom_report.txt`. This supplements the existing
census without replacing its historical scope. Dependencies, source pins and
licenses are shipped in `lean4/projection_vendor/`; no sibling paper or network
fetch is needed. Only `propext`, `Quot.sound` and `Classical.choice` are allowed.

| Bound | Lean result | Explicit premise retained |
|---|---|---|
| Robust rate and onset | `lowerRate_le`, `uncertain_onset`, `half_slope_window` | A two-sided rate enclosure and the actual Taylor lower estimate on its horizon |
| Correction deadline | `correction_window_iff`, `zero_rate_window`, `safe_horizon`, `exhausted_budget` | Positive rate for division; a separate zero-rate branch; independently valid budgets and horizon |
| Actual corrected update | `corrected_step`, `accumulated_budget` | A nonexpansive evolution, residual enclosure and correction displacement bound |
| Finite transported jumps | `transported_jump_bound` | The variation-of-constants identity, an integral bound, and contractive transports |
| Product and observed residual uncertainty | `factor_replacement_bound`, `product_residual_uncertainty`, `product_defect_uncertainty`, `observed_residual_bound`, `observed_defect_interval` | A factor-replacement path with each step bounded by the state distance; a declared Lipschitz observation |

The scalar results are over the real numbers. The jump and residual theorems
are over arbitrary normed additive groups, so they apply to a trace-norm
carrier once its physical obligations are proved. In particular, the constant
$k+1$ is derived by telescoping $k$ factor replacements and adding the original
state discrepancy. The finite sum of jump norms is derived from the supplied
transported-jump identity. Lean does not construct the continuous propagator,
prove the density-matrix tensor/partial-trace estimates, or certify numerical
integration in this supplement. Those statements remain written analytic
premises. The new bounds do not turn a supplied error radius into an observed
or statistically justified radius.

Three compiled examples check the exact allowed budget, a strictly excessive
budget, and a rate completely explained by uncertainty. The companion Python
examples test exact arithmetic on supplied budgets; the fresh Lean replay
checks the general implications above.
