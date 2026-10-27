/- Imported so that this repository carries its own Lean evidence.
   Original sha256: a576d78131f40e65aff8238eb8ddbb03198f9a1cf7d8fd0b64ec83a90495bb20 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisDerivation.PaperOrbit
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
import Imported.GenesisDerivation.PaperCanonical
import Imported.GenesisDerivation.Derivation.Pigeonhole
import Init.Data.Order

/-!
Concrete isomorphism-to-serialization bridge. The collections represent sets,
so the completeness direction requires duplicate-free inputs. All finite
bijections below are constructed from the supplied isomorphism.
-/

namespace GenesisPaper.Orbit

open Derivation GenesisPaper

local instance {A B : Type} [Ord A] [Ord B] : Ord (A × B) := lexOrd

-- The library's factory-built Nat order-law instances use choice on this
-- toolchain. These proofs establish the laws of the same comparator directly.
theorem natTransOrd : Std.TransOrd Nat where
  eq_swap := (Nat.compare_swap _ _).symm
  isLE_trans := fun hab hbc => Nat.isLE_compare.mpr
    (Nat.le_trans (Nat.isLE_compare.mp hab) (Nat.isLE_compare.mp hbc))

theorem natLawfulEqOrd : Std.LawfulEqOrd Nat where
  compare_self := Nat.compare_eq_eq.mpr rfl
  eq_of_compare := Nat.compare_eq_eq.mp

local instance : Std.TransOrd Nat := natTransOrd
local instance : Std.LawfulEqOrd Nat := natLawfulEqOrd

theorem bounded_injection_le (n m : Nat) (f g : Nat → Nat)
    (bound : ∀ x, x < n → f x < m)
    (inverse : ∀ x, x < n → g (f x) = x) : n ≤ m := by
  have nd := Pigeonhole.map_nodup_of_inj f n (by
    intro x hx y hy hne heq
    apply hne
    have h := congrArg g heq
    simpa [inverse x hx, inverse y hy] using h)
  have hl := Pigeonhole.nodup_length_le m ((Pigeonhole.upto n).map f) nd (by
    intro y hy
    obtain ⟨x, hx, rfl⟩ := List.mem_map.mp hy
    exact bound x (Pigeonhole.upto_mem n x hx))
  simpa [Pigeonhole.upto_length] using hl

theorem iso_data_eq {r s : Regime} (h : Iso r s) : r.data = s.data :=
  Nat.le_antisymm
    (bounded_injection_le _ _ h.dmap h.dinv
      (fun x hx => h.dmap_lt x (List.mem_range.mpr hx))
      (fun x hx => h.dinv_dmap x (List.mem_range.mpr hx)))
    (bounded_injection_le _ _ h.dinv h.dmap
      (fun x hx => h.dinv_lt x (List.mem_range.mpr hx))
      (fun x hx => h.dmap_dinv x (List.mem_range.mpr hx)))

theorem iso_form_count_eq {r s : Regime} (h : Iso r s) :
    r.forms.length = s.forms.length :=
  Nat.le_antisymm
    (bounded_injection_le _ _ h.fmap h.finv
      (fun x hx => h.fmap_lt x (List.mem_range.mpr hx))
      (fun x hx => h.finv_fmap x (List.mem_range.mpr hx)))
    (bounded_injection_le _ _ h.finv h.fmap
      (fun x hx => h.finv_lt x (List.mem_range.mpr hx))
      (fun x hx => h.fmap_finv x (List.mem_range.mpr hx)))

def extendFinite (n : Nat) (f g : Nat → Nat)
    (fb : ∀ x, x < n → f x < n) (gb : ∀ x, x < n → g x < n)
    (gf : ∀ x, x < n → g (f x) = x)
    (fg : ∀ x, x < n → f (g x) = x) : DRen n where
  f := padF n f
  g := padF n g
  fg := fun x => by
    by_cases hx : x < n
    · rw [padF_lt _ hx, padF_lt _ (fb x hx), gf x hx]
    · rw [padF_ge _ hx, padF_ge _ hx]
  gf := fun x => by
    by_cases hx : x < n
    · rw [padF_lt _ hx, padF_lt _ (gb x hx), fg x hx]
    · rw [padF_ge _ hx, padF_ge _ hx]
  fbound := fun x hx => by rw [padF_lt _ hx]; exact fb x hx
  gbound := fun x hx => by rw [padF_lt _ hx]; exact gb x hx

