# Operational claim-boundary fixes for PRs 144 and 147

AuthorityEffect: None.
Original base: `0364c3c9744e72f05ec6a7ebd14f971f1ddd1c2c` on `lean-v4-35`.
Integration base: `d65cbaf95732567cc558946f43e816508e232b18` on `main`, which absorbed
`lean-v4-35` in PR152; the remote legacy branch was then deleted.
This follow-up corrects terminology and adds formal witnesses and semantic controls.
It does not discharge physical admission, product-effect separation, or the
carrier catalogue from operational primitives.

## Claim triple and remaining assumptions

1. **Construction under stated closure rules.** A bounded effect followed by an
   admitted normalized positive preparation constructs an admitted positive
   subnormalized reset. A spanning preparation family and separating global
   effects imply irreducibility. Ordered carrier data and operational admission
   remain explicit premises in the general theorem. `orthant` and
   `canonicalAdmission` instantiate them in concrete rational classical examples.
2. **Schur-type reformulation.** Descent makes the observation kernel invariant;
   irreducibility and calibrated observation imply injectivity. For a calibrated
   finite nonempty coordinate target, the existence of some descending
   irreducible family is equivalent to injectivity, by
   `OperationalFilterFamily.exists_descending_irreducible_iff`. Selecting a family
   independently remains an additional operational justification. The converse
   constructs unrestricted linear maps; it does not assert physical admission.
3. **Boundary.** Doubled product coordinates admit descending but reducible
   product resets and nonseparating product effects. Global orthant effects give
   admitted irreducible resets that cannot all descend through that observation.
   Identity observation supplies the tomographic side of the equivalence.

## Changes requested and supplied

- The PR144 run and review explanations now use Schur-type reformulation and
  state the existential converse. The formerly independent-sounding paragraph
  around README line 96 is corrected.
- `OperationalTomography.doubledProduct` has an eight-coordinate carrier
  `(Fin 2 × (Fin 2 × Fin 2)) → ℚ` and four product coordinates. Observation sums
  hidden blocks; preparation splits them equally. Lean proves calibration,
  block-diagonal product descent, noninjectivity, and nonirreducibility.
- `OperationalFieldSelection.two_hypotheses_satisfiable` witnesses the complete
  algebraic headline at d = 2. `selected_carrier` selects `.complex` in the
  supplied real/complex/quaternion catalogue; it does not identify the ambient
  coefficient field with ℂ. Calibration supplies the nonzero observation, so the
  redundant hypothesis has been removed from `selected_parameter`.
- `OperationalBoundaryWitnesses` provides the orthant OrderedModel and proved
  sequential admission, normalized basis preparation span, bounded effects,
  admitted reset family, and concrete witnesses on both sides of the boundary.
- PR147 wording now says construct under stated closure rules and includes the
  claim triple above. Historical candidate payloads are not rewritten.
- The 277 tomography and 623 filter perturbation cases are **fixture-integrity
  checks**: rejecting changes to fixed certificates is not semantic necessity.
  New semantic tests accept asymmetric valid calibrations, show injective
  observation with a descending reducible diagonal family, and compare
  nonseparating versus separating effect sets. The reducibility witnesses are
  actual proper invariant kernels or lines, not failures of a sufficient
  full-matrix-span criterion.

## Validation and reproducibility

Run `py -3.12 -X utf8 replay.py --output <new-directory>` from this directory.
The output directory must not already exist. The replay verifies the inherited
pin envelope and a fresh complete declared input set before and after running
Lean, Python, Rust, both independent certificate oracles, byte-for-byte
construction replay, DAG/sync checks, contracts, and whitespace checks.
`verified_main/receipt.json` records the current-main integration results. The
initial `verified/receipt.json` and its exact source envelope remain recoverable
at commit `1484db6d096339d8b172170c8c781989872cd88d`, before the main integration.
The full repository suite is not claimed. Standard Lean axioms are allowed;
`sorryAx`, custom axioms, `admit`, `sorry`, and `native_decide` are rejected.

Historical candidates, pin envelopes, and receipt bytes are retained. Only the
four explicitly listed historical README files are edited. Upstream changes to inherited inputs are accepted only when their bytes equal
the pinned main base Git blobs. This follow-up makes no canonical DAG changes.
The initial replay passed 56 Lean axiom audits, 49 Python tests, 347 Rust tests,
7,073 contract records, both independent oracles, fixture-integrity checks, and
all three DAG synchronizations. Main integration is checked again because the
DAG validators, Cargo workspace and Lean root manifest changed upstream. Failed development attempts remain in
`attempts/` separately from the final verification. The separate operational
independence draft PR151 is not changed by this branch.
