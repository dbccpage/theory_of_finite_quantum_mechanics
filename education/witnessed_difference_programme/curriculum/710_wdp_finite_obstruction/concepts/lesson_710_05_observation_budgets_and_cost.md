---
documentation_contract: education-documentation/v1
title: 'Lesson 710.05: Observation budgets, calibrated reports and joint supports'
kind: pedagogical-lesson
track: 710
status: active
claim_status: written-theorems-and-finite-examples
authority_effect: 'None'
source_version: "2.4.1"
source_paths:
  - atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md
---

# Observation budgets, calibrated reports and joint supports

This lesson follows result R15 of the monograph's theorem map (Appendix T)
and the cost appendices that reuse it (§14.6, Appendices X and Y). It
assumes [lesson 710.02](lesson_710_02_exact_quotient_obstruction.md) and the
report-fiber criterion R2. It introduces no new Genesis stage.

Each statement below carries one of three separate completion labels, as
the monograph's theorem map requires:

- **[Written]**: the finite or conditional proof is in the monograph.
- **[Mechanized]**: a named Lean statement exists, with audited axioms.
- **[Executed]**: a native Rust or Python check replays the stated finite
  examples.

None of these labels implies another. Appendices T, X and Y are
[Written]. Their finite examples are [Executed] in `omega_wdp`. This lesson
cites no new Lean evidence for them.

## 1. Two questions, two budgets (Appendix T, WDP-DIM-1)

[Declared] Work over Q. Linear maps `D_s:U→V`, `D_r:F→V` and `Q:V→Y` are
given as matrices. Write `R = im D_s` (realizable defects),
`B = im D_r` (repairs), and `K = ker Q`. Do **not** assume `R = B`. Add
rows `E`, so the new observer is `A = (Q, E)`. Put `T = R ∩ K ∩ B`.

[Written] The sharp row counts are:

| Target | Condition on `A` | Sharp count |
| --- | --- | --- |
| Raw | `R ∩ ker A = 0` | `dim(R∩K)` |
| Quotient | `ker A ⊆ B` | `dim K − dim(K∩B)` |
| Joint | both | `dim K − dim(K∩B) + dim T` |
| Realizable quotient (WDP-DIM-R) | `R ∩ ker A ⊆ B` | `dim(R∩K) − dim T` |

The raw and quotient counts add up to more than the joint count. The excess
is `dim((R∩K)/T)`. It vanishes exactly when `R∩K ⊆ B`; the §10.6 case `R = B`
is one instance.

Work this example by hand before running anything. Take `V = Q^3`,
`Q = (0,0,1)`, `D_s` with columns `e1, e2`, and `D_r` with the single column
`e1`. Then `R = K = span{e1,e2}`, `B = span{e1}` and `T = B`.

1. Predict `m_raw`, `m_quot` and `m_both`.
2. Compare the separate sum with the joint count.

You should get 2, 1 and 2, with a separate sum of 3.

[Written] A submitted witness carries `lower_columns`. These are accepted
only as an obstruction basis for the claimed target, and matching width
and rank alone do not qualify. On the example above, the columns `e2, e3`
have width 2 and rank 2. They are still rejected because `e3 ∉ ker Q`.

[Executed] The producer/checker pair is in
[`distinct_image_completion.rs`](../../../../../../omega_engine/crates_rs/omega_wdp/src/distinct_image_completion.rs).
The checker recomputes every dimension from the matrices, using the exact
elimination owner in `linear_algebra`. It also covers three more cases:

- T.5 restricted menus: rows that annihilate `B`, and a priced finite shelf.
- The T.6 rule that a repair claim needs a replayed operation
  `D_adm u = r⋆ = δ`, with `r⋆ ∈ B`.
- The T.8 realizable-domain corollary.

The checker also applies the lower-columns rule to the realizable-quotient
target. That rule is an implementation extension; T.3 states it only for
the raw, quotient and joint targets.

## 2. Priced fixed and adaptive observation (§14.6)

[Declared] A finite set of candidates carries a free visible report, a
protected answer and a shelf of priced instruments.

- An unresolved pair has the same visible report and different answers.
- A fixed suite must separate every unresolved pair, which makes it a
  weighted hitting set.
- The adaptive value obeys this recursion: `W(C)=0` if the answer is
  constant on `C`; otherwise `W(C) = min_i [c_i + max_branch W(C∩branch)]`.

[Written] The LP relaxation of the hitting set is a lower bound and does
not certify the integer fixed cost. On the Fano plane, the LP optimum is
`7/3` and the fixed cost is `3`.

[Executed] [`observation_cost.rs`](../../../../../../omega_engine/crates_rs/omega_wdp/src/observation_cost.rs)
is a native port of the paper's `code/finite_observation/solver.py`. It
builds complete `2^m` fixed tables and complete `2^n` Bellman tables.
`verify_certificate_json` replays a submitted certificate row by row and
never calls the solver to repair a bad table. Its canonical instance digest
matches the Python digest, so the five stored Python certificates replay
natively.

## 3. Calibrated interval reports (Appendix X)

[Declared] A raw reading `r` converts to `z = γ r + δ` with `γ ≠ 0`. Each
candidate declares a nominal report and a radius in the calibrated unit.
X.1 transports a raw radius `ρ` to `|γ| ρ`.

