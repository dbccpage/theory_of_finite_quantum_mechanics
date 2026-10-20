# Six-directory review checkpoint

AuthorityEffect: None.

133 subjects have 266 source-bound scoring/contract sidecars.
511 scoped test cases passed. 0 five-gate assessments are complete.
The L4A goal remains unfinished. Null gates are unassessed; known E findings remain visible.

Capability counts: L1=17, L2=6, L3=108, L4=2.
An individually reviewed L4 capability does not imply a completed grade A.

Designated faults: 70 killed, 2 survived, 0 equivalent, 0 invalid, 0 inconclusive, 0 unrun. R=0.9722222222222222.
The surviving LGGR early-return mutation changes allocation/error behavior but leaves final Boolean rejection intact.
The campaign ratio does not certify every file or all failure classes.

| Directory | Subjects | Completed assessments | Known E | Source functions above A ceilings |
|---|---:|---:|---:|---:|
| holonomy | 15 | 0 | 0 | 20 |
| homology | 19 | 0 | 0 | 1 |
| homotopy_type_theory | 25 | 0 | 0 | 6 |
| lie_theory | 21 | 0 | 0 | 35 |
| linear_algebra | 32 | 0 | 2 | 94 |
| local_green_global_red_lggr | 21 | 0 | 1 | 7 |

Structural counts include explicit source in disabled/test/support files and compatibility entries;
they are not a measurement of compiler-expanded production execution or a semantic defect count.

Established structural E subjects (none if the list is empty):


Counterexample controls establish these semantic/failure E subjects:

- `code/rust/src/linear_algebra/scalars.rs`
- `code/rust/src/linear_algebra/smith_form.rs`
- `code/rust/src/local_green_global_red_lggr/adequacy.rs`

These files are entirely disabled and require an explicit implementation/compatibility decision:

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
`qr` now returns `Result<Q, RationalConstructionError>`. Remaining public graph/connection/scalar
admission, external provider trust, consumer composition, numerical-interface policies,
per-file independent challenges and operational costs still require individual review.

No commit, push, PR or merge is asserted by this checkpoint.

The four former CCN-above-50 findings are cleared at the measured source boundary.
Other functions still exceed A ceilings. The dense Smith implementation now has
reviewed L4 capability, but the whole file is L4E because a separate sparse API
admits cheap (usize::MAX, 0, []) metadata and panics while allocating mul_vec([]).
The other demonstrated E subjects are the scalar provider's overflowing i64
ExactRing implementation and the public LGGR NaN-to-zero conversion helper.
That helper case does not establish that admitted evidence constructors accept NaN.

The primary 72-candidate campaign retains both survivors: the LGGR early-return
case and scalar component privacy under an incomplete filtered test command.
The separate 20261020T014249Z-mutations replay selects doctests explicitly and
kills the same privacy candidate. privacy_replay_comparison.json binds equal
source/candidate bytes and both commands; the original primary outcome is not
overwritten and the corrective replay does not inflate the primary ratio.

Sealed differential controls record 746 Smith output/error comparisons, 48 full
ordered detector diagnostic vectors, and 30 quintic validation outcomes. They
passed against pre-refactor bodies on exercised cases. One new workspace
refusal is intentionally not replayed against the old allocation path. These
controls are separate from the 511 ordinary scoped test cases.
