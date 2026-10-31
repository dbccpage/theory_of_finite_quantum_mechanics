# PR #492 review and repair

AuthorityEffect: None.

Reviewed head: `cf8ea2ce7838cc934ca85ef773d2190281f2e1aa`.
This branch incorporates #493 (`9e2ffdeba`) so that the inherited determinant,
chirality and replay defects are corrected together with the new material.
Review #493 first; both pull requests remain unmerged for the maintainer.

## Findings addressed

1. **Exact-input corruption.** The new holonomy converter used
   `limit_denominator(10**9)`. A nonzero `2^-40` entry became zero and made an
   invertible diagonal matrix appear singular. Float components now retain their
   exact binary rational values through `as_integer_ratio`, including NumPy
   extended precision. Intended rationals use `Fraction` or real/imaginary
   `Fraction` pairs. No rational reconstruction or trace rounding occurs.
   The two-by-two input shape and singular-matrix boundaries are tested.
2. **Another incorrect determinant formula.** TFQ-1050's new standalone checker
   used `s^8 - 4r^4 s^4`, giving `3/4` at `(m,r)=(0,1/2)` instead of `15/4`.
   It now compares the corrected polynomial to direct exact elimination.
   A separate standard-library construction checks all Clifford relations and
   the complete sixteen-by-sixteen colored periodic Wilson operator at four
   Wilson parameters. The independent check no longer labels scalar block
   examples as a full operator replay.
3. **Scope exceeded the statements.** The scalar link/onsite theorem contains no
   lattice or matrix. Its description now says so. The assembled theorem covers
   its explicit four-component/four-direction rational kernel under link-reversal
   adjointness; the original dimension-two/four and arbitrary-representation
   refinement remains OPEN. The theta calculation uses seven supplied charges
   and paired coefficients, with no derivation from a Dirac-index sector measure.
   Y-junction exchange is an actual collision-free path; its negative sign uses
   a supplied fermionic convention. Axis-label preservation is an assumption,
   not a derivation of dipole conservation or Hamiltonian dynamics.
4. **Replay provenance.** All three receipts are regenerated from actual pinned
   Lean 4.35 output. FQCD requests resolve in their actual nested namespaces;
   unmatched, duplicate or unsafe reports fail. The two FQCD receipts retain all
   31 audited declarations; the FSP receipt retains all 12. CI verifies the
   source/log hashes and exact declaration coverage for all three receipts.

The original reproductions are retained in
`dag/research/pr492_review/reproductions.json`. Current validation logs and
source pins are under `dag/research/pr492_review/`. The earlier
`campaign_tfq-1052_correction_validation.json` belongs to #493's original
snapshot; this review's validation records the combined branch.

No physical sign-free theorem, general dipole law, arbitrary Clifford-carrier
bridge, continuum limit or scientific target promotion is claimed.
