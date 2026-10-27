Status: AI-drafted, awaiting human review.

# Untwisted finite-group counting under four-dimensional Pachner moves

AuthorityEffect: None.

For every finite group G, count flat oriented edge connections on the canonical
1–5, 2–4 and 3–3 Pachner balls, with a fixed flat connection on their common
boundary. Divide the number of fillings by |G| to the number of interior
vertices. The two local amplitudes agree. The corresponding normalized counts
also agree after gluing to any finite family of compatible exterior
configurations, represented by dependent pairs.

This supplies a particular model for `FSP-PACHNER-INVARIANCE-CLAIM`. The original
source did not specify a partition function, and its cited Lean declaration
was absent. The result here chooses untwisted finite-group gauge counting.
It does not justify invariance of every triangulation sum or of the Regge
action. The node's statement is narrowed to the theorem above; its status
applies to that statement. This is a **Narrowed** campaign result.

## Choice of target

The campaign queue measures downstream impact, not mathematical difficulty.
This was the next unclaimed high-impact target after excluding recorded
attempts and targets already held by open pull requests. It was chosen for
the substantial obligation of verifying all three four-dimensional moves
with boundary data, rather than checking only a single group or closed ball.
The supplied-group connection convention is `DFM-GROUP-CONNECTION`.
The Regge action is historical context, not a premise of this proof.

## The model and its actual local complexes

Use the six vertices 0,…,5. A facet is the five-element set obtained by
omitting one vertex. For p = 1, 2, 3, let the left ball consist of the facets
omitting a vertex less than p; let the right ball consist of those omitting
a vertex at least p. Their common subcomplex is the boundary used here.
`facetFace`, `localFacets`, `face_is_in_a_facet` and
`local_facets_have_five_vertices` identify this finite combinatorial model.
The facet, edge, triangle and interior-vertex identities are checked by
ordinary kernel reduction over `Fin 6`.

| Move | Facets, left/right | Boundary vertices | Boundary tetrahedra | Interior vertices, left/right |
|---|---|---|---|---|
| 1–5 | 1 / 5 | 5 | 5 | 0 / 1 |
| 2–4 | 2 / 4 | 6 | 8 | 0 / 0 |
| 3–3 | 3 / 3 | 6 | 9 | 0 / 0 |

The independent script constructs every face from these facets and recomputes
the table. The Lean `*_boundary_skeleton` theorems identify the common edge
and triangle sets with the predicates used in the algebraic proof.

A connection assigns e_ij in G, with e_ii = 1 and e_ji = e_ij inverse.
Flatness on a triangle means e_ij e_jk = e_ik, in this order. Missing edges
are represented by identity placeholders. They have no free labels and are
not extra edges in the complex. Repeated-vertex equations are consequences
of the connection laws. The model has no cocycle twist or additional
simplex weight.

For fixed boundary b, let F(b) be the finite set of flat fillings and let n
be the number of interior vertices. Define A(b) = |F(b)| / |G|^n in the
rationals. A group is nonempty, so the denominator is nonzero. This is a
normalized count of connections, not a count of gauge orbits with each
orbit assigned unit weight.

## Flat connections from a root

Flatness on a triangle (r,i,j) implies

    e_ij = (e_ri) inverse · e_rj.

Thus a complete flat connection is determined by one row of edge values.
Conversely, any potentials p_i define a flat connection by
e_ij = p_i inverse · p_j. Both statements use only group cancellation and
associativity; commutativity is never assumed.

## The 1–5 move

The left side is the simplex on vertices 1,…,5. Its boundary has the same
edge and triangle sets, so every flat boundary has exactly one left filling.
On the right, vertex 0 is interior, and the edge and triangle sets are
complete on all six vertices.

Take root 1. For any t in G set p_0 = t and p_i = e_1i for i different from
0. The associated potential connection extends the boundary. Conversely,
any right filling has t = e_10 and is recovered by this construction.
`oneFillingEquiv` proves the explicit bijection F_right(b) ≃ G. Hence the
counts are 1 and |G|, and the normalized amplitudes are both 1.

`unnormalized_one_five_iff` additionally proves that omitting normalization
gives equal raw counts exactly when |G| = 1.

## The 2–4 move

The common boundary and left side have every edge except 01, and all
triangles that avoid that edge. Root 2 meets every vertex, and (2,i,j) is
a boundary triangle for every boundary edge ij. Setting p_i = e_2i gives
a flat complete connection on the right, extending the boundary.
Every right filling has the same root row and is therefore this filling.
Both sides have exactly one filling and neither has an interior vertex.

