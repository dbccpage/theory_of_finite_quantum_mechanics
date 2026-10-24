# Stage FINITE_TOPOLOGICAL

Part of the [evidence map](../README.md). AuthorityEffect: None.

Nodes: 9. Grades: E0 2, E1 6, E3 1. Statuses: COMPUTATIONALLY_CHECKED 7, OPEN 2.

| Node | Status | Grade | Statement | Counted in-repo evidence | Flags |
|---|---|---|---|---|---|
| [TFQ-0043](../nodes/TFQ-0043.md) | `COMPUTATIONALLY_CHECKED` | E1 | anyon.rs reads a simple charge from a RibbonFusionCategory: dual, quantum dimension, twist, and an invertibility bit from fusion multipli... | [catalog.rs](../../../code/rust/src/fusion_categories/catalog.rs)<br>[lib.rs](../../../code/rust/src/wdp/lib.rs) | computational_no_runnable_test |
| [TFQ-0044](../nodes/TFQ-0044.md) | `OPEN` | E3 | anyon_model.rs wraps a ribbon category after braided validation and a dimension check. Its SU(2)_k constructor uses the shared Racah gaug... | [CampaignTfq0044FiniteTopological.lean](../../../lean4/CampaignTfq0044FiniteTopological.lean): `qphi_golden_ratio_identities`, `racah_level3_fibonacci_f_matrix_not_euclidean_orthonormal`, `racah_level3_fibonacci_f_matrix_weighted_metric_unitarity` +7<br>[su2_level.rs](../../../code/rust/src/fusion_categories/su2_level.rs)<br>[tfq-0044.py](../../../checks/independent/tfq-0044.py) | - |
| [TFQ-0045](../nodes/TFQ-0045.md) | `COMPUTATIONALLY_CHECKED` | E0 | r_matrix.rs stores an exact exchange on a tensor product or on a fusion space whose dimension need not be a square. try_new refuses a non... | none in this checkout | computational_no_runnable_test |
| [TFQ-0046](../nodes/TFQ-0046.md) | `COMPUTATIONALLY_CHECKED` | E1 | yang_baxter_equation.rs keeps the residual matrix of a braid-form defect or of a spectral defect R12(u-v) R13(u) R23(v), including a mult... | [yang_baxter.rs](../../../code/rust/src/fusion_categories/yang_baxter.rs) | computational_no_runnable_test |
| [TFQ-0047](../nodes/TFQ-0047.md) | `COMPUTATIONALLY_CHECKED` | E1 | modular_tensor_category.rs builds ModularData::verified from an AnyonModel and exposes ground_state_degeneracy at a declared genus. The m... | [modular.rs](../../../code/rust/src/fusion_categories/modular.rs) | computational_no_runnable_test |
| [TFQ-0048](../nodes/TFQ-0048.md) | `COMPUTATIONALLY_CHECKED` | E0 | toric_code.rs builds a rectangular CSS code on periodic_square_complex, with a budget of 256 plaquettes. It computes star and plaquette s... | none in this checkout | computational_no_runnable_test |
| [TFQ-0049](../nodes/TFQ-0049.md) | `COMPUTATIONALLY_CHECKED` | E1 | frobenius_algebra.rs asks both Frobenius identities, units, and counits to replay on matrices over Q(i), with dimension from 1 to 16, and... | [fusion_category.rs](../../../code/rust/src/fusion_categories/fusion_category.rs) | computational_no_runnable_test |
| [TFQ-0050](../nodes/TFQ-0050.md) | `OPEN` | E1 | catalog.rs pins exact ribbon data for Ising, Fibonacci, semion, pointed braided categories, the toric code as D(Z_2), a three-fermion mod... | [catalog.rs](../../../code/rust/src/fusion_categories/catalog.rs)<br>[su2_level.rs](../../../code/rust/src/fusion_categories/su2_level.rs) | - |
| [TFQ-0051](../nodes/TFQ-0051.md) | `COMPUTATIONALLY_CHECKED` | E1 | spin_structure_obstruction.rs lifts a flat rational rotation transport on a declared finite 2-complex to SU(2) matrices, using omega_lie_... | [su2.rs](../../../code/rust/src/lie_theory/su2.rs) | computational_no_runnable_test |

