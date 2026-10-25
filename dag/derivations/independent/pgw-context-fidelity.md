Status: AI-drafted, awaiting human review.

# Derivation note: two-value context fidelity

**AuthorityEffect:** None.
**Target node:** `PGW-CONTEXT-FIDELITY`
**Outcome:** Narrowed. The node stays OPEN. The sealed Genesis grammar and the Rust `certifies` predicate are not this carrier.

## What is asked

The source asks for a trace semantics in which a trace valid at a declared context `s'` need not be valid at a different replayed state `s`, and for an execution contract that accepts a context binding only when that context equals the replay of the history. The trial transcript is the motivation. It is not given a formal trace predicate in the cited certifiers.

## Carrier

The carrier has two values, `false` and `true`. A history is a finite list of two events. `supplyDiamond` leaves the value unchanged. `designateA` sets it to `true`. Replay starts from `false` and applies the events from left to right.

There are two steps. `assertOnlyDiamond` is valid only at `false`. `assertHasA` is valid only at `true`. A trace is valid at a value when every step in it is valid there.

## A stale context does not transfer

Let `s` and `s'` be values with `s ≠ s'`. Define one step from `s'`: `assertHasA` when `s'` is `true`, and `assertOnlyDiamond` when `s'` is `false`. That step is valid at `s'` by the two clauses above, and it is not valid at `s`, because the two values disagree and each step accepts only one of them. The one-element list of that step is therefore a trace valid at `s'` and not at `s`.

There are 2 ordered pairs of distinct values, and the same one-step trace separates each of them. This count is the length of that filtered list, recomputed by the Lean definition `unequalPairs` and by the independent script.

## Sound contracts

Call a contract sound when every trace valid at an accepted context stays valid at `replay(H)`.

If the contract accepts `c` on `H` only when `c = replay(H)`, then validity at `c` is validity at `replay(H)`, so the contract is sound.

Conversely, suppose the contract is sound and accepts `c` on `H`, but `c ≠ replay(H)`. The one-step trace of the previous section is valid at `c` and not at `replay(H)`, which contradicts soundness. So a sound contract on this carrier accepts a binding only when the context equals `replay(H)`.

The equality contract is one such contract. The contract that accepts `false` on the history `supplyDiamond` then `designateA` is not: that history replays to `true`, and `assertOnlyDiamond` is valid at `false` and not at `true`.

## Two recorded histories

The one-event history `supplyDiamond` replays to `false`, so the only-diamond answer on it is `verified`. The two-event history `supplyDiamond` then `designateA` replays to `true`, so the only-diamond answer on it is `retracted`. The two answers differ because the two replays differ. Each answer is computed from the history it receives.

There are 7 histories of length at most 2: 1 empty history, 2 of length 1, and 4 of length 2. Replay on each of them is a function of the list.

## What is proved

On this two-value carrier, a one-step trace valid at `s'` need not be valid at `s` when `s ≠ s'`. A contract preserves trace validity at `replay(H)` if and only if it accepts a context only when that context equals `replay(H)`. The history `supplyDiamond` replays to `false` and answers `verified`; the history `supplyDiamond` then `designateA` replays to `true` and answers `retracted`.

## What is assumed

The two events, the two steps, and the left fold from `false` are the definitions of this carrier. No fact about the sealed six-event grammar is used.

## What is open

Trial 2, Result 15, Prompt 12, and the Prompt 17 window are not instantiated. `ValidTrace` here is not the Rust `certifies` predicate. A trace semantics for an arbitrary regime, and a verifier that reconstructs replay before certifying a Genesis step, stay open. The node stays OPEN.
