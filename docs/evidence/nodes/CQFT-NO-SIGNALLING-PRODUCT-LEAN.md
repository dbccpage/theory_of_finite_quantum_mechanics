# CQFT-NO-SIGNALLING-PRODUCT-LEAN

Stage: [CAUSAL_QFT](../stages/CAUSAL_QFT.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> lean4/NoSignallingCore.lean establishes, for natural-number-valued tables of the product form P x y a b = PA x a * PB y b in which each PB y sums to 1 over a listed outcome set, that the marginal on the first party does not depend on the second party's setting (product_noSignalling, marginalA_product), and that the table sig, in which the first outcome equals the second setting, has a setting-dependent marginal, so NoSignallingBA fails (sig_signals). Scope: product tables over the naturals with outcome lists; no quantum states, no commuting local observables, no relation to the posets of CausalOrder.lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The quantum statement that commuting local measurements at spacelike separated points give setting-independent marginals is not stated in this file.

## Source status

Declarations read in this change from the cited Lean file, which is a root in lean4/lakefile.lean; the file was not rebuilt here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/NoSignallingCore.lean`

- file: [lean4/NoSignallingCore.lean](../../../lean4/NoSignallingCore.lean)
- sha256 (`bytes`): `f3fbd4ff4c66675ef44d1ed8e6b6c439f7a7ed93d29df66d038b843573bdaca7`
- cited in: node.lean, record TFQ-2101
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_causal_qft.json](../../../dag/research/lean_replay_campaign_causal_qft.json) (module `NoSignallingCore`): recorded sha256 `f3fbd4ff4c66675ef44d1ed8e6b6c439f7a7ed93d29df66d038b843573bdaca7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build NoSignallingCore`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `marginalA_product` | yes | yes | yes | none | `#print axioms marginalA_product` |
| `product_noSignalling` | yes | yes | yes | none | `#print axioms product_noSignalling` |
| `sig_signals` | yes | yes | yes | none | `#print axioms sig_signals` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/31_causal_qft/tfq_2101_cqft_no_signalling_product_lean.md`

- file: [dag/derivations/31_causal_qft/tfq_2101_cqft_no_signalling_product_lean.md](../../../dag/derivations/31_causal_qft/tfq_2101_cqft_no_signalling_product_lean.md)
- sha256 (`lf-normalised`): `54114917a67498fd8b67912ba2f3a84ca2de294b1cbf0db77af9ff3097930cbe`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2101
- counts toward the grade: no

## Routes

Incoming (1):

- `FRO-R-CQFT-NO-SIGNALLING-PRODUCT-LEAN` `RECORD_PARENT`: [DS-QM074-NO-SIGNALING-MARGINAL](DS-QM074-NO-SIGNALING-MARGINAL.md) (PROVED_LEAN)

Outgoing (0):

