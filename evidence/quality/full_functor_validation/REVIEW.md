# FullFunctor declared-lift review

AuthorityEffect: None.

The attachment ends mid-test. The implemented API follows its obligation/witness
model while keeping supplied-list validation separate from actual fullness.

Corrections to the proposal:
- A target arrow absent from F's image can be exactly the missing lift that
  obstructs fullness. It is not excluded from the obligations for that reason.
- The lists do not encode completeness or a lift for every source-object pair.
- Duplicate raw-map keys are rejected before indexing; they cannot overwrite.
- Empty maps cannot support a populated record. Internal-only checking remains
  available through validate_shell.
- Duplicate witness copies are deduplicated in multiply_preimages. Cross-Hom
  collisions do not refute faithfulness. Diagnostics sort by full arrow tuples.
- The bound-Functor entry point checks functor_ref as well as the supplied maps.

The scope-counterexample test uses admitted finite categories and a lawful
functor from a discrete two-object category to a terminal category. The record
passes its supplied-list checks and the functor is injective on each source
Hom-set, but two cross-object pairs have no lift of the target identity.
This is a finite runtime witness, not a Lean theorem.

Validation: 494 library tests, four serde boundary tests, and twelve corrected
guard mutations. A first attempt had four killed mutants, one invalid
type-inference recipe, and seven unrun cases; every original log and recipe
is retained separately. No mutation percentage is claimed.

Compatibility: constructors are retained; omitted new lists in legacy JSON
default to empty and are explicitly vacuous. External Rust struct literals
must now supply the new fields or use constructors. Deserialization and public
mutation remain raw boundaries; validated() checks only the current candidate.

Assessment: L2D, with an adjacent byte-bound scored contract. The canonical
workspace/build hook and optional external packages were not compiled through
the test harness. Governance still requires L4; no exception, baseline or policy
change is applied. Sealed sources and derivation statuses are unchanged.

Superseded (2026-10-23): explicit maintainer approval later permitted an
exact-source baseline-floor exception for these source bytes; see
evidence/quality/functor_shell_pr/exception_authorization.json. The L2D score
and the global L4/D floor are unchanged. The assessment above is historical.
