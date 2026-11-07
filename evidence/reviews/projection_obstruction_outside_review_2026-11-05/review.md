# Projection Obstruction v6.9.20: check of an outside review and of the "structure of self" working note

Date: 2026-11-05. Paper: `papers/000_projection_obstruction/projection_obstruction.md` (v6.9.20, 2026-10-23; identical to the file reviewed). WDP monograph: `atlas/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md` (v2.4.5). Replays: `checks.py` in this folder (18 checks, all pass; run from the repository root).

Tags. **Witnessed** = replayed here by exact computation or read in the cited Lean source. **Derived** = follows from a statement in the paper or monograph by a short argument given here. **Supplied** = asserted by the outside review or the working note with no support in the paper or monograph. Agreement between reviews is not evidence; every row names what it rests on.

## 1. Verdict

The outside review reads the paper correctly on structure and on three of its four named results. It misreports one citation (the paper never cites WDP-DIM-1), it overstates the novelty of Theorem 5.16, and its restructuring advice is reasonable editorial opinion.

The working note does not follow from the mathematics. Its three "legs" are real theorems, but each is used for a claim the theorem does not make. In the paper's own example the "global defect that constitutes the self" is a coboundary with quotient class zero, three added linear rows make the observers sound, and the onset order of a residual changes when the access map changes. CH03-P01 says nothing about selves or containers. Details in Section 4.

## 2. The outside review's claims about the paper

| Claim in the review | Status | What it rests on |
|---|---|---|
| Local Green / Global Red (Prop. 7.4.5, Cor. 7.4.6) is correct and is the part most relevant to the Mind project | Witnessed (correctness) / Supplied (relevance) | C1a, C1b: I(s)=6, all three tallies 0, scaling to any R>0. Lean `po000_l004_observer_visibility.lean` states `three_patch_witness` and `no_recovery_modulus`; manifest records the file green with 14 axiom reports. Relevance is opinion. |
| Theorem 5.16 is "the most novel technical result" | Supplied | The paper itself disclaims priority for polynomial lifting and Krylov observability (Carleman, Koopman, Sedoglavic) and claims only the certificate packaging and the Steiner-tree link. The theorem is correct: C3 reproduces kappa=p+1 and onset p on the sharpness example; C4 reproduces onset 1, persistent zero, and the onset-3 jet printed in Section 6.3. |
| "The sharp observer completion theorem (WDP-DIM-1, cited from the WDP monograph)" | Supplied (false as stated) | The paper does not cite WDP-DIM-1, T.8, or Section 10.6 anywhere. Its only WDP reference (ref. 12) is marked "historical series context only". WDP-DIM-1 exists in the monograph, Appendix T, and is correct linear algebra (C2 applies it). |
| Theorem 3.1 has a two-line proof dressed up | Witnessed | Section 3.3 prints the two-line proof. Lemma 3.2 and Lemma 3.3 are scaffolding for the chart transfer, not for the theorem. |
| Theorem 4.2 is "RE3 + RE5 gives unweighted l1" | Witnessed | Section 4.2 item 4 says exactly this and adds that RE1, RE2, RE4 are unnecessary for it. Lean `ReplicaHierarchy.unweighted_sum_of_replicaAdditive_of_singleton_calibration` is named for it. |
| Proposition 7.4.5 is buried in Section 7.4 | Witnessed | It is the fifth numbered item of Section 7.4; the introduction mentions it in one clause of item 3. |
| Theorem 5.16 is "sandwiched" between stratification and local zero certificates | Witnessed | Section 5.16 sits between 5.15 and 5.17. |
| The paper "does not draw the connection between the mathematics and the conceptual claim about selves and qualia" | Witnessed, and correct that it does not | The paper contains no occurrence of "self", "qualia", "mind", or "consciousness". Its scope statement says quantum Hilbert spaces are declared host assumptions and repairable mass R is not defined in the paper. |
| The supplemental section is "useful infrastructure" that does not change the picture | Witnessed | The supplement's own table says Lean proves scalar and normed-group implications only; the propagator, partial-trace estimates and numerical integration remain written premises. |

Two things the review missed, found while checking:

- **Dangling reference.** Section 5.16's roadmap paragraph cites "Proposition 4.7's rank-nullity argument". There is no Proposition 4.7 in the paper (the only 4.7 in the file is the version number v4.7.0 of PO-007). The count it wants is WDP-DIM-1 raw sufficiency, or plain rank-nullity; the text should say which.
- **Section 7.4.8 undercuts the note's reading.** Every I(s)>0 in Section 7.4 is the represented norm of an exact cochain d0 s, so its quotient class is zero (C1c). "Global Red" is red in the raw norm only.