def datumRen {r s : Regime} (h : Iso r s) : DRen r.data :=
  extendFinite r.data h.dmap h.dinv
    (fun x hx => by rw [iso_data_eq h]; exact h.dmap_lt x (List.mem_range.mpr hx))
    (fun x hx => h.dinv_lt x (List.mem_range.mpr (by rwa [← iso_data_eq h])))
    (fun x hx => h.dinv_dmap x (List.mem_range.mpr hx))
    (fun x hx => h.dmap_dinv x (List.mem_range.mpr (by rwa [← iso_data_eq h])))

def formRen {r s : Regime} (h : Iso r s) : DRen r.forms.length :=
  extendFinite r.forms.length h.fmap h.finv
    (fun x hx => by rw [iso_form_count_eq h]; exact h.fmap_lt x (List.mem_range.mpr hx))
    (fun x hx => h.finv_lt x (List.mem_range.mpr (by rwa [← iso_form_count_eq h])))
    (fun x hx => h.finv_fmap x (List.mem_range.mpr hx))
    (fun x hx => h.fmap_finv x (List.mem_range.mpr (by rwa [← iso_form_count_eq h])))

theorem cmpLE_iff {A : Type} [Ord A] (a b : A) :
    (compare a b != Ordering.gt) = (compare a b).isLE := by
  cases compare a b <;> rfl

theorem sortValues_eq_of_perm {A : Type} [Ord A] [Std.TransOrd A] [Std.LawfulEqOrd A]
    {xs ys : List A} (hp : xs.Perm ys) : sortValues xs = sortValues ys := by
  have trans : ∀ a b c : A, (compare a b != Ordering.gt) →
      (compare b c != Ordering.gt) → (compare a c != Ordering.gt) := by
    intro a b c hab hbc
    simp only [cmpLE_iff] at *
    exact Std.TransOrd.isLE_trans hab hbc
  have total : ∀ a b : A, (compare a b != Ordering.gt) || (compare b a != Ordering.gt) := by
    intro a b
    rw [Std.OrientedOrd.eq_swap (a := b) (b := a)]
    cases compare a b <;> decide
  exact List.Perm.eq_of_pairwise (fun a b _ _ hab hba => by
    simp only [cmpLE_iff] at hab hba
    exact Std.LawfulEqOrd.compare_eq_iff_eq.mp (Std.OrientedCmp.isLE_antisymm hab hba))
    (List.pairwise_mergeSort trans total xs) (List.pairwise_mergeSort trans total ys)
    ((List.mergeSort_perm xs _).trans (hp.trans (List.mergeSort_perm ys _).symm))

