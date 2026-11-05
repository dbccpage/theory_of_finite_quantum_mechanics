# Witnessed Difference notebook curriculum

This is the executable learning path for the canonical monograph. Start at
`000` and follow the numeric sequence: later lessons reuse names and distinctions
introduced earlier. The ten core lessons listed below are output-free and are executed
twice by the replay gate—once from the paper root and once from this directory.

The first notebook contains a dependency-free HTML range widget. In an
ordinary browser it is interactive; automated replay sets
`WDP_NOTEBOOK_STATIC=1` and records its deterministic static fallback. The
fallback receipt is not represented as a browser-interaction test.

| Order | Lesson | Level | First objective |
|---:|---|---|---|
| 00 | [Primitive difference and finite symmetry](000_primitive_difference.ipynb) | Novice | Compute the same/different primitive and its xor parity |
| 01 | [Cochains, exactness, and the vector obstruction](010_cochains_and_vector_obstruction.ipynb) | Novice to intermediate | Compute exact 0- and 1-coboundaries on a finite complex |
| 02 | [Retention, re-access, and witnessed difference](020_retention_and_reaccess.ipynb) | Intermediate | Construct a retained registration and content-bound witness |
| 03 | [Three observer representations and explicit bridges](030_observer_representations.ipynb) | Intermediate | Keep quotient, operational, and observer-object representations distinct |
| 04 | [From an observation attempt to a typed measurement](040_observation_to_measurement.ipynb) | Intermediate to advanced | Validate every rung of the observation ladder |
| 05 | [Witnessed duration and finite multiplicity](050_duration_and_finite_probability.ipynb) | Applied intermediate | Sum strictly positive exact duration weights |
| 06 | [Bounded history enumeration and cancellation](060_bounded_history_sums.ipynb) | Advanced | Enumerate endpoint-constrained paths under an explicit step budget |
| 07 | [Declared U(1) phases, holonomy, and gauge change](070_declared_u1_holonomy.ipynb) | Advanced | Validate unit-modulus edge phases on a finite carrier |
| 08 | [Relative claim status and canonical receipts](080_claim_status_and_receipts.ipynb) | Advanced | Route a claim through an explicit evaluator profile |
| 09 | [Mutation recovery, evidence composition, and terminal scope](090_mutation_recovery_and_scope.ipynb) | Deep expert | Explain copy-on-write mutation testing and pristine-source recovery |

The supplements have separate scope: lesson 100 is stored without outputs; lesson 110 retains recorded outputs. The ten-lesson replay receipt does not cover either supplement.

## How to study

1. Read the idea and derivation before executing the worked example.
2. Predict refusal codes as well as accepted values.
3. Attempt the exercise before opening or executing the tagged solution cell.
4. End with the scope check; it is part of the lesson, not boilerplate.

Run `uv run python scripts/execute_notebooks.py --check` from the paper root to
verify the stored two-working-directory receipt. The notebooks are finite
educational witnesses only. **AuthorityEffect: None.**
