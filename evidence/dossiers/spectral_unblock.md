# Unblocking C500: what is actually required, and one thing that cannot be repaired

AuthorityEffect: None. Citation: `sealed-derivation-v1` (`3100c4e`).
Reviewed object: CODA `origin/main` at `1ab791507be54ee6f29825d1beac66cb4308bc37`.
Author: Claude (Opus 5), reviewer. Not the owner, not an executor.

This is an analysis by one reviewer. It is not a plan the repository has
adopted, and nothing in it discharges a gap by being written down.

## 1. The state, pinned

| Fact | Source on `origin/main` |
| --- | --- |
| C500 is 250 targets, `C500-T301`–`C500-T550`, in ten blocks | `campaigns/c500/README.md` |
| Planning tree published, `execution_status: NOT_STARTED` | `campaigns/c500/sealed_targets.json` |
| PR #214 executed it once; that publication is withdrawn | `campaigns/c500_execution/WITHDRAWAL.md` |
| **All 250 original targets remain `OPEN` at their original scope** | `WITHDRAWAL.md`, and ten `GAP-C500-B01..B10` entries |
| Campaign terminal stands at `FQMC1_OPEN_INTERNAL_GAPS` | `c500_execution/block_10/result.json` |
| Eleven Codex bets intact, digest-pinned to reviewed head `1c20e420…` | `campaigns/c500/tools/verify_campaign.py` |
| Twelve blocking gaps: `GAP-C500-LAUNCH`, `GAP-C500-PINS`, `GAP-C500-B01..B10` | `claims/gap_register.yaml` |

Every kernel PR #214 produced is retained under `c500_execution/` with narrowed
claims. Those are usable inputs. They are not target discharges.

## 2. What blocks a relaunch

Launch precondition 9 and precondition 6 of `campaigns/c500/INSTRUCTIONS.md` are
the two that are not met, and they are not met for different reasons.

**Precondition 9 — the frozen `FQMC-1` class.** There is no
`class/fqmc1_class.json` anywhere in the tree. The contract requires it nonempty,
machine-readable, inhabited by a witness, SHA-256 pinned, and frozen *before the
first target executes*. Without it, clause-by-clause closure has no domain to
quantify over, and `GAP-C500-LAUNCH` says so. This is the single largest missing
artifact and it is also the cheapest to produce: it is a declaration, not a
computation.

**Precondition 6 — two independently authored bet sets.** The eleven Codex bets
are one planner's pre-registrations. `bets/INDEPENDENT_BET_SLOTS.md` asks for an
owner set and a reviewer set and neither exists.

Separately, `GAP-C500-PINS` records that 28 of 33 asserted predecessor blob
identifiers mismatched the publication commit. That is a custody defect, not a
launch precondition, and it is repaired by recomputing rather than by argument.

## 3. The thing that cannot be repaired

`GAP-C500-LAUNCH` puts it in one clause: *"fresh replay cannot repair their
historical timing."* That deserves to be stated at full strength, because it
changes what a relaunch can claim.

The withdrawn execution's ten `result.json` files, ten `RESULT.md` files and ten
`review.json` files are **public on `main` right now**. Anyone sealing a bet on
`C500-T301`–`C500-T550` today can read what the withdrawn attempt computed for
those very targets first.

So: **C500 can never again be a blind campaign on these 250 targets.** No
custody procedure fixes this; the information is already out. A relaunch has
three honest options and only three:

1. **Relaunch informed.** New bets are sealed and scored, and every one is
   labelled `INFORMED_NOT_BLIND` in the registry, with the reason. The campaign
   yields verified mathematics and no prediction record. This is the cheapest
   and it is not a defeat — most mathematics is done this way.
2. **Score what was blind.** The eleven Codex bets *were* sealed before any
   execution and their digests are pinned to a reviewed head. They can be scored
   against the withdrawn results as a recorded single-planner result. That is a
   real, if narrow, prediction record, and it costs almost nothing to produce
   because both halves already exist. It does not satisfy precondition 6, which
   asks for independence, not for a score.
3. **Move the blind protocol elsewhere.** Run the blind campaign on targets no
   executor has touched. That is what C750 and C1000 are for.

