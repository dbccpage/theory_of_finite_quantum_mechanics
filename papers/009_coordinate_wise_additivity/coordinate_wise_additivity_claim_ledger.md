Claim Ledger — GS-000: Coordinate-Wise Additivity and Local ℓ¹ Gauge Selection
==============================================================================

**Paper Key:** `002_projection_obstruction/009_coordinate_wise_additivity`  
**Paper Identity:** `GS-000` (`coordinate_wise_additivity.md`)

**Canonical Publication:** `v6.1.1`, DOI `10.5281/zenodo.20723753`

**Repository State:** unpublished post-v6.1.1 draft; no later version or DOI assigned

**Legacy Paper Identity:** `Paper 003` / `Paper 004`  
**Authority:** None.

This ledger catalogs every claim in `GS-000` with its type, governing hypotheses, proof location, mechanization status, and open obligations.

---

1. Claim-by-Claim Matrix

---

| ID | Claim | Type | Hypotheses | Proof / support | Mechanization | Open obligation |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | Main claim: H1-H5 force edgewise coordinatewise $\ell^1$; graph invariance gives orbit-weighted $\ell^1$; edge-transitivity gives unweighted $\ell^1$. | PROVEN, CONDITIONAL | H1-H5 below | §2, Theorems 1-3 | Mechanized-Partial | Lean H2 permutation action & H4 graph orbits |
| C2 | $C^1(G, \mathbb{R}^k) = \bigoplus_e \mathbb{R}^k$ setup. | DEFINITION | Finite graph cochain space | §2.1 | Defined | None |
| C3 | Edge locality (Axiom H1). | DECLARED AXIOM | Observer locality assumption | §2.1 | Defined | None |
| C4 | Coordinate permutation symmetry (Axiom H2). | DECLARED AXIOM | Observer symmetry assumption | §2.1 | `basis_equal` field | Model H2 as true permutation action |
| C5 | Disjoint-coordinate additivity (Axiom H3). | DECLARED AXIOM | Observer additivity assumption | §2.1 | `disjoint_add` field | None |
| C6 | Graph isomorphism invariance + $\ell^1$-isometric fiber action (Axiom H4). | DECLARED AXIOM | Fiber clause (signed coordinate permutations) | §2.1 | `hiso` assumption | Model true $\mathrm{Aut}(G)$ orbit action |
| C7 | Seminorm absolute homogeneity (Axiom H5). | DECLARED AXIOM | Seminorm homogeneity over $\mathbb{R}$ | §2.1 | `coord_hom` field | None |
| C8 | Theorem 1: Edgewise $\nu_e = w_e \|\cdot\|_1$. | PROVEN, CONDITIONAL | H2, H3, H5 | §2.2 | `PaperGS003.coord_real_l1_weighted_sum` | None |
| C9 | Theorem 2: Orbit-weighted global aggregation. | PROVEN, CONDITIONAL | H1-H5 | §2.3 | `PaperGS003.orbit_weighted_l1_aggregation` | Model derived graph orbits |
| C10 | Theorem 3: Edge-uniformity $\implies$ unweighted global $\ell^1$. | PROVEN, CONDITIONAL | H1-H5 + edge-transitivity | §2.4 | `PaperGS003.edge_uniformity_collapses_finite_l1` | None |
| C11 | Worked Replay (two-edge, $k=2$, values 13 vs 10). | WORKED EXAMPLE | Python replay computation | §2.4 | Replay receipt | None |
| C12a | CE1-CE4: failures of disjoint additivity, coordinate symmetry, edge locality, and edge uniformity. | PROVEN BY COUNTEREXAMPLE, PROSE | Constructions in §2.5; k≥2 for CE1/CE2; trivial fiber action for CE2/CE3 | §2.5 | PARTIAL arithmetic analogues: CE1 is a natural-number quadratic and CE3 a coupled polynomial; neither checks all real seminorm hypotheses | Formalize the actual real witnesses and retained hypotheses |
| C12b | CE5 candidate after weakening seminormhood: symmetric disjoint-additive subadditive power gauge with 0<p<1. | OPEN / NOT_VERIFIED (full matching formalization) | Nonnegative zero-at-zero gauge premise replaces seminormhood | §2.5 | `ce5_lp_not_homogeneous` fixes p=2 over naturals; it is outside the subadditive candidate range | Match the weakened premise and parameter range; p>1 also violates subadditivity |
| C13 | Broader real-cochain / cross-graph LGGR interpretation. | OPEN / NOT_VERIFIED | Explicit real record carrier, relation, graph transport, and weight comparison required | §3.5 | Finite `Nat` record helpers allow weights to vary; they do not establish fixed-profile non-descent | Formalize the exact comparison; the earlier fixed-profile non-descent assertion is withdrawn |
| C14 | Fixed-profile weighted totals factor through per-edge diagnostic equality. | PROVEN, ELEMENTARY PROSE | Same graph and weight profile in both cochains | §3.5, finite sum proof; `lggr_obstruction_witness` fixed-profile pair | Python finite examples only; no new Lean claim | None for the prose fact |
| C15 | Equal unweighted totals can give weighted totals 13 and 17. | EXACT WORKED EXAMPLE | Two-edge magnitudes (7,3) / (3,7), fixed weights (1,2); relation forgets distribution | §3.5; Python quotient witness | Exact integer exercise and floating companion; distinct from C14's relation | No general cross-graph promotion |
| C16 | A diagnostic kernel alone does not determine norm geometry. | PROVEN BY COUNTEREXAMPLE, PROSE | k≥2; L1 and L2 share zero kernel | §3.6 | No new Lean declaration | The EPK connection remains interpretive |
| C17 | Coordinate-additivity failures imply PCC returning obstructions. | INTERPRETIVE / OPEN | A separate projection, transition rule, congruence, and bridge theorem would be needed | Programme discussion after §2.6 | No PCC proof packaged here | Supply the bridge; no implication is established here |

<!-- claim-id-body-only-sync:begin -->

Body-only ID sync (packaging)
---

**AuthorityEffect:** None. Packaging hygiene; no OPEN→PROVED.

| ID | Claim | Type | Status |
|---|---|---|---|
| GS-000 | Body claim-shaped ID registered for bijection packaging only; OPEN; not upgraded | OPEN | packaging |

<!-- claim-id-body-only-sync:end -->
