# Finite lattice gauge theory: Yang–Mills and QCD targets

AuthorityEffect: None. This stage overview replaces the historical Atlas draft. It records finite targets and their evidence limits; it is not a proof of continuum QCD or the Yang–Mills mass gap. Audited statuses and obligations live in [the DAG JSON](../../derivation_dag.json).

## Placement and coverage

Keep this overview in `17_finite_qcd`. Its six targets already have DAG nodes and TFQ records; the finite-group surface-counting target belongs to the adjacent `14_finite_gauge` stage. There is no need for a second set of derivation nodes. The draft's speculative analogy section and repeated announcement discussion have been removed.

| Target | Record and current status | What remains |
| --- | --- | --- |
| `FQCD-FINITE-TRANSFER-MATRIX-GAP` | [TFQ-1049](tfq_1049_fqcd_finite_transfer_matrix_gap.md), OPEN | Construct the finite Wilson transfer matrix, establish positivity and gauge equivariance, and apply Perron–Frobenius on the physical sector. Handle a zero subleading spectral radius and a one-dimensional sector explicitly. |
| `FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY` | [TFQ-1050](tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.md), OPEN | Connect the checked four-component rational matrix construction and its backward-adjointness assumption to the stated general periodic-lattice operator. |
| `FGAUGE-MEDNYKH-2D-YANG-MILLS` | [TFQ-1051](../14_finite_gauge/tfq_1051_fgauge_mednykh_2d_yang_mills.md), OPEN | Derive the character formula for general finite groups and prove cellulation independence; numerical Euler/genus identities are insufficient. |
| `FQCD-STRONG-COUPLING-AREA-LAW` | [TFQ-1052](tfq_1052_fqcd_strong_coupling_area_law.md), CONDITIONAL | Construct the actual finite Wilson measure and derive the cluster bounds supplied as fields of the Lean expectation structures. Specify and justify the non-screening regime. |
| `FQCD-FINITE-GROUP-FREEZING-FENCE` | [TFQ-1053](tfq_1053_fqcd_finite_group_freezing_fence.md), SOURCE_RECORD | External numerical evidence limits extrapolation from fixed finite subgroups; it is not a theorem about every finite group. |
| `FQCD-CONTINUUM-EXISTENCE-ANNOUNCEMENT` | [TFQ-1054](tfq_1054_fqcd_continuum_existence_announcement.md), SOURCE_RECORD | Evaluate a released derivation and its assumptions before importing any result. An announcement changes no local proof status. |

## Finite model and evidence limits

A finite gauge model assigns an element of a finite group to each oriented edge, with inverse elements on reversed edges. Vertex gauge transformations act on edge endpoints. Products around loops transform by conjugation, so their characters are gauge invariant. A finite lattice and finite group give a finite configuration space; sums and matrix identities can be checked exactly when their coefficients are exact. Real exponential Wilson weights require their own analytic treatment.

Choosing a spanning tree supplies useful finite dressing coordinates and residual root conjugation. The [Dressing Field Method dossier](../24_dressing_field/ravera_dfm_dossier.md) and its audited records separate those constructions from continuum gauge fixing, Gribov claims, renormalization and gravity. Neither a tree coordinate change nor a finite determinant identity constructs continuum QCD.

The transfer-matrix target concerns finite volume. After constructing a positive, gauge-equivariant matrix with Perron eigenvalue `lambda_0 > 0`, define `q` as the largest modulus of a non-Perron eigenvalue in the physical sector divided by `lambda_0`, taking `q = 0` if that sector has no non-Perron eigenvalues. The target is `q < 1`. The finite real logarithmic gap `-log q` is defined only for `q > 0`; `q = 0` corresponds to an infinite spectral decay rate, not division by zero. A correlation-decay theorem also needs the relevant self-adjointness or operator estimates. None of this gives a bound uniform in volume or lattice spacing.

The current [strong-coupling Lean module](../../../lean4/FQCD/StrongCouplingAreaLaw.lean) establishes consequences of declared structures:

- `abelian_strong_coupling_area_law` uses `AbelianWilsonExpectation.cluster_expansion_bound`. That field is a premise, not a derived property of a constructed lattice measure.
- `center_protected_3d_strong_coupling_area_law` uses `NonAbelianWilsonExpectation.center_protected_bound` and the supplied spanning-minimality hypothesis. A vanishing cubic character sum alone does not establish those premises.
- `finite_group_2d_character_decimation_area_law` unfolds `exact2DDecimationValue`; it does not identify that definition with an integrated Wilson expectation on a general periodic lattice.

The useful next step is therefore a measure-to-bound construction: define the finite configuration sum and normalization, derive its character expansion with the chosen boundary conditions, prove the required convergence and spanning estimates, and then instantiate the existing bound lemmas. The current general statement must be restricted to a justified non-screening regime; arbitrary representations in higher dimensions can screen.

For a closed orientable surface of genus `g`, the separate Mednykh target is

`|Hom(pi_1(Sigma_g), G)| / |G| = sum_R (|G| / dim R)^(2g - 2)`.

The left side is a groupoid-weighted count, not the unweighted number of gauge orbits. Its derivation needs finite-group representation theory and a cellulation argument. The DAG keeps that obligation open.

The existing finite color factors, Wilson-loop formulas, fermion determinant examples and sign-problem records remain scoped to their definitions and witnesses. Gamma5 hermiticity can imply a real determinant under the stated operator assumptions; it does not by itself imply positivity of every one-flavor determinant or solve the finite-density sign problem. Spin and anomaly examples likewise do not supply the missing continuum, chirality or renormalization arguments.

## Continuum boundary and external sources

Passing to a continuum theory requires a specified sequence of lattices and gauge models, scale control, limiting correlation functions, and the required reconstruction and spectral properties. Finiteness alone supplies none of those uniform estimates. A fixed finite-group model cannot be identified with `SU(3)` by relabeling its elements or matching a few color coefficients.

The [OpenAI announcement of October 26, 2026](https://openai.com/index/building-scientific-understanding-with-academic-communities/) describes work on four-dimensional Yang–Mills/QCD existence and a Lean formalization effort. The page also says the physics artifacts await collaborators' write-up. It is the source for TFQ-1054, not an imported proof or a resolution of the mass-gap problem.

The following references are retained from the earlier draft as research leads; their bibliographic details and hypotheses have not been re-audited here. Before treating an external theorem as a premise, record its exact hypotheses and how the finite construction satisfies them.

## Retained research references

- M. Creutz, Phys. Rev. D 15 (1977) 1128 (lattice gauge fixing and transfer matrices).
- K. G. Wilson, Phys. Rev. D 10 (1974) 2445.
- K. Osterwalder, E. Seiler, Ann. Phys. 110 (1978) 440.
- A. D. Mednykh, Soviet Math. Dokl. 19 (1978) 318.
- A. A. Migdal, Sov. Phys. JETP 42 (1975) 413.
- E. Witten, Commun. Math. Phys. 141 (1991) 153.
- D. Petcher, D. H. Weingarten, Phys. Rev. D 22 (1980) 2465.
- G. Bhanot, C. Rebbi, Phys. Rev. D 24 (1981) 3319.
- P. H. Ginsparg, K. G. Wilson, Phys. Rev. D 25 (1982) 2649.
- M. Luescher, Phys. Lett. B 428 (1998) 342.
- M. Troyer, U.-J. Wiese, Phys. Rev. Lett. 94 (2005) 170201.
- A. Jaffe, E. Witten, Quantum Yang-Mills theory, Clay Mathematics Institute problem description (2000).
