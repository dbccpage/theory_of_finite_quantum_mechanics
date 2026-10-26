# MUB6-COVER56-CURVATURE-PREMISE

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Certified membership of a point in the stored 56-interval moduli cover is equivalent to geometric membership together with a supplied curvature certificate for its triple.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: stale 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `receipt_not_current`: lean4/TargetA12SmaleSentry.lean: replay stale against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

None recorded.

## Bottleneck

The 56 stored intervals carry a depth label 64 and positive margins but no contractor execution, per-cell boxes, interval Jacobians or cusp collars; the curvature certificate remains a premise of conjecture3_szollosi_deltoid_closure. The legacy 28-cell, 56-cell, 24-leaf cusp and collar receipts are relabelled NOT_A_CERTIFICATE (literal margins) as of 2026-10-21.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-LEDGER-COVER56 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/TargetA12SmaleSentry.lean`

- file: [lean4/TargetA12SmaleSentry.lean](../../../lean4/TargetA12SmaleSentry.lean)
- sha256 (`bytes`): `7158a5c991e22efb8526564e05c1ef14b2ade65a874c82a7cd1d814d45e92ec5`
- cited in: node.lean, record TFQ-1273
- replay: `stale`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `TargetA12SmaleSentry`): recorded sha256 `6a4201c699a5e4a266922d0ab7ee990ac95446af61fc435c31be7c6d7c9d7497` differs from the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build TargetA12SmaleSentry`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `certified_point_in_cover56_iff` | yes | yes | yes | - | `#print axioms certified_point_in_cover56_iff` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1273_mub6_cover56_curvature_premise.md`

- file: [dag/derivations/25_mub/tfq_1273_mub6_cover56_curvature_premise.md](../../../dag/derivations/25_mub/tfq_1273_mub6_cover56_curvature_premise.md)
- sha256 (`lf-normalised`): `fe179c436de6e57f0f13f862f8a83b28d9fff55a6ae2e4176c521b316dfd51f3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1273
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-COVER56-CURVATURE-PREMISE` `DERIVED_LEAN`: [MUB6-SZOLLOSI-TWO-CIRCULANT](MUB6-SZOLLOSI-TWO-CIRCULANT.md) (PROVED_LEAN)

Outgoing (0):

