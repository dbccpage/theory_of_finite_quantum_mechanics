# DYN-ALGEBRAIC-HAMILTON

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `CONDITIONAL`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Every Q(i)-linear adjoint-preserving derivation of the full algebra M_d(Q(i)), for positive d, has the form delta(A)=-i\[H,A\] for a Hermitian H, unique modulo a rational scalar identity.

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

- full matrix algebra over Q(i)
- positive dimension
- Leibniz derivation
- adjoint preservation

## Bottleneck

Set S=sum_j delta(E_j1)E_1j. Leibniz on E_ab E_j1 shows \[S,E_ab\]=delta(E_ab). Adjoint preservation makes S+S adjoint central, so replace S by its anti-Hermitian part. H=iS works. The commutant of the full matrix algebra is scalar, and Hermitian scalars in Q(i) are rational. This gives no time parameter or flow. Independent proof review or Lean formalization is still required.

## Source status

Editorial proof sketch awaiting independent replay; no new Lean build.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/11_finite_qm_dynamics/DYNAMICS_HAMILTON_NOETHER.md`

- file: [dag/derivations/11_finite_qm_dynamics/DYNAMICS_HAMILTON_NOETHER.md](../../../dag/derivations/11_finite_qm_dynamics/DYNAMICS_HAMILTON_NOETHER.md)
- sha256 (`lf-normalised`): `7eb3d20a172d523fc33b07123fb3b900d512cdc83e888945874354192fb3dc2e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_2619_dyn_algebraic_hamilton.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_2619_dyn_algebraic_hamilton.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_2619_dyn_algebraic_hamilton.md)
- sha256 (`lf-normalised`): `2a26648fba969c84f390ec78e1c2b1dc038118c49e5f9c2559b63179e0d2add2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2619
- counts toward the grade: no

## Routes

Incoming (1):

- `SCI-R-DYN-ALGEBRAIC-HAMILTON` `DERIVED_PROSE`: [L1-WDP-REALIFICATION-J](L1-WDP-REALIFICATION-J.md) (DEFINITION)

Outgoing (0):

