# WDP-APPX-JOINT-SUPPORT

Goal id: WDP-APPX-JOINT-SUPPORT

Selected scope for WDP-APPX-JOINT-SUPPORT is recorded in this note.

## Selected scope

Shared-noise control only. Candidates are {0,1}. The free report is the constant `*`. The protected answer equals the candidate. Instruments A and B each have price 1 in one cost unit. The declared joint supports are `L_0 = {(e,e): e in [-1,1]}` and `L_1 = {(1+e,-1+e): e in [-1,1]}`, with every slope equal to 1. The labelled carrier is the ten critical-cell worlds in the opened sampler's order:

1. `(0, (-1,-1))`
2. `(1, (0,-2))`
3. `(0, (0,0))`
4. `(0, (1/2,1/2))`
5. `(1, (1/2,-3/2))`
6. `(0, (1,1))`
7. `(1, (1,-1))`
8. `(0, (-1/2,-1/2))`
9. `(1, (3/2,-1/2))`
10. `(1, (2,0))`

On this carrier the exact fixed cost is 2 and the exact adaptive cost is 2. The same two integers hold for these two segments by the pointwise identity below, not by a limit. The product of the marginal intervals is a different carrier. Its stored ideal-product optimum is null. No independent residual, arbitrary support, physical law, or continuum limit is in scope.

The goal row is open and has no fence. Its listed source is the archive member `wdp_review_2026_10_08.md` inside `history.zip`, at the joint-support anchor. Grep found no anchor text in that zip. `read_file` was not used to decode the member. The anchor string appears in the goal record only. The stored status field of `WDP-APPX-WRITTEN` is `done`. The command `goal_dag.py show WDP-APPX-WRITTEN` was not run. This note uses the opened Appendix X, Appendix Y, the joint-recovery reference, the shared-error certificate, the correlated-enclosure certificate, and the shared-error test source. No pytest and no cargo run was executed for this note. Writing this note does not close the goal.

## Hypotheses

The hypotheses are selected for this carrier. They are inputs, not consequences of a continuum limit.

H1. One complete report vector is fixed. Each instrument is queried at most once. Strategies are deterministic functions of the exact reports received. A finite cost is a worst-case guarantee of the correct answer. Abstention is not a finite value of that objective.

H2. A history `(*, H, r_H)` admits candidate `x` exactly when one vector in the declared support of `x` matches `r_H` on every coordinate in `H`. Separate membership of each coordinate in its marginal interval is not that test. An empty admitted set is model inconsistency, not acceptance. An answer is certified only when the admitted candidates are nonempty and share that answer.

H3. On the ten worlds, the realizable supports are the listed vectors: five for answer 0 and five for answer 1. Exact optima on the carrier use those sets. On the two named segments, a vector is realizable only when one common `e` in `[-1,1]` produces both coordinates. The inclusion of each segment in the product of its marginal intervals is outer-bound validity only. It keeps answer soundness and the comparison of actual cost against product-model cost. It does not make every product vector realizable.

H4. Fixed cost is the minimum price of a suite whose joint projections separate every same-free, different-answer pair, or infinite when no suite does. Adaptive cost is the minimax recursion on the residual compatible worlds: 0 when the answer is constant, and otherwise the minimum over a remaining instrument of its price plus the worst remaining cost on a realized reading. The candidate set alone is not the state.

H5. Prices are the rational 1. Readings below are exact rationals. The opened channels for the joint model use raw gain 1 and raw offset 0, so the listed coordinates are both the raw readings and the calibrated reports.

H6. The product carrier is the opened `correlated_enclosure`: instrument `plus` has intervals `[-1,1]` and `[0,2]`, instrument `minus` has intervals `[-1,1]` and `[-2,0]`, each at price 1, for answers 0 and 1. It is not the ten-world list and not the two segments.

## Derivation

### Common parameter, not marginal membership

On every vector of the two named segments, `z_A - z_B = 2x`. Thus `(0,0)` lies in `L_0` at `e = 0` and does not lie in `L_1`: the parameter forced by `z_A = 0` on answer 1 is `e = -1`, and that parameter forces `z_B = -2`. The same difference equals `2x` on each of the ten listed worlds.

