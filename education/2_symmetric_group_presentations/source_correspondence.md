# Source correspondence and verification scope

AuthorityEffect: None. Reviewed 2026-10-09.

The source for this review is [19L57G1 at `f1d56c010e6ba10a3b9418bd7cc5953c067250f2`](https://github.com/dbccpage/19L57G1/tree/f1d56c010e6ba10a3b9418bd7cc5953c067250f2).
This strand develops an educational presentation of that work. Its stage labels,
ledger conventions, finite examples and wire grammar are later constructions.
They are useful ways to continue the programme, provided each map and its
preserved questions are specified.

| Topic | Pinned source | Construction in this strand |
| --- | --- | --- |
| Empty admitted regime; supply does not admit | `lean4/Derivation/Inertia.lean`: `genesis_underivable`, `supply_no_op` | Label S(0), ground syntax `<>`; Python empty-state example |
| Retention and collapse | `Inertia.lean`: `R2L_collapsed`, `R2F_collapsed` | S(2) labels the challenge; the local parsed-pair grammar is separate |
| First separation cost | `Minimality.lean`: `cost1_insufficient_general`, `mu2_unique`; `MinimalityF.lean`: `mu2_unique_F` | S(3), comparing declared item count and arity cost |
| Closure under an issued policy | `lean4/Derivation/Progress.lean`, Python closure implementation | S(4) labels selected closure work; it is not an automatic transition |
| Further external challenges | Source continuation policies and open questions | S(5) labels an issued continuation request |
| Exact partial recovery | No source theorem with S(6)/`NON_DESCENT` as this strand defines them | S(6), a section and a partial inverse on its actual image |
| Active and historical registers | Not source regime fields | Explicit W, H bookkeeping, supplied example counts |
| Finite examples E10–E21 | Not additional source stages | Written finite mathematical arguments; see each page's implementation scope |

The source inscription `<ab>` is **one opaque datum**. Reading L admits the
opaque wholes `<a>` and `<ab>`; reading F also retains `<>`. The flat S(n)
codec instead assigns `<ab>` the constructor `RetainedPair(a,b)`. That is a
declared interpretation in a new grammar, not the source token's intrinsic
structure. Similarly a parsed `<a->a>` is syntax, not evidence of an
irreflexive relation.

## What the executable files establish

- `code/sn_core.py` contains small finite examples. Its `s_n` and cost fields
  are declared inputs, not outcomes of a source replay or minimality search.
  Supply and admission have different methods. Exact descent tests whether
  the new coordinate is zero; it does not infer descent from a stage counter.
- `code/sn_realizations.py` checks the displayed elementary operations. A
  section/retraction test is not an adjunction theorem; a sum of dimensions
  is not a Hodge decomposition; an arrow involution supplies no composition.
- `code/sn_verification.py` is a local state-machine example. Verification and
  policy approval are separate calls. Callback results must be actual booleans.
  Neither callback authenticates a grantor or produces a digital signature.
- `code/sn_applications.py` has a finite join, a two-step channel toy and
  floating-point triangle/hinge calculations. The richer FIFO and Regge models
  in `domains/` are written specifications, not implemented by those toys.
- `grammar/sn_conformance_cases.json` contains syntax cases SN_001–SN_085.
  The high-numbered lift/retraction strings contain no proof, matrix, cost,
  permission or trace payload. They do not verify E10–E21 mathematics.
- `code/sn_audit.py` checks explicit syntax profiles, a finite witnessed
  irreflexive relation, bounded graph colouring, and YAML schema structure.
  A well-shaped normal-form contract is not execution of its stated verifier.

## Lean scope

`SnSyntax.lean` supplies flat syntax with bounded lowercase-letter and digit
constructors. It has no parser or cross-language equivalence theorem.
`SnCarrier.lean` declares finite example carriers as `Fin (carrierCard n)`;
the table of cardinalities is chosen, not derived from Genesis. The earlier
unbounded `higher` constructor, which incorrectly inhabited the ground carrier,
is removed.

`sectionLift` now accepts only `BasePresentation`: ground, supplied mark or
relation constructors. This type prevents the previous fallback from erasing
nested lifts, retractions or refusals into ground. `old_image_base` proves the
round trip for every value of that source type and every index. The decoder
refuses unlifted presentations, wrong-index lifts and unsupported bodies.
`ground_carrier_empty` proves the actual index-zero carrier is empty.

The table identities in `SnTheorems.lean` remain table identities. They do not
prove that a lone mark creates a demand, that closure is forced, or that
S(0)–S(6) is the only possible history. Source admission correspondence and a
categorical or physical interpretation require their own stated maps.

## Prescribed ledgers

For finite unresolved-demand sets W, let D be a subset of the old W and let B
be disjoint from W minus D. Then

\[
W'=(W\setminus D)\sqcup B,\qquad |W'|=|W|-|D|+|B|.
\]

The example `(0,1,1,1,0,1,1)` chooses demands and their discharge events.
It is not inferred from carrier size. H accumulates completed receipts while
the ordered event history retains event multiplicity and order. A cost-two
minimum, a two-endpoint relation and a two-entry ledger measure different data.
