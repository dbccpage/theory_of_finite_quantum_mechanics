# Before the First Mark

Jeremy H. Carroll · version 1.0.0 · publication candidate, 2026-10-09.

Read [the manuscript](paper.md), [the rendered paper](paper.pdf),
[the change log](paper_change_log.md), and [source provenance](source_provenance.json).
Manuscript text: [CC BY 4.0](LICENSE). Companion code: [PolyForm Noncommercial](LICENSE-CODE).
Vendored Genesis Python and Lean sources retain [Apache 2.0](code/derivation/LICENSE).
Historical source records retain their original licenses; see the
[source reader](docs/references.md) and [citation manifest](manifests/cited_sources.json).
All manuscript citations can be followed within the package. Both original
repositories are private; their pinned URLs record provenance rather than
provide the reader's only access to cited material.

This package runs outside the repository. No sibling checkout, network service,
registry dependency or monorepo import is required for mathematical reproduction.
Install Python 3.10 or later, Rust/Cargo, and Lean **4.33.0** with elan.
The proof source pin is `19L57G1@f1d56c010e6ba10a3b9418bd7cc5953c067250f2`.

From this directory:

```sh
python code/reproduce.py --lean-wire
python code/verify_sources.py
cd lean4
lake build
cd ..
python tools/census.py
cargo test --offline --manifest-path code/rust/Cargo.toml --lib -- --skip alpha_projection_obstruction
```

The replay checks all four minimum-response counts, 35 context counts and
fresh-mark preservation on 3,996 targets in 1,436 regimes. It independently
compares native Rust's complete portable keys and every context observation
against frozen Python for all those regimes. The Rust primitive regression
suite has 135 tests; its 55 projection-study tests are outside this paper's scope.
The source naming collision and uniform-rule collapse remain explicit
counterexamples. Native builds fail on toolchain errors; they never substitute
an offline assertion for execution.

The Lean census includes 2,475 non-internal compiled theorem constants,
including generated theorems, across the bundled pinned derivation,
canonicalization and continuation modules and manuscript companion. Pinned
modules permit only `propext` and `Quot.sound`. The general image-factorization
companion additionally uses `Classical.choice`. The report is a compiled
population, not a count of paper claims or an audit of all source research trees.
The companion also proves that equality of sorted structural tuples after
supplied bijections implies regime isomorphism. Its wire module formalizes the
actual length-prefixed layout and unsigned 64-bit byte encoding, including a
structural decoder and injectivity proofs. The orbit/search companions construct
the finite bijections, enumerate exactly all permutations and prove that the
executable minimum classifies well-formed regimes with duplicate-free collections.
They also prove byte-key classification under the unsigned-word bounds. General
source-program refinement remains open.
Native Lean agrees with Python on 1,439 wire encodings, and Python/Rust decoders
agree on 72 explicit acceptance and rejection cases.
The proved Lean canonical search agrees on the 1,436 labelled regimes, plus
two mixed-arity/unordered-list probes. Its native interface checks the actual
well-formedness and duplicate-free predicates and rejects 17 invalid or
over-budget cases. The native replay caps each index dimension at eight and
the permutation-pair budget at 100,000; the mathematical theorems have neither cap.
The replay also checks the largest admitted population of 80,640 candidate pairs.

The custody controls create isolated fixture repositories and require Git on
`PATH`. To run those controls and the mathematical tests, install pytest and run:

```sh
python -m pip install pytest
python -m pytest --import-mode=importlib code/tests -q
python verify_deposit.py --lean
```

The Python tests include custody controls, mathematical/protocol checks and
source-citation failure controls. The portable-key boundary can additionally be checked with mypy; frozen
upstream imports retain their bytes and are outside that type-checking scope:

```sh
python -m pip install mypy
python -m mypy --strict --follow-imports=silent code/portable_key.py
```

To rebuild derived files after an authorized source change:

```sh
python tools/census.py --write
python scripts/build_pdf.py
python scripts/regen_sha256sums.py
python scripts/build_deposit_zip.py --out 000_genesis_19l57g1_2026-10-09.zip
python verify_deposit.py --integrity-only --archive 000_genesis_19l57g1_2026-10-09.zip
```

The PDF build requires Pandoc and XeLaTeX. The archive's default filename and
member timestamps use the declared metadata date, not the current calendar day.
The explicit output above identifies this release even when other dated ZIPs
exist. The integrity-only check compares that exact file with both manifests,
the live tree and the complete canonical archive bytes; it executes no tests.

For the final release check, extract that exact ZIP into a new clean directory,
then run from its extracted `genesis` package root:

```sh
python verify_deposit.py --archive /absolute/path/to/000_genesis_19l57g1_2026-10-09.zip --lean
```

Use the actual absolute path on your platform. The verifier checks the outer ZIP
against the extracted files, runs the package tests and native replay, adds the
full Lean census, and rechecks tree/manifests/archive afterward. Record the outer
ZIP's SHA-256 and command results in a release receipt outside the archive it
identifies. A tree-only run without `--archive` does not certify a selected ZIP.

Normal deposit verification already requires Lean for native wire and canonical
search replay. `--lean` additionally compiles the full theorem population and
checks its axiom census. `--test` selects Python test files; it does not skip the
native replay. Checksums and an integrity-only pass do not replace these checks.
Review dossiers are retained in the repository's internal intelligence area;
they are not publication evidence packaged for the reader.

See [the portable-key protocol](docs/portable_keys.md) before exchanging keys.
The historical Python and Rust refined local keys have different ordering
conventions. Their existing fingerprints are implementation-specific.

Universal mathematical statements have the Lean hypotheses named in the
manuscript. Finite Python/Rust agreement does not establish a general
source-code refinement theorem. The primitive-to-WDP incidence construction
and historical continuation census retain their separately stated scopes.
No DOI registration, deposit or external publication is claimed.
