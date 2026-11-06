# DYN-CLASSICAL-HAMILTON-NOETHER

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a path-connected with every loop contractible plane domain with omega=dq wedge dp, a C1 area-preserving vector field has a Hamiltonian H with qdot=H_p and pdot=-H_q. For H=p squared/2 the q-translation charge p is conserved.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- oriented state plane
- C1 vector field and local flow
- area preservation
- path-connected with every loop contractible domain

## Bottleneck

Area preservation gives u_q+v_p=0, hence alpha=u dp-v dq is closed. Exactness on the path-connected with every loop contractible domain supplies H. For the specified H, pdot=-H_q=0. Coordinates, regularity, topology and flow are supplied, not derived from the primitive. Independent proof review or Lean formalization is still required.

## Source status

Editorial proof sketch awaiting independent replay; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/11_finite_qm_dynamics/dynamics_hamilton_noether.md`

- file: [dag/derivations/11_finite_qm_dynamics/dynamics_hamilton_noether.md](../../../dag/derivations/11_finite_qm_dynamics/dynamics_hamilton_noether.md)
- sha256 (`lf-normalised`): `7f59f6870f54dead1f7d1bca037c0691d6fd1fd7c927551f1e7bd6fe85820866`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_2618_dyn_classical_hamilton_noether.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_2618_dyn_classical_hamilton_noether.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_2618_dyn_classical_hamilton_noether.md)
- sha256 (`lf-normalised`): `11efa2a368f24e490f998eb0f65047a3fe147c3fd49b652d9d16d1580c1df2fb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2618
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-DYN-CLASSICAL-HAMILTON-NOETHER` `DERIVED_PROSE`: [PG-ROOT-DIFF-STRUCTURE](PG-ROOT-DIFF-STRUCTURE.md) (ADMITTED_PRIMITIVE)

Outgoing (0):

