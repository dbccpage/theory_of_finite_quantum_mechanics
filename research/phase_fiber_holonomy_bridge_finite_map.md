# QM-207 Phase Fiber and the Finite Multi-Report Holonomy Bridge

**Scope:** research note for `006_finite_qm`; not part of the manuscript, not a claim promotion.
**Code:** `python/finite_qm/use_cases/holonomy_bridge_control.py`, tests in `tests/e2e/test_e2e_holonomy_bridge_control.py`.
**Status marks used:** PROVED (argument given here, finite and checkable), COMPUTED (exact arithmetic in a cyclotomic field, replayable), IMPORTED (added structure that nothing finite here produces), CONJECTURED (none in this note).

Authority status: none. This note changes no admitted claim.

## 1. The question

QM-207 states the first of five imports between finite nonnegative weights and complex quantum mechanics: the complex phase fiber. The question has two parts.

- Give the full account of that import: what the weights provide, what is added, why relative path phase is a loop holonomy, and why nothing finite forces the fiber.
- Build an explicit finite multi-report holonomy control and say how far the five imports QM-207 through QM-211 reduce to finite transition-cycle invariants plus Cauchy completion.

The answer to the second part is: each import splits into a finite transition-cycle invariant that is computed exactly here, a completion step that is itself an import, and a residual structural import that neither of the first two supplies. The reduction is real but not total. Section 6 names every residual.

## 2. Setting

A finite connected carrier graph G = (V, E) with |V| = n loci. Report means a locally indexed observer record: here a path from a source locus to a sink locus. Several reports from one source to one sink are the multi-report situation; comparing two reports is comparing two paths.

Fix a conductor N. All arithmetic takes place in the cyclotomic field Q(ζ_N), implemented exactly by `CyclotomicElement` (power basis modulo Φ_N, rational coefficients). The roots of unity μ_N = {ζ_N^k} are the finite stand-in for U(1).

## 3. What ℓ¹ weights provide

Weights w : V → Q≥0 with total W > 0 give diagonal probabilities P_v = w_v / W. Write c_v for any amplitude with c_v conj(c_v) = w_v.

**Theorem 3.1 (phase blindness). PROVED.** For every locus gauge χ : V → U(1), the weights of (χ_v c_v) equal the weights of (c_v). Proof: (χ c) conj(χ c) = χ conj(χ) c conj(c) = c conj(c). The map from amplitudes to weights factors through the quotient by the locus gauge group, so no weight datum selects a point of the fiber. COMPUTED: `l1_phase_blind` returns true on the control fixture.

Consequence: the only amplitude data the weights fix is the nonnegative square root √w_v. Even the sign is a Z/2 fiber choice. Without a fiber import the amplitudes are nonnegative reals and the two-report readout can only add constructively (Section 6, QM-208 row: the trivial-fiber interference term is +6 on the fixture, never negative).

## 4. The import, stated exactly

**Definition 4.1 (phase cochain).** A U(1) 1-cochain is a map A : E → U(1); in the finite control A : E → μ_N. A locus gauge χ acts by A(u,v) ↦ χ(u) A(u,v) conj(χ(v)). Transport along a walk is the ordered product of edge values, with the conjugate on an edge traversed against its orientation. Holonomy is transport around a closed walk.

**Theorem 4.2 (gauge invariance of holonomy). PROVED.** Holonomy around a closed walk is unchanged by every locus gauge, since consecutive χ(v) conj(χ(v)) factors cancel and the walk closes. COMPUTED on the fixture under a non-trivial gauge.

**Theorem 4.3 (finite classification of the fiber data). PROVED.** Let T be a spanning tree and b₁ = |E| − |V| + 1. Every cochain is gauge equivalent to exactly one cochain whose tree edges are all 1; that cochain is determined by its b₁ cotree values, and each cotree value equals the holonomy of the fundamental cycle through that cotree edge. Hence

C¹(G; μ_N) / gauge ≅ Hom(H₁(G; Z), μ_N) ≅ μ_N^{b₁}.

Proof. Set χ(root) = 1 and define χ down the tree by χ(child) = χ(parent) · A(parent, child) (conjugate if the edge points upward). The gauged cochain has value 1 on every tree edge. Two tree-gauged cochains that are gauge equivalent differ by a χ constant along every tree edge, hence constant on V, hence trivial on edges. The fundamental cycle through cotree edge e traverses tree edges (value 1) and e once, so its holonomy is the cotree value. H₁ of a connected graph is free abelian on the fundamental cycles, which gives the Hom description. ∎

