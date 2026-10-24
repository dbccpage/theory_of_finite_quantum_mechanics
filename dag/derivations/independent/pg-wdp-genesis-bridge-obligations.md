Status: AI-drafted, awaiting human review.

# Derivation note: symmetrised adjacency is not a directed-step certificate

**AuthorityEffect:** None.
**Target node:** `PG-WDP-GENESIS-BRIDGE-OBLIGATIONS`
**Outcome:** Narrowed. The node stays OPEN. Register rows GEN-WDP-O01 through O05 are not discharged.

## What is asked

The node lists five open Genesis-to-WDP bridge obligations. O02 asks for a preservation and reflection map from a source transition or admission system to the WDP bridge. One candidate already in the sources is symmetrised adjacency of a finite window: the Bool `adj(u,v) || adj(v,u)`. The register does not say that this candidate is that map. The other four obligations are not treated here.

## Finite windows

Fix a natural number `m ≥ 1` and a function `adj` from pairs of vertices in `{0, ..., m-1}` to `{false, true}`. Call this a window. A directed step from `u` to `v` is the proposition `adj(u,v) = true`.

Define `pairDefect(u,v) = adj(u,v) || adj(v,u)`.

## Both directions off

The Bool disjunction `a || b` is false exactly when `a` is false and `b` is false. Applying that to the two adjacency bits gives:

`pairDefect(u,v) = false` if and only if `adj(u,v) = false` and `adj(v,u) = false`.

So the symmetrisation knows that an undirected pair is absent, and it forgets which way a present edge points.

## Directed-step certificate

Say that a Bool-valued function `φ` of a window and a pair is a directed-step certificate when, for every window and every pair,

`adj(u,v) = true` if and only if `φ(window, u, v) = true`.

The function that returns `adj(u,v)` itself is a certificate, on a window of any finite size. Its existence means that not every function of a window fails to be a certificate. In particular, a countermodel to one candidate is not a refutation of O02, which asks for some map and is not given a source admission system in this note.

## Two vertices

Let `edge01` be the window on vertices `{0,1}` whose only true adjacency is `0 → 1`. Let `edge10` be the window whose only true adjacency is `1 → 0`.

Then:

- `pairDefect(edge01, 0, 1) = true`
- `pairDefect(edge10, 0, 1) = true`
- `0 → 1` is a directed step of `edge01` and not of `edge10`
- `1 → 0` is a directed step of `edge10` and not of `edge01`

If `pairDefect` were a directed-step certificate, `pairDefect(edge10, 0, 1) = true` would force a directed step `0 → 1` on `edge10`. There is no such step. Therefore `pairDefect` is not a directed-step certificate on two vertices.

## No positive integer solution of `p² = 2 q²`

Suppose `q > 0` and `p * p = 2 * q * q`. The right-hand side is even, so `p * p` is even, so `p` is even: an odd `p = 2k+1` would make `p * p = 4k(k+1)+1` odd. Write `p = 2r`. Substitute:

`4 * r * r = 2 * q * q`, hence `q * q = 2 * r * r`.

Here `r > 0`, because `r = 0` would force `q = 0`. Also `r < q`: otherwise `q * q ≤ r * r`, while `q * q = 2 * r * r > r * r`. The pair `(q, r)` is a positive solution with a strictly smaller second component. Repeating the step cannot continue forever in the positive integers. This contradiction shows there is no such pair. The instance `p = q = 1` is the numerical check `1 ≠ 2`.

This arithmetic statement is the content of the separate row GEN-WDP-68 at general scope. It does not choose a scalar field, a probability, or a Hilbert carrier, so it is not O04.

## What is proved

On every finite window, symmetrised adjacency is false at a pair exactly when both directed adjacencies are false. On two vertices it is not a directed-step certificate, with the witness `edge01` versus `edge10`. The identity on adjacency is a directed-step certificate for every finite size, so the candidate's failure does not refute O02. No positive integers `p, q` satisfy `p * p = 2 * q * q`.

## What is assumed

Boolean disjunction, the ordering of the natural numbers, and division by 2 with remainder. No continuum, no Hilbert space, and no fact about the Genesis register beyond the names of the open rows.

## Independent checker

The checker enumerates all 16 two-vertex windows. Symmetrised adjacency is false exactly when both directions are off. The identity on the adjacency bit matches every directed step, and the constant-true map misses every window that is not full. `pairDefect` agrees on `edge01` and `edge10` at `(0, 1)` while the directed steps do not. The search `p * p = 2 * q * q` for `q = 1..200` finds no solution. A bit compared with itself, the literal squares `200^2` and `2 * 200^2`, and the identity `(2r)^2 = 4 r^2` are not rechecked.

## What is open

O01, O03, O04, and O05 are untouched. O02 remains open: no preservation and reflection map is constructed for a source transition or admission system. The identity certificate is the adjacency itself, not a bridge map. End-to-end discharge of the five obligations is not claimed.