The one-reading history `(*, {A}, 0)` still admits both candidates. On the segments the forced continuations are `(0,0)` and `(0,-2)`. Both of those worlds are in the ten-world list, at rows 3 and 2, so the history is not certified on the carrier either.

The joint history `(*, {A,B}, (0,0))` admits only answer 0. The joint history `(*, {A,B}, (0,-2))` admits only answer 1. The joint history `(*, {A,B}, (0,1))` admits neither candidate: no common `e` produces it on either segment, and no listed world has those two coordinates. It is inconsistent, not vacuously accepted.

The opened `evaluate` implements that test. It solves the first reading for one parameter of one segment and requires every later reading to equal that segment's affine prediction. The opened shared-error test calls this on `(A,B) = (0,0)` and records verification of answer 0, rejection of answer 1, and abstention after the single reading `A = 0`. The same test records inconsistency for `(0,1)`. Those assertions were read. They were not executed in this pass.

### Sampler order of the ten worlds

The opened `sample_worlds` admits the lower endpoint of each segment first, then, for each instrument, every complete first-reading fiber at a critical-cell representative whose answers are not all equal. Upper endpoints and pure cells are not inserted by themselves. Dict insertion order is the world order.

The lower endpoints are row 1, `e = -1` on answer 0, and row 2, `e = -1` on answer 1. The first-coordinate critical values are `-1, 0, 1, 2`, because the two later-coordinate predictions are parallel and contribute no isolated root. The mixed representatives are `0`, `1/2`, and `1`, which insert rows 3 through 7. The second-coordinate critical values are `-2, -1, 0, 1`. The still-new mixed fibers are the reading `-1/2`, which inserts rows 8 and 9, and the reading `0`, which inserts row 10. The count is 10. No two of these vectors are equal. The opened test source asserts that count. This pass did not call the function.

### Fixed cost on the ten worlds

The empty suite fails because both answers occur. Instrument A alone fails: the reading `0` occurs at row 3, answer 0, and at row 2, answer 1. The readings `1/2` and `1` are likewise mixed. Instrument B alone fails: the reading `-1` occurs at row 1, answer 0, and at row 7, answer 1. The readings `-1/2` and `0` are likewise mixed.

The suite `{A,B}` separates every cross-answer pair because the ten vectors are pairwise distinct. Its price is `1+1 = 2`. It is the only sufficient suite. The fixed optimum on this carrier is therefore 2.

That 2 is the joint hitting cost. It is not the sum of two one-instrument optima. Each one-instrument problem on this carrier has no sufficient suite, so each one-instrument robust cost is null, not 1.

The stored shared-error fixed table matches this partition: masks 0, 1, and 2 are insufficient at price strings `"0"`, `"1"`, and `"1"`, and mask 3 is sufficient at price string `"2"`. The stored fixed value is `"2"`. The adaptive table was not re-audited row by row. Its stored value string is `"2"`.

### Adaptive cost on the ten worlds

There is one free-report fiber, and the answer is not constant on it. Query A splits the ten worlds into seven readings. The mixed readings and their residual vectors are

- `0`, with `{(0,0), (0,-2)}`;
- `1/2`, with `{(1/2,1/2), (1/2,-3/2)}`;
- `1`, with `{(1,1), (1,-1)}`.

B separates each pair at added cost 1. The other four A-readings, `-1`, `-1/2`, `3/2`, and `2`, are pure and cost 0 more. The worst child is 1, so the option "query A first" costs 2.

Query B has three mixed readings,

- `-1`, with `{(-1,-1), (1,-1)}`;
- `-1/2`, with `{(-1/2,-1/2), (3/2,-1/2)}`;
- `0`, with `{(0,0), (2,0)}`.

A separates each at added cost 1. The other four B-readings are pure. This option also costs 2. The adaptive optimum on the carrier is therefore 2.

Querying both instruments is a sound upper bound of 2. On this carrier it equals both exact optima. The two mixed histories after a first reading have the same candidate set `{0,1}` and different residual vectors. The candidate set alone would not state the remaining cost.

### These two segments, without a transfer theorem