COMPUTED: `gauge_orbit_census` enumerates all 3⁵ cochains on the control carrier (b₁ = 2) and finds 3² classes of size 3³, keyed by the two cycle invariants. `gauge_equivalence_matches_invariants` checks both directions by full enumeration on a triangle with N = 2: same invariants if and only if some gauge carries one cochain to the other.

**Theorem 4.4 (holonomy factorizes through cycle invariants). PROVED.** For any closed walk γ, Hol(γ) = ∏_e h_e^{m_e}, where e runs over cotree edges, h_e is the fundamental-cycle invariant and m_e is the signed number of traversals of e by γ. Proof: in the tree gauge the tree edges contribute 1, so only cotree traversals remain. COMPUTED on five test loops including a non-simple one.

**Theorem 4.5 (relative report phase is a holonomy). PROVED.** For two reports p₁, p₂ from s to t, U(p₁) conj(U(p₂)) = Hol(p₁ · p₂⁻¹), which is gauge invariant by 4.2 and factorizes by 4.4. This is the statement of QM-207 §2, now with the coefficient structure made explicit. COMPUTED: the three pairwise relative phases of the three reports on the fixture are ζ₁₂^{10}, ζ₁₂^{2}, ζ₁₂^{4}, unchanged under gauge.

**Which cohomology.** On a graph every U(1) bundle is trivial, because H²(G; Z) = 0. The holonomy class therefore does not live in a Čech H¹ classifying bundles; it lives in cellular cohomology with the coefficient group U(1), H¹(G; U(1)) = Hom(H₁(G), U(1)) (Ext vanishes since H₀ is free). On a 2-complex the face condition Hol(∂f) = 1 is the cocycle condition, and the quotient by gauge is the cellular H¹ of the 2-complex. This is consistent with the manuscript's firewall on phase holonomy (nontrivial connection holonomy on a trivial bundle) and sharpens it: the correct object is the connection class in H¹(G; U(1)), not a bundle class.

**What is imported here.** The existence of a nontrivial fiber group acting on amplitude labels. Theorem 3.1 shows the weights are constant on fiber orbits, so no finite computation from weights produces a point of μ_N, let alone U(1). This is the content of the QM-207 import, and it is not reduced.

## 5. Cauchy completion

Everything in Section 4 is exact for every conductor N. Two limits separate the finite data from U(1).

- Algebraic direct limit: the union of all μ_N is the torsion group Q/Z, and the union of all Q(ζ_N) is the maximal abelian extension of Q. Every statement of Section 4 holds at each finite stage and passes to this union without any completion. PROVED (each stage is finite; the union is a directed union of groups).
- Metric completion: with the circle metric d(x, y) = min_k |x − y − k|, the Cauchy completion of Q/Z is R/Z ≅ U(1), and Q/Z is dense in it. IMPORTED: this step uses the completeness of the reals. No construction in this package or in the `007_finite_to_continuum` code builds the completion; they check finite interval enclosures or name completion as a hypothesis (gap register GAP-F001-S000-002, GAP-F001-S000-005).

So QM-207 = (finite cyclic transition-cycle invariants in Hom(H₁, μ_N), exact) + (Cauchy completion Q/Z → R/Z, imported) + (the fiber itself, imported). The completion step is an import and is reported as one.

## 6. The bridge control and the five imports

The control is one function, `evaluate_holonomy_bridge_control(conductor=12)`. Carrier: the diamond 0–1–3, 0–2–3 with chord 1–2 (b₁ = 2), three reports from 0 to 3, a μ₁₂ cochain, the Weyl pair on C⁴, the two-qubit Pauli square, and a Z/3 ⊂ Z/6 ⊂ Z/12 clock tower. All values are exact; the test file pins them.

