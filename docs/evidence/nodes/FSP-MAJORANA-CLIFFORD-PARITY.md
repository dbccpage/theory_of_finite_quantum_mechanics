# FSP-MAJORANA-CLIFFORD-PARITY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For N CAR modes, gamma_{2j-1} = c_j + c_j^dagger and gamma_{2j} = -i(c_j - c_j^dagger) are self-adjoint with {gamma_a, gamma_b} = 2 delta_ab, generate the Clifford algebra on 2N generators, and P = prod_j (-i gamma_{2j-1} gamma_{2j}) is the fermion parity (-1)^N_op.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 39
- cited Lean declarations covered by a current replay receipt: 39
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Majorana operator decomposition of CAR modes (standard literature result)
- fermion parity superselection (physical postulate)

## Bottleneck

Standard algebra imported, not derived here; the trunk mechanizes only the two-generator case (DS-QM212-MAJORANA-PROBLEM). Parity superselection is a physical postulate, not a consequence of the algebra. CampaignMajoranaCliffordParity supplies CAR-conditional self-adjointness, anticommutators, equality of generated complex subalgebras, occupation projections, the signed local parity identity and ordered parity action on supplied common occupation eigenvectors. A formal one-mode positive trace-one density matrix need not commute with parity. The all-mode abstract Clifford identification, source CAR/Fock refinement and occupation-basis completeness remain outside these witnesses; no physical superselection law is inferred.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-020 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMajoranaCliffordParity.lean`

- file: [lean4/CampaignMajoranaCliffordParity.lean](../../../lean4/CampaignMajoranaCliffordParity.lean)
- sha256 (`bytes`): `8cfb139d896964ec36adc500b6d2f37fa9894785fb0f85af99333ff745e6028e`
- cited in: node.lean, receipt dag/research/campaign_fsp-majorana-clifford-parity_lean_replay.json (CampaignMajoranaCliffordParity), record TFQ-1186
- replay: `verified`
  - receipt [dag/research/campaign_fsp-majorana-clifford-parity_lean_replay.json](../../../dag/research/campaign_fsp-majorana-clifford-parity_lean_replay.json) (module `CampaignMajoranaCliffordParity`): recorded sha256 `8cfb139d896964ec36adc500b6d2f37fa9894785fb0f85af99333ff745e6028e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/CampaignMajoranaCliffordParity.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignMajoranaCliffordParity.CARFamily.annihilate_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.annihilate_sq` |
| `CampaignMajoranaCliffordParity.CARFamily.dd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.dd` |
| `CampaignMajoranaCliffordParity.CARFamily.gamma_ac` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.gamma_ac` |
| `CampaignMajoranaCliffordParity.CARFamily.gamma_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.gamma_star` |
| `CampaignMajoranaCliffordParity.CARFamily.generated_algebra` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.generated_algebra` |
| `CampaignMajoranaCliffordParity.CARFamily.localParity_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_action` |
| `CampaignMajoranaCliffordParity.CARFamily.localParity_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_pair` |
| `CampaignMajoranaCliffordParity.CARFamily.localParity_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_sq` |
| `CampaignMajoranaCliffordParity.CARFamily.localParity_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.localParity_star` |
| `CampaignMajoranaCliffordParity.CARFamily.mixed_rev` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.mixed_rev` |
| `CampaignMajoranaCliffordParity.CARFamily.occupation_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.occupation_sq` |
| `CampaignMajoranaCliffordParity.CARFamily.occupation_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.occupation_star` |
| `CampaignMajoranaCliffordParity.CARFamily.parity_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.parity_action` |
| `CampaignMajoranaCliffordParity.CARFamily.parity_product` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.parity_product` |
| `CampaignMajoranaCliffordParity.CARFamily.recover_c` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.recover_c` |
| `CampaignMajoranaCliffordParity.CARFamily.recover_star_c` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.CARFamily.recover_star_c` |
| `CampaignMajoranaCliffordParity.ac_add_left` | yes | yes | yes | propext | `#print axioms CampaignMajoranaCliffordParity.ac_add_left` |
| `CampaignMajoranaCliffordParity.ac_add_right` | yes | yes | yes | propext | `#print axioms CampaignMajoranaCliffordParity.ac_add_right` |
| `CampaignMajoranaCliffordParity.ac_comm` | yes | yes | yes | none | `#print axioms CampaignMajoranaCliffordParity.ac_comm` |
| `CampaignMajoranaCliffordParity.ac_smul_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.ac_smul_left` |
| `CampaignMajoranaCliffordParity.ac_smul_right` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.ac_smul_right` |
| `CampaignMajoranaCliffordParity.ac_sub_left` | yes | yes | yes | propext | `#print axioms CampaignMajoranaCliffordParity.ac_sub_left` |
| `CampaignMajoranaCliffordParity.ac_sub_right` | yes | yes | yes | propext | `#print axioms CampaignMajoranaCliffordParity.ac_sub_right` |
| `CampaignMajoranaCliffordParity.gamma_index_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.gamma_index_count` |
| `CampaignMajoranaCliffordParity.oneCAR` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.oneCAR` |
| `CampaignMajoranaCliffordParity.oneRho_gram` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.oneRho_gram` |
| `CampaignMajoranaCliffordParity.oneRho_idempotent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.oneRho_idempotent` |
| `CampaignMajoranaCliffordParity.oneRho_posSemidef` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.oneRho_posSemidef` |
| `CampaignMajoranaCliffordParity.oneRho_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.oneRho_star` |
| `CampaignMajoranaCliffordParity.oneRho_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.oneRho_trace` |
| `CampaignMajoranaCliffordParity.one_parity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.one_parity` |
| `CampaignMajoranaCliffordParity.parity_superselection_not_forced` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajoranaCliffordParity.parity_superselection_not_forced` |
| `gamma_ac` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms gamma_ac` |
| `gamma_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms gamma_star` |
| `generated_algebra` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms generated_algebra` |
| `localParity_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms localParity_pair` |
| `occupation_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms occupation_sq` |
| `parity_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms parity_action` |
| `parity_superselection_not_forced` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms parity_superselection_not_forced` |
- counts toward the grade: yes

### Python: `checks/independent/fsp-majorana-clifford-parity.py`

- file: [checks/independent/fsp-majorana-clifford-parity.py](../../../checks/independent/fsp-majorana-clifford-parity.py)
- sha256 (`bytes`): `67027ee66074805b2029dbc9a85eccd0d62d84daaf3ae304a80d4ee739908264`
- cited in: record TFQ-1186
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md`

- file: [dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md](../../../dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md)
- sha256 (`lf-normalised`): `050a132fdcdfcbc959ca88240ae9b5c2646b14261140da205852442658e5ebb5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1186
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-MAJORANA-CLIFFORD-PARITY` `CONDITIONAL_ON_IMPORT`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)
