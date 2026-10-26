# QM-210 Born Rule and State–Effect Quadratic Pairing: the Finite Map

**Scope:** research note for `finite_quantum_mechanics`; not part of the manuscript, not a claim promotion. Companion to `phase_fiber_holonomy_bridge_finite_map.md`.
**Code:** `python/finite_qm/use_cases/frame_function_control.py`, tests in `tests/e2e/test_e2e_frame_function_control.py` (9 tests).
**Status marks used:** PROVED (argument given here, finite and checkable), COMPUTED (exact arithmetic over Q and F₂, replayable), IMPORTED (added structure that nothing finite here produces), CONJECTURED (none in this note).

Authority status: none. This note changes no admitted claim.

## 1. The question

QM-210 names the fourth import: the Born rule as a quadratic pairing between states and effects, P(E | ρ) = Tr(ρ E), with ρ positive of trace one. In the continuum theory Gleason's theorem derives this pairing from noncontextuality of a frame function on every orthonormal basis in dimension at least 3. The task is to research and discover the finite map to this problem.

The finite map splits the Gleason statement in two. Its linear half holds exactly on the declared finite frame sets: every function on the rays that sums to one over every declared basis is the restriction of a real symmetric trace-one quadratic form, and the nullity of that comparison is zero. Its positive half fails on every finite set examined: a trace-one form that is nonnegative on every declared ray need not be positive semidefinite. The import is the positive half together with the choice of quadratic forms as carrier.

## 2. What ℓ¹ provides

Weights on one basis. The ℓ¹ data is one probability vector on the loci, which is one frame function on one basis and nothing on any other basis. The QM-207 lift gives diagonal Born weights equal to the weights (an identity, recorded in the QM-207 note). Once a second basis is declared (QM-209), the question of a function that sums to one on every basis arises, and that is the frame-function question.

## 3. The finite invariant

The carrier is the Cabello configuration in Q⁴: 18 rays and 9 orthogonal bases, every ray in exactly two bases. The second carrier is the Peres configuration: 24 rays with entries in {−1, 0, 1}, 24 orthogonal bases, every ray in four bases.

**Theorem 3.1 (the frame identity is exact). PROVED.** For an orthogonal basis B of Q⁴ and any symmetric ρ, Σ_{v∈B} vᵀρv / vᵀv = Tr(ρ Σ_{v∈B} P_v) = Tr ρ. COMPUTED on the maximally mixed state, a pure state and a generic trace-one form: every basis sums to 1. Bases that fail orthogonality are refused by the control, not summed.

**Theorem 3.2 (finite linear Gleason, nullity zero). COMPUTED.** Let F be the affine space of functions f on the rays with Σ_{v∈B} f(v) = 1 for every declared basis, and let Q be the affine space of functions v ↦ vᵀρv / vᵀv with ρ real symmetric of trace one, restricted to the rays. Then Q ⊆ F, and the nullity dim F − dim Q is:

| frame set | rays | rank of the basis constraints over Q | dim F | dim Q | span of the ray projectors in Sym₄ | nullity |
| --- | --- | --- | --- | --- | --- | --- |
| Cabello, first 3 bases | 10 | 3 | 7 | 7 | 8 | 0 |
| Cabello, first 6 bases | 15 | 6 | 9 | 9 | 10 | 0 |
| Cabello, all 9 bases | 18 | 9 | 9 | 9 | 10 | 0 |
| Peres, 24 bases | 24 | 15 | 9 | 9 | 10 | 0 |

So on each of these sets every frame function, with no positivity assumed, is the restriction of a real symmetric trace-one form. When the ray projectors span all of Sym₄ (dimension 10), that form is unique; on the 3-basis prefix the span is 8 and the representative has a two-dimensional ambiguity. For the full Cabello set the uniqueness is the statement already used in section 11.5 of the manuscript; the census here shows that it needs no positivity and holds on the prefixes and on the Peres set as well. This outcome was not expected before the computation and is reported as found.

**Theorem 3.3 (F₂ parity obstruction, no two-valued frame function). PROVED for Cabello, COMPUTED for Peres.** A two-valued frame function assigns 1 to exactly one ray of every basis. Summing the nine Cabello basis equations over F₂ counts every ray twice, so the left side is 0 while the right side is 9 ≡ 1: no such function exists. COMPUTED: the 9 × 18 system over F₂ has rank 8 and is inconsistent; a backtracking search confirms; every prefix of 1 to 8 bases admits a two-valued function and the first uncolorable prefix is 9. For the Peres set every ray lies in four bases, so the total-parity argument gives 0 = 0 and decides nothing; F₂ elimination finds the system of rank 14 inconsistent and the search confirms. This is the same F₂ mechanism as the Peres–Mermin obstruction of the QM-209 note.

**Theorem 3.4 (positivity gap). PROVED in general, COMPUTED as a witness.** The trace-one symmetric forms nonnegative on finitely many rays form a polyhedron in the nine-dimensional affine space (finitely many linear inequalities), while the trace-one positive semidefinite forms form a convex body that is not a polyhedron; so the first strictly contains the second. Witness over Q:

