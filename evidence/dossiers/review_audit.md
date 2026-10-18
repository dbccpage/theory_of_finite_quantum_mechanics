# C250 review: finite results and unresolved bridges

AuthorityEffect: None.

This review supersedes the completion and scoring interpretations in the ten
historical block summaries. The campaign supplies finite models, conditional
proofs and useful counterexamples. It does not establish a complete derivation
of quantum mechanics or a necessary, independent and exhaustive price list.

The source reviewed was PR #207 at
`22824045918194a72a9557b9410bf5d2e5380b93`, integrated with CODA main at
`7df073e3f61130b51e905d035cbbcc2cb2eea856`. All 39 campaign application claims
have dispositions in [the claim review](c250_claim_review_20260907.json).
The current ledger and generated summary use those statements.

## Claim reconciliation

| Block | Defensible result | Remaining boundary |
| :--- | :--- | :--- |
| 01 | Conditional finite effect recovery and an unsharp-effect counterexample | Rational homogeneity takes a witness; the rational self-bracket is not real completion or a general Busch theorem. |
| 02 | Denominator clearing and CHSH multiplicity 25 | Four excluded root candidates do not exhaust rational roots without the rational-root theorem. |
| 03 | Integer Gram identities and an explicit mixed-state embedding example | The integer evaluation surrogate does not construct the real embedding bridge. |
| 04 | Nonzero imaginary numerators for every positive power of the rational rotation | Density needs topology; closure alone selects neither a time action nor a generator. |
| 05 | A rival bilinear map fails covariance; three product MUBs are constructed | General tensor uniqueness and the fourth dimension-six MUB remain open. |
| 06 | Complex Choi checks and a redundant rational Kraus construction | Selected square-root conductors do not bound every Kraus realization. |
| 07 | Checked finite Peres and Cabello models | A finite conductor-12 family does not establish the global least conductor. |
| 08 | Quadratic Sorkin identity and a separate inhabited triangle model | Root-multiplicity classification is cited; the SignRepair transport bridge is open. |
| 09 | Fixed-list denominator bounds and LCMs of declared conductor tables | Unbounded indices do not prove physical conductor necessity or construct a continuum. |
| 10 | A six-entry inventory and evidence-loss counterexample | Independence, exhaustiveness and the general terminal claim remain open. |

