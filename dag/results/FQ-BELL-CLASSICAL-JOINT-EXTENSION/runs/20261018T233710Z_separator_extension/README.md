# Bell separator extension stage

**Stopped after P5 for review. Changes are uncommitted.** AuthorityEffect: None.
The full formal rational Fine converse remains open. Only this Bell target was
advanced; no external provider was dispatched. This was a local Codex/exact-solver
execution of the file-based PFP stage protocol, with separate native processes
and an independent certificate checker. No independent human/model review or
total chat-cost measurement is claimed.

## Result and boundary

Lean 4.33.1 proves that compatible positive pair **counts at a common integer
scale** admit a shared separator parameter iff the complete CHSH family holds.
It also proves existence of parameters satisfying the two explicit nonnegative
triple-cell systems, and the full scaled facet bound for arbitrary Nat-weighted
binary-assignment lists. These are general theorems, not grid exhaustions.

Rust and Python construct exact rational extensions by splitting triples and
conditional gluing. The independent checker accepted **3642 extension
witnesses** and **368 facet obstructions** over **4010 public inputs**.
Rust and Python agree exactly on all values and witnesses. The input family is
the complete compatible numerator grids with denominators 1,2,3,4, plus one
arbitrary-precision input. This finite evidence is not promoted to a universal
proof of the native implementations.

The general rational gluing marginal/unit-mass theorem, the conversion between
arbitrary Q-valued pair tables and integer PairCounts, and the connection from
positive cell systems to normalized Lean table arrays remain unformalized. The
native certificates check actual normalized arrays and projections. A complete
formal rational Fine converse requires those missing connections.

## Actual stage history

| Stage | Result |
| --- | --- |
| P0 | Mined exact pair compatibility, typed/refined operations, checking predicates and source pins. Public inputs contained no expected witnesses or classifications. |
| P1 | Submitted native witnesses and original Lean proof source. |
| P2 | All numerical witnesses and native tests passed; Lean rejected the source after a timeout and proof dependency errors. This attempt is retained. |
| P3 | Kept the target and inputs; expanded max/min bounds into linear constraints and repaired proof dependency/induction scope. The public repair packet contains bounded G5 feedback only. Local source work used normal compiler diagnostics; no blinded-trial claim is made. |
| P2 recheck | Repaired Lean anchors and replacement certificate binding passed. Unchanged Rust/Python source reused the original passed native receipts. |
| P4 | Rejected five false submissions and checked zero separator slices, incompatible input and mismatched triple marginals. Added a two-sided standard-CHSH control. |
| P5 | Collected complete typed generator/relation records, exact source snapshots, open obligations and next step. Stopped for review. |

Every executed checkpoint has `request.json`, original local response bytes,
candidate, host result and `operad_delta.yaml`. The responses are serialized
local artifacts, not fabricated remote-provider transcripts. Historical runs and
the earlier review folder were not rewritten. Current source hashes differ from
older runs' working-source pins as expected; their retained snapshots are still
historical evidence.

## Construction and operads

Observed pair order is 00,01,10,11; cell order is --,-+,+-,++.
For each B setting and outcome b, write

    u = P(A0=+, B=b), v = P(A1=+, B=b), w = P(B=b).
    max(0,u+v-w) <= t_b <= min(u,v).

The common separator mass r=P(A0=+,A1=+) must lie in both setting intervals
`[sum_b lower_b, sum_b upper_b]`. Once r is chosen, split each triple and glue by

    p(s,b0,b1) = T0(s,b0) * T1(s,b1) / q(s)   when q(s)>0,
    p(s,b0,b1) = 0                            when q(s)=0.

Nonnegativity and matching separator marginals force zero slice cells, so no
epsilon or arbitrary substitute denominator is introduced. A naive unconditioned
product has mass 1/2 on the retained uniform-pair control; the correct glue has
mass one. The new semantic operation chain is

    FeasiblePairData -> FeasibleSeparatorProblem -> SeparatorChoice
      -> CompatibleTriplePair -> JointLaw -> CompatiblePairData.

These context-retaining mathematical wrappers describe the native composition;
the constructor retains pair data in its local environment. No serialized
typestate API or formal Lean operad of probability subtypes is claimed. The
existing heterogeneous function-substitution model supplies ambient semantics;
specific new subtype transport and universal rational composition identities
remain obligations. `p5/operad_delta.yaml` records signatures, relations, checked
scopes, a rejected separator-incompatible composition, and open work.

All eight CHSH signed facets are checked. The supplemental compatible pair input
in `p4/two_sided_chsh_control.json` has standard CHSH value zero and another
facet value four: it passes both signs of the standard bound but has no common
extension. The earlier P4 control passed only the upper standard facet; its
precise limitation is retained rather than being relabelled.

Fine's original paper supplies target orientation, not an imported proof:
[Arthur Fine, PRL 48, 291 (1982)](https://doi.org/10.1103/PhysRevLett.48.291).
The source/proof work here is local. Physical locality and setting independence
remain additional assumptions.

## Verification and review

Actual checks passed: 10 new Python tests, 6 new Rust tests,
12 PFP protocol tests, 4 replay/schema guard regressions, four
named repaired Lean axiom reports, and all 4010 exact cross-language cases.
The failed kernel output is preserved separately and is never accepted as proof.
No full repository suite, `lake build`, or hosted-CI success is claimed.

From this directory:

    py -3.9 -X utf8 replay.py --working-sources
    py -3.9 -X utf8 -O replay.py --working-sources

Replay verifies saved bytes, all stage bindings, both numerical submissions,
required native receipt coverage, exact Rust agreement, actual mutation
rejections and source pins. It does not rerun compilers or authenticate the
artifact author. `manifest.json` seals the complete run inventory; `sources/`
and `inputs/` retain exact source/build bytes. `tools/` contains the actual local
construction scripts and fragments with their original worktree path; those
scripts may write checkpoints and are provenance, not a safe replay entry point.

The next mathematical step, after review, is the general zero-safe rational
gluing theorem and normalized table identity, followed by common-denominator
transport to connect the integer separator result to the full rational converse.
