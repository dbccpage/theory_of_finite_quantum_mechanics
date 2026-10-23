# Independent review of PR #230

AuthorityEffect: None.

Scope: fe60a951520378108828cc27af64950fc8e513dc plus focused checker repairs and missing scored companions. Full 208-line Lean module and checker read. Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM for the continuum target; the node remains OPEN. Merge refused because the substantive proof module is L3D, below L4D (SCORING.md:64-72).

| Claim | Lean declaration | Boundary |
|---|---|---|
| Four-entry residual covariance | unnormalized_covariance, lean4/CampaignDfmElectroweakContinuumFence.lean:117 | Arbitrary Gaussian-rational pairs and doublets |
| A common supplied root remains a root under unit scaling | unit_shares_norm :139, unit_normalized_covariance :145 | Unit norm and root equation are explicit premises |
| Rational unit witness | witness_three_fifths :160 | (3/5)^2+(4/5)^2=1 on the axis doublet |
| Own-root normalization fails for a nonunit | nonunit_normalized_entries_differ :173 | z=2 gives squared norms 1 and 4, and entries 1 and 2 |
| Positive normalizer, unitary/determinant invariant, continuum derivative or electroweak model | Not proved | Remain outside this module |

The identity permits total division at zero and a signed supplied rational root. The note now distinguishes this from a genuine nonzero normalized dressing. The substantive module defines component formulas and local algebraic lemmas, without a verified normalization interface or field/matrix structure integration. That meets the bounded-domain L3 description; support-file exceptions cannot be used for it. No artificial L4 score is assigned.

Actionable repairs: the checker had 62 strict-mypy errors and accepted binary floats/booleans through Fraction; comparison with an unrelated object raised AttributeError. It now has complete signatures, an exact-input guard, a nonzero denominator guard and safe object equality. Six invalid constructor inputs and zero denominator are refused. Existing numeric output is preserved in normal and optimized mode. One actual source mutant replaces complex conjugation by identity; the generic residual identity rejects it in both modes. Three source-bound scored YAML companions were added or updated, preserving historical entries.

Fresh focused Lake build: 842 jobs. Direct Lean: twelve audits, all within propext/Classical.choice/Quot.sound. Exact outputs reproduce the generic sample, 3/5+4/5 i witness, z=2 own-root entries 1 and 2, and shared-denominator equality. Checker maximum CCN 15 and cognitive 14. Proof L3D, bounded regression checker L2D, declarative Lake L1D.

No complete campaign pipeline or hosted-check success is claimed. The full continuum obligation remains open. Independent review receipts are in dag/research/campaign_dfm-electroweak-continuum-fence_review_validation.json; scanner details are recorded separately.
