# FSP-WILSON-DIRAC-GAMMA5

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Wilson-Dirac operator satisfies gamma5 D_W gamma5 = D_W^dagger, so its nonreal eigenvalues come in conjugate pairs and det D_W is real; for two degenerate flavors det(D_W)^2 \>= 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/CampaignFspWilsonDiracGamma5.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- Wilson-Dirac lattice fermion operator with r = 1 (standard lattice QCD)

## Bottleneck

A single-flavor det D_W can be negative; the JSONL claim that det D_W is nonnegative is only the two-flavor square. The gamma5 adjoint, reality of det D_W, and the two-flavor square for this operator are not Lean theorems in this checkout. Euclidean Clifford data in dimensions 2 and 4 are checked in Lean. An exact check on one periodic 2x2 lattice, mass -1, U(1), finds det = -3.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-033 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspWilsonDiracGamma5.lean`

- file: [lean4/CampaignFspWilsonDiracGamma5.lean](../../../lean4/CampaignFspWilsonDiracGamma5.lean)
- sha256 (`bytes`): `1731bf59cd9e9c71586d911c13468c52b817549715edf0cea12ecdefb8246d09`
- cited in: receipt dag/research/campaign_fsp-wilson-dirac-gamma5_lean_replay.json (CampaignFspWilsonDiracGamma5)
- replay: `verified`
  - receipt [dag/research/campaign_fsp-wilson-dirac-gamma5_lean_replay.json](../../../dag/research/campaign_fsp-wilson-dirac-gamma5_lean_replay.json) (module `CampaignFspWilsonDiracGamma5`): recorded sha256 `1731bf59cd9e9c71586d911c13468c52b817549715edf0cea12ecdefb8246d09` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspWilsonDiracGamma5`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspWilsonDiracGamma5.charpoly_rootMultiplicity_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWilsonDiracGamma5.charpoly_rootMultiplicity_conj` |
| `CampaignFspWilsonDiracGamma5.euclideanClifford2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWilsonDiracGamma5.euclideanClifford2` |
| `CampaignFspWilsonDiracGamma5.euclideanClifford4` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWilsonDiracGamma5.euclideanClifford4` |
| `CampaignFspWilsonDiracGamma5.two_flavor_det_eq_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWilsonDiracGamma5.two_flavor_det_eq_sq` |
| `CampaignFspWilsonDiracGamma5.two_flavor_det_real_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignFspWilsonDiracGamma5.two_flavor_det_real_nonneg` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1197_fsp_wilson_dirac_gamma5.md`

- file: [dag/derivations/26_fsp/tfq_1197_fsp_wilson_dirac_gamma5.md](../../../dag/derivations/26_fsp/tfq_1197_fsp_wilson_dirac_gamma5.md)
- sha256 (`lf-normalised`): `2e031a71c1f5b38b75e949e8655e3b09ec2ed452e8c8401cb64a7e38beb0c77d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1197
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-wilson-dirac-gamma5.md`

- file: [dag/derivations/independent/fsp-wilson-dirac-gamma5.md](../../../dag/derivations/independent/fsp-wilson-dirac-gamma5.md)
- sha256 (`lf-normalised`): `9201405d6d55ddd1ffeb4679791dbe9df4c05fe7be3dcb22e2db9ed09640aa96`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-WILSON-DIRAC-GAMMA5` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN), [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (2):

- `APP-R-FSP-LATTICE-ANOMALY-INFLOW` `GAP_NO_DERIVATION`: [FSP-LATTICE-ANOMALY-INFLOW](FSP-LATTICE-ANOMALY-INFLOW.md) (OPEN)
- `APP-R-FSP-SU2-ADJOINT-REAL-DET` `CONDITIONAL_ON_IMPORT`: [FSP-SU2-ADJOINT-REAL-DET](FSP-SU2-ADJOINT-REAL-DET.md) (IMPORTED_ASSUMPTION)
