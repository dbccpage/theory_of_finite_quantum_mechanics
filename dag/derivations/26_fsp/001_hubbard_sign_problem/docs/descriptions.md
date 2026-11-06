# Component Descriptions for the Fermi-Hubbard Sign Problem Package

AuthorityEffect: None.

## Core Modules

### `code/hubbard_exact_model.py`
High-level programmatic harness for exact Fermi-Hubbard model evaluation. Provides entry points for:
- Direct Fock state occupation Hamiltonian construction with canonical anticommutation relations (CAR).
- Diagonal sign-gauge obstruction detection via signed double cover reachability in SQLite.
- Shortest negative configuration cycle extraction in integer Fock occupation masks.
- Auxiliary-field determinant expansion with Suzuki palindromic kinetic product $T$.
- Exact verification of particle-hole symmetry $\eta T \eta = T^{-1}$ and $\det(I+P_\downarrow) = \det(I+P_\uparrow) / \det P_\uparrow$.
- Dual-number logarithmic fugacity derivative calculation of total particle number without singular matrix division.
- Explicit negative field witness extraction for doped rings and frustrated triangles.

### `code/hubbard_schema.sql`
Relational schema and SQL views defining exact Hubbard evaluation tables:
- `hubbard_basis`, `hubbard_hamiltonian`: Fock basis and matrix elements.
- `dq_parameter`, `dq_kinetic`, `dq_product`, `dq_determinant`: Auxiliary-field propagation and permutation-fold determinants.
- `dq_weight`: Up and down determinant product with optional field-dependent attractive scalar.
- `dq_number`: Logarithmic fugacity derivative tracking particle number expectations.

### `code/tests/test_hubbard_paper_reproducibility.py`
Automated test suite verifying 100% of the mathematical tables, symmetries, and negative field witnesses reported in `paper.md`.
