# Joint-support recovery reference

Appendix Y of the [paper](../../witnessed_difference_programme.md) derives
fixed and adaptive recovery costs for explicit joint report supports. This
reference implements its finite reduction for unions of rational affine
segments. Each segment uses one common parameter across all coordinates;
every coordinate slope must be nonzero. The supplied supports are assumptions,
not inferred noise distributions or authenticated calibration records.

From the paper directory, using Python 3.12:

```sh
python -m pytest -o addopts='' code/unit_tests/test_joint_recovery.py
PYTHONPATH=code python -m joint_recovery.replay --verify code/joint_recovery/certificates.json
```

The four stored certificates give these fixed/adaptive costs:

| Model | Fixed | Adaptive |
| --- | ---: | ---: |
| Shared affine error | 2 | 2 |
| Isolated complete-report collision | infeasible | infeasible |
| Two parity classes of point supports | 2 | 2 |
| Isolated interior cost peak | 3 | 3 |

The last model is a sampling control: retaining only segment endpoints
incorrectly gives cost 2 for the continuous model. The complete construction
retains critical interior equalities as well as interval endpoints.

`evaluate(model, report, proposed_answer)` checks one proposed answer. Report
dictionaries have the same exact schema as the [interval reference](../calibrated_recovery/README.md),
but bind a joint model. All readings must match one parameter in one component
of a candidate. Distinct components may not supply different readings for a
single history. The five statuses are `VERIFIED`, `ABSTAIN`, `INCONSISTENT`,
`INVALID_REPORT`, and `INVALID_PROPOSAL`. None grants action authority.

Models declare output, raw and parameter units and one common cost unit.
They admit exact rational inputs with at most 256-bit numerators and
denominators, ten segments and twelve instruments. The constructed witness
must also fit the existing ten-world solver limit. Exceeding a cap raises a
resource error; it does not mean recovery is impossible. A detected collision
can instead supply a genuine two-world certificate of infeasibility.

`conditional_instance(model, i, value, visible)` takes an exact `Fraction`
in calibrated output units. It checks the 256-bit report limit on the inverse
raw conversion, just as `evaluate` checks the raw reading before calibration.
The derived calibrated value may have a larger numerator or denominator.

To generate a proposal, use `replay --propose PATH`, then replay it with
`--verify PATH`. Verification reconstructs the finite witness and checks the
submitted tables using the existing `finite_observation` checker; it never
calls the proposal solver to replace missing or rejected data. The model
digest binds supports, labels, units, calibration and prices. It does not
authenticate their source. A caller decoding JSON before `evaluate` must
reject duplicate keys; the certificate replay CLI does so itself.

This implementation certifies costs for the admitted affine models. The
paper explains how to transfer a finite policy to continuous reports, but
this module does not implement that controller. General joint supports,
segments thickened by independent error, physical realizability, and new
Lean formalizations remain outside its scope. The arbitrary-support finite
witness theorem is an existence result, not an effective sampling algorithm.
