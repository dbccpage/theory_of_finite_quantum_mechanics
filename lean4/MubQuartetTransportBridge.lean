import MubMonomialTransport
import ConcreteSemantics
import SzollosiQuadraticSystem
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

/-!
# Transport connected to the campaign's concrete quartet equations

AuthorityEffect: None.

This module reconciles row-Gram and column-Gram conventions, identifies the
existing Hadamard equivalence predicate, and connects raw quartet completion
to the existing normalized quartet equations. No exclusion premise is supplied.
-/

noncomputable section
namespace MUB.MonomialTransport
open SzollosiTwoCirculant SzollosiQuartetSystem SzollosiQuadraticSystem

private theorem six_mul_comm (A B : Mat (Fin 6))
    (h : A * B = (6 : ℂ) • (1 : Mat (Fin 6))) :
    B * A = (6 : ℂ) • (1 : Mat (Fin 6)) := by
  have hs : ((1 / 6 : ℂ) • A) * B = 1 := by
    rw [Matrix.smul_mul, h, smul_smul]
    norm_num
  have ht := mul_eq_one_comm.mp hs
  rw [Matrix.mul_smul] at ht
  calc
    B * A = (6 : ℂ) • ((1 / 6 : ℂ) • (B * A)) := by
      rw [smul_smul]
      norm_num
    _ = (6 : ℂ) • (1 : Mat (Fin 6)) := by rw [ht]

theorem rawHadamard_iff_isCH6 (H : Mat (Fin 6)) :
    RawHadamard H ↔ ConcreteSemantics.IsCH6 H := by
  change ((∀ i j, Complex.normSq (H i j) = 1) ∧
      H.conjTranspose * H = (6 : ℂ) • 1) ↔
    ((∀ i j, Complex.normSq (H i j) = 1) ∧
      H * H.conjTranspose = (6 : ℂ) • 1)
  exact ⟨fun h => ⟨h.1, six_mul_comm _ _ h.2⟩,
    fun h => ⟨h.1, six_mul_comm _ _ h.2⟩⟩

theorem monomialEquivalent_iff_hadamardEquivalent (H K : Mat (Fin 6)) :
    MonomialEquivalent H K ↔ ConcreteSemantics.HadamardEquivalent H K := by
  constructor
  · rintro ⟨σ, τ, r, c, hr, hc, rfl⟩
    exact ⟨σ, τ, r, c, hr, hc, fun _ _ => rfl⟩
  · rintro ⟨σ, τ, r, c, hr, hc, h⟩
    exact ⟨σ, τ, r, c, hr, hc, funext (fun i => funext (h i))⟩

theorem hasRawQuartet_iff_rawCandidates (H : Mat (Fin 6)) :
    HasRawQuartet H ↔ RawHadamard H ∧ ∃ U V, RawCandidates H U V := by
  constructor
  · rintro ⟨hH, U, V, hU, hV, hHU, hHV, hUV⟩
    exact ⟨hH, U, V, hU.2, hU.1, hHU, hV.2, hV.1, hHV, hUV⟩
  · rintro ⟨hH, U, V, hU, hIU, hHU, hV, hIV, hHV, hUV⟩
    exact ⟨hH, U, V, ⟨hIU, hU⟩, ⟨hIV, hV⟩, hHU, hHV, hUV⟩

theorem hasRawQuartet_iff_normalized_quartet (H : Mat (Fin 6))
    (hH : RawHadamard H) :
    HasRawQuartet H ↔ ∃ U V,
      Quartet (bases (normalize H) (normalize U) (normalize V)) := by
  have hu := (normalize_unitary_iff H).mpr hH.2
  have hi := (normalize_identity_mu_iff H).mpr hH.1
  rw [hasRawQuartet_iff_rawCandidates]
  simp only [hH, true_and]
  exact ⟨fun ⟨U, V, h⟩ => ⟨U, V, (normalize_quartet_iff H U V hu hi).mpr h⟩,
    fun ⟨U, V, h⟩ => ⟨U, V, (normalize_quartet_iff H U V hu hi).mp h⟩⟩

theorem hasRawQuartet_iff_of_hadamardEquivalent {H K : Mat (Fin 6)}
    (hHK : ConcreteSemantics.HadamardEquivalent H K) :
    HasRawQuartet H ↔ HasRawQuartet K :=
  hasRawQuartet_iff_of_monomialEquivalent
    ((monomialEquivalent_iff_hadamardEquivalent H K).mpr hHK)

