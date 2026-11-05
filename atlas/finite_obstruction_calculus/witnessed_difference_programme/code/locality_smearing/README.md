# Exact locality and smearing reference

From the paper's `code` directory (with the repository on `PYTHONPATH`):

```sh
python -m locality_smearing.replay check
python -m certified_progress.calculus
```

Both replay the submitted witnesses without model calls. The first reconstructs
the original sixteen-state CAR operators, checks four rational response matrices
against independent congruence witnesses, and checks syndrome, readout, temporal
pairing and cochain data. It also binds the integer M=1 Lean matrix to the actual
CAR construction. Its rational time-limit threshold is a consequence of the
written analytic estimate, not a numerical proof of that estimate.

Use `python -m locality_smearing.replay generate` or
`python -m certified_progress.calculus --write` only to regenerate local evidence
after intentional source changes. Regeneration is distinct from replay; a
failed submitted witness is not repaired inside the checker.

`car.py` and the generation branch propose concrete witnesses. `checker.py`,
`locality.py`, the reused exact congruence verifier, and the progress checker
replay them against separately supplied inputs. No billed usage or physical
instrument realization is inferred. See the paper's
[evidence map](../../docs/derivation_evidence.md) for exact proof boundaries.