## The 3–3 move

Both sides have all edges. The left side omits triangle 012; the right
omits triangle 345. Their common boundary omits both. For any triangle
(i,j,k), there is a vertex r such that (r,i,j), (r,j,k) and (r,i,k) all
lie in the common boundary (`boundary_has_triangle_cone`). The three
boundary flatness equations imply

    e_ri (e_ij e_jk) = e_rk = e_ri e_ik.

Cancellation gives flatness of (i,j,k). Thus a flat common boundary already
satisfies every triangle equation, including the two missing ones.
It extends uniquely to both sides; no new edges or interior vertices occur.

## Boundary admission and exterior gluing

The filling theorems quantify over flat boundaries. This is an explicit
domain condition. `nonflat_boundary_has_no_extension` proves the general
restriction principle: if boundary triangles are bulk triangles and their
edges match, a non-flat boundary cannot be extended by a flat bulk field.
Non-flat boundary data therefore contribute zero to either physical count.

Let X be any finite family of compatible exterior configurations, with
boundary b(x), and let N count all vertices outside the local interior,
including the boundary. The glued configuration set in this interface is
the dependent pair type (x, filling of b(x)). Define

    Z = |Σ x : X, F(b(x))| / |G|^(N + n).

Counting dependent pairs sums the local filling counts over x. For 1–5 the
numerator is multiplied by |G| and the denominator by the same factor.
For the other two moves the numerators and exponents coincide. The Lean
theorems `glued_one_five`, `glued_two_four` and `glued_three_three` prove
these identities for every finite X and every boundary map, including an
empty family and repeated boundary values.

This interface states precisely how gluing is represented. A library
construction of arbitrary triangulations, an equivalence from its global
connection type to these dependent pairs, and a theorem relating arbitrary
PL-homeomorphic triangulations by a sequence of moves are not formalized
here. None is part of the revised node statement.

## Replay and independent computation

`lean4/FiniteGroupPachner.lean` is a non-default Lake target. The
replay receipt is
`dag/research/campaign_fsp-pachner-invariance-claim_lean_replay.json`.
It records Lean 4.35.0, the pinned Mathlib source, source digests before and
after the build, the exact audit importer and axiom reports. Every explicit
definition, theorem, abbreviation, structure and named instance is audited;
only `propext`, `Classical.choice` and `Quot.sound` are permitted. The full
repository Lean workspace is outside this targeted build.

The independent Python script imports no repository modules. It constructs
the simplicial complexes from facets and enumerates edge assignments by
triangle constraint propagation, without using the potential formula.
It validates the multiplication tables before use. All C2 assignments are
also brute-forced without that propagation, and the solution sets agree.
Arithmetic uses integers and exact fractions.

| Group | Flat 1–5 boundaries | 1–5 total fillings, left/right | Flat 2–4 and 3–3 boundaries, each |
|---|---|---|---|
| C1 | 1 | 1 / 1 | 1 |
| C2 | 16 | 16 / 32 | 32 |
| C3 | 81 | 81 / 243 | 243 |
| C4 | 256 | 256 / 1024 | 1024 |
| C5 | 625 | 625 / 3125 | 3125 |
| S3 | 1296 | 1296 / 7776 | 7776 |

The script recomputes every count above, all boundary-fiber weights and a
nonconstant exterior multiplicity sum. Negative controls detect non-flat
boundaries, omitted vertex normalization, incorrectly fixing the new 01
edge to the identity, and omitted interior triangle constraints. For the
last control with C2, 32 unconstrained new-edge assignments give amplitude
16 instead of 1. These finite checks supplement the universal Lean proof;
they are not an exhaustive test of all finite groups.

## What is proved

The exact normalized flat-connection counting identities for the specified
three canonical four-dimensional Pachner pairs, every finite group and
every flat boundary, and their dependent-pair finite-exterior gluing form.
The revised DAG statement has these declarations as its full scope.

## What is assumed

A supplied finite group with its group laws; the untwisted flat-connection
model and vertex normalization; the stated canonical local complexes; and
the declared finite exterior family with its compatible boundary map.
These data are not selected or derived from primitive difference.

## What is open

The unspecified state sum in the historical source; a full triangulation
and PL-topology formalization; twisted or Crane–Yetter models; invariance
of a Regge action; and any fermion-sign, spin-statistics, continuum or
physical identification. Human review of this AI-drafted derivation and
its statement-to-theorem correspondence remains pending.
