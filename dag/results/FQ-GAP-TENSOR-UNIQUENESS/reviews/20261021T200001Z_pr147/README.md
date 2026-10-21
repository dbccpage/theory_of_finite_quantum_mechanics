# Independent review of PR 147

Reviewed head: `b56af2b93b7bfb5946dc526e99f697b0e8261b46`.
Base: `lean-v4-35` at `3b50a1a980fa8535590356a65ff82b1d682dac29`.
AuthorityEffect: None.

The conditional mathematics is sound; no Lean proof changes were needed.
Testing followed by preparation constructs a reset. Bounded globally separating
effects force faithful normalization on the cone; cone generation then gives
normalized preparation span and reset irreducibility. Physical admission is a
separate sequential rule. Product-observable effects yield descent and kill the
observation kernel, so closing their algebra cannot remove hidden directions.
For calibrated observation, product-reset irreducibility is equivalent to
tomography. Descent of globally separating resets with one visibly normalized
output is likewise equivalent to tomography. These results leave the stated
operational hypotheses explicit and do not derive unconditional tomography.

Two implementation defects were reproduced and fixed in the independent Rust
checker. It accepted deleted assumptions and undeclared extra claims, and its
JSON Value parser silently overwrote duplicate fields. Typed deserialization now
rejects missing, unknown, duplicate and ill-typed fields; the entire premise list
is checked. Regression tests cover both defects, duplicate model names, changed
premises and strict dimension/scalar types. `attempts/` retains the failing logs
and regression patch. The valid candidate and all Lean/Python sources are unchanged.

`independent_oracle.py` imports neither the builder nor either checker. Exact
Bareiss determinants of preparation, effect and operator minors independently
verify the finite ranks. It checks calibration, outcome bounds, descent and
hidden witnesses, and adds nonorthogonal spanning preparations/effects and an
asymmetric calibrated model. A nonzero hidden output shows why nonzero alone
cannot replace the visible-output premise. These are finite controls, not a
replacement for the conditional universal Lean proofs.

Run the review gates from the repository root into a new output directory:

```powershell
py -3.12 -X utf8 dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T200001Z_pr147/replay.py --output <new-directory>
```

The review preserves all original evidence and pins the complete inherited
source set plus review sources. Only the repaired Rust source and its two
companion records may differ from the original pins. The original replay is a
historical command after these repairs; current-source acceptance is this
review's `verified/receipt.json`, its command logs, and the staged/committed Git
blob audit. Checks cover the Lean filter family and selection/hidden modules,
three Python test modules, the full finite-probability Rust library, exact
candidate reconstruction, mutation controls, DAG validation/synchronization,
contracts and whitespace. They do not claim a whole-repository or hosted-CI run.
