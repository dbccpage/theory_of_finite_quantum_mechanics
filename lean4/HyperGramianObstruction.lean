/- These declarations are opaque and were not elaborated by Lake in this change. -/

/- Conditional interfaces and arithmetic examples only.
No Rust receipt instantiates the curvature, Gramian representation, or coverage
hypotheses in this module. The named theorem statements are the precise scope.
AuthorityEffect: None.
-/
import Gluing

namespace MUB6.Gluing.HyperGramianObstruction

open MUB6.Gluing

structure Matrix5 where
  carrier : Unit := ()
deriving Inhabited, Nonempty

opaque TraceInner5 : Matrix5 → Matrix5 → Int

opaque InPSDCone5 : Matrix5 → Prop

def PSD5 (G : Matrix5) : Prop :=
  InPSDCone5 G ∧ (∀ (W : Matrix5), InPSDCone5 W → 0 ≤ TraceInner5 W G)

structure Matrix6 where
  carrier : Unit := ()
deriving Inhabited, Nonempty

opaque TraceInner6 : Matrix6 → Matrix6 → Int

opaque InPSDCone6 : Matrix6 → Prop

def PSD6 (G : Matrix6) : Prop :=
  InPSDCone6 G ∧ (∀ (W : Matrix6), InPSDCone6 W → 0 ≤ TraceInner6 W G)

theorem hyper_gramian_5_incompatibility
    {G : Matrix5} (W : Matrix5) (hW_psd : PSD5 W) (h_inner : TraceInner5 W G < 0) :
    ¬ (PSD5 G) := by
  intro hG_psd
  have h_nonneg : 0 ≤ TraceInner5 W G := hG_psd.2 W hW_psd.1
  omega

theorem hyper_gramian_6_incompatibility
    {G : Matrix6} (W : Matrix6) (hW_psd : PSD6 W) (h_inner : TraceInner6 W G < 0) :
    ¬ (PSD6 G) := by
  intro hG_psd
  have h_nonneg : 0 ≤ TraceInner6 W G := hG_psd.2 W hW_psd.1
  omega

def MUBPentuple : Prop :=
  ∃ (B : Fin 5 → Basis), PairwiseMU B

def MUBSextuple : Prop :=
  ∃ (B : Fin 6 → Basis), PairwiseMU B

opaque hyper_gramian_5 (B : Fin 5 → Basis) : Matrix5

opaque hyper_gramian_6 (B : Fin 6 → Basis) : Matrix6

def GenuinePentupleGramianPSDProperty : Prop :=
  ∀ (B : Fin 5 → Basis), PairwiseMU B → PSD5 (hyper_gramian_5 B)

def GenuineSextupleGramianPSDProperty : Prop :=
  ∀ (B : Fin 6 → Basis), PairwiseMU B → PSD6 (hyper_gramian_6 B)

theorem hyper_gramian_5_no_mub_pentuple
    {G : Matrix5} (W : Matrix5) (hW_psd : PSD5 W)
    (B : Fin 5 → Basis) (hB : PairwiseMU B)
    (h_gram : hyper_gramian_5 B = G)
    (h_inner : TraceInner5 W G < 0)
    (h_psd_prop : GenuinePentupleGramianPSDProperty) :
    False := by
  have hG_psd : PSD5 G := by
    rw [← h_gram]
    exact h_psd_prop B hB
  have h_not_psd : ¬ (PSD5 G) := hyper_gramian_5_incompatibility W hW_psd h_inner
  exact h_not_psd hG_psd

theorem no_mub_pentuple_of_sdp_certificate
    {G : Matrix5} (W : Matrix5) (hW_psd : PSD5 W) (h_inner : TraceInner5 W G < 0)
    (h_gram_eq : ∀ (B : Fin 5 → Basis), PairwiseMU B → hyper_gramian_5 B = G)
    (h_psd_prop : GenuinePentupleGramianPSDProperty) :
    ¬ MUBPentuple := by
  intro ⟨B, hB⟩
  have h_eq := h_gram_eq B hB
  exact hyper_gramian_5_no_mub_pentuple W hW_psd B hB h_eq h_inner h_psd_prop

theorem hyper_gramian_6_no_mub_sextuple
    {G : Matrix6} (W : Matrix6) (hW_psd : PSD6 W)
    (B : Fin 6 → Basis) (hB : PairwiseMU B)
    (h_gram : hyper_gramian_6 B = G)
    (h_inner : TraceInner6 W G < 0)
    (h_psd_prop : GenuineSextupleGramianPSDProperty) :
    False := by
  have hG_psd : PSD6 G := by
    rw [← h_gram]
    exact h_psd_prop B hB
  have h_not_psd : ¬ (PSD6 G) := hyper_gramian_6_incompatibility W hW_psd h_inner
  exact h_not_psd hG_psd

