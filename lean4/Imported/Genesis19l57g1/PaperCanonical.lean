/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/PaperCanonical.lean
   Original sha256: 1fcbd905c75af3b094f6e2bb9e068373ed14b658d9c7ecb9ad48ba4ebd2ad3f0 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.Genesis19l57g1.PaperCanonical
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.Genesis19l57g1.Derivation.IsoCanon
import Imported.Genesis19l57g1.Derivation.Ext
import Init.Data.List.Sort.Lemmas
import Init.Data.Ord

/-!
Concrete five-field serialization soundness. These companion results close
the collection-sort gap recorded in the unchanged pinned IsoCanon module.
They do not assume search minimality or an implementation refinement theorem.
-/

namespace GenesisPaper

open Derivation

local instance {A B : Type} [Ord A] [Ord B] : Ord (A × B) := lexOrd

def sortValues {A : Type} [Ord A] (values : List A) : List A :=
  values.mergeSort (fun a b => compare a b != Ordering.gt)

theorem mem_sortValues {A : Type} [Ord A] (x : A) (values : List A) :
    x ∈ sortValues values ↔ x ∈ values := by
  exact List.mem_mergeSort

def normalizeCollections (r : Regime) : Regime :=
  { r with insts := sortValues r.insts, rules := sortValues r.rules,
           reqs := sortValues r.reqs }

theorem normalizeCollections_ext (r : Regime) : RegimeExt r (normalizeCollections r) :=
  ⟨rfl, rfl, fun x => (mem_sortValues x r.insts).symm,
   fun x => (mem_sortValues x r.rules).symm, fun x => (mem_sortValues x r.reqs).symm⟩

theorem regimeExt_trans {r s t : Regime} (h : RegimeExt r s) (k : RegimeExt s t) :
    RegimeExt r t :=
  ⟨h.1.trans k.1, h.2.1.trans k.2.1,
   fun x => (h.2.2.1 x).trans (k.2.2.1 x),
   fun x => (h.2.2.2.1 x).trans (k.2.2.2.1 x),
   fun x => (h.2.2.2.2 x).trans (k.2.2.2.2 x)⟩

theorem normalized_eq_ext {r s : Regime}
    (h : normalizeCollections r = normalizeCollections s) : RegimeExt r s := by
  have hn : RegimeExt (normalizeCollections r) (normalizeCollections s) := by
    rw [h]
    exact RegimeExt.refl' _
  exact regimeExt_trans (normalizeCollections_ext r)
    (regimeExt_trans hn (normalizeCollections_ext s).symm')

/-- Membership-extensional collections give an identity-index isomorphism.
Only ordered requirements are needed; duplicate-free collections are not
needed for this soundness direction. -/
def isoOfExt {r s : Regime} (h : RegimeExt r s)
    (ordered : ∀ q ∈ r.reqs, q.1 ≤ q.2) : Iso r s where
  dmap := id
  dinv := id
  fmap := id
  finv := id
  dmap_lt := fun d hd => by simpa [h.1] using List.mem_range.mp hd
  dinv_lt := fun d hd => by simpa [h.1] using List.mem_range.mp hd
  dinv_dmap := fun _ _ => rfl
  dmap_dinv := fun _ _ => rfl
  fmap_lt := fun f hf => by simpa [h.2.1] using List.mem_range.mp hf
  finv_lt := fun f hf => by simpa [h.2.1] using List.mem_range.mp hf
  finv_fmap := fun _ _ => rfl
  fmap_finv := fun _ _ => rfl
  arity := fun _ _ => by simp [h.2.1]
  insts_fwd := fun p hp => by simpa using (h.2.2.1 p).mp hp
  insts_bwd := fun p hp => by simpa using (h.2.2.1 p).mpr hp
  rules_fwd := fun f hf => (h.2.2.2.1 f).mp hf
  rules_bwd := fun f hf => (h.2.2.2.1 f).mpr hf
  reqs_fwd := fun q hq => by
    simpa [sortPair, ordered q hq] using (h.2.2.2.2 q).mp hq
  reqs_bwd := fun q hq => by
    have hr := (h.2.2.2.2 q).mpr hq
    simpa [sortPair, ordered q hr] using hr

theorem relabel_requirements_ordered (r : Regime)
    (pi : DRen r.data) (phi : DRen r.forms.length) :
    ∀ q ∈ (relabel r pi phi).reqs, q.1 ≤ q.2 := by
  intro q hq
  obtain ⟨p, _, rfl⟩ := List.mem_map.mp hq
  exact Nat.le_trans (Nat.min_le_left _ _) (Nat.le_max_left _ _)

/-- The same structural tuple used by Python and Rust, before byte encoding. -/
abbrev StructuralKey := Nat × List Nat × List Inst × List Nat × List (Nat × Nat)

def structuralKey (r : Regime) : StructuralKey :=
  (r.data, r.forms, sortValues r.insts, sortValues r.rules, sortValues r.reqs)

def keyRegime (key : StructuralKey) : Regime :=
  ⟨key.1, key.2.1, key.2.2.1, key.2.2.2.1, key.2.2.2.2⟩

theorem keyRegime_structuralKey (r : Regime) :
    keyRegime (structuralKey r) = normalizeCollections r := rfl

def serializedRelabel (r : Regime) (pi : DRen r.data)
    (phi : DRen r.forms.length) : StructuralKey :=
  structuralKey (relabel r pi phi)

/-- Equal sorted relabelling tuples yield an explicit structural isomorphism.
The maps are returned by composing the input bijections with the identity
isomorphism between the membership-extensional relabelled regimes. -/
def isoOfSerializedRelabelEq {r s : Regime}
    (pir : DRen r.data) (phir : DRen r.forms.length)
    (pis : DRen s.data) (phis : DRen s.forms.length)
    (hr : ∀ q ∈ r.reqs, q.1 ≤ q.2) (hs : ∀ q ∈ s.reqs, q.1 ≤ q.2)
    (heq : serializedRelabel r pir phir = serializedRelabel s pis phis) : Iso r s :=
  let ext := normalized_eq_ext (congrArg keyRegime heq)
  (relabel_iso r pir phir hr).trans
    ((isoOfExt ext (relabel_requirements_ordered r pir phir)).trans
      (relabel_iso s pis phis hs).symm)

theorem serializedRelabel_sound {r s : Regime}
    (pir : DRen r.data) (phir : DRen r.forms.length)
    (pis : DRen s.data) (phis : DRen s.forms.length)
    (hr : r.wf) (hs : s.wf)
    (heq : serializedRelabel r pir phir = serializedRelabel s pis phis) :
    Nonempty (Iso r s) :=
  ⟨isoOfSerializedRelabelEq pir phir pis phis
    (fun q hq => Nat.le_of_lt (hr.2.2.1 q hq).1)
    (fun q hq => Nat.le_of_lt (hs.2.2.1 q hq).1) heq⟩

end GenesisPaper
