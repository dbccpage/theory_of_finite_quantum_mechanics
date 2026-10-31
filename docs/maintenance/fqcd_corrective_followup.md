# FQCD corrective follow-up for PRs #486 and #489

AuthorityEffect: None.

The working branch starts from remote main `86d8ccb0446e`. The reviewed merges
are `8ad7f27a8091585f940cff2e3b3fe2f2ac59e881` and
`aac4b75da6046b83e1e8b946da689f4180bf8f47`.

## Mathematical corrections

For the specified periodic two-by-two Wilson background, put `s = m + 2r`.
The determinant is

```
s² (s² - 2r²) (s² + 2) (s² + 2 - 2r²).
```

At `r = 1` this reduces to `s⁸ - 4s⁴`. At `(m,r) = (0,1/2)` it is `15/4`;
the previous general-parameter formula gave `-3`. The Python tests construct
the matrix independently from the spin projectors and gauge links, compare
all entries, and calculate its determinant at nine parameter pairs, including
zero and negative Wilson parameters and singular matrices. A symbolic matrix
determinant comparison checks the general polynomial as well. The standalone
checker uses rational Gaussian elimination. Lean proves identities and signs
of the corrected polynomial; it does not formalize the eight-by-eight determinant.

With `D = (I + Γ₅ε)/a`, `Γ₅(I-aD) = -ε`, so its square is `(c²+b²)I`.
The corrected Lean statement constructs these matrices, proves their square
for every nonzero rational spacing and every rational `c,b`, and proves the
unit-circle involution. Python tests actually multiply the matrices at `(1,0)`,
`(-1,0)`, `(3/5,4/5)`, `(5/13,12/13)` and the off-circle point `(2,3)`, at
three nonzero spacings. Zero spacing is explicitly rejected by the Python helper.

The tensor-depth outputs are power-counting estimates. Python result keys now
start with `power_counting_`; the historical function name remains available.
Lean and Rust documentation and the manuscript use the same interpretation.
These monomials omit character multiplicities, factorial coefficients,
normalization and higher orders and do not supply Wilson coefficient ratios.

Theorem 15 describes fixed genus-three sums and their comparisons with genus
two. Theorem 17 describes five defect sums, three candidate contraction values,
Euler-exponent identities and listed count expressions. Historical declaration
names remain available for existing references. Neither a general genus limit
nor a transfer-matrix spectral theorem is claimed. The corresponding general
DAG targets remain OPEN; no DAG status is promoted.

## Replay and governance

Run with the repository-pinned Lean toolchain on `PATH`:

```
python -I -X utf8 scripts/replay_fqcd_lean.py
python -I -X utf8 scripts/replay_fqcd_lean.py --verify-receipt
```

The first command builds the module and explicitly requests kernel axiom
reports for its audit declarations. It writes the receipt only after checking
exact fully qualified name coverage, the axiom allowlist, the pinned Lean
version and unchanged input hashes. The retained log supplies the actual
axiom lists. Offline verification rejects stale pins, altered logs, unmatched
names, duplicate reports and unexpected axioms. Governance CI also runs that
verification. In this module declarations are `FQCD.<name>`; the file's module
name `FQCD.StrongCouplingAreaLaw` is not their namespace.

The PR #489 retrospective uses the immutable pre-merge base
`16a9464c666eb19693244442f64e003f26a36ed4` and the original merge snapshot.
The retained before/after receipt records the original five binding failures
and the result of applying the corrected FQCD sources and refreshed companions
to that snapshot. It does not compare an old base against later unrelated
changes on current main. Contract and score records are appended; their
historical bytes are retained.

CI selects the pull request's recorded base SHA, the push event's `before` SHA,
or the explicit `base_sha` input for manual retrospective runs. It prints and
checks the resolved commit and uses it for all changed-source checks. A
regression test puts stale source bytes on a simulated moving main and
shows that a check against the recorded pre-change SHA still detects the
binding failure. Empty changes remain valid when there were genuinely no
governed edits.

Validation results and source hashes are recorded in
`dag/research/campaign_tfq-1052_correction_validation.json`. These results are
bounded checks of this correction, not a certification of the whole repository.
