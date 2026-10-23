Status: AI-drafted, awaiting human review.

# Derivation note: finite non-locality of rooted tree dressing (DFM-CONTINUUM-INTERFACE)

**AuthorityEffect:** None.
**Target node:** `DFM-CONTINUUM-INTERFACE`
**Outcome:** Narrowed. The node stays OPEN. The continuum obligations in the node statement are not discharged.

## Setup

Let `G` be a group, written multiplicatively. The graph has vertices `{root, p, a, b}` and oriented edges

- `eRP : root → p`
- `ePA : p → a`
- `eRB : root → b`
- `eAB : a → b`

The supplied rooted tree is the three edges `eRP`, `ePA` and `eRB`. The chord is `eAB`. This tree is data. Nothing below proves that a spanning tree exists, or that every finite graph has one.

Transport follows the convention of the finite-graph dressing theorem. The empty walk at a vertex has transport `1`. An edge contributes its label. Reversing a walk inverts the transport. Concatenating walk `p` and then walk `q` multiplies with the later factor on the left: `transport(q) * transport(p)`.

The tree transport `T(v)` is the transport of the unique tree path from `root` to `v`. The rooted dressing is `u(v) = T(v)^{-1}`. The dressed label of an edge `e : s → t` is

`u(t) * U(e) * u(s)^{-1}`.

The closed star of the chord is the set of edges that meet `{a, b}`. Those edges are `ePA`, `eRB` and `eAB`. The edge `eRP` runs from `root` to `p` and does not meet `{a, b}`.

## Path products

The tree paths give

- `T(root) = 1`
- `T(p) = U(eRP)`
- `T(a) = U(ePA) * U(eRP)`
- `T(b) = U(eRB)`

Substitute the dressing into the chord:

`u(b) * U(eAB) * u(a)^{-1} = T(b)^{-1} * U(eAB) * T(a) = U(eRB)^{-1} * U(eAB) * U(ePA) * U(eRP)`.

The last step is associativity only. No element is assumed to commute.

## The star does not determine the dressed chord

Keep `U(ePA)`, `U(eRB)` and `U(eAB)` fixed, and replace `U(eRP)` by a different group element. The three star labels are unchanged, because `eRP` is not one of them. The displayed product changes whenever the two values of `U(eRP)` differ, since left multiplication by a fixed element `U(eRB)^{-1} * U(eAB) * U(ePA)` is bijective. In particular, if the three star labels are the identity and the outer label is `x`, the dressed chord equals `x`.

Three concrete checks, recomputed by `checks/independent/dfm-continuum-interface.py`:

- In the additive group of the integers, outer labels `2` and `5` with the other three labels `0` give dressed chords `2` and `5`.
- In `SL(2, Z)`, the same pattern with outer matrices `[[1, 1], [0, 1]]` and `[[1, 2], [0, 1]]` gives those matrices as the dressed chords.
- A non-identity choice `U(eRP) = [[1, 1], [0, 1]]`, `U(ePA) = [[1, 0], [1, 1]]`, `U(eRB) = [[1, 3], [0, 1]]`, `U(eAB) = [[0, -1], [1, 0]]` has dressed chord `[[-4, -5], [1, 1]]`. Replacing only `U(eRP)` by `[[1, 2], [0, 1]]` changes it to `[[-4, -9], [1, 2]]`. The opposite multiplication order is a different matrix, so the later-on-the-left convention is part of the result.

## General dependency API

For any group and directed graph, a typed walk is built from an empty walk,
an edge, reversal and composable concatenation. Its edge list is empty,
a singleton, unchanged by reversal, or the concatenation of the child lists.
Induction on the walk proves that labels agreeing on this list have equal
transport, including the noncommutative multiplication order.

A Plan supplies a root and a typed path to every vertex. For edge e its
footprint is e together with the two endpoint path lists. The evaluator uses
the inverse destination transport, the edge label and the source transport.
Agreement on this footprint therefore implies agreement of the evaluator.
Contrapositively, different outputs require at least one changed label in
the footprint. Any superset remains a sound certificate. This is a conservative
support, not a claim that every listed edge is necessary: cancellation can
make some dependencies redundant. No spanning-tree existence is inferred.

The original four-vertex example is a Plan client. The outside edge eRP occurs
in its footprint even though it misses the chord's closed star. The existing
finite counterexample therefore illustrates the boundary of the general API.
An independent exact SL(2,Z) checker exercises 85 loop words of length at most
three, 255 append cases, reversal and off-support changes; three malformed
paths are refused. Three selected semantic faults are detected. These finite
tests supplement the general kernel proof and do not establish a continuum.

## What is proved

On this supplied rooted tree, the dressed chord is `U(eRB)^{-1} U(eAB) U(ePA) U(eRP)`. Changing only the edge outside the closed star of the chord changes the dressed chord, while every label on that star stays fixed. The additive pair `2` and `5` is one witness.

## What is assumed

The group, the four-vertex graph, the orientation, the multiplication convention, and the rooted tree paths are supplied. The dressing map is the one already fixed by the finite-graph dressing theorem. No continuum field, smooth structure, or measure is used.

## What is open

The node statement still stands: a finite graph dressing theorem leaves smooth-field existence, patching, topology, locality of a continuum field, and continuum dynamics as separate obligations. The witness shows that one finite rooted dressing is not a function of the closed star. It does not define a refinement family, compatibility maps, a topology, or a convergence theorem, and it does not transport any identity to smooth gauge theory. The node stays OPEN.
