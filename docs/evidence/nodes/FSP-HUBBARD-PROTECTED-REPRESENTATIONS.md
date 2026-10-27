# FSP-HUBBARD-PROTECTED-REPRESENTATIONS

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the Trotter auxiliary-field Hubbard determinants, the spin-determinant product d_up d_down is nonnegative under the stated pairing relations (half-filled bipartite: d_down = d_up/det P_up with det P_up \> 0; attractive spin-balanced: equal spin determinants with a nonnegative field prefactor), and two exact fields, mask 15721 on the four-site ring at z=2 and mask 1281 on the triangle at z=1, have d_up \> 0 \> d_down, so the product is not nonnegative for every field.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- stated Hubbard model and protected symmetry hypotheses

## Bottleneck

Not stated in Lean: (1) that the half-filled bipartite relation d_down = d_up/det P_up with det P_up \> 0 and the attractive spin-balanced relation d_up = d_down follow from the Trotter transfer matrices, since the Lean theorems take the first as a hypothesis and the second as the form C d^2; (2) that the stored rational pairs for masks 15721 and 1281 are det(I+P_sigma) of the ring and triangle matrices; (3) any statement that positivity fails on all or generic fields outside the protections. Lean states the arithmetic consequences and the sign of two stored products. The pairing relations are checked exactly only on 256 ring fields and 64 triangle fields at two slices, and the two witnesses by checks/independent/fsp-hubbard-protected-representations.py.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FermionSignHubbardProtected.lean`

- file: [lean4/FermionSignHubbardProtected.lean](../../../lean4/FermionSignHubbardProtected.lean)
- sha256 (`bytes`): `365483617d0e2261ff3450ab9e5a891e0c51a8bc2ee69bfecbb702d00544f2e9`
- cited in: node.lean, receipt dag/research/campaign_fsp-hubbard-protected-representations_lean_replay.json (FermionSignHubbardProtected)
- replay: `verified`
  - receipt [dag/research/campaign_fsp-hubbard-protected-representations_lean_replay.json](../../../dag/research/campaign_fsp-hubbard-protected-representations_lean_replay.json) (module `FermionSignHubbardProtected`): recorded sha256 `365483617d0e2261ff3450ab9e5a891e0c51a8bc2ee69bfecbb702d00544f2e9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignHubbardProtected`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FermionSignHubbardProtected.attractive_pairing_sq_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.attractive_pairing_sq_nonneg` |
| `FermionSignHubbardProtected.attractive_weight_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.attractive_weight_nonneg` |
| `FermionSignHubbardProtected.attractive_weight_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.attractive_weight_pos` |
| `FermionSignHubbardProtected.half_filled_bipartite_weight_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.half_filled_bipartite_weight_eq` |
| `FermionSignHubbardProtected.half_filled_bipartite_weight_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.half_filled_bipartite_weight_nonneg` |
| `FermionSignHubbardProtected.half_filled_bipartite_weight_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.half_filled_bipartite_weight_pos` |
| `FermionSignHubbardProtected.hubbard_determinant_positivity_is_restricted` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.hubbard_determinant_positivity_is_restricted` |
| `FermionSignHubbardProtected.not_unconditional_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.not_unconditional_positivity` |
| `FermionSignHubbardProtected.opposite_signs_weight_neg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.opposite_signs_weight_neg` |
| `FermionSignHubbardProtected.witness_doped_ring_d_down_neg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.witness_doped_ring_d_down_neg` |
| `FermionSignHubbardProtected.witness_doped_ring_d_up_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.witness_doped_ring_d_up_pos` |
| `FermionSignHubbardProtected.witness_doped_ring_weight_neg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.witness_doped_ring_weight_neg` |
| `FermionSignHubbardProtected.witness_triangle_d_down_neg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.witness_triangle_d_down_neg` |
| `FermionSignHubbardProtected.witness_triangle_d_up_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.witness_triangle_d_up_pos` |
| `FermionSignHubbardProtected.witness_triangle_weight_neg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FermionSignHubbardProtected.witness_triangle_weight_neg` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_0408_fsp_hubbard_protected_representations.md`

- file: [dag/derivations/26_fsp/tfq_0408_fsp_hubbard_protected_representations.md](../../../dag/derivations/26_fsp/tfq_0408_fsp_hubbard_protected_representations.md)
- sha256 (`lf-normalised`): `9a23cc13f78442d23b4852e3edb6c06ceb20dc6a9699025192a1cf57d0b1968c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0408
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-hubbard-protected-representations.md`

- file: [dag/derivations/independent/fsp-hubbard-protected-representations.md](../../../dag/derivations/independent/fsp-hubbard-protected-representations.md)
- sha256 (`lf-normalised`): `063cc88f2b49307f6e58edd7951eaffb0018b811f334c3b4ee113d6ccf5ae969`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/README.md`

- file: [papers/core/fsp/README.md](../../../papers/core/fsp/README.md)
- sha256 (`lf-normalised`): `49bf9e23ec5b96cfd3fbd8bfff74f2a03d0151e20c497589d4233136dc24ca5b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/docs/sql_meron_hubbard.md`

- file: [papers/core/fsp/docs/sql_meron_hubbard.md](../../../papers/core/fsp/docs/sql_meron_hubbard.md)
- sha256 (`lf-normalised`): `88c5febb35077085c1e428eb5a75dc2d85357afd66bc2faff916abd8bf1a74de`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-HUBBARD-PROTECTED-REPRESENTATIONS` `CONDITIONAL_ON_IMPORT`: [FSP-SWITCHING-NORMAL-FORM](FSP-SWITCHING-NORMAL-FORM.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-FSP-EFFICIENT-SAMPLING-OBLIGATIONS` `GAP_NO_DERIVATION`: [FSP-EFFICIENT-SAMPLING-OBLIGATIONS](FSP-EFFICIENT-SAMPLING-OBLIGATIONS.md) (OPEN)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-U1-WILSON-ACTION` `DERIVED_LEAN`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN)
