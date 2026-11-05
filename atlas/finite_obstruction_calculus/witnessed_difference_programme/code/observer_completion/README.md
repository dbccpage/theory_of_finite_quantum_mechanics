# Sharp Observer Completion

Read [the full theorem](sharp_observer_completion_theorem.md) for the proofs,
source graphs, scope conditions, and counterexamples. WDP §10.6 and
GEN-WDP-46 integrate this finite rational result into the monograph.

The proposal and exact matrix code use Python 3 and the standard library. Functional evaluation and certificate replay require the installed WDP package (or its code directory on PYTHONPATH) and the native `evaluate_wdp_functionals` executable from `code/rust`. Set WDP_FUNCTIONALS_BIN to its absolute path. No network is used during replay.

Run from this directory:

~~~text
python replay_examples.py check observer_completion_certificates.json
python replay_examples.py adversarial observer_completion_certificates.json
python observer_completion.py check generic_receipt.json generic_input.json
~~~

Generate a fresh receipt for the supplied generic problem:

~~~text
python observer_completion.py solve generic_input.json
~~~

The solve command prints JSON to standard output. To regenerate the full
example certificate file, use:

~~~text
python replay_examples.py generate observer_completion_certificates.json
~~~

The source replay checks four cases: the three-patch carrier, both source
conventions for the coupled carrier, and the scalar quotient witness
extended by a newly declared zero observer. Matrices are reconstructed from
the source site/interface operators. All numbers use exact rational arithmetic.

The general solver accepts d0, Q, and a target of raw, quotient, or both.
An optional V_facets/augmented_facets pair requests sharp constants.
Matrix encoding contains rows, cols, and data, with rational entries stored
as strings. The completion row count follows from the theorem; the
augmented report norm must have that many additional dimensions.

General polyhedral recovery uses exhaustive vertex enumeration and can
be very expensive. The source examples instead carry compact global
linear identities and saturation witnesses.

The delivered package contains:

- Source graph, image, kernel, and intersection dimensions.
- All twelve displayed minimum completions and their recovery constants.
- Generic exhaustive polyhedral recovery and weighted rational LP duals.
- Rejection of 15 deliberately tampered certificates.
- Restricted-coordinate-menu counterexample and zero-space cases.
- Generic CLI solve/check agreement with a separately supplied input.

Repository review additionally corrected the zero-recovery-domain convention
and the scope of rational distance certificates. The checker now validates
strict JSON and canonical rational strings, independent expected inputs,
every retained field, nested evidence scopes, adapted subspace bases,
active vertex rows, initial failures, and zero-dimensional branches.
Delivered receipts retain their historical source bindings. Regeneration and replay must use the current declared inputs and current checker.

The reviewed adversarial command rejects 15 mutations. A further 27 scoped
pytest cases cover source witnesses, malformed inputs, changed claims,
vacuous recovery and an independent determinant-minor oracle over 81 tiny
presentations and 243 completions. From the WDP package root, with pytest
installed and `code` on `PYTHONPATH`, run:

~~~text
python -m pytest -o addopts='' -q code/unit_tests/test_observer_completion.py
~~~

This is a paper-scoped reference implementation. No full repository suite,
or Lean formalization is claimed. Norm and dual-pairing evaluations delegate to omega_functional through the native executable; the completion identities are checked by the Python certificate checker. Certificates
are mathematical evaluation evidence and have no authority effect.

[source_provenance.json](source_provenance.json) preserves the delivered
source commit, Git blobs and the author's WDP attachment hash. The three
Git blobs were independently confirmed. The original WDP attachment bytes
were not supplied here, so that hash remains source-declared provenance.
[delivered_sha256sums.txt](delivered_sha256sums.txt) preserves the original
eight package hashes, all checked before modification; it does not describe
the reviewed files. [repository_review.json](repository_review.json)
records checks and corrections. The parent WDP release manifests bind the
reviewed tree. Checksums establish byte consistency, not authorship or proof.
