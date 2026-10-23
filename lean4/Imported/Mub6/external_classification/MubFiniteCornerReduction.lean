/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/mub6/external_classification/MubFiniteCornerReduction.lean
   Original sha256: 643812223a62d04d7c6c2bc3674b3aa98ce6a0f593cd198ab1f6e8d98115ed42 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.Mub6.external_classification.MubFiniteCornerReduction
   Reason         : MUB6
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Hadamard6.PaperTheorem
import MubIndexTransport
import MubQuartetTransportBridge
import Mathlib.Logic.Equiv.Fin.Basic

/-!
# Actual quartets and retained finite-corner completions

AuthorityEffect: None.

This is a separate replay target under the external classification's pinned
Lean and Mathlib versions; it is not imported by the canonical Mub6 package.
The external theorem supplies coverage. The canonical matrix lemmas supply
normalization, reindexing, and simultaneous monomial transport. The result
leaves precisely the retained-completion nonextension obligation open.
-/

noncomputable section
namespace MUB.FiniteCornerReduction
open MonomialTransport

def blockIndex : Hadamard6.I6 ≃ Fin 6 := finSumFinEquiv

private theorem six_mul_comm (A B : Hadamard6.Mat6)
    (h : A * B = (6 : ℂ) • (1 : Hadamard6.Mat6)) :
    B * A = (6 : ℂ) • (1 : Hadamard6.Mat6) := by
  have hs : ((1 / 6 : ℂ) • A) * B = 1 := by
    rw [Matrix.smul_mul, h, smul_smul]
    norm_num
  have ht := mul_eq_one_comm.mp hs
  rw [Matrix.mul_smul] at ht
  calc
    B * A = (6 : ℂ) • ((1 / 6 : ℂ) • (B * A)) := by
      rw [smul_smul]
      norm_num
    _ = (6 : ℂ) • (1 : Hadamard6.Mat6) := by rw [ht]

theorem rawHadamard_iff_external (H : Hadamard6.Mat6) :
    RawHadamard H ↔ Hadamard6.IsHadamard H := by
  have hcard : Fintype.card Hadamard6.I6 = 6 := by decide
  simp only [RawHadamard, Hadamard6.IsHadamard, Hadamard6.EntrywiseUnit, hcard]
  exact ⟨fun h => ⟨h.1, six_mul_comm _ _ h.2⟩,
    fun h => ⟨h.1, six_mul_comm _ _ h.2⟩⟩

theorem monomialEquivalent_iff_external (H K : Hadamard6.Mat6) :
    MonomialEquivalent H K ↔ Hadamard6.Equivalent H K := by
  constructor
  · rintro ⟨σ, τ, r, c, hr, hc, rfl⟩
    exact ⟨σ, τ, r, c, hr, hc, fun _ _ => rfl⟩
  · rintro ⟨σ, τ, r, c, hr, hc, h⟩
    exact ⟨σ, τ, r, c, hr, hc, funext (fun i => funext (h i))⟩

theorem exists_retained_completion_of_rawQuartet
    (H : Hadamard6.Mat6) (hH : HasRawQuartet H) :
    ∃ (p : Hadamard6.CornerData) (B C : Hadamard6.Mat3),
      Hadamard6.Retained p.matrix B C ∧
      HasRawQuartet (Hadamard6.completion p.matrix B C) := by
  obtain ⟨p, B, C, hret, heq⟩ := Hadamard6.paper_finite_corner_completeness
    ((rawHadamard_iff_external H).mp hH.1)
  exact ⟨p, B, C, hret, hasRawQuartet_transport
    ((monomialEquivalent_iff_external _ _).mpr heq) hH⟩

theorem exists_quartet_iff_retained_completion :
    (∃ Q : Fin 4 → Mat (Fin 6), SzollosiQuartetSystem.Quartet Q) ↔
      ∃ (p : Hadamard6.CornerData) (B C : Hadamard6.Mat3),
        Hadamard6.Retained p.matrix B C ∧
        HasRawQuartet (Hadamard6.completion p.matrix B C) := by
  rw [exists_quartet_iff_exists_rawQuartet,
    exists_rawQuartet_index_iff blockIndex]
  constructor
  · rintro ⟨H, hH⟩
    exact exists_retained_completion_of_rawQuartet H hH
  · rintro ⟨p, B, C, _, hH⟩
    exact ⟨Hadamard6.completion p.matrix B C, hH⟩

/-- This equivalence identifies the remaining exclusion, without assuming it. -/
theorem no_quartet_iff_retained_nonextension :
    (∀ Q : Fin 4 → Mat (Fin 6), ¬ SzollosiQuartetSystem.Quartet Q) ↔
      ∀ (p : Hadamard6.CornerData) (B C : Hadamard6.Mat3),
        Hadamard6.Retained p.matrix B C →
        ¬ HasRawQuartet (Hadamard6.completion p.matrix B C) := by
  constructor
  · intro hn p B C hret hH
    obtain ⟨Q, hQ⟩ := exists_quartet_iff_retained_completion.mpr ⟨p, B, C, hret, hH⟩
    exact hn Q hQ
  · intro hn Q hQ
    obtain ⟨p, B, C, hret, hH⟩ := exists_quartet_iff_retained_completion.mp ⟨Q, hQ⟩
    exact hn p B C hret hH

#print axioms rawHadamard_iff_external
#print axioms monomialEquivalent_iff_external
#print axioms exists_retained_completion_of_rawQuartet
#print axioms exists_quartet_iff_retained_completion
#print axioms no_quartet_iff_retained_nonextension
end MUB.FiniteCornerReduction
