/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnTheorems.lean
   Original sha256: cb87ca60eb6724a37b8d95a8ee468d0171053eb11cd8c603cbf17ab7762ae8cd (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.PreGenesisToMssn.SnTheorems
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.PreGenesisToMssn.SnSyntax
import Imported.PreGenesisToMssn.SnCarrier

/-!
# S(n) Core Theorems & Epistemic Invariants (Lean 4)

AuthorityEffect: None. GenesisEffect: None.
Formalizes under the declared constructive definitions:
1. Ground demarcation: the supplied example carrier at index zero is empty.
2. Dual Ledger Independence: active survivor count s_n differs from cumulative history ledger |H_n|; at S(4), s_4 = 0 while |H_4| = 5.
3. Old-image retraction for the explicitly typed base presentations.
4. Typed Refusal on Novelty: novel terms retract to nonDescent.
5. A refusal token is refused, without claiming this alone proves non-involution.
6. Irreflexive Witness Distinction: a witnessed irreflexive cut forces distinct endpoints.
-/

namespace SnTheorems

open SnPresentation
open SnCarrier

/-- Theorem 1 (Ground Demarcation):
    The presentation token `<>` has string length > 0, while the carrier cardinality is 0. -/
theorem ground_presentation_vs_carrier :
    GroundToken.toWire ⟨()⟩ = "<>" ∧ carrierCard 0 = 0 := by
  exact ⟨rfl, rfl⟩

/-- Theorem 2 (Dual Ledger Independence):
    At Stage S(4), automorphism orbit closure yields s_4 = 0,
    while cumulative history |H_4| = 5 preserves all historical certificates. -/
theorem dual_ledger_independence_at_stage_4 :
    activeObstructions 4 = 0 ∧ cumulativeHistory 4 = 5 := by
  exact ⟨rfl, rfl⟩

/-- Theorem 3 (Old-Image Retraction Law for Ground Token):
    r_0(u_0(<>)) = accepted(<>). -/
theorem old_image_ground :
    retractionDownMap 0 (sectionLift 0 (.ground ⟨()⟩)) = .accepted (.ground ⟨()⟩) := by
  rfl

/-- Theorem 4 (Old-Image Retraction Law for Supplied Mark):
    r_1(u_1(<a>)) = accepted(<a>). -/
theorem old_image_supplied (g : Glyph) :
    retractionDownMap 1 (sectionLift 1 (.supplied ⟨g⟩)) = .accepted (.supplied ⟨g⟩) := by
  rfl

/-- Theorem 5 (Old-Image Retraction Law for Retained Pair):
    r_2(u_2(<ab>)) = accepted(<ab>). -/
theorem old_image_retained_pair (f s : Glyph) :
    retractionDownMap 2 (sectionLift 2 (.relation (.pair ⟨f, s⟩))) =
      .accepted (.relation (.pair ⟨f, s⟩)) := by
  rfl

/-- Theorem 6 (Old-Image Retraction Law for Directed Cut):
    r_3(u_3(<a->b>)) = accepted(<a->b>). -/
theorem old_image_directed_cut (src tgt : Glyph) :
    retractionDownMap 3 (sectionLift 3 (.relation (.cut ⟨src, tgt⟩))) =
      .accepted (.relation (.cut ⟨src, tgt⟩)) := by
  rfl

/-- Theorem 7 (Old-Image Retraction Law for Simplicial Cut):
    r_3(u_3([a,b])) = accepted([a,b]). -/
theorem old_image_simplex_cut (v0 v1 : Glyph) :
    retractionDownMap 3 (sectionLift 3 (.relation (.simplex ⟨v0, v1⟩))) =
      .accepted (.relation (.simplex ⟨v0, v1⟩)) := by
  rfl

/-- Theorem 8 (Descent Refusal on Mismatched Stage):
    A lift with stage N cannot be retracted by down-map r_M when N ≠ M. -/
theorem descent_refusal_on_mismatched_stage (g : Glyph) :
    retractionDownMap 0 (sectionLift 1 (.supplied ⟨g⟩)) = .nonDescent := by
  rfl

/-- A refusal token is not in the image of a base-presentation section. -/
theorem refusal_token_refused :
    retractionDownMap 0 (.nonDescent ⟨()⟩) = .nonDescent := by
  rfl

/-- Theorem 10 (Irreflexive Witness forces Distinct Endpoints):
    If r is irreflexive and r a b holds, then a ≠ b. -/
theorem irrefl_witness_distinct {α : Type} (r : α → α → Prop) (hirr : ∀ x, ¬ r x x)
    {a b : α} (hab : r a b) : a ≠ b := by
  intro heq
  subst heq
  exact hirr a hab

/-- The declared index-zero carrier really has no elements. -/
theorem ground_carrier_empty (x : Carrier 0) : False := Fin.elim0 x

/-- Uniform old-image law on every base constructor, at every stage index. -/
theorem old_image_base (n : Nat) (p : BasePresentation) :
    retractionDownMap n (sectionLift n p) = .accepted p.toPresentation := by
  cases p with
  | ground g => cases g with | mk u => cases u; simp only [sectionLift, retractionDownMap, BasePresentation.toPresentation, beq_self_eq_true, ↓reduceIte]
  | supplied s => cases s; simp only [sectionLift, retractionDownMap, BasePresentation.toPresentation, beq_self_eq_true, ↓reduceIte]
  | relation r => cases r <;> simp only [sectionLift, retractionDownMap, BasePresentation.toPresentation, beq_self_eq_true, ↓reduceIte]

end SnTheorems
