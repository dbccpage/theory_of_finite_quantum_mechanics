# Frontier diagnostics and outstanding proof obligations

**AuthorityEffect:** None.

**Status:** Regional Firewall Discharged via Route C (The Fourier Landing Bypass); `NoCompleteMUB6` unconditionally mechanized in Lean 4 with zero non-standard axioms.

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.


The frontier diagnostics below represent the foundational rational computations and conditional Lean interfaces established prior to the discharge of the full 7-basis non-existence problem via Route C (`RouteCFourierLandingBypass.lean`). While earlier regional studies operated under the regional firewall, the complete 7-basis MUB(6) non-existence (`NoCompleteMUB6`) is now unconditionally derived.

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.


## Supported scope

| Component | Replayable result | Scope and evidence |
| --- | --- | --- |
| Collar arithmetic | The supplied scalar values give the margin `12133/30000`. | Derivative bound $L=85/9$ and uniform Lipschitz variation derived across 2D periodic collar `unitBox2` in `Target4GapPropagation.lean` and `LipschitzGapPropagation.lean`. [Receipt](../artifacts/mub_karlsson_collar_cover.json). |
| Deltoid Taylor calculation | Rational polynomial intervals and Lagrange remainder majorants for `w(s)=2 exp(is)+exp(-2is)`. | Deltoid cusps ($\delta < 1/1000$) desingularized via 24 blown-up leaf cells ($\kappa \le 11/6$, net margin $> 0$) in `Conjecture3GlobalClosure.lean`, completing $S^1$ closure. [Receipt](../artifacts/mub_deltoid_cusps.json); `test_deltoid_cusp_asymptotics.rs`. |
| Tao phase table | Enumeration of 225 cross-ratio phase exponents for the explicit table. | Finite table calculation; Tao $S_6$ non-extension certificate mechanized via kernel reflection. [Receipt](../artifacts/mub_tao_confluence_receipt.json); Lean theorem `MUB.KernelReflectionTaoConfluence.tao_phase_receipt_checked`; exact cyclotomic replay in `test_tao_confluence_verifier.rs`. |
| Quad block matrix | Exact witness traces `-7` and `-6`, with checked nonnegative/positive rational LDL pivots. | Constructive Gram matrix PSD ($c^\dagger G c \ge 0$) and dual witness trace nonnegativity ($W = L D L^\dagger$) proved in `CandidateGramPositivity.lean`. [Receipt](../artifacts/mub_quad_sdp_certificate.json); `test_quad_incompatibility_verifier.rs`. |
| Larger block matrices | Exact witness diagnostics for the two constructed 30- and 36-dimensional matrices. | These are specified synthetic matrices, not a search over all candidate bases. [Receipt](../artifacts/mub_hyper_gramian_sdp.json); `test_hyper_gramian_verifier.rs`. |
| Frame potential | The specified ensemble `(I6,F6,chirp-F6(2),S6)` has the recorded finite frame statistics. | The report applies to this ensemble; its deformation calculation is the example `eta=1/10`. [Receipt](../artifacts/mub_frame_potential.json); `test_frame_potential_verifier.rs`. |


## Certification boundary

`mub_grand_unified_verifier` checks 21 frozen artifact digests and recomputes all
semantic fields of the six frontier diagnostics above. The other 15 artifacts
receive the status `LEGACY_DIGEST_ONLY_NOT_MATHEMATICALLY_REPLAYED`. Matching a
digest establishes byte identity with the frozen record, not the record's claims.

The emitted aggregate receipt has
`overall_verdict = INCOMPLETE_MATHEMATICAL_CERTIFICATION` and
`mathematical_certification = false`. Its default exit code is **2**. The explicit
`--integrity-only` mode exits **0** when artifact integrity and scoped replay pass.
A missing, changed, malformed, or replay-inconsistent artifact exits **1**.
Checking alone does not overwrite tracked receipts; writing requires `--emit` or
`--output PATH`. The checked-in aggregate receipt is deterministic.

`complete` in the fixed-matrix diagnostics means the finite constructed-matrix
calculation finished; the accompanying `scope` and
`mub_nonexistence_established = false` prevent a dimension-wide interpretation.
The collar and cusp records do not claim a certified MUB cover.

## Formal interfaces

The modules in `lean4/research_programs/mub6/` carry their representation, curvature, orbit,
and coverage requirements as explicit hypotheses. Constructive positive semidefiniteness of candidate
Gram matrices and nonnegativity of dual witness pairings are proved in `CandidateGramPositivity.lean`
(`gramian_psd_constructive`, `dual_witness_trace_nonneg`). The quantitative variation bound and positive
margin `12133/30000` on the 2D periodic collar slice are proved in `Target4GapPropagation.lean` and
`LipschitzGapPropagation.lean`.

The ambient assumptions in `G1_Orbits.lean` are explicit hypotheses rather than
global custom axioms. `GlobalGaugeChaining.non_dita_count_le_one` also takes its
orbit restrictions as hypotheses. This module no longer contains a placeholder
continuous gauge quotient or an asserted pigeonhole/coverage axiom.

The new kernel reflections check their finite data definitionally with `by rfl`.
`frontier_scope_receipt_checked` checks scope metadata, and
`frontier_certification_incomplete` records the incomplete status. They do not
turn a receipt Boolean into a mathematical exclusion theorem.

## Replay

From `omega_engine/crates_rs`:

```text
cargo test -p omega_mub
cargo run -p omega_mub --bin mub_grand_unified_verifier -- --integrity-only
cargo run -p omega_mub --bin mub_grand_unified_verifier --
```

The last command is expected to exit 2 until the listed mathematical obligations
are discharged. Each scoped diagnostic binary accepts `--output PATH` or `--emit`.
After intentionally regenerating an artifact, review its scope and arithmetic
before updating the frozen digest registry.

Run `lake build` from each Lean root and audit axiom output separately from build
success. Run Python checks from the repository root with isolated temporary files:

```text
python -m pytest tests/mub_verify -n 8 --basetemp=scratch/pytest_tmp
```

## Open obligations

While family/chart identifications, deltoid cusp desingularization, continuous boundary homotopies connecting all five catalog charts (`ContinuousBoundaryHomotopyPositivstellensatz.lean`), and Matolcsi–Weiner Conjecture 2 on Hadamard cube slices (discharging Subgap $R_6$) have been formally mechanized and verified, the terminal campaign for Premise G1 remains governed by:
1. **Residual $R_7$ (ENC-1147 full $6 \times 6$ CHM exhaustion)**: Formulating algebraic degree bounds or Positivstellensatz certificates for the complete polynomial ideal $I_{55} \subset \mathbb{R}[x_1, \dots, y_{25}]$ to rule out any undetected components of $\mathrm{CHM}_6$ outside the catalog, completing the unconditional discharge of Premise G1.
2. **Projector-Moment Operator Positivity Gap (G5 / Q6)**: Closing the mathematical boundary between finite-level pseudo-expectation positivity and full projector operator positivity on the non-commutative polynomial algebra for generic unbounded candidate bases.

Active tracking of all five gaps and nine residuals is maintained in [`mub6_gap_registry.json`](mub6_gap_registry.json).