My recommendation is all three: do (2) now because it is nearly free, do (1) for
the relaunch, and let (3) carry the prediction programme. What must not happen is
a relaunch that quietly presents informed bets as blind ones — that is the same
class of defect the withdrawal was written to correct.

## 4. The unblock sequence

Ordered. Each step names what it produces and what it costs.

**Step 1 — freeze the class.** Write `campaigns/c500/class/fqmc1_class.json`:
every system with its carrier, scalar domain, states, effects, instruments,
composition, dynamics, and one inhabited witness per `FQMC-1` clause, plus an
emptiness guard and a freeze rule forbidding post-result restriction. Pin it in
the first block's `LAUNCH.json`.

`campaigns/c750/class/fqmi1_class.json` and `campaigns/c1000/class/fqmr1_class.json`
are working templates of exactly this shape, including the paired
witness-plus-negative-control pattern (`S6`/`S7`, `X1`/`X2`) that lets a block
fail its own claim at its own witness. Cost: hours, not days. This is a
declaration.

**Step 2 — recompute the pins.** For every C250 artifact any block consumes,
compute the SHA-256 fresh from the current tree. Do not copy from
`withdrawn_pin_audit.json`; that file is the record of what went wrong, and
reusing it reproduces the defect. Write the results into each block's
`LAUNCH.json`. Discharges `GAP-C500-PINS`. Cost: an afternoon, mostly scripted.

**Step 3 — settle the bet question.** Score the eleven Codex bets against the
withdrawn results and publish that as a single-planner record. Then decide
between options 1–3 of §3 and write the decision into the registry's
`independence_scope` field, where the existing
`SINGLE_CODEX_PLANNER_NOT_AN_INDEPENDENT_PANEL` string already sets the
precedent for saying this plainly.

**Step 4 — new execution root.** `campaigns/c500_execution2/`, distinct from both
the planning tree and the withdrawn root. Nothing under `c500_execution/` is
rewritten; it stays as the record.

**Step 5 — write the missing adjudication maps.** The withdrawal records that
block 01 listed 25 target adjudications and **blocks 02 through 10 had none**.
Before those nine blocks execute, each needs a per-target map: statement,
carrier, quantifier scope, dependencies, falsifier, and the one evidence class it
will receive. This is the largest documentation task and it is what makes the
difference between 225 targets that ran and 225 targets that were adjudicated.

**Step 6 — execute, one block per pull request.** Base `main`, independently
mergeable, local battery output verbatim in the body while hosted Actions is not
running.

## 5. The cost, honestly

250 targets, each requiring exact Python, an independent Rust reimplementation,
a Lean statement with a fresh axiom report, and a per-target adjudication. On the
evidence of what one block of this size has cost so far, finishing C500 at its
original scope is the largest single piece of work in this application.

Two ways to reduce it, both legitimate if declared before execution:

- **Re-issue at a narrowed target scope.** The contract forbids narrowing the
  *class* after results are read. Narrowing the *target set* before execution is
  a different act: issue it as `C500-R` with the dropped targets listed and each
  moved to the gap register as `OPEN`, not deleted. Honest, and it stops the
  campaign pretending to a completeness it will not reach.
- **Drop cross-language parity where it buys nothing.** Rust parity is
  valuable where an independent implementation could disagree. On a target whose
  content is a Lean theorem or a declaration, it is ceremony. Decide per target
  at Step 5 rather than per campaign.

What should not be dropped: the negative tests, the independent checkers, and
the per-target evidence class. Those are what distinguish this application's
output from the 741 inherited claims that lack mapped evidence.

## 6. Interaction with C750 and C1000

Neither consumes any C500 result; both say so in their contracts and both carry
a `c750_artifact_consumed` / predecessor-consumption field so the independence is
checked rather than asserted. So all three can run in any order, or in parallel.

If the author wants one thing to happen next, Step 1 is the highest value per
hour in the whole application: it is a few hours of declaration that discharges
the blocking half of `GAP-C500-LAUNCH`, and the same artifact is what C750 and
C1000 need before their own first blocks launch.

## 7. What this document does not claim

That C500's targets are the right targets. That the withdrawal was wrong — it was
right, and the analysis above depends on it. That any step here discharges a gap
by being written down; each discharges a gap by being executed and receipted.
That the effort estimates are anything but one reviewer's reading.

`AuthorityEffect: None.`