ρ₂ = [[0, −1/4, 0, 0], [−1/4, 1/2, 0, 1/4], [0, 0, 1/2, 0], [0, 1/4, 0, 0]].

COMPUTED: Tr ρ₂ = 1; the frame identity holds on every Cabello and every Peres basis; vᵀρ₂v ≥ 0 on all 18 Cabello rays and all 24 Peres rays; ρ₂ is not positive semidefinite (leading 2 × 2 minor −1/16; exact Sylvester test over all principal minors), and vᵀρ₂v = −1/2 at v = (2, 1, 0, 0). Section 11.5 of the manuscript already shows that every one of the 146 vertices of the Cabello frame polytope has a non-positive representative; ρ₂ adds a single rational point that is nonnegative on both ray sets at once, with a displayed negative direction.

Reading. The finite invariant of QM-210 is a pair: the Z/2 parity class of the frame set (an obstruction to classical values, as in QM-209) and the nullity zero of the linear comparison. What the finite set does not fix is the cone.

## 4. Completion step

Gleason's theorem needs every orthonormal basis of a real or complex Hilbert space of dimension at least 3, and it uses the continuity that this continuum of frames supplies; Busch's effect version needs every effect. Passing from finitely many frames to all of them is what shrinks the polyhedron of Theorem 3.4 to the positive semidefinite body. Neither statement is finite. IMPORTED.

## 5. Residual import

Positivity, and the selection of real symmetric quadratic forms as the carrier of the pairing. The finite set fixes the linear span of the frame functions (nullity zero) and not the cone: ρ₂ is nonnegative on every declared ray and is not a state. Noncontextuality as a selection rule yields, on a finite set, an obstruction (no classical value assignment) and not the quantum state space. Complex Hermitian forms are not examined by this control.

## 6. Three-layer table

| Layer | Status | Content |
| --- | --- | --- |
| finite invariant | COMPUTED | frame identity exact on Cabello and Peres; nullity zero on the prefixes of 3, 6, 9 bases and on the Peres set, with a unique trace-one representative whenever the projectors span Sym₄; no two-valued frame function (F₂ rank 8 and 14, inconsistent), every prefix of 1 to 8 Cabello bases colorable |
| completion | IMPORTED | Gleason needs every frame in dimension ≥ 3; Busch needs every effect |
| residual import | IMPORTED | positivity (the cone) and real symmetric forms as carrier; ρ₂ is a trace-one form nonnegative on every declared ray and not positive semidefinite |

## 7. Negative controls

- Eight Cabello bases: a two-valued frame function exists and the F₂ system is consistent; the obstruction appears at the ninth basis only.
- A pure state: positive semidefinite by the same Sylvester test, with quadratic form 4 at (2, 1, 0, 0), against −1/2 for ρ₂.
- A tampered basis with a non-orthogonal pair is refused (`FrameControlRefusal`), so the frame identity is never summed over a non-frame.

## 8. What the control does not show

- Gleason's theorem. The positive half fails on every finite set examined, by Theorem 3.4, and no finite analogue of the positive half is available here.
- Complex Hermitian forms, infinite frame sets, and dimensions other than 4.
- That noncontextuality selects the Born pairing. On a finite set it selects the linear span (Theorem 3.2) and forbids classical values (Theorem 3.3); the cone is left open.
- Independence from the other imports. Theorem 3.2 presupposes the declared bases (QM-209) and the quadratic form family (QM-208).

## 9. Manuscript passages this bears on

Section 11.5 (the Cabello frame polytope and its 146 half-integral vertices) and section 13.8 (the five-import boundary, where the quadratic geometry and the Born pairing are said to overlap). The nullity census is the linear half of the uniqueness statement in 11.5, made explicit on the prefixes and on the Peres set without positivity; ρ₂ is one rational point of the gap that 11.5 exhibits at the vertices. The overlap noted in 13.8 is visible here: the QM-210 linear invariant lives inside the QM-208 quadratic family and uses the QM-209 bases. Nothing in the manuscript is edited by this note.

## 10. Claim envelope

- Supports: on the Cabello set in Q⁴ and its 3- and 6-basis prefixes, and on the Peres 24-ray set, every frame function is a real symmetric trace-one form (nullity zero), the frame identity holds exactly, no two-valued frame function exists, and the explicit trace-one form ρ₂ is nonnegative on every declared ray while not positive semidefinite.
- Does not support: Gleason's theorem or any finite analogue of its positive half; complex Hermitian statements; a derivation of the Born pairing; independence of QM-210.
- Narrowest claim: on the declared finite carriers the QM-210 import splits into an exactly computed linear invariant plus a Z/2 parity obstruction, an imported continuum completion (all frames), and the imported positive cone.
- Next test: `cd sources/atlas/papers/finite_quantum_mechanics && PYTHONPATH=python python3 -m pytest tests/e2e/test_e2e_frame_function_control.py -q -p no:cacheprovider` (expect 9 passed).
