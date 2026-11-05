# Calibrated recovery reference

Appendix X of the [paper](../../witnessed_difference_programme.md) gives the
written interval, finite-reduction, and cost proofs. This reference accepts
exact rational data. It treats interval products as adversarial report models;
it cannot infer physical realizability or calibration traceability.

Cost certificates require the scope tag
`"cost_domain": "ideal_calibrated_interval_product"`. They certify costs for
the full ideal calibrated product, without raw-encoding resource bounds.
Untagged older certificates must be explicitly reproposed and replayed;
verification never silently supplies the missing contract.

The raw API admits at most 160 characters per canonical rational value and
256 bits per numerator/denominator, before applying calibration. Model
admission does not establish inverse-calibration closure within this domain.
For gain `1/2**255`, offset zero and point supports `{0}` and `{2**255}`,
the two-state ideal fixed/adaptive costs are both `1`, but the high state's
unique raw value `2**510` needs 511 bits and yields `INVALID_REPORT`. The low
state's raw value `0` verifies. This resource refusal is neither mathematical
infeasibility nor an accepted wrong answer. A cost claim for operation through
this bounded API requires a separate admitted-encoding argument.

From the paper directory, using Python 3.12:

```sh
python -m pytest -o addopts='' code/unit_tests/test_calibrated_recovery.py code/unit_tests/test_finite_observation.py
PYTHONPATH=code python -m calibrated_recovery.replay --verify code/calibrated_recovery/certificates.json
lean code/calibrated_recovery/TransferLaws.lean
```

The Lean source uses core only and is checked with Lean 4.33.1. The first three
declarations depend on `propext`, `Classical.choice`, and `Quot.sound`; the last
three have no axiom dependencies. They prove logical transfer and soundness,
not the real-analysis or observation-cost theorems.

The three stored cost certificates cover the separated example (fixed 7,
adaptive 4), touching intervals (infeasible), and the rectangular enclosure
of the shared-noise example (infeasible). The actual shared-noise model has
cost 2 by the written cancellation proof. Passing its enclosure to the checker
does not authorize a claim of physical impossibility.

`evaluate(model, report, proposed_answer)` validates a separate proposal against
the trusted model and the report. Its statuses are `VERIFIED`, `ABSTAIN`,
`INCONSISTENT`, `INVALID_REPORT`, and `INVALID_PROPOSAL`. None grants action
authority. The model must come from the caller's trusted configuration.
Unit tags and the model digest detect mismatched data; they do not authenticate
a sensor or prove that its supplied error bounds hold.

Reports are dictionaries with exactly these fields:

```json
{
  "model_sha256": "the digest of the separately supplied model",
  "visible": "*",
  "readings": [{"channel": "A", "raw_unit": "raw", "value": "-1/2"}]
}
```

There is no JSON-text parser in this API: a caller decoding bytes must reject
duplicate keys before handing over the dictionary. Reading values must be
canonical rational strings. Calibration is the model's declared nonzero affine
map; its enclosures already include the admitted error budget.
Both report and cost-certificate parsers bound the text and reject exponent,
decimal, and non-ASCII forms before constructing a fraction. Cost text has a
separate limit that accommodates sums of all twelve admitted 256-bit prices.

To propose new finite certificates, run `replay --propose` with an explicit
output path, then replay that file with `--verify`. Verification reconstructs
the finite lift from the trusted model and checks the supplied tables. It
never calls the solver to replace an invalid certificate. The existing
ten-state and twelve-instrument caps are enforced before exhaustive solving;
exceeding a cap is a resource refusal, not infeasibility. No native production
cost evaluator is added by this reference.
