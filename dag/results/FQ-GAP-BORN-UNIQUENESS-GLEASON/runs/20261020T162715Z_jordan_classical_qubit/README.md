# Concrete classical and qubit catalogue — staged review checkpoint

Status: **constructed, compiled and stopped for review**. AuthorityEffect: None.

- [Classical simplex family](ClassicalModel.lean): an actual compact convex System in every affine dimension n>=0, with n+1 perfectly distinguishable vertices, proved capacity/dimension calibration, exact probability chart and spectral decomposition.
- [Qubit ball model](QubitModel.lean): an actual rank-two, dimension-four System; pure sphere; explicit antipodal effects and spectral mixtures. Its capacity bound follows from the [general central-symmetry argument](CatalogueGeometry.lean).
- [Concrete real Jordan products](ConcreteJordanProducts.lean) and [exact square cones](JordanConeSquares.lean): classical and spin products satisfy the displayed bilinear, unit, commutative and Jordan identities. Their declared positive cones equal their Jordan-square cones.
- [Supported catalogue](SupportedJordanCatalogue.lean): calibrated entries for every classical arithmetic tag and both singleton qubit spellings. Unsupported families have no default. The global extension function still requires every remaining entry as an argument.
- [Concrete applications](CatalogueApplications.lean): the state models match normalized Jordan squares, and the new qubit model instantiates the earlier classical-composite exclusion theorem.
- [Eight collected stage ledgers](stage_index.json), [12 scoped operation records](operad_delta.json), [128 exact exported types](verification/exported_signatures.json), and [112 axiom receipts](verification/kernel_axioms.json).
- [Validation](validation.json), [failed/superseded attempt index](verification/attempt_index.json), [mutation controls](verification/mutation_controls.json), [dependency pins](verification/dependency_packages.json), [preserved prior evidence](provenance.json), and [file seal](manifest.json).
- [Mathematical review and boundaries](review.md), [claim statuses](claim_status.json), and [next derivations](next_steps.md).

Eleven accepted source compilations include three unchanged foundations, seven construction/application modules, and a type export. There are **65 new checked declarations** and 47 rechecked foundation declarations; all printed receipts contain only standard Lean logical axioms or none. The **19 arithmetic receipts and original arithmetic source bytes are preserved**. Five custody/scope mutations were rejected under optimized Python. All 1,015 earlier sealed entries across 23 manifests were reverified.

**Review boundaries:** the classical affine basis is a noncomputable coordinate choice from a proved existence theorem. Real scalars, Euclidean topology and full affine effects remain declared foundations. The qubit construction is the real spin/Bloch model; identifying it with complex Hermitian matrices is still open. Strong symmetry, bundled Euclidean Jordan instances, unsupported catalogue families, the classification bridge, tensor compatibility and full process equivalence are not claimed. A complete higher-arity operad is not constructed. See the exact premises in the operation records.

The pinned Lean 4.33.1 compiler and existing Mathlib cache were used. Local modules were rebuilt from frozen source snapshots; Mathlib itself was not rebuilt. Each successful receipt saves compiler/dependency hashes, exact arguments, stdout/stderr and compiled bytes. Earlier failed attempts remain separate from accepted sources. Transient build/ products are excluded from the seal; accepted binary evidence is saved in verification.

Replay in a fresh copy with tools/replay.py SOURCE NEW_LABEL --lean PINNED_LEAN --project CONFIGURED_LEAN4_PROJECT, following the import dependencies. tools/evidence.py verify --sealed rechecks the local recorded compiler/cache artifacts as well as source and seal custody; those host paths must be available for a live replay check.

No provider inference, commit, push, PR or merge was performed. The work is ready for review.
