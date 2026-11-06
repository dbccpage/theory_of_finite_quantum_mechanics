# Claim Ledger for Pure Mathematics, Category Theory & Homological Algebra

**Domain Key:** `mathematics`  
**AuthorityEffect:** `None`  

| coverage_id | operation | disposition | admitted_steps | basis | what_does_not_follow |
| --- | --- | :---: | :---: | --- | --- |
| `cov_mathematics_create_structure` | `create_structure` | `admitted` | `2, 4, 6, 8, 10, 12, 14, 16` | Scaffolds constructive mathematics distinctions and relational complexes. | Does not imply universal empirical truth or unproved continuity. |
| `cov_mathematics_remove_obstruction` | `remove_obstruction` | `admitted` | `3, 5, 7, 9, 11, 13, 15` | Discharges active structural constraints, deadlock, and symmetry ambiguities. | Does not eliminate fundamental recovery gaps or unproved conjectures. |
| `cov_mathematics_simplicial_nilpotency` | `simplicial_boundary_nilpotence` | `admitted` | `1-3, admit_triangle, evaluate_boundary_closure (test_simplicial_complex)` | Exact integer matrix representations $B_1 \in \mathbb{Z}^{n_0 \times n_1}$ and $B_2 \in \mathbb{Z}^{n_1 \times n_2}$, verifying $B_1 B_2 = \mathbf{0}$ with zero floating-point drift across triangles, planar meshes, and tetrahedron shells. | Does not imply continuous differential forms, smooth manifolds, or de Rham cohomology on infinite-dimensional spaces without taking continuous limits. |

## Verification Status
- Scenario Schema: Strictly validated (16 steps with 14-field specification).
- Code Tests: Pytest unit suite passing (15/15 tests passing in 2_mathematics/tests).
- Formal Model: Lean 4 kernel checked under `{propext, Quot.sound}` (`mathematics_core.lean`, `simplicial_complex.lean`, `k_simplex_homology.lean`, `integral_homology_torsion.lean`).