theorem gram_left_unitary (W U V : Mat (Fin 6)) (hW : W.conjTranspose * W = 1) :
    (W * U).conjTranspose * (W * V) = U.conjTranspose * V := by
  rw [Matrix.conjTranspose_mul, Matrix.mul_assoc,
    ← Matrix.mul_assoc W.conjTranspose W V, hW, Matrix.one_mul]

theorem quartet_left_unitary (B : Fin 4 → Mat (Fin 6)) (hB : Quartet B)
    (W : Mat (Fin 6)) (hW : W.conjTranspose * W = 1) :
    Quartet (fun a => W * B a) := by
  constructor
  · intro a
    rw [gram_left_unitary W (B a) (B a) hW]
    exact hB.1 a
  · intro a b hab i j
    change Complex.normSq (((W * B a).conjTranspose * (W * B b)) i j) = 1 / 6
    rw [gram_left_unitary W (B a) (B b) hW]
    exact hB.2 a b hab i j

/-- Every actual quartet admits the raw normalization used by the classification route. -/
theorem exists_rawQuartet_of_quartet (B : Fin 4 → Mat (Fin 6)) (hB : Quartet B) :
    ∃ H : Mat (Fin 6), HasRawQuartet H := by
  let W := (B 0).conjTranspose
  have hW : W.conjTranspose * W = 1 := by
    simpa [W] using mul_eq_one_comm.mp (hB.1 0)
  have htrans := quartet_left_unitary B hB W hW
  have he : bases (W * B 1) (W * B 2) (W * B 3) = (fun a => W * B a) := by
    funext a
    fin_cases a <;> simp [bases, W, hB.1 0]
  have hq : Quartet (bases (W * B 1) (W * B 2) (W * B 3)) := by
    rw [he]
    exact htrans
  let H := amplifier • (W * B 1)
  have hn : normalize H = W * B 1 := normalize_amplify _
  have hH : RawHadamard H := by
    constructor
    · apply (normalize_identity_mu_iff H).mp
      rw [hn]
      exact hq.2 0 1 (by decide)
    · apply (normalize_unitary_iff H).mp
      rw [hn]
      exact hq.1 1
  refine ⟨H, (hasRawQuartet_iff_normalized_quartet H hH).mpr
    ⟨amplifier • (W * B 2), amplifier • (W * B 3), ?_⟩⟩
  simpa only [hn, normalize_amplify] using hq

theorem exists_quartet_iff_exists_rawQuartet :
    (∃ B : Fin 4 → Mat (Fin 6), Quartet B) ↔
      ∃ H : Mat (Fin 6), HasRawQuartet H := by
  constructor
  · rintro ⟨B, hB⟩
    exact exists_rawQuartet_of_quartet B hB
  · rintro ⟨H, hH⟩
    obtain ⟨U, V, h⟩ := (hasRawQuartet_iff_normalized_quartet H hH.1).mp hH
    exact ⟨bases (normalize H) (normalize U) (normalize V), h⟩

/-- The remaining mathematical input is exclusion for every representative. -/
theorem no_quartet_of_concrete_representatives (S : Set (Mat (Fin 6)))
    (hcover : ∀ H, ConcreteSemantics.IsCH6 H →
      ∃ K ∈ S, ConcreteSemantics.HadamardEquivalent H K)
    (hexclude : ∀ K ∈ S, ¬ HasRawQuartet K) :
    ∀ B : Fin 4 → Mat (Fin 6), ¬ Quartet B := by
  have hraw : ∀ H : Mat (Fin 6), ¬ HasRawQuartet H :=
    no_raw_quartet_of_complete_representatives S (by
      intro H hH
      obtain ⟨K, hKS, hHK⟩ := hcover H ((rawHadamard_iff_isCH6 H).mp hH)
      exact ⟨K, hKS, (monomialEquivalent_iff_hadamardEquivalent H K).mpr hHK⟩) hexclude
  intro B hB
  obtain ⟨H, hH⟩ := exists_rawQuartet_of_quartet B hB
  exact hraw H hH

#print axioms rawHadamard_iff_isCH6
#print axioms monomialEquivalent_iff_hadamardEquivalent
#print axioms hasRawQuartet_iff_rawCandidates
#print axioms hasRawQuartet_iff_normalized_quartet
#print axioms hasRawQuartet_iff_of_hadamardEquivalent
#print axioms gram_left_unitary
#print axioms quartet_left_unitary
#print axioms exists_rawQuartet_of_quartet
#print axioms exists_quartet_iff_exists_rawQuartet
#print axioms no_quartet_of_concrete_representatives
end MUB.MonomialTransport
