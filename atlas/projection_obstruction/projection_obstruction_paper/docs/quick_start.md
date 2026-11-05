# Projection Obstruction: quick start

**Version:** v6.9.13, author-review revision, 2026-10-10. The Python package remains 6.9.4 and checks Example 3.5 only.

The paper measures information lost by product projection and by a declared
observer. Its local starting bound is D_e(t) ≥ ν_e t − 24g²t². The new results
identify when that retraction is first-order optimal, quantify lost phases,
and extend local correlation calculations to connected cumulants.

| Question | Read |
| --- | --- |
| Is the product of marginals the nearest product? | §§5.11–5.12: generally no; leading optimality holds for pure product Hamiltonian curves. |
| Does the edge tally control global trace norm? | §5.13: unrestricted equivalence fails in both directions. |
| When can a connected k-site correlation start? | §§5.14–5.15: Steiner-length onset, exact local coefficients, remainder and fixed-shape density bounds. |
| What can weights alone predict? | §§7.5–7.6: sharp scalar phase ambiguity, resolved effects, and completed linear observers. |
| When does curvature control the repair quotient? | §7.7: supplement it with a report separating retained cohomology. |
| Which research paths remain conditional? | Appendix D: geometric adapters, protected extensions and unitary stability. |
| Which added axiom selects complex quantum theory? | Appendix E: purification, relative to the explicit Jordan–Lie, composition, compression and full-process base. |

From the package root, with Python ≥ 3.11:

```bash
pip install .[jets]
python -m pytest -q code/tests/test_metric_phase_derivations.py code/tests/test_connected_cumulants.py
python -m pytest -q code/tests/test_short_time_jets.py
python code/derivation_replays.py
python scripts/regen_sha256sums.py --check
```

These are exact finite replays using SymPy. The general analytic statements
have written proofs, not new Lean certificates. Existing formal cores and
historical verification are described in [the package README](../README.md)
and [the Lean guide](../lean4/README.md).

[Read the manuscript](../projection_obstruction.md) or
[open the rendered PDF](../projection_obstruction.pdf).

## Finite certificate replay (v6.9.1)

Install the `jets` extra for the local-zero checker. In an explicitly opted-in repository integration (`PO000_NATIVE_INTEGRATION=1`),
set `OMEGA_SYMBOL_GAME_HOST` to a native host binary and make its Python host adapter importable.
The native host is not part of this package.
Run from the paper package:

```bash
python -m pytest -q code/test_finite_certificates.py code/tests/test_local_persistent_zero.py
python code/replay.py --output /tmp/po000_current_replay.json
python code/verify_certificate.py /tmp/po000_current_replay.json
```

The three measurement records include an Ising five-cycle and a separable
correlated control. The two local-zero records include a commuting boundary
and a nonconstant local flow with an invariant polynomial. General theorem
dispositions are separate. A missing native host or SymPy produces an explicit
capability refusal; a verified record cannot be accepted without its checker.
See the [active dependency inventory](claim_dependencies.json) for proof scope.

## Conditional reconstruction (v6.9)

Appendix E classifies three operational theories under its additional B1–B4
axioms: classical, complex quantum, and complex quantum with arbitrary
superselection sectors. Purification selects the complex quantum theory;
continuous reversible access between pure states is equivalent within this
base. This does not derive B1–B4 from finite distinctions or obstruction data.
The conclusion includes the Born pairing, standard tensor product, all effects,
and all quantum channels. Run the exact examples separately:

```bash
python -m pytest -q code/tests/test_quantum_selector.py
```

These are finite identity and counterexample checks, not a general theorem verifier.
The scoped [E.1 Lean build](../lean4/README.md) separately checks the
complexified identity package, faithful C*-image and positive cone. It does
not mechanize the block classification or operational selector.

## Finite onset certificates (v6.6)

With the SymPy extra installed, run `python -m pytest -q code/tests/test_polynomial_onset.py`
from the package root. The exact rational checker verifies model-specific lifted
annihilators and residual jets. Section 5.16 supplies the general written proof;
no new Lean build or growing-system cutoff is claimed.