Meyer's coloring concerns the rational **unit sphere**, not all unnormalized
rational projective directions. The code and ledger now state that domain.
[Meyer (1999)](https://arxiv.org/abs/quant-ph/9905080).
The cited root-sum theorem concerns roots with nonnegative integer
multiplicities. A parity check or a stored conductor does not formalize its
classification. [Lam and Leung](https://arxiv.org/abs/math/9511209).

Declared target censuses remain inventories. Their labels are not independent
replays of every target implementation. Definitions and arithmetic reductions
in Lean remain useful, but their theorem names do not enlarge their statements.
In particular, the historical zero-price and conductor records prove only
their stored values. The review withdraws their broader interpretation.

## Two substantive corrections

For three complex amplitudes, write

```text
I3 = |a+b+c|² - |a+b|² - |a+c|² - |b+c|² + |a|² + |b|² + |c|².
```

Expanding each square, every single-amplitude term has coefficient
`1 - 2 + 1 = 0`, and every pair term has coefficient `1 - 1 = 0`.
Thus `I3 = 0` for arbitrary amplitudes under quadratic intensity, including
`a = b = c = 1`, whose sum is three. It is not a statement that three roots
sum to zero. A quartic intensity rule gives `81 - 48 + 3 = 36`, showing the
quadratic assumption matters. H065 proves the rational complex identity;
independent exact Python calculations check 27 rational complex examples.
The distinct triangle identity is proved in an inhabited two-coordinate
Eisenstein model with `omega² = -1 - omega`.

For integers `a >= 0`, `b > 0`, the rational weight `a/b` equals the sum of
`a*b` copies of `(1/b)²`. Given a rational mixture of Gaussian-rational
unitaries, use that many Kraus operators `U/b` for each weight. Then
`sum K* K = I`, and the resulting map is exactly the original mixture.
For depolarization, the Pauli weights are `1 - 3p/4, p/4, p/4, p/4`;
these are rational for `p = 1/3` and `p = 1/7`. They yield a Kraus family
and its stacked isometry over `Q(i)`, without the claimed square-root
extension. This construction permits additional Kraus operators. It makes
no assertion about a minimal orthogonal family or a prescribed unitary
completion. H063 proves the rational weight identity. Python independently
checks the Pauli matrices and trace identity; Rust checks the weights.

## Evidence and executable repairs

The channel checker retains imaginary components and exact binary values of
floating inputs. It checks every principal minor and exact Hermiticity.
For example, the Hermitian matrix with rows `(1, 2i)` and `(-2i, 1)` has
determinant `-3` and is rejected. Tiny negative minors are not rounded away.
Numerical channel fixtures declare their tolerance; passing them is an
approximate check under that tolerance. Exact rational fixtures use none.
Empty and malformed matrices and non-real partial traces are rejected.

The block validator requires existing files inside the declared root, checks
their actual SHA-256 hashes and rejects missing receipts, empty receipt lists,
false gates and integers masquerading as Boolean success. The scorer rejects
empty, malformed and duplicate machine clauses. A valid receipt followed by
a byte mutation supplies a negative control. The contextuality receipt's hash
now binds the bytes actually written on Windows.

The CLI emits the ten reports and an unresolved campaign outcome. Its older
22-target status field has its original finite-fixture scope. It supplies no
campaign-wide certification. H067 replaces synthetic success flags with an
inhabited collision: equal displayed labels can carry different verification
evidence, so no function of the label reconstructs every verification result.

## Replay and custody

[The custody manifest](c250_review_custody_20260907.json) records the original
Git blobs and SHA-256 hashes for 30 predictions, ten results and twenty
narrative summaries. Predictions are byte-identical to the reviewed head.
The old summaries remain in place with supersession notices. Current result
records retain the predecessor pointer and current receipt hashes.

The [machine report](c250_machine_review_20260907.json) replays all 191 machine
clauses: 94 HIT, 32 MISS and 65 OPEN, including clauses originally labelled
FORCED. A HIT compares the scoped recorded value; it does not prove the
mathematical predicate. Unsupported or narrower evidence is left OPEN.
Judged prose clauses remain unscored. Therefore the terminal report continues
to say that the standing bets are not fully scored.

From `apps/finite_qm`, replay with:

```powershell
python campaigns/c250/tools/replay_review.py
python campaigns/c250/tools/score_block.py --self-test
python code/consolidate_sources.py --check
python -m pytest code/tests -n 8 --basetemp C:/Temp/coda-c250-review -q
```

Create a writable external temporary parent before pytest. Run
`cargo test --release --locked` and
`cargo clippy --all-targets -- -D warnings` from `code_rs`, and `lake build`
from `lean4` using the locked Lean 4.33.1 toolchain. The
[native review record](c250_native_review_20260907.json) binds commands,
observed results and source hashes. Hosted Actions results are reported
separately on the PR; they are not replaced by local success.

The successful application build has 132 Lean sources and 1,145 printed
declaration reports, including the eight previously unreported dynamics
declarations. All reported dependencies lie in `propext`, `Quot.sound` and
`Classical.choice`; the 80 declarations using `Classical.choice` are explicit.
The receipt covers printed declarations and does not claim that every
declaration in every predecessor source project was freshly audited.
Historical source-project entries retain their stated historical scope.

The external sealed derivation is cited at
[`sealed-derivation-v1`](https://github.com/dbccpage/19L57G1/tree/3100c4ed5ce70d2b6cff6d2ccd3b0251cf918d0a).
Its mechanical receipt does not establish these CODA interpretations.
