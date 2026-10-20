# [TFQ-0408] Protected Hubbard representations and negative witnesses

**Stage:** `FERMION_SIGN` | **Status:** `CONDITIONAL` | **AuthorityEffect:** None.

**Parent:** [TFQ-0406](../26_fsp/tfq_0406_fsp_switching_normal_form.md)
**DAG node:** `FSP-HUBBARD-PROTECTED-REPRESENTATIONS`
**Required DAG inputs:** `FSP-SWITCHING-NORMAL-FORM`

## Statement and derivation

The package distinguishes protected half-filled bipartite and attractive
spin-balanced determinant representations from fields outside those assumptions.
For each proposed extension, specify the Hamiltonian, auxiliary-field transform,
time discretization, spin symmetry and boundary conditions. Derive equality with
the original finite partition function and then the determinant pairing that
makes each weight nonnegative.

Reconstruct small cases independently in full Fock space. Keep negative fields
outside the protection as countermodels. A site-tree geometry alone does not
remove exchange cycles in configuration space. This branch records a conditional
target with exact package controls, not a general Hubbard sign theorem.

## Evidence and next obligation

- [papers/core/fsp/README.md](../../../papers/core/fsp/README.md)
- [papers/core/fsp/docs/sql_meron_hubbard.md](../../../papers/core/fsp/docs/sql_meron_hubbard.md)

Prove the required determinant pairing and Hamiltonian-to-representation equality for each stated model, including boundary cases.