[Written] An answer is certified when the compatible candidates are
nonempty and all share one answer. An empty compatible set means the report
is inconsistent with the model, which is different from acceptance.

The X.6 table has four candidates and three instruments with prices 1, 3
and 3. For radius `ε < 5`:

1. The fixed cost is exactly 7, because three pairs force B, A and C.
2. The adaptive cost is exactly 4: query A first, then B on the low branch
   or C on the high branch.
3. At `ε = 5`, the vector `(5,5,5)` is compatible with all four candidates,
   and both costs are infinite.

[Executed] [`calibrated_reports.rs`](../../../../../../omega_engine/crates_rs/omega_wdp/src/calibrated_reports.rs)
covers the check statuses (Verified, Abstain, Inconsistent, InvalidReport
and InvalidProposal) and the X.3 finite lift. It computes the X.4 costs two
ways, by the direct interval recursion and by lifting to the finite solver,
and the tests require the two answers to agree.

## 4. Joint supports keep the correlation (Appendix Y)

[Declared] Let one hidden error `e ∈ [−1,1]` affect two unit-price
instruments: `z1 = x + e` and `z2 = −x + e`, with `x ∈ {0,1}`.

[Written] Each marginal interval overlaps the other candidate's. The
product of marginals admits `(0,0)` for both answers, so its cost is
infinite (Appendix X). The joint support satisfies `(z1 − z2)/2 = x`, so
both exact costs are 2 (Y.6).

Y.1–Y.3 state the general criteria:

- **Fixed suites (Y.1).** A suite works exactly when the projected joint
  supports are disjoint for every cross-answer pair.
- **Adaptive recovery (Y.2).** The adaptive recursion must retain the
  residual joint support, not only the candidate set.

The crossing example in Y.3 shows why. After first readings `0` and `1/3`,
the same candidates `{0,1}` remain, yet the remaining costs are 1 and
infinity.

[Written] For finitely many rational affine segments, the Y.5
critical-value construction gives a finite witness `W` with `F_W = F_Ω`
and `A_W = A_Ω` (Theorem Y.4). The construction has three steps:

1. Take the segment endpoints.
2. For each first instrument, find the first-reading image endpoints and
   the isolated roots where two predictions agree. Partition the readings
   into cells at these values.
3. Keep the complete first-reading fiber at each cell representative whose
   answers differ.

Sampling only the endpoints is not enough. In the isolated cost peak,
which has prices 1, 1 and 3, endpoint sampling suggests cost 2. The
interior collision of A and B at `(0,0)` makes the true cost 3.

[Executed] [`joint_support_recovery.rs`](../../../../../../omega_engine/crates_rs/omega_wdp/src/joint_support_recovery.rs)
ports `code/joint_recovery/reference.py`. It provides:

- the collision early exit;
- the critical witness, which is refused rather than truncated above the
  10-world solver cap;
- the conditional remaining instance;
- the answer check, which uses one common parameter per segment.

The native tests replay all four stored Python certificates. The
model-digest field is not reproduced natively. Instance digests are
compared instead.

[Open] An independent per-coordinate residual thickens the support and
leaves the Y.5 class. An effective reduction for that larger class is the
monograph's next stated target.

## Laboratory Workbench

- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_710_05_observation_budgets_and_cost.ipynb)

## Run the native checks

From the repository root:

```powershell
cargo test --manifest-path omega_engine/crates_rs/Cargo.toml -p omega_wdp --test wdp_observation_completion_and_cost --test wdp_joint_support_recovery
```

A passing run covers only the stated finite examples and the stored
certificates. It does not establish the written theorems at their full
scope, and it does not show that any physical error model is valid.

## Retrieval and transfer

1. In the T.4 "neither inclusion" example, which vector spans `T`? Which
   count changes if you add `e3` to `B`?
2. Why does choosing `B = V` make `m_quot = 0` without solving the original
   defect? Which T.6 witness fields are then required?
3. Give one reason the Fano LP value `7/3` cannot be a fixed suite cost.
4. In X.6, why is a budget of 3 insufficient adaptively?
5. In the parity-points model, `L0 = {(0,0),(1,1)}` and
   `L1 = {(0,1),(1,0)}`. Why would matching each coordinate to a different
   component produce a false compatibility result?
6. Which assumption of Y.5 fails once an independent rounding residual is
   added to each coordinate?

Answers:

1. `T = span{e2}`. Adding `e3` to `B` gives `K ⊆ B`, so `m_quot` becomes 0.
2. The quotient map is injective, but no repair has been exhibited. The
   witness needs `(D_adm, u, r⋆, δ)`, with the matrix identities replayed.
3. A suite either contains an instrument or it does not. The LP allows
   fractional inclusion, so its optimum is only a lower bound. Here the
   integer optimum, 3, is larger than `7/3`.
4. Any budget below 4 cannot pay for A plus a second instrument, and B or
   C alone leaves different answers unresolved.
5. The certification rule needs one complete vector that extends every
   reading.
6. After one reading, the latent parameter is no longer unique, so the
   first-reading fibers need not be finite.
