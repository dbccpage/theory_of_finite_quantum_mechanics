# PG-GEN-SUPPLY-ERASURE review

SupplyErasure proves supply removal for the source replay. This selected interpreter checks complete guarded final states and failures before and after supply removal, preserving original-history failure indices. Lean separately proves the generic Option-event erasure identity for arbitrary total admission transitions; lifting this to the entire partial source interpreter remains explicit.

Supported: Full guarded replay states agree after supply erasure on the retained histories; generic erasure/filterMap and supply-prefix identities are kernel checked.

Remaining: Prove the partial Option/failure and five-field Regime representation bridge for every source history. Erasure does not erase guard failures, actual admissions or external custody requirements.

Historical source annotations and all stage bytes are preserved. No external provider dispatched. AuthorityEffect: None.