Restriction to the ten worlds cannot raise either cost, so both optima of the two named segments are at least 2. For the matching upper bound, use the identity on every admitted `e`, not a limit of the sample. If both instruments are read, `(z_A - z_B)/2` equals the candidate. No complete vector belongs to both segments. The suite `{A,B}` therefore suffices on the segments, and its price is 2. Hence the segment fixed cost is at most 2, and the segment adaptive cost is at most the fixed cost.

The same realized collisions give the adaptive lower bound directly. After `A = 0`, the only admitted continuations are `(0,0)` and `(0,-2)`, answers 0 and 1, and B separates them at cost 1. After `B = -1`, the only admitted continuations are `(-1,-1)` and `(1,-1)`, and A separates them at cost 1. Every first query therefore has worst-case cost at least 2. Both segment optima are exactly 2.

This check uses the explicit parametrization of these two segments and four admitted points. It does not invoke the critical-cell theorem, and it does not encode every report. Theorem Y.4 in section Y.5 is the monograph's general transfer from a critical witness to a declared affine support. It was not re-proved here. Theorem Y.3 in section Y.4 is an existence proof that some finite witness preserves both costs for an arbitrary declared support. Its selection uses the true branch optima. It is not an algorithm, not an encoding of every report, and not the carrier above. Section Y.7 states that an independent residual added to each coordinate leaves a parameter range after one reading, so the finite-fiber reduction does not apply to that larger class.

### The marginal product is a different carrier

The coordinate enclosure uses `plus` intervals `[-1,1]` and `[0,2]`, and `minus` intervals `[-1,1]` and `[-2,0]`, each at price 1. The product vector `(0,0)` lies in both rectangles: `0` meets both `plus` intervals and both `minus` intervals. No suite separates the answers. Appendix X.6 records both product optima as infinite. The opened enclosure test is written to abstain at the joint report `(0,0)`.

In the stored ideal-product certificate every fixed row is insufficient, including mask 3, whose price string is `"2"` and whose sufficient flag is false. Both the fixed value and the adaptive value are null. Infinity, and the stored null that stands for it, is a sound but uninformative upper comparison with any actual support contained in the product. It is not an exact optimum. The insufficient price entry `"2"` must not be reused as one.

On the actual joint report `(0,0)`, only answer 0 is compatible with one common parameter. The product model abstains there because it treats the two zeros as separately realizable. Outer validity supplies `F_actual <= F_box` and `A_actual <= A_box`. With `F_box` infinite, that comparison does not identify the exact value 2.

The opened shared-error test is written to check the pair `("2","2")`, the count 10, verification of answer 0 at joint report `(0,0)`, rejection of answer 1 there, and abstention by the enclosure. No test was executed for this note.

## Claims this note does not make

- It does not claim a continuum limit, a physical noise law, a calibration traceability result, sensor authentication, or action authority.
- It does not claim a closed cost theorem for an arbitrary joint support, for an arbitrary subset of real report space, or for segments thickened by independent per-coordinate residuals.
- It does not treat a product of coordinate enclosures as a realizable joint support. An infinite product cost is not physical impossibility, and an outer bound is not an exact optimum or a physical lower bound.
- It does not treat the insufficient product-table price `"2"` as a product optimum, and it does not treat either one-instrument null as the number 1.
- It does not treat Theorem Y.3 as a decision procedure or as a finite code for every report. It does not re-prove Theorem Y.4. The six Lean transfer lemmas do not formalize this cost theorem. The reference is not a general joint-support solver and does not implement the continuous policy controller described in the monograph.
- It does not use the crossing model at `(1/3,1/3)`, the parity-point supports, or the interior cost-peak supports as this carrier. An endpoint-only sample of a different support is not an exact optimum of that support.
- A cap, a 256-bit input refusal, or a witness above the ten-world solver limit is not mathematical infeasibility. No such refusal was exercised here.
- The archive member inside `history.zip` was not byte-decoded, so no joint-support optimum is certified from that review. The stored `done` field of `WDP-APPX-WRITTEN` is not a run of `goal_dag.py show`. This note does not close `WDP-APPX-JOINT-SUPPORT`.
