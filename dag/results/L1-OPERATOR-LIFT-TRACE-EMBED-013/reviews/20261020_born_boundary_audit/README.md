# L1-OPERATOR-LIFT-TRACE-EMBED-013 review

The source trace_norm_eq_mass is an integer-list identity, not a real operator embedding. Build the actual signed diagonal and singular-value list. Normalized absolute weights lose scale and sign; an admitted mass reconstructs absolute magnitudes only, and an incorrect supplied mass fails the original-data comparison. Output layout: status;diag9;singular3;mass;scaled_mass;p3;scaled_p3;mass_tag;reconstructed3;matches_original_magnitudes

Supported: Exact diagonal/singular-value mass, nonzero-scale invariance and declared-mass reconstruction controls; generic absolute scaling and sign-loss statements in Lean.

Remaining: Construct the real Banach/operator embedding and exact signed-data reconstruction contract. Retain sign data separately; probability weights plus mass cannot recover signs.

Historical source annotations and all stage bytes are preserved. No external provider dispatched. AuthorityEffect: None.