## 3. The restructuring advice

Cuts 1 to 6 and additions 1 to 3 are editorial opinion; nothing in them is wrong, and a front "core results" box plus named theorems for Prop. 7.4.5 and Thm. 5.16 would help readers. Two cautions:

- Addition 4 ("what this paper does not do", naming the Mind project as future work) and addition 5 (a paragraph tying Local Green / Global Red to "the self") would put the working note's claim into the paper by reference. Until Section 4 below is answered, that paragraph would be an unsupported import into a paper whose discipline is to declare imports.
- The paper's existing non-claims (scope statement, "repairable mass R is not defined", Theorem 5.16's priority non-claim) are the right model for any such section.

## 4. The working note, leap by leap

### 4.1 "The self is a report map whose kernel is structurally blind to the global defect that constitutes it"

What Section 7.4 proves (Witnessed, C1): on a fixed finite carrier, a section s with I(s)=6 and three contractive observers with full edge coverage, each tally zero; scaling gives any raw norm with all tallies zero, so no function of the best tally bounds I(s).

What the note adds (Supplied):

- "Constitutes it." Nothing in Section 7.4 is constituted by the defect. The section s is a declared input; the defect Δ(s)=d0 s is computed from it; the observers are a second declared input. The note needs a map from "self" to (carrier, s, observer family) and gives none.
- "Structurally blind." The blindness is a property of the pair (defect, observer kernels), not of the observer alone (Prop. 7.4.4: All-Green iff Δ(s)_e lies in every watcher kernel). Prop. 7.4.7-B shows observers with nontrivial kernels on every edge that are nevertheless sound, because the carrier couples the edges. Blindness is not structural to kernels; it is a joint condition on the carrier.
- "Global defect." In the three-patch example the defect is exact: Φ([Δ(s)])=0 (Section 7.4.8, C1c). Choosing the repair α=s removes it entirely. If the note means something the self cannot repair, the example shows the opposite.

### 4.2 "Any self has a broken symmetry ... every container has a visible entry fee" (CH03-P01)

What CH03-P01 proves (Witnessed, read at monograph lines 650-668, Lean `WitnessedDifference.Symmetry.no_fully_invariant_point`): no S_X-equivariant selection of a point of an unstructured finite set with at least two elements. The monograph adds: this is a nonselection theorem, not an impossibility of choice; a label, base point, order, seed, boundary condition or external input can select, and the theorem requires the asymmetry source to be named.

What the note adds (Supplied):

- "Any self has a broken symmetry." CH03-P01 is about selecting a point from a set with no structure. It says nothing about what a self is, and it does not say every object breaks a symmetry; it says a selection without a named input does not exist.
- "The break must be visible in the injection ledger." The injection ledger (Section 3.2) is a recording discipline: write down the first symmetry-breaking input. It is not a theorem that the break is visible; it is an instruction to make it visible. "Must be" is the author's rule, not a consequence.
- "A cosmos without containers is impossible" and "every container has a visible entry fee." The word "container" does not occur in the monograph in this sense, and CH03-P01 is not about cosmoses. The sibling paper PO-035 is titled "Zero-Container Relational Spacetime"; if the note means to contradict it, that is a dispute between two documents by the same author, and CH03-P01 does not settle it, because a relational carrier can carry its asymmetry sources as declared inputs without being a container.

### 4.3 "The self is a layered observer (CH10-D01 to D04)"

Witnessed: CH10-D01 to D04 define presentation (X, P, q, C), memory, evaluator, policy, with an interpretive remark that an observer "is not a person, a sensor or a conscious state" and that a human "can operate the packet; neither is the packet."

Supplied: the identification self = packet. The monograph forbids it in its own voice (CH00-N02, CH14-N01, consolidated nonclaim 21.7 item 7: "that a quotient evaluator is a conscious observer"). The note can disagree with the monograph, but it cannot cite the monograph as support.

One mismatch of levels: Section 7.4's q_e^α is a single presentation map per edge, which the monograph's vocabulary table (line 8962) explicitly calls "a single layer (CH10-D01)", not an observer. The note treats the Section 7.4 family as a four-layer observer without supplying memory, evaluator or policy.

### 4.4 "Qualia are the onset of the residual under the self's access map" (Theorem 5.16)

