# SQL sign-problem experiments

AuthorityEffect: None.

`run_sign_sql.py` runs the original illustrative walk database.
`exact_models.py` constructs finite physical Meron and Hubbard ensembles and
uses SQLite for graph components, cancellation, matrix products, determinant
expansion, and particle-number derivatives. Reduced rational weights use an
exact stepwise aggregate; no determinant UDF or floating-point sign decision is
used.

```text
python code/sign_sql/exact_models.py
python -m pytest -n 8 --dist=loadfile --import-mode=importlib code/sign_sql/tests
```

Run these commands from the paper directory. On Windows an external writable
`--basetemp` and `-o cache_dir=...` can be supplied.

The default replay covers actual Meron orbit cancellation, its squared
staggered observable, Hubbard occupation-gauge obstructions, protected
auxiliary-field sectors, exact particle-number estimates, and negative doped
and frustrated determinant witnesses. The JSON receipt records all parameters
and the evaluator/schema/test source hashes. Selected witnesses have no
reported full-ensemble average sign.

See `../../docs/sql_meron_hubbard.md` from this directory for derivations,
positive normalization factors, finite Trotter scope, reconstruction tests,
and exponential enumeration costs. These are finite model computations and
protected-sector identities; they do not solve the generic fermion sign problem.
