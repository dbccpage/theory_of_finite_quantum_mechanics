# MSS-N publication-support review

AuthorityEffect: None. Review date: 2026-10-09 (America/New_York).

This correction set supports the first-publication Genesis review. It does not
claim that all 101 MSS specifications have implementations or that the whole
MSS estate has been formally verified. The frozen source comparison uses
`dbccpage/19L57G1` at `f1d56c010e6ba10a3b9418bd7cc5953c067250f2`.
MSS is an independently designed atlas, not a continuation transcript or a
byte-for-byte implementation of that source.

## Inventory and review extent

The initial tree contains 352 tracked files: 153 Markdown, 92 Python, 25 Lean,
24 Rust, 22 SVG, 15 YAML, 14 SQL, three JSON, one EBNF, one Cargo manifest,
one Cargo lock and one toolchain file. The review inventoried every path,
scanned explanatory claims and local Markdown links, read the active entry
points, alphabet construction, grammar/codec implementation, six top-level
Lean modules and four domain cores, and corrected the contradictions below.
Other domain algorithms, illustrations and SQL/Rust examples retain the scope
and limitations of their existing individual evidence. This is not a claim
of an exhaustive new line-by-line proof audit of all 352 files.

## Corrections

- Replaced the alphabet insert's false finite-category and free-monoid
  isomorphisms with an irreducible-generator proof. Supplied the prefix-free
  code `x_k ↦ 1^k0`, its exact image and partial inverse. Removed unsupported
  claims that individual glyphs force topology or transfinite reflection.
- Kept the constructive distinction between old-word preservation and
  preservation of newly admitted meanings. The extended substitution maps
  both `α` and `alpha` to `alpha`; it is a retraction, not a lossless encoding.
- Repaired the Python codec's ASCII digit boundary, finite Unicode profile and
  missing raw-glyph representation. Checked serialization rejects malformed
  direct AST constructions. Extended tokenization now preserves invalid layout
  for refusal instead of silently dropping newlines.
- Removed Lean routines that assigned teleportation fidelity and anyon
  certification without calculating them. Retained actual rational arithmetic
  and the correction lookup table. Replaced assumed pure-gauge cancellation
  with a proof from the group laws. Marked supplied Smith/volume data as fixtures,
  required positive invariant factors, and separated a candidate Boolean from
  a verified or authorized lift.
- Proved that the former four domain “recovery gap” predicates say exactly that
  every element equals the designated root. An irreflexive witnessed pair refutes
  them. These are no longer advertised as continuum or undecidability theorems.
  Replaced fictional expert dialogues and scripted discovery claims with the
  concrete local model and its proof boundaries.
- Distinguished language restriction from a word decoder in the draft normal-form
  contract, removed the false full-contract execution label, and kept whitespace
  preservation explicit. Standardized retraction notation to `r_N` throughout
  active atlas rows without changing chain differentials.
- Clarified rational Hodge assumptions and nonunique potentials, the separate
  univalence obligation, all-orientation CHSH scope and exact squared Tsirelson
  comparison, and the boundary-word witness needed for noncommutative Bianchi
  cancellation. Cohomology operations must return cocycles; quotient comparison
  does not presume a norm over an arbitrary coefficient ring.
- Updated entry points to the already consolidated Paper 001 and marked the
  October 8 physics cleanup as a historical receipt. Its removals remain in force.

## Checks and limits

The grammar replay checks 39 cases over 22 starts. The two codec files have
88 passing tests, including observed pre-fix failures for the repaired input
boundaries. The positive/rejection cases are compared with the independent EBNF
recognizer; this is finite evidence, not a universal parser-equivalence proof.

The six top-level Lean modules and four corrected domain cores directly compile
with Lean 4.33.1. No `sorry` or new axiom was introduced. The new cancellation and
fixed-root lemmas are actual proof terms; fixture theorems retain their narrower
scope. A full Lake build under the package's requested Lean 4.34.0 was not run.

Targeted Python domain regressions pass: mathematics 5, computation 19, SQL 13,
and token/precedence examples 8. The computation file initially failed because
its subprocess could not find `lean`; rerunning with the declared compiler on
PATH passed. Tests are
run in separate processes because the examples reuse top-level module names.
A source inventory, exact commands, exit codes, compiler version, hashes and
remaining obligations are returned with this review; none is an authorization
or a physical correctness certificate.

No PDF, narrated video, release archive or full repository test suite was rebuilt
by this documentation correction set. The video source was updated. Per-row
historical evidence flags are catalog metadata and must not be consumed as fresh
verification receipts. Before extracting a construction into a canonical math
crate, bind its carrier, operations and equality to the corresponding source
construction and test the stated preservation and reflection laws.
