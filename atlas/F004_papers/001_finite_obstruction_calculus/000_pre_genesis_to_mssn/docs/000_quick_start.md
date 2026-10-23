# Reproducing the consolidated paper

The main results are the report criterion, finite demand accounting,
old-image injectivity and the chain-retraction obstruction. `lean4/Paper.lean`
formalizes these statements. Imported S(n) proofs retain their original bytes;
the package toolchain pin is tested separately from each predecessor's pin.
`lean4/Homology.lean` constructs the quotient homology groups, their group laws,
induced maps and the injectivity theorem for a chain retraction. It also proves
the integer quotient class criterion and a nonzero order-two class.
`lean4/FreeAbelian.lean` constructs the free abelian group and establishes its
extension and uniqueness properties. `lean4/GraphHomology.lean` identifies
integral zeroth graph homology with the free abelian group on connected components and
vertex-class equality with connectivity. Loops and parallel edges are allowed.
The [theorem map](mechanization.md) identifies the additional finite-coordinate,
triangle, free-word and probability constructions and their remaining limits.

`code/reproduce.py --native` compares finite report, demand, code-collision,
CHSH, integral quotient classes, graph boundaries and integral component
coordinates, triangle classes, cochains, fixed-width coding, typed word recovery,
trace reversal, free-word reduction and rational joint mixtures with freshly executed
Lean and Rust programs.
Equality on this replay population does not prove general compiler refinement.

The graph examples use exact integers and fractions. Syntax conformance checks
exercise the recorded positive and negative controls for all three grammars.
They do not establish semantics for every atlas capability.

`python scripts/build_pdf.py` requires Pandoc and XeLaTeX and builds three passes.
`python tools/rebuild_release.py` regenerates the two hash manifests and ZIP
using `zenodo_metadata.json`'s declared `publication_date`, including the archive
name and member timestamps. Rebuilding this release on another day retains
2026-10-09. Creating a new release requires a deliberate metadata date change
and corresponding manuscript, rendered PDF and citation updates before rebuilding.
`python tools/rebuild_release.py --check` checks the existing release without writing.

`python verify_deposit.py` independently reconciles both manifests, sweeps the
retained tree and checks the existing archive's membership, hashes and complete
canonical bytes. A missing or invalid ZIP fails this command. It does not rebuild
an archive to make a check pass. Add `--lean` for fresh Lean compilation and the
axiom census. Add explicit `--test code/tests/test_name.py` arguments for selected
tests. After either optional check, the verifier repeats release validation and
requires the original manifests and ZIP bytes to remain unchanged.

Run `python -m pytest --import-mode=importlib code/tests` for the package tests;
importlib mode avoids a collision between this package's `code` directory and
Python's standard-library module of the same name. Generated build caches are
excluded. A release-integrity pass alone reports no Lean, Rust or Python-test replay.
