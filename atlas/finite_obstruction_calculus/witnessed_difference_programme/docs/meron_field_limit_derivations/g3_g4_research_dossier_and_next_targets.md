# Meron field-limit proposals: current status

The historical closure claims for Theorems A and B, G3/G4 and Gate D are
withdrawn. The [retained dossier](../source_archive/superseded_derivations_20261008/g3_g4_dossier.md)
does not supply the required uniform cluster estimates or a joint probabilistic
limit. Its model-generated scorecard is not mathematical evidence.

| Question | Current scope |
| --- | --- |
| G4: covariance and volume limit | The original dossier's claimed closure is withdrawn. Later conditional results have their own explicit hypotheses in the [covariance](../meron_euclidean_covariance_positivity.md) and [thermodynamic-limit](../meron_euclidean_thermodynamic_limit.md) notes. |
| G3: uniform mixed-cumulant control | Unproved in the dossier. The [analyticity note](../meron_time_dependent_analyticity.md) separates the needed uniform bounds from their conditional consequences. |
| Theorem A: continuous-time Gaussian field | Unproved in the dossier. A covariance formula or higher-cumulant estimate alone does not establish a field-valued probability limit. |
| Theorem B: joint discrete volume/time limit | Unproved. Uniform estimates, a covariance limit and probabilistic tightness have not been supplied by the retained argument. |
| Gate D: complex winding sectors | The claimed phase pinning and zero-free region are withdrawn; the required uniform estimates remain unproved. |
| Gate E: finite positivity test | One exact counterexample at $L=4$, $M=1$, $r=1/10$. It establishes failure of positivity for that matrix only. |

The Gate E witness has quadratic form $v^\top Gv=-1/88305$ for the
stated eight-component sign vector. Its [code](code/gate_e_exact_counterexample.py)
does not establish nonpositivity at every finite time discretization, mode
extinction, or a continuum limit.

[Appendix W](../../witnessed_difference_programme.md#appendix-w--accepted-trotter-proofs-and-the-gate-e-boundary)
and the linked notes state the maintained results. The [source errata](../source_errata_20261008.md)
identify the failures in the earlier arguments. The complete reviewed dossier
is preserved byte for byte for comparison, including its superseded equations
and status claims. No new field-limit derivation is included here.
