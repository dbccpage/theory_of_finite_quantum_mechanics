# Observer-presheaf checker review

AuthorityEffect: None.

The existing observer-presheaf source, six new single-class domain components
and four independent test sources receive retention label **5** and completed
**L4B** assessments. This adds eleven sources to the current systematic pass,
bringing its distinct completed total to 75. Label 5 is a retention decision,
not a perfection claim. Every current source has an adjacent source-bound
contract. The previous application and companion are preserved byte-for-byte
in the original-source archives; the existing companion history is appended.

## Findings and repairs

| Finding | Correction and regression evidence |
|---|---|
| The simplex boundary accepted a float objective, producing an exact representation of binary rounding; dimensions and arithmetic growth were not bounded. | `ExactLinearProgram` owns exact inputs, rejects float/bool aliases, admits at most 32 equations and 64 variables, checks 4096-bit products and prefixes, and limits search to 4096 pivots. Tests cover maximal dimensions, cancellation and pivot exhaustion. |
| Search failures and certificate truth were coupled; infeasibility could become a `None` unpack and unboundedness used process exit. | A closed certificate value distinguishes optimal, infeasible and unbounded. The aggregate independently verifies primal/dual/gap, Farkas, or descending kernel-ray witnesses before returning success. Expected failures use typed outcomes. |
| Scenario construction accepted boolean size, duplicate positions and mutable context aliases; negative restriction positions selected the last coordinate. | An owned scenario requires 1–6 measurements, 1–16 distinct increasing contexts covering the carrier, exact binary assignments and in-range nonrepeated query positions. Copies and detached exports prevent caller mutation. |
| Probability mixtures truncated unmatched rows through `zip`; out-of-range noise produced negative probabilities. | An empirical model owns every complete nonnegative mass-one row. Mixture requires equal scenarios; noise is admitted only in [0,1]. Signed cochains remain a separate domain. |
| Exponential enumeration lacked executable preflight; narrated Rust ceilings did not constrain Python. | Incidence is capped at 4096 entries, matching families at 4096 candidates, and LP dimensions are checked before allocation. Full-cover descent explicitly has no ambiguous extension category: each compatible family determines one assignment, whose global-support membership is tested. |
| The advertised Čech dual norm was not actually checked, and a gauge-shift upper bound was narrated. | The owned complex checks sup norm, annihilation on every zero-cochain basis coordinate, the actual shifted primal residual and equality of upper/lower bounds. Whole shapes are admitted even for an empty nerve; unequal edge/triple overlaps are tested. |
| Global `CHECKED` state prevented independent runs, and complex routines exceeded structural ceilings. | Per-run `Cases`, explicit boolean conditions, silent imports, bounded single-class components and compressed control routines replace global state and duplicate elimination logic. All 50 named CLI groups remain. |
| Literal parity/role/resource controls could be mistaken for broader proofs. | Every parity target is checked and its census verified. Historical Rust ceiling arithmetic, role/principal countermodels, finite executable evidence and universal/formal claims remain explicitly separate. |

## Verification and custody

The final quality receipt records strict pinned mypy over all eleven sources;
33 new test groups and the 24-group existing regression harness both normally
and with Python optimization; 20 existing DAG certificate cases; and the
existing DAG test requiring the `50 checks passed` CLI. All 13 commands pass.
Generated properties use 80 deterministic examples each. Independent bases
include SymPy vertex enumeration and signed reconstruction, direct binary
coordinates and marginals, and a forest oracle over all 64 simple graphs on
four vertices. Maximum CCN is 15, cognitive complexity 18 and nesting depth 4;
each source contains at most one class and no production assertions.

The initial 80-fault campaign detected 76 faults. Four survivor tests were
masked by other certificate conditions. Additive tests isolate negative
primal entries, dual infeasibility and a non-kernel unbounded ray while the
other conditions hold, and isolate primal Čech norm overflow from dual
overflow. All four then fail for their intended mutation. The original
tests, initial outcomes and exact additive changes remain recorded. A final
complete campaign on the final source, tests and manifest detects **80/80**,
with no invalid, equivalent, inconclusive, surviving or unrun candidates.
The unused application incidence adapter and its imports were removed before
that final replay; the exact prior bytes and diff remain preserved.

The original executable path, 50-group receipt and scalar `verify_lp` returning
`ValueError` on invalid certificates remain compatible with the audited DAG
consumers. Its newly explicit standard form requires nonnegative RHS; no
negative-RHS live caller was found. Constructors raise typed `Violation` for
failed admission; public fallible aggregate queries use `Outcome`, and the
application owns its CLI evaluation boundary. Internal simplex workspace and
fixture adapters are not independently exposed service APIs. Unexpected
programming errors and cancellation propagate.

The complete original source, derivation note, claim ledger, two DAG
derivations and `LggrFiniteResults.lean` were reviewed. Their digests and all
declaration-to-requirement/test mappings are recorded in the requirements
receipt. Imported sources and scientific DAG status are unchanged. This
assessment neither rebuilds Lean/Rust nor claims hosted CI success, universal
LP termination within the budgets, general sheaf exactness or a continuum
theorem. Source-checkout replay is recorded separately after guarded copying.

All sizes and operation counts are detailed in the contracts: finite bit
budgets are enforced on intermediate terms, not just final results. The
private tableau has at most 32×97 entries and 4096 pivots; binary scenario
size is at most six; every Čech degree has at most 4096 coordinates. Resource
refusal remains distinct from a mathematical infeasibility certificate.

The review continues with `fq-gap-born-uniqueness-gleason-mod2.py`, followed by
the remaining `checks` files before entering `code`.