| Import | Finite transition-cycle invariant (COMPUTED) | Completion step (IMPORTED) | Residual import (IMPORTED, not reduced) |
| --- | --- | --- | --- |
| QM-207 U(1) fiber | cycle invariants (ζ₁₂², ζ₁₂⁸) in Hom(H₁, μ₁₂); 9 gauge classes of size 27 at N = 3; holonomy factorization on all test loops | Q/Z → R/Z | a fiber group acting on amplitudes at all |
| QM-208 ℓ² readout | I₂ = |Σc|² − Σ|c|² ≠ 0 and real; Sorkin I₃ = 0 for the quadratic rule (matches the existing `sorkin_i3` certifier); I₃ = 36 for the quartic rule on the trivial-fiber amplitudes | none for the rule; √w needs an algebraic extension when w is not a square | the add-then-square composition rule; I₃ = 0 characterizes it inside a rule family, it does not derive it |
| QM-209 noncommuting contexts | X Z X⁻¹ Z⁻¹ = ζ₁₂⁹ · I = −i · I, a central μ₄ holonomy of the 4-cycle of context transitions; any diagonal pair gives I; F Z F† = X⁻¹ exactly | unitaries with entries in ∪ Q(ζ_N) are dense in U(d) | a second context at all; weights have one diagonal |
| QM-210 Born pairing | diagonal Born weights equal the weights (identity from the lift); transported weights (0,0,0,1) under F keep the total; Peres–Mermin Z/2 parity holonomy −1 against value-assignment parity +1 | Gleason needs every frame in dimension ≥ 3 | noncontextuality of the frame function; finite Kochen–Specker and Peres–Mermin sets give obstructions, not uniqueness |
| QM-211 continuous unitary dynamics | clocks of order 3, 6, 12 with exact eigenphases, no smaller order, each half-step squaring to the coarser clock | direct limit Q/Z, then Cauchy completion to R/Z and the one-parameter group | strong continuity of t ↦ U(t) (Stone) and the action unit |

Reading of the table. Four of the five imports share one finite shape: a cycle invariant valued in an abelian coefficient group (μ_N for 207, the center μ_d for 209, Z/2 for 210, μ_m for 211). QM-208 does not: its invariant is an inclusion–exclusion identity, not a holonomy. The completion column is the same import of completeness in four rows and a continuum theorem (Gleason) in the fifth. The residual column is non-empty in every row.

Two things the control does not show.

- Independence of the five imports. The control shows that each import has a finite invariant that can be switched off while the others stay on (distinguishability). It does not show that any import fails to follow from the other four. The manuscript's correction stands: the five are a catalogue of structures used by complex quantum mechanics, not a proved minimal basis, and bipartite composition is absent from the list.
- The Bell minimum. The control is about the cascade to Cⁿ quantum mechanics. The manuscript's Tsirelson witness over Q(√2) uses no complex phase and no dynamics; that result is unchanged.

## 7. Status of the existing evidence that the five-import boundary cites

Checked on main at `dc4346860`.

- `research/lean4/qm_import_independence.md` is Lean text in a `.md` file; the folder README says these files are reading guides that no Lake project builds. Its "independence" models are records of eight booleans with one flag set false by hand, and `admits` reads the flag. Every proof is `rfl`, `decide` or trivial. It does not establish independence of any import, and says so: `fullBasisIndependence_open : Prop := True`.
- The QM_122 Lean files H007, H008, H010, H011, H012, H013, H016 import no Mathlib. Their general theorems are elementary (global phase blindness, no descent of a readout through the phase-blind map from one witness pair, diagonal 2×2 matrices commute, bilinearity of the pairing, no report-level square root of the toggle). Their "selector" and "uniqueness not discharged" results are `rfl` on hand-set flags, as their own docstrings say.
- Target 2 of the manuscript (the diamond 2-complex) declares its holonomy values ρ_J = i and ρ_τ = ζ₃; the ledger row states that no holonomy map or selection theorem is claimed. This note's Theorem 4.3 supplies the missing classification for the graph case and names the declared values as a choice of a point in Hom(H₁, μ₁₂).
- Several QM identifiers cited in the five-import synthesis are labels without backing on main (QM-200 through QM-205 empty, QM-007 a redirect, QM_061 and ENC-1063 pointing at Lean that does not exist or lives as text). This note relies on none of them.

## 8. What would close more

- A Lean statement of Theorem 4.3 over an arbitrary finite connected graph type with a decidable spanning tree, elaborated in a Lake project that builds. The kernel is a tree induction; Mathlib is not needed.
- A Rust port of `holonomy_bridge_control` into `omega_quantum_physics`, using `omega_number_theory::cyclotomic_field::CyclotomicNumber`, so the authoritative core carries the control and Python stays a thin layer.
- For QM-208, a finite statement of which readout rules on three amplitudes have I₃ = 0; Sorkin's characterization is the target, and only the quadratic and quartic cases are computed here.
- For QM-210, a finite analogue of Gleason on a declared finite frame set is not available and should stay marked IMPORTED until one is proved.