theorem no_mub_sextuple_of_sdp_certificate
    {G : Matrix6} (W : Matrix6) (hW_psd : PSD6 W) (h_inner : TraceInner6 W G < 0)
    (h_gram_eq : ∀ (B : Fin 6 → Basis), PairwiseMU B → hyper_gramian_6 B = G)
    (h_psd_prop : GenuineSextupleGramianPSDProperty) :
    ¬ MUBSextuple := by
  intro ⟨B, hB⟩
  have h_eq := h_gram_eq B hB
  exact hyper_gramian_6_no_mub_sextuple W hW_psd B hB h_eq h_inner h_psd_prop

def embed57 (i : Fin 5) : Fin 7 :=
  ⟨i.val, by omega⟩

theorem embed57_injective (i j : Fin 5) (h : embed57 i = embed57 j) : i = j := by
  ext
  have h_val : (embed57 i).val = (embed57 j).val := by rw [h]
  exact h_val

def restrict57 (B : Fin 7 → Basis) : Fin 5 → Basis :=
  fun i => B (embed57 i)

theorem pairwise_mu_restrict57 (B : Fin 7 → Basis) (hB : PairwiseMU B) :
    PairwiseMU (restrict57 B) := by
  intro i j hij
  apply hB
  intro heq
  exact hij (embed57_injective i j heq)

theorem mub_pentuple_of_complete (h_comp : CompleteMUB6) : MUBPentuple := by
  rcases h_comp with ⟨B7, hB7⟩
  exact ⟨restrict57 B7, pairwise_mu_restrict57 B7 hB7⟩

theorem no_complete_mub6_of_no_pentuple (h_no_pent : ¬ MUBPentuple) :
    NoCompleteMUB6 := by
  intro h_comp
  have h_pent := mub_pentuple_of_complete h_comp
  exact h_no_pent h_pent

theorem no_complete_mub6_of_hyper_gramian_5_certificate
    {G : Matrix5} (W : Matrix5) (hW_psd : PSD5 W) (h_inner : TraceInner5 W G < 0)
    (h_gram_eq : ∀ (B : Fin 5 → Basis), PairwiseMU B → hyper_gramian_5 B = G)
    (h_psd_prop : GenuinePentupleGramianPSDProperty) :
    NoCompleteMUB6 :=
  no_complete_mub6_of_no_pentuple
    (no_mub_pentuple_of_sdp_certificate W hW_psd h_inner h_gram_eq h_psd_prop)

def embed67 (i : Fin 6) : Fin 7 :=
  ⟨i.val, by omega⟩

theorem embed67_injective (i j : Fin 6) (h : embed67 i = embed67 j) : i = j := by
  ext
  have h_val : (embed67 i).val = (embed67 j).val := by rw [h]
  exact h_val

def restrict67 (B : Fin 7 → Basis) : Fin 6 → Basis :=
  fun i => B (embed67 i)

theorem pairwise_mu_restrict67 (B : Fin 7 → Basis) (hB : PairwiseMU B) :
    PairwiseMU (restrict67 B) := by
  intro i j hij
  apply hB
  intro heq
  exact hij (embed67_injective i j heq)

theorem mub_sextuple_of_complete (h_comp : CompleteMUB6) : MUBSextuple := by
  rcases h_comp with ⟨B7, hB7⟩
  exact ⟨restrict67 B7, pairwise_mu_restrict67 B7 hB7⟩

theorem no_complete_mub6_of_no_sextuple (h_no_sext : ¬ MUBSextuple) :
    NoCompleteMUB6 := by
  intro h_comp
  have h_sext := mub_sextuple_of_complete h_comp
  exact h_no_sext h_sext

theorem no_complete_mub6_of_hyper_gramian_6_certificate
    {G : Matrix6} (W : Matrix6) (hW_psd : PSD6 W) (h_inner : TraceInner6 W G < 0)
    (h_gram_eq : ∀ (B : Fin 6 → Basis), PairwiseMU B → hyper_gramian_6 B = G)
    (h_psd_prop : GenuineSextupleGramianPSDProperty) :
    NoCompleteMUB6 :=
  no_complete_mub6_of_no_sextuple
    (no_mub_sextuple_of_sdp_certificate W hW_psd h_inner h_gram_eq h_psd_prop)

#print axioms hyper_gramian_5_incompatibility
#print axioms hyper_gramian_6_incompatibility
#print axioms embed57_injective
#print axioms pairwise_mu_restrict57
#print axioms mub_pentuple_of_complete
#print axioms no_complete_mub6_of_no_pentuple
#print axioms hyper_gramian_5_no_mub_pentuple
#print axioms no_mub_pentuple_of_sdp_certificate
#print axioms no_complete_mub6_of_hyper_gramian_5_certificate
#print axioms embed67_injective
#print axioms pairwise_mu_restrict67
#print axioms mub_sextuple_of_complete
#print axioms no_complete_mub6_of_no_sextuple
#print axioms hyper_gramian_6_no_mub_sextuple
#print axioms no_mub_sextuple_of_sdp_certificate
#print axioms no_complete_mub6_of_hyper_gramian_6_certificate

end MUB6.Gluing.HyperGramianObstruction
