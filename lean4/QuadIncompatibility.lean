/- These declarations are opaque and were not elaborated by Lake in this change. -/

/- Conditional interfaces and arithmetic examples only.
No Rust receipt instantiates the curvature, Gramian representation, or coverage
hypotheses in this module. The named theorem statements are the precise scope.
AuthorityEffect: None.
-/
import Gluing

namespace MUB6.Gluing.QuadIncompatibility

open MUB6.Gluing

structure Matrix where
  carrier : Unit := ()
deriving Inhabited, Nonempty

opaque TraceInner : Matrix → Matrix → Int

opaque InPSDCone : Matrix → Prop

def PSD (G : Matrix) : Prop :=
  InPSDCone G ∧ (∀ (W : Matrix), InPSDCone W → 0 ≤ TraceInner W G)

theorem quad_incompatibility
    {G : Matrix} (W : Matrix) (hW_psd : PSD W) (h_inner : TraceInner W G < 0) :
    ¬ (PSD G) := by
  intro hG_psd
  have h_nonneg : 0 ≤ TraceInner W G := hG_psd.2 W hW_psd.1
  omega

def MUBQuadruple : Prop :=
  ∃ (B : Fin 4 → Basis), PairwiseMU B

opaque quad_gramian (B : Fin 4 → Basis) : Matrix

def GenuineQuadGramianPSDProperty : Prop :=
  ∀ (B : Fin 4 → Basis), PairwiseMU B → PSD (quad_gramian B)

theorem quad_incompatibility_no_mub_quadruple
    {G : Matrix} (W : Matrix) (hW_psd : PSD W)
    (B : Fin 4 → Basis) (hB : PairwiseMU B)
    (h_gram : quad_gramian B = G)
    (h_inner : TraceInner W G < 0)
    (h_psd_prop : GenuineQuadGramianPSDProperty) :
    False := by
  have hG_psd : PSD G := by
    rw [← h_gram]
    exact h_psd_prop B hB
  have h_not_psd : ¬ (PSD G) := quad_incompatibility W hW_psd h_inner
  exact h_not_psd hG_psd

theorem no_mub_quadruple_of_sdp_certificate
    {G : Matrix} (W : Matrix) (hW_psd : PSD W) (h_inner : TraceInner W G < 0)
    (h_gram_eq : ∀ (B : Fin 4 → Basis), PairwiseMU B → quad_gramian B = G)
    (h_psd_prop : GenuineQuadGramianPSDProperty) :
    ¬ MUBQuadruple := by
  intro ⟨B, hB⟩
  have h_eq := h_gram_eq B hB
  exact quad_incompatibility_no_mub_quadruple W hW_psd B hB h_eq h_inner h_psd_prop

def embed47 (i : Fin 4) : Fin 7 :=
  ⟨i.val, by omega⟩

theorem embed47_injective (i j : Fin 4) (h : embed47 i = embed47 j) : i = j := by
  ext
  have h_val : (embed47 i).val = (embed47 j).val := by rw [h]
  exact h_val

def restrict47 (B : Fin 7 → Basis) : Fin 4 → Basis :=
  fun i => B (embed47 i)

theorem pairwise_mu_restrict47 (B : Fin 7 → Basis) (hB : PairwiseMU B) :
    PairwiseMU (restrict47 B) := by
  intro i j hij
  apply hB
  intro heq
  exact hij (embed47_injective i j heq)

theorem mub_quadruple_of_complete (h_comp : CompleteMUB6) : MUBQuadruple := by
  rcases h_comp with ⟨B7, hB7⟩
  exact ⟨restrict47 B7, pairwise_mu_restrict47 B7 hB7⟩

theorem no_complete_mub6_of_no_quadruple (h_no_quad : ¬ MUBQuadruple) :
    NoCompleteMUB6 := by
  intro h_comp
  have h_quad := mub_quadruple_of_complete h_comp
  exact h_no_quad h_quad

theorem no_complete_mub6_of_sdp_dual_certificate
    {G : Matrix} (W : Matrix) (hW_psd : PSD W) (h_inner : TraceInner W G < 0)
    (h_gram_eq : ∀ (B : Fin 4 → Basis), PairwiseMU B → quad_gramian B = G)
    (h_psd_prop : GenuineQuadGramianPSDProperty) :
    NoCompleteMUB6 :=
  no_complete_mub6_of_no_quadruple
    (no_mub_quadruple_of_sdp_certificate W hW_psd h_inner h_gram_eq h_psd_prop)

#print axioms quad_incompatibility
#print axioms embed47_injective
#print axioms pairwise_mu_restrict47
#print axioms mub_quadruple_of_complete
#print axioms no_complete_mub6_of_no_quadruple
#print axioms quad_incompatibility_no_mub_quadruple
#print axioms no_mub_quadruple_of_sdp_certificate
#print axioms no_complete_mub6_of_sdp_dual_certificate

end MUB6.Gluing.QuadIncompatibility
