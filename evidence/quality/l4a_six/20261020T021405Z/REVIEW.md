# Six-directory review checkpoint

AuthorityEffect: None.

133 subjects have 266 source-bound scoring/contract sidecars.
519 scoped test cases passed. 2 five-gate assessments are complete.
The L4A goal remains unfinished. Null gates are unassessed; known E findings remain visible.

Capability counts: L1=17, L2=6, L3=106, L4=4.
An individually reviewed L4 capability does not imply a completed grade A.

Designated faults: 92 killed, 2 survived, 0 equivalent, 0 invalid, 0 inconclusive, 0 unrun. R=0.9787234042553191.
Every survivor remains disclosed in the bound campaign; no survivor is silently reclassified as equivalent.
The campaign ratio does not certify every file or all failure classes.

| Directory | Subjects | Completed assessments | Known E | Source functions above A ceilings |
|---|---:|---:|---:|---:|
| holonomy | 15 | 0 | 0 | 20 |
| homology | 19 | 1 | 0 | 1 |
| homotopy_type_theory | 25 | 0 | 0 | 6 |
| lie_theory | 21 | 0 | 0 | 35 |
| linear_algebra | 32 | 1 | 1 | 93 |
| local_green_global_red_lggr | 21 | 0 | 0 | 7 |

Explicit individual gate decisions (null remains unassessed):

| Subject | G1 | G2 | G3 | G4 | G5 | Result |
|---|---|---|---|---|---|---|
| holonomy/matrix.rs | null | null | null | A | null | incomplete |
| homology/graded_vector.rs | B | A | C | null | B | incomplete |
| homology/rank_certificate.rs | A | A | B | B | B | L4B |
| linear_algebra/smith_form.rs | B | A | B | B | B | L4B |

A completed B assessment remains below the requested A target.

Structural counts include explicit source in disabled/test/support files and compatibility entries;
they are not a measurement of compiler-expanded production execution or a semantic defect count.

Established structural E subjects (none if the list is empty):


Counterexample controls establish these semantic/failure E subjects:

- `code/rust/src/linear_algebra/scalars.rs`

These files are entirely disabled and still require executable L4 replacements:

- `code/rust/src/homotopy_type_theory/a_infinity.rs`
- `code/rust/src/homotopy_type_theory/quasi_category.rs`
- `code/rust/src/homotopy_type_theory/substitution.rs`

Focused changes cover overflow-free trace comparison, typed rational construction,
LGGR product/witness admission and lazy witness generation, and typed holonomy endpoint failures.
The holonomy matrix now has private admitted storage, typed access/setters/decoding, a sealed Q/Q(i)
scalar domain, borrowed admitted scalar operations, exact elimination and cell/work preflight.
Its independent finite matrix challenges and API privacy doctests are recorded separately from grading.
Root Gaussian components are now private and admitted through checked construction/decoding.
Rational hashing refuses undefined fractions before hasher mutation; homology digest and manifest
APIs propagate typed failures while retaining the existing valid-input byte frames.
The four former CCN E functions have been factored into admitted/validation phases; the rank
certificate identity phase is also factored. Smith workspace admission precedes allocation,
and its extended-Euclid loop is iterative. Sealed differential controls are separate evidence
and are never counted as ordinary production baseline tests.
Sparse vector/dense conversion now admits output and metadata storage before fallible allocation.
Finite binary64 conversion returns a typed refusal for NaN or infinity and preserves supplied binary values.
Zero-rank certificates check M=0 after shape/domain admission and handle huge zero-area metadata directly.
`qr` now returns `Result<Q, RationalConstructionError>`. Remaining public graph/connection/scalar
admission, external provider trust, consumer composition, numerical-interface policies,
per-file independent challenges and operational costs still require individual review.

No commit, push, PR or merge is asserted by this checkpoint.

The successful 94-candidate campaign is `20261020T022308Z-mutations`.
Its five untouched and five restored package baselines all passed, every
candidate source was restored, and source/dependency hashes remained stable.
Both surviving candidates remain recorded:

- LG06 removes the early zero-Dv refusal. Final Boolean rejection remains, but
  extra multiplication/allocation work is no longer skipped; that work ordering
  has not been decisively challenged.
- RK05 removes the matrix hash precheck. Identity replay still rejects a changed
  matrix. Tests did not require the specific binding diagnostic or skipped
  replay work; no forged-certificate acceptance was demonstrated.

The earlier disk-guarded `20261020T021802Z-mutations` attempt remains separate:
1 killed, 93 unrun. Its source manifest equals the successful retry's manifest.
The retry admitted commands at 2 GiB free based on scoped caches observed below
1 GiB. The receipt records this as pre-command headroom, with external disk
activity outside that admission guarantee. This review's build caches were
removed at completion.

Fresh six-control observations are in `20261020T022912Z-defect-controls`.
Only the external i64 ExactRing overflow reproduced. Gaussian raw admission,
NaN coercion and sparse huge-capacity panic did not reproduce. Two newly
suspected boundary/coboundary capacity panics also did not reproduce: the live
provider already uses fallible reservation. The interpretation note is bound
into the sidecars. These counterexample controls are separate from the 519
ordinary scoped test cases.

The current public API migrations are `SparseColMatrix::from_dense` returning
`Result` and `float_to_rational` returning `Result` for finite binary64 admission.
Repository callers were checked and adapted. Rank-certificate public signatures
are retained; its zero-rank construction and checker product paths changed.

The two completed L4B assessments are rank_certificate.rs and smith_form.rs.
Both still require A remediation. The shared graded-vector file has reviewed
L4 capability with incomplete engineering evidence. The holonomy matrix has
G4 A for its independent finite challenges and 18 detected designated faults;
its other gates remain unassessed. Three disabled HoTT files now have concrete
implementation obligations, but still deliver no executable replacement.
