# Independent review of PR 144

Reviewed head: `afd802ce5d82cb344d8a6453bb0026ee49e7b306`.
Base: `lean-v4-35` at `1ea6b5a0aa9eee53d43078d6015c1d2a00435d75`.
AuthorityEffect: None.

The conditional mathematics is sound. Calibration splits states into reconstructed
coordinates and the observation kernel. Descent makes that kernel invariant;
irreducibility and a nonzero observation eliminate it. Independent product dual
frames give calibration. These statements do not derive their hypotheses from
primitive difference. The normalization obstruction and doubled countermodel
remain essential: ordinary normalization-preserving operations cannot satisfy
this irreducibility premise when the normalization kernel is nonzero and proper.
The field-selection bridge determines the dimension-family parameter d=2 under
its extra dimension hypotheses, not the scalar field by itself.

The review found and repaired exact-arithmetic and validation defects. Python now
converts direct integer inputs to Fraction before elimination and rejects floats,
booleans and malformed matrices. Rust requires complete paired operation families
and validates matrix shapes before zip/index arithmetic. The review replay also
rejects missing or duplicate entries in the typed fragment. See `review.json` and
retained `red_python.log`, `red_rust.log`, and `initial_findings.json` for details.
The valid original JSON models were not affected by the Python integer-input bug.

`independent_oracle.py` does not import the original builder or checker. It proves
finite ranks using nonzero basis determinants and orthogonal operator Gram
matrices, and checks calibration, kernel witnesses, positivity, normalization,
local product filters, and protected questions with exact rationals. Finite
witnesses supplement the Lean proof; they do not establish physical availability.

Run the current-source review gates from the repository root:

```powershell
py -3.12 -X utf8 dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/replay.py --output <new-directory>
```

The output directory must be new. `source_pins.json` binds the complete original
source set and the review sources to their current bytes. The original pin
envelope and candidate are separately fixed by digest. Original run receipts
remain historical, so their replay is not the current-source acceptance command
after checker repairs. Current acceptance is `verified/receipt.json`, its command
logs, and the staged/committed Git-blob pin audit. The gates cover the two new Lean
modules, existing hidden countermodel, finite-probability Rust library, two
Python modules, DAG validation/synchronization, and contract records; they do not
claim a whole-repository test run.