What Theorem 5.16 proves (Witnessed, C3, C4): for R(t)=f(e^{tA}m) with f polynomial and f(m)=0, R is identically zero iff its first κ derivatives vanish, where κ=dim of the cyclic space ≤ binom(n+p,p); otherwise the first nonzero derivative has order between 1 and κ−1.

What the note adds (Supplied), and what the replays show:

- The theorem has no access map in it. R is the full residual of a declared model. The readout O in the proof is part of f, not an observer.
- When an access map is composed in front, the onset order changes with the map. C5: on two qubits under H=X⊗X from |00⟩ the residual has onset 1; read through the ZZ coordinate alone it has onset 2; read through the trace alone it is persistent zero while the residual is nonzero. "The first nonzero derivative as seen by the report map" is therefore a property of the pair (model, map), and a blind map returns "no onset" for a nonzero residual. That is Local Green again, not a new structure.
- The onset order is a nonnegative integer. Calling it "qualia" adds a word, not a claim; nothing is predicted that was not already predicted by the integer.
- Falsifier 3 ("if a residual has onset at every order (no finite m)") cannot fire: Theorem 5.16 proves every nonzero polynomial residual of a finite model has a finite onset order. A falsifier that the theorem forbids is not a falsifier.

### 4.5 "The self lacks those observations by construction" (WDP-DIM-1, T.8)

What WDP-DIM-1 proves (Witnessed, read at Appendix T; C2 applies it): over Q, with R=im D_s, B=im D_r, K=ker Q, the minimum added rows are m_raw=dim(R∩K), m_quot=dim K−dim(K∩B), m_both=m_quot+dim(R∩K∩B); T.8 gives dim(R∩K)−dim(R∩K∩B) when candidates are restricted to R.

Applied to the three-patch family (C2): dim V=18, dim R=dim B=15, dim K=6, dim(R∩K)=3. So:

| Question | Added rows |
|---|---|
| raw soundness on realizable defects | 3 |
| repair-class soundness on arbitrary cochains | 3 |
| both | 6 |
| repair-class soundness restricted to realizable defects (T.8) | 0 |

C2c constructs the 3 rows and checks the augmented observer is injective on R. Nothing in the paper or monograph says a self cannot add three rows. "Lacks those observations by construction" is Supplied; the construction says the opposite: the count is finite, explicit, and attained by dual coordinates. The T.8 row of zero is worth stating plainly: on realizable defects, the repair-class question needs no extra observation at all, because every realizable defect in this example is exact.

### 4.6 The falsifiers (note Section 7)

1. Trivial kernels: correct as a condition (Cor. 7.4.7), but Prop. 7.4.7-B shows nontrivial kernels can still be sound, so this falsifier is sufficient, not necessary; the note's "does not apply" is too strong in the other direction too.
2. Faithful access map: same remark.
3. Onset at every order: cannot occur (4.4 above).
4. Empty injection ledger "violates CH03-P01": an empty ledger with a selection present means an undeclared input, which is a bookkeeping failure, not a violation of a theorem.
5. A realizable self achieving the row count: C2 gives the count as 3 for the paper's own example; the burden is on the note to show why three linear rows are unavailable.

### 4.7 The non-claims (note Section 6)

They are consistent with the monograph's nonclaims and should stay. The sentence after them ("the self is a local observer in the precise sense of PO Section 7.4, and qualia are the residual structure under its access map in the precise sense of PO Theorem 5.16") is the claim the non-claims are meant to protect, and it is the claim Sections 4.1 and 4.4 show is not made precise by either theorem.

## 5. What was and was not checked

- Checked: the paper text; Lean source of `po000_l004_observer_visibility.lean` (statements read, theorems named as in Section 7.4.9); `lean4/manifest.json` records the file green standalone with 14 axiom reports. The Lean file was **not** recompiled in this session.
- Checked: `code/tests/test_polynomial_onset.py` (39 pass) and `checks.py` here (18 pass) on sympy 1.14.
- Not checked: PO-035, PO-007 to PO-009, the Rust sources in ref. 26.

## 6. Recommendation

- Accept the editorial parts of the outside review (core results box, named theorems B and C, "what this paper does not do"). Do not add a Mind-project paragraph to the paper.
- Fix the dangling "Proposition 4.7" reference in Section 5.16.
- If the paper is to cite WDP-DIM-1, cite it (Appendix T, with T.8) and say what it is used for; at present the review's statement that it is cited is false.
- Before any "structure of self" paper, write the missing map: which carrier, which section, which observer family, and why the self cannot add dim(R∩K) rows. Until then the three legs stand and the body does not.
