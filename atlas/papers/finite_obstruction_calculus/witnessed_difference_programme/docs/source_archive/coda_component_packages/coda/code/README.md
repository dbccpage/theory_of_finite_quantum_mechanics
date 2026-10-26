# Executable companion

`coda_core.py` implements finite image factorization, bounded repair menus,
the specific three-coordinate FOC packet in §4, exact certificate checking,
finite parity constraints, and the two integral examples. All mathematical
arithmetic inputs are integers or `Fraction` values. Floats and Booleans are
rejected at that boundary. This is not a general LP or continuum solver.

`run_examples.py` writes exact rational JSON. `audit_legacy_embedding.py`
loads the unchanged historical discipline code and exhibits its Z2 arrow
collision. `generate_figures.py` plots the exact example values.
`build_notebook.py` specifies the walkthrough; `replay_notebook.py` executes
it. `verify_package.py` checks provenance, claim/Lean indexing, local links,
saved example values, notebook structure, and file hashes.

Tests in `tests/` independently check all 256 pairs of Boolean observation
and query tables on a four-state domain; menu boundaries and ties; exact
primal/dual witnesses and forged certificates; parity gluing; integral
identities; and the actual legacy counterexample. Run the suite from the
package root as documented in [README](../README.md).

The [ledger](../coda_claim_ledger.md) is the authority on claim scope.
