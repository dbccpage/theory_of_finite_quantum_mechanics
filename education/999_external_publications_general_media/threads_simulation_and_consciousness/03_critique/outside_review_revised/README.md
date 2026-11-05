# Holographic brain review

Revised 5 November 2026.

The published model provides separate calculations for emission, holographic reconstruction, capacity and density control. It has not demonstrated a complete biological write–hold–read mechanism. This review identifies concrete equation discrepancies and specifies the tests needed to connect those calculations.

## Read in this order

1. [Main review](holographic_brain_review.md): mathematical findings and their limits.
2. [Research plan](research_plan.md): prioritized tests, further reasoning and naming conventions.
3. [Field constraints and retention](field_constraints_and_retention.md): detailed derivations.
4. [Counterexamples](assumption_counterexamples.md): limits on conclusions drawn from projection, observation and thermal arguments.
5. [Claim register](claim_register.md): assumptions, evidence and unresolved questions.

The [scope analysis](scope_analysis.md), [public replies](public_replies.md) and [variants](public_reply_variants.md) address the discussion separately. The [discussion record](discussion_record.md) preserves the supplied quotations.

## Substantive corrections

- The derivative directions in A88/A89 disagree with A82/A84; direct substitution exposes the mismatch. The resonance threshold after A29/A47 also needs a squared frequency.
- The Appendix A contradiction is retained with its exact scope. Appendix C instead needs a total medium/source charge model; its matter-only Gauss residual is not automatically proof of total charge nonconservation.
- The late density distortion is not treated as observed erasure. A rotational energy is not assumed to be a memory barrier or the simulated mass.
- The 2.5 PB arithmetic survives as an ideal estimate. Screening strength is separated from reconstructed-image amplitude.
- Projection bounds are stated with their finite-dimensional, locality, initial-state and trajectory assumptions. Correlation defects are distinguished from entanglement.
- Gauge transformations are separated from physical phase removal. Report-channel limitations are separated from universal claims about observers or consciousness.

Repeated conclusions and review-round narration have been consolidated. Each retained technical conclusion now states its equations, assumptions or evidentiary limits.

## Verification

Run from this directory:

```bash
python -m pip install -r verification/requirements.txt
python verification/review_checks.py
```

The script exits nonzero on failure. It writes no files unless `--json PATH` is provided. It includes an opt-in `--failure-fixture` switch that must exit nonzero, to check failure reporting.

The [recorded results](verification/test_results.json) identify the executed cases and numerical outputs. These are algebraic checks and finite examples, not a reproduction of Figures 4–6, a proof of the general projection theorem, or a Lean compilation.

Validation on 5 November 2026: all 30 checks passed. The negative-control run returned exit code 1 with exactly its one intentional failure and no other failures or errors.

## Sources

- Nishiyama et al., [published PDF](ijms-25-02399.pdf), [DOI](https://doi.org/10.3390/ijms25042399). The supplied PDF and [Markdown transcription](ijms-25-02399.md) are unchanged. The transcription contains editorial equation notes and figure descriptions; the PDF is authoritative.
- Charles H. Bennett, [Notes on Landauer's Principle, Reversible Computation and Maxwell's Demon](https://arxiv.org/abs/physics/0210005), 2003. Used for the distinction between information removal and reversible copying.
- Jeremy H. Carroll, [Projection Obstruction for Factorized States](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/main/atlas/papers/projection_obstruction/projection_obstruction_paper/projection_obstruction.md), §§5.1 and 5.10. The local reference examined for this revision identifies itself as version 6.9.18; the repository link may advance. The finite checks here do not independently validate the entire monograph.
- The operational definitions used in this review are stated in the [claim register](claim_register.md). They are conventions for this analysis, not empirical results imported from a separate theory.

Source-file SHA-256 values are recorded in [source hashes](verification/source_hashes.json). The public-reply checks count the complete quoted posts, including embedded line breaks.
