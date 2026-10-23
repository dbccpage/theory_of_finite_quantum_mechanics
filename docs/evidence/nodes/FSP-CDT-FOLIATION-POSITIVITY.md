# FSP-CDT-FOLIATION-POSITIVITY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a global proper-time foliation in CDT forbids spatial branching, removes Lorentzian cancellations, yields a sign-free positive transfer matrix and a 4D de Sitter universe; the de Sitter phase is numerical literature and the checkout has no transfer-matrix or positivity computation.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Positivity in CDT uses a Wick rotation of a declared action; derive it for a declared finite model and keep numerical phase results as external evidence.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-051 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/fsp/cdt_fermion_sign_evaluator.py`

- file: [code/python/src/fsp/cdt_fermion_sign_evaluator.py](../../../code/python/src/fsp/cdt_fermion_sign_evaluator.py)
- sha256 (`bytes`): `bb756d8f519cff0f0929436f4166acf65886d4d78024887cdaec3dafe64f4e8e`
- cited in: record TFQ-1215

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CdtFermionSignEvaluator` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1215_fsp_cdt_foliation_positivity.md`

- file: [dag/derivations/26_fsp/tfq_1215_fsp_cdt_foliation_positivity.md](../../../dag/derivations/26_fsp/tfq_1215_fsp_cdt_foliation_positivity.md)
- sha256 (`lf-normalised`): `3bedbbf68e6a1eca021c32d444d7583f2ba5fddca1a7f3ff54d3b9dc60d12a4a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1215
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-DISCRETE-WDW-CONSTRAINT](FSP-DISCRETE-WDW-CONSTRAINT.md) (OPEN), [FSP-PACHNER-INVARIANCE-CLAIM](FSP-PACHNER-INVARIANCE-CLAIM.md) (OPEN)

Outgoing (1):

- `APP-R-FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` `GAP_NO_DERIVATION`: [FSP-DIRAC-KAHLER-SPINFOAM-CLAIM](FSP-DIRAC-KAHLER-SPINFOAM-CLAIM.md) (OPEN)
