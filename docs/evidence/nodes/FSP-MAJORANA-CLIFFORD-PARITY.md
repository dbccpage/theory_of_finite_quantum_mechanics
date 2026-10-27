# FSP-MAJORANA-CLIFFORD-PARITY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For N CAR modes, gamma_{2j-1} = c_j + c_j^dagger and gamma_{2j} = -i(c_j - c_j^dagger) are self-adjoint with {gamma_a, gamma_b} = 2 delta_ab, generate the Clifford algebra on 2N generators, and P = prod_j (-i gamma_{2j-1} gamma_{2j}) is the fermion parity (-1)^N_op.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 32
- distinct cited Lean declarations covered by a current replay receipt: 32
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

Standard algebra imported, not derived here; the trunk mechanizes only the two-generator case (DS-QM212-MAJORANA-PROBLEM). Parity superselection is a physical postulate, not a consequence of the algebra. MajoranaCliffordParity supplies CAR-conditional self-adjointness, anticommutators, equality of generated complex subalgebras, occupation projections, the signed local parity identity and ordered parity action on supplied common occupation eigenvectors. A formal one-mode positive trace-one density matrix need not commute with parity. The all-mode abstract Clifford identification, source CAR/Fock refinement and occupation-basis completeness remain outside these witnesses; no physical superselection law is inferred.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-020 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MajoranaCliffordParity.lean`

- file: [lean4/MajoranaCliffordParity.lean](../../../lean4/MajoranaCliffordParity.lean)
- sha256 (`bytes`): `fc18f654b974824154b0f93102d48073b0c6a2b2e2141b94280a4b05b0a69f04`
- cited in: node.lean, receipt dag/research/campaign_fsp-majorana-clifford-parity_lean_replay.json (MajoranaCliffordParity), record TFQ-1186
- replay: `verified`
  - receipt [dag/research/campaign_fsp-majorana-clifford-parity_lean_replay.json](../../../dag/research/campaign_fsp-majorana-clifford-parity_lean_replay.json) (module `MajoranaCliffordParity`): recorded sha256 `fc18f654b974824154b0f93102d48073b0c6a2b2e2141b94280a4b05b0a69f04` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MajoranaCliffordParity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `MajoranaCliffordParity.CARFamily.annihilate_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.annihilate_sq` |
| `MajoranaCliffordParity.CARFamily.dd` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.dd` |
| `MajoranaCliffordParity.CARFamily.gamma_ac` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.gamma_ac` |
| `MajoranaCliffordParity.CARFamily.gamma_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.gamma_star` |
| `MajoranaCliffordParity.CARFamily.generated_algebra` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.generated_algebra` |
| `MajoranaCliffordParity.CARFamily.localParity_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.localParity_action` |
| `MajoranaCliffordParity.CARFamily.localParity_pair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.localParity_pair` |
| `MajoranaCliffordParity.CARFamily.localParity_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.localParity_sq` |
| `MajoranaCliffordParity.CARFamily.localParity_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.localParity_star` |
| `MajoranaCliffordParity.CARFamily.mixed_rev` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.mixed_rev` |
| `MajoranaCliffordParity.CARFamily.occupation_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.occupation_sq` |
| `MajoranaCliffordParity.CARFamily.occupation_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.occupation_star` |
| `MajoranaCliffordParity.CARFamily.parity_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.parity_action` |
| `MajoranaCliffordParity.CARFamily.parity_product` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.parity_product` |
| `MajoranaCliffordParity.CARFamily.recover_c` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.recover_c` |
| `MajoranaCliffordParity.CARFamily.recover_star_c` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.CARFamily.recover_star_c` |
| `MajoranaCliffordParity.ac_add_left` | yes | yes | yes | propext | `#print axioms MajoranaCliffordParity.ac_add_left` |
| `MajoranaCliffordParity.ac_add_right` | yes | yes | yes | propext | `#print axioms MajoranaCliffordParity.ac_add_right` |
| `MajoranaCliffordParity.ac_comm` | yes | yes | yes | none | `#print axioms MajoranaCliffordParity.ac_comm` |
| `MajoranaCliffordParity.ac_smul_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.ac_smul_left` |
| `MajoranaCliffordParity.ac_smul_right` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.ac_smul_right` |
| `MajoranaCliffordParity.ac_sub_left` | yes | yes | yes | propext | `#print axioms MajoranaCliffordParity.ac_sub_left` |
| `MajoranaCliffordParity.ac_sub_right` | yes | yes | yes | propext | `#print axioms MajoranaCliffordParity.ac_sub_right` |
| `MajoranaCliffordParity.gamma_index_count` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.gamma_index_count` |
| `MajoranaCliffordParity.oneCAR` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.oneCAR` |
| `MajoranaCliffordParity.oneRho_gram` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.oneRho_gram` |
| `MajoranaCliffordParity.oneRho_idempotent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.oneRho_idempotent` |
| `MajoranaCliffordParity.oneRho_posSemidef` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.oneRho_posSemidef` |
| `MajoranaCliffordParity.oneRho_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.oneRho_star` |
| `MajoranaCliffordParity.oneRho_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.oneRho_trace` |
| `MajoranaCliffordParity.one_parity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.one_parity` |
| `MajoranaCliffordParity.parity_superselection_not_forced` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms MajoranaCliffordParity.parity_superselection_not_forced` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-majorana-clifford-parity.py`

- file: [checks/independent/fsp-majorana-clifford-parity.py](../../../checks/independent/fsp-majorana-clifford-parity.py)
- sha256 (`bytes`): `67027ee66074805b2029dbc9a85eccd0d62d84daaf3ae304a80d4ee739908264`
- cited in: record TFQ-1186
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md`

- file: [dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md](../../../dag/derivations/26_fsp/tfq_1186_fsp_majorana_clifford_parity.md)
- sha256 (`lf-normalised`): `ba788966796f33334eea2fc8f0de4cb20e187eb3a71d5800b1d3a253402e3135`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1186
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-MAJORANA-CLIFFORD-PARITY` `CONDITIONAL_ON_IMPORT`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)