theorem perm_of_nodup_membership {A : Type} [BEq A] [LawfulBEq A] [DecidableEq A]
    {xs ys : List A} (hx : xs.Nodup) (hy : ys.Nodup)
    (hm : ∀ a, a ∈ xs ↔ a ∈ ys) : xs.Perm ys := by
  induction xs generalizing ys with
  | nil =>
    cases ys with
    | nil => exact .nil
    | cons a ys => exact False.elim (List.not_mem_nil ((hm a).mpr (List.mem_cons_self ..)))
  | cons a xs ih =>
    have ha : a ∈ ys := (hm a).mp (List.mem_cons_self ..)
    obtain ⟨pre, suf, rfl⟩ := List.append_of_mem ha
    have hp : (pre ++ a :: suf).Perm (a :: (pre ++ suf)) := List.perm_middle
    have hn := List.nodup_cons.mp (hp.nodup hy)
    have hm' : ∀ b, b ∈ xs ↔ b ∈ pre ++ suf := by
      intro b
      by_cases hb : b = a
      · subst b
        exact ⟨fun h => False.elim ((List.nodup_cons.mp hx).1 h),
          fun h => False.elim (hn.1 h)⟩
      · simpa only [List.mem_cons, List.mem_append, hb, false_or] using hm b
    exact ((ih hx.tail hn.2 hm').cons a).trans hp.symm

def SetCollections (r : Regime) : Prop :=
  r.insts.Nodup ∧ r.rules.Nodup ∧ r.reqs.Nodup

theorem structuralKey_eq_of_ext {r s : Regime} (he : RegimeExt r s)
    (hr : SetCollections r) (hs : SetCollections s) : structuralKey r = structuralKey s := by
  have hi := sortValues_eq_of_perm (perm_of_nodup_membership hr.1 hs.1 he.2.2.1)
  have hu := sortValues_eq_of_perm (perm_of_nodup_membership hr.2.1 hs.2.1 he.2.2.2.1)
  have hq := sortValues_eq_of_perm (perm_of_nodup_membership hr.2.2 hs.2.2 he.2.2.2.2)
  simp only [structuralKey, he.1, he.2.1, hi, hu, hq]

theorem datumRen_f {r s : Regime} (h : Iso r s) {d : Nat} (hd : d < r.data) :
    (datumRen h).f d = h.dmap d := padF_lt _ hd

theorem formRen_f {r s : Regime} (h : Iso r s) {f : Nat} (hf : f < r.forms.length) :
    (formRen h).f f = h.fmap f := padF_lt _ hf

theorem formRen_g {r s : Regime} (h : Iso r s) {f : Nat} (hf : f < r.forms.length) :
    (formRen h).g f = h.finv f := padF_lt _ hf

theorem mapInst_iso {r s : Regime} (h : Iso r s) (hr : r.wf)
    {p : Inst} (hp : p ∈ r.insts) :
    ((formRen h).f p.1, p.2.map (datumRen h).f) = (h.fmap p.1, p.2.map h.dmap) := by
  rw [formRen_f h (hr.1 p hp).1]
  congr 1
  exact List.map_congr_left (fun a ha => datumRen_f h ((hr.1 p hp).2.2 a ha))

theorem getD_eq_getElem {A : Type} (xs : List A) (d : A) {i : Nat} (hi : i < xs.length) :
    xs.getD i d = xs[i] := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]
  rfl

theorem relabel_ext_of_iso {r s : Regime} (h : Iso r s) (hr : r.wf) (hs : s.wf) :
    RegimeExt (relabel r (datumRen h) (formRen h)) s := by
  have hi : (relabel r (datumRen h) (formRen h)).insts =
      r.insts.map (fun p => (h.fmap p.1, p.2.map h.dmap)) := by
    rw [relabel_insts, List.map_map]
    exact List.map_congr_left (fun p hp => mapInst_iso h hr hp)
  have hu : (relabel r (datumRen h) (formRen h)).rules = r.rules.map h.fmap := by
    rw [relabel_rules]
    exact List.map_congr_left (fun f hf => formRen_f h (hr.2.1 f hf))
  have hq : (relabel r (datumRen h) (formRen h)).reqs =
      r.reqs.map (fun q => sortPair (h.dmap q.1, h.dmap q.2)) := by
    rw [relabel_reqs]
    apply List.map_congr_left
    intro q hq
    rw [mapReq_eq_sortPair, datumRen_f h (Nat.lt_trans (hr.2.2.1 q hq).1 (hr.2.2.1 q hq).2),
      datumRen_f h (hr.2.2.1 q hq).2]
  refine ⟨by simpa using iso_data_eq h, ?_, ?_, ?_, ?_⟩
  · rw [relabel_forms]
    apply List.ext_getElem
    · simpa using iso_form_count_eq h
    · intro j hj hj'
      have hjr : j < r.forms.length := by simpa using hj
      rw [← getD_eq_getElem _ 0 hj, ← getD_eq_getElem _ 0 hj', permForms_getD _ _ hjr,
        formRen_g h hjr]
      have e := h.arity (h.finv j) (List.mem_range.mpr (h.finv_lt j (List.mem_range.mpr hj')))
      rw [h.fmap_finv j (List.mem_range.mpr hj')] at e
      exact e.symm
  · intro p
    rw [hi]
    constructor
    · intro hp
      obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hp
      exact h.insts_fwd q hq
    · intro hp
      refine List.mem_map.mpr ⟨(h.finv p.1, p.2.map h.dinv), h.insts_bwd p hp, ?_⟩
      have ep : (p.2.map h.dinv).map h.dmap = p.2 := by
        rw [List.map_map]
        exact map_eq_self_of_mem (fun a ha => h.dmap_dinv a
          (List.mem_range.mpr ((hs.1 p hp).2.2 a ha)))
      simp only [h.fmap_finv p.1 (List.mem_range.mpr (hs.1 p hp).1), ep]
  · intro f
    rw [hu]
    constructor
    · intro hf
      obtain ⟨g, hg, rfl⟩ := List.mem_map.mp hf
      exact h.rules_fwd g hg
    · intro hf
      exact List.mem_map.mpr ⟨h.finv f, h.rules_bwd f hf,
        h.fmap_finv f (List.mem_range.mpr (hs.2.1 f hf))⟩
  · intro q
    rw [hq]
    constructor
    · intro hq
      obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hq
      exact h.reqs_fwd p hp
    · intro hq
      refine List.mem_map.mpr ⟨sortPair (h.dinv q.1, h.dinv q.2), h.reqs_bwd q hq, ?_⟩
      rw [sortPair_map_sortPair,
        h.dmap_dinv q.1 (List.mem_range.mpr (Nat.lt_trans (hs.2.2.1 q hq).1 (hs.2.2.1 q hq).2)),
        h.dmap_dinv q.2 (List.mem_range.mpr (hs.2.2.1 q hq).2),
        sortPair_of_le (Nat.le_of_lt (hs.2.2.1 q hq).1)]

theorem map_nodup_injective {A B : Type} (f : A → B)
    (inj : ∀ x y, f x = f y → x = y) :
    ∀ xs : List A, xs.Nodup → (xs.map f).Nodup := by
  intro xs
  induction xs with
  | nil => intro _; exact .nil
  | cons x xs ih =>
    intro hn
    refine .cons ?_ (ih hn.tail)
    intro y hy he
    obtain ⟨z, hz, rfl⟩ := List.mem_map.mp hy
    exact (List.nodup_cons.mp hn).1 ((inj x z he) ▸ hz)

theorem map_nodup_on {A B : Type} (f : A → B) :
    ∀ xs : List A, xs.Nodup →
      (∀ x ∈ xs, ∀ y ∈ xs, f x = f y → x = y) → (xs.map f).Nodup := by
  intro xs
  induction xs with
  | nil => intro _ _; exact .nil
  | cons x xs ih =>
    intro hn inj
    refine .cons ?_ (ih hn.tail (fun y hy z hz =>
      inj y (List.mem_cons_of_mem _ hy) z (List.mem_cons_of_mem _ hz)))
    intro y hy he
    obtain ⟨z, hz, rfl⟩ := List.mem_map.mp hy
    exact (List.nodup_cons.mp hn).1
      ((inj x (List.mem_cons_self ..) z (List.mem_cons_of_mem _ hz) he) ▸ hz)

theorem relabel_setCollections (r : Regime) (pi : DRen r.data) (phi : DRen r.forms.length)
    (hr : SetCollections r) (ordered : ∀ q ∈ r.reqs, q.1 ≤ q.2) :
    SetCollections (relabel r pi phi) := by
  refine ⟨?_, ?_, ?_⟩
  · rw [relabel_insts, List.map_map]
    apply map_nodup_injective _ _ _ hr.1
    intro p q he
    have hf := congrArg (fun x : Inst => phi.g x.1) he
    have ha := congrArg (fun x : Inst => x.2.map pi.g) he
    simp only [Function.comp_apply, mapInst, mapInstForm, phi.fg] at hf ha
    have inv : ∀ xs : List Nat, (xs.map pi.f).map pi.g = xs := by
      intro xs
      rw [List.map_map]
      exact map_eq_self_of_mem (fun x _ => pi.fg x)
    rw [inv, inv] at ha
    exact Prod.ext hf ha
  · rw [relabel_rules]
    exact map_nodup_injective phi.f (fun x y he => by
      have e := congrArg phi.g he
      simpa only [phi.fg] using e) _ hr.2.1
  · rw [relabel_reqs]
    -- The requirement action is injective on ordered pairs, including a
    -- possible diagonal; arbitrary reversed pairs would otherwise collide.
    apply map_nodup_on _ _ hr.2.2
    intro q hq p hp he
    have einv := congrArg (mapReq pi.g) he
    simp only [mapReq_eq_sortPair, sortPair_map_sortPair, pi.fg,
      sortPair_of_le (ordered q hq), sortPair_of_le (ordered p hp)] at einv
    exact einv

theorem serializedRelabel_of_iso {r s : Regime} (h : Iso r s)
    (hr : r.wf) (hs : s.wf) (nr : SetCollections r) (ns : SetCollections s) :
    serializedRelabel r (datumRen h) (formRen h) = structuralKey s :=
  structuralKey_eq_of_ext (relabel_ext_of_iso h hr hs)
    (relabel_setCollections r _ _ nr (fun q hq => Nat.le_of_lt (hr.2.2.1 q hq).1)) ns

theorem relabel_wf (r : Regime) (pi : DRen r.data) (phi : DRen r.forms.length)
    (hr : r.wf) : (relabel r pi phi).wf := by
  let hiso := relabel_iso r pi phi (fun q hq => Nat.le_of_lt (hr.2.2.1 q hq).1)
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro p hp
    rw [relabel_insts, List.map_map] at hp
    obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hp
    have hqwf := hr.1 q hq
    refine ⟨by simpa [mapInst, mapInstForm] using phi.fbound q.1 hqwf.1, ?_, ?_⟩
    · change (q.2.map pi.f).length = (relabel r pi phi).forms.getD (phi.f q.1) 0
      have ea := hiso.arity q.1 (List.mem_range.mpr hqwf.1)
      change (relabel r pi phi).forms.getD (phi.f q.1) 0 = r.forms.getD q.1 0 at ea
      rw [List.length_map, ea]
      exact hqwf.2.1
    · intro a ha
      obtain ⟨b, hb, rfl⟩ := List.mem_map.mp ha
      exact pi.fbound b (hqwf.2.2 b hb)
  · intro f hf
    rw [relabel_rules] at hf
    obtain ⟨g, hg, rfl⟩ := List.mem_map.mp hf
    simpa using phi.fbound g (hr.2.1 g hg)
  · intro q hq
    rw [relabel_reqs] at hq
    obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hq
    have hpwf := hr.2.2.1 p hp
    have h1 := pi.fbound p.1 (Nat.lt_trans hpwf.1 hpwf.2)
    have h2 := pi.fbound p.2 hpwf.2
    have hne : pi.f p.1 ≠ pi.f p.2 := by
      intro he
      have e := congrArg pi.g he
      simp only [pi.fg] at e
      omega
    change min (pi.f p.1) (pi.f p.2) < max (pi.f p.1) (pi.f p.2) ∧
      max (pi.f p.1) (pi.f p.2) < r.data
    rcases Nat.lt_or_gt_of_ne hne with hlt | hgt
    · rw [Nat.min_eq_left (Nat.le_of_lt hlt), Nat.max_eq_right (Nat.le_of_lt hlt)]
      exact ⟨hlt, h2⟩
    · rw [Nat.min_eq_right (Nat.le_of_lt hgt), Nat.max_eq_left (Nat.le_of_lt hgt)]
      exact ⟨hgt, h1⟩
  · intro a ha
    rw [relabel_forms] at ha
    obtain ⟨j, hj, rfl⟩ := List.mem_map.mp ha
    have hjb := phi.gbound j (List.mem_range.mp hj)
    apply hr.2.2.2
    rw [getD_eq_getElem _ 0 hjb]
    exact List.getElem_mem hjb

def OrbitKey (r : Regime) (key : StructuralKey) : Prop :=
  ∃ pi : DRen r.data, ∃ phi : DRen r.forms.length, serializedRelabel r pi phi = key

theorem orbitKey_iso {r s : Regime} (h : Iso r s)
    (hr : r.wf) (hs : s.wf) (nr : SetCollections r) (ns : SetCollections s)
    (key : StructuralKey) : OrbitKey r key ↔ OrbitKey s key := by
  have transport : ∀ (r s : Regime) (h : Iso r s),
      r.wf → s.wf → SetCollections r → SetCollections s → OrbitKey s key → OrbitKey r key := by
    intro r s h hr hs nr ns hk
    obtain ⟨pi, phi, he⟩ := hk
    let k := h.trans (relabel_iso s pi phi (fun q hq => Nat.le_of_lt (hs.2.2.1 q hq).1))
    refine ⟨datumRen k, formRen k, ?_⟩
    exact (serializedRelabel_of_iso k hr (relabel_wf s pi phi hs) nr
      (relabel_setCollections s pi phi ns (fun q hq => Nat.le_of_lt (hs.2.2.1 q hq).1))).trans he
  exact ⟨transport s r h.symm hs hr ns nr, transport r s h hr hs nr ns⟩

def identityRen (n : Nat) : DRen n where
  f := id
  g := id
  fg := fun _ => rfl
  gf := fun _ => rfl
  fbound := fun _ hx => hx
  gbound := fun _ hx => hx

theorem relabel_identity (r : Regime) (ordered : ∀ q ∈ r.reqs, q.1 ≤ q.2) :
    relabel r (identityRen _) (identityRen _) = r := by
  refine Regime.ext' (r := relabel r (identityRen _) (identityRen _)) (s := r) rfl ?_ ?_ ?_ ?_
  · change permForms id r.forms = r.forms
    apply List.ext_getElem (by simp)
    intro j hj hj'
    rw [← getD_eq_getElem _ 0 hj, ← getD_eq_getElem _ 0 hj']
    exact permForms_getD id r.forms hj'
  · rw [relabel_insts, List.map_map]
    have e : (mapInstForm (identityRen r.forms.length).f ∘ mapInst (identityRen r.data).f) = id := by
      funext p
      simp [mapInst, mapInstForm, identityRen]
    rw [e, List.map_id]
  · simp [relabel_rules, identityRen]
  · rw [relabel_reqs]
    have e : r.reqs.map (mapReq (identityRen r.data).f) = r.reqs.map id :=
      List.map_congr_left (fun q hq => by
        change mapReq id q = q
        rw [mapReq_eq_sortPair]
        exact sortPair_of_le (ordered q hq))
    simpa only [List.map_id] using e

theorem orbitKey_self (r : Regime) (hr : r.wf) : OrbitKey r (structuralKey r) :=
  ⟨identityRen _, identityRen _, congrArg structuralKey
    (relabel_identity r (fun q hq => Nat.le_of_lt (hr.2.2.1 q hq).1))⟩

theorem common_orbitKey_iff_iso {r s : Regime}
    (hr : r.wf) (hs : s.wf) (nr : SetCollections r) (ns : SetCollections s) :
    (∃ key, OrbitKey r key ∧ OrbitKey s key) ↔ Nonempty (Iso r s) := by
  constructor
  · rintro ⟨key, ⟨pir, phir, her⟩, ⟨pis, phis, hes⟩⟩
    exact serializedRelabel_sound pir phir pis phis hr hs (her.trans hes.symm)
  · rintro ⟨h⟩
    exact ⟨structuralKey s, (orbitKey_iso h hr hs nr ns _).mpr (orbitKey_self s hs),
      orbitKey_self s hs⟩

end GenesisPaper.Orbit
