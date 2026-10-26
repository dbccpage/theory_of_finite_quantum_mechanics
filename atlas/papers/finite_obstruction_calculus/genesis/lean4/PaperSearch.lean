import PaperOrbit
import PaperWire
import Derivation.Rounds
import Init.Data.List.Nat.Pairwise

/-!
Finite exhaustive canonical search, using all datum and form permutations.
The insertion enumerator differs in enumeration order from itertools and
Rust; its membership theorem proves that it enumerates exactly the same
permutation tables. Minimum selection is independent of that order.
-/

namespace GenesisPaper.Search

open Derivation GenesisPaper GenesisPaper.Orbit

local instance {A B : Type} [Ord A] [Ord B] : Ord (A × B) := lexOrd
local instance : Std.TransOrd Nat := natTransOrd
local instance : Std.LawfulEqOrd Nat := natLawfulEqOrd

def insertEverywhere (a : Nat) : List Nat → List (List Nat)
  | [] => [[a]]
  | b :: bs => (a :: b :: bs) :: (insertEverywhere a bs).map (b :: ·)

def permutations : List Nat → List (List Nat)
  | [] => [[]]
  | a :: xs => (permutations xs).flatMap (insertEverywhere a)

theorem insertEverywhere_sound (a : Nat) : ∀ ys xs,
    xs ∈ insertEverywhere a ys → xs.Perm (a :: ys) := by
  intro ys
  induction ys with
  | nil => intro xs hx; simpa [insertEverywhere] using hx
  | cons b bs ih =>
    intro xs hx
    simp only [insertEverywhere, List.mem_cons, List.mem_map] at hx
    rcases hx with rfl | ⟨zs, hz, rfl⟩
    · exact .refl _
    · exact ((ih zs hz).cons b).trans (List.Perm.swap a b bs)

theorem insertEverywhere_at (a : Nat) (pre suf : List Nat) :
    pre ++ a :: suf ∈ insertEverywhere a (pre ++ suf) := by
  induction pre with
  | nil => cases suf <;> simp [insertEverywhere]
  | cons b bs ih =>
    apply List.mem_cons_of_mem
    exact List.mem_map.mpr ⟨bs ++ a :: suf, ih, rfl⟩

theorem permutations_sound : ∀ ys xs, xs ∈ permutations ys → xs.Perm ys := by
  intro ys
  induction ys with
  | nil => intro xs hx; simpa [permutations] using hx
  | cons a ys ih =>
    intro xs hx
    obtain ⟨zs, hz, hxz⟩ := List.mem_flatMap.mp hx
    exact (insertEverywhere_sound a zs xs hxz).trans ((ih zs hz).cons a)

theorem permutations_complete : ∀ ys xs, xs.Perm ys → xs ∈ permutations ys := by
  intro ys
  induction ys with
  | nil => intro xs hp; rw [hp.eq_nil]; simp [permutations]
  | cons a ys ih =>
    intro xs hp
    have ha : a ∈ xs := hp.symm.subset (List.mem_cons_self ..)
    obtain ⟨pre, suf, rfl⟩ := List.append_of_mem ha
    have ht : (pre ++ suf).Perm ys := (List.perm_middle.symm.trans hp).cons_inv
    exact List.mem_flatMap.mpr ⟨pre ++ suf, ih _ ht, insertEverywhere_at a pre suf⟩

theorem mem_permutations (xs ys : List Nat) : xs ∈ permutations ys ↔ xs.Perm ys :=
  ⟨permutations_sound ys xs, permutations_complete ys xs⟩

abbrev Table (n : Nat) := {xs : List Nat // xs.Perm (List.range n)}

def tables (n : Nat) : List (Table n) :=
  (permutations (List.range n)).attach.map
    (fun xs => ⟨xs.val, (mem_permutations _ _).mp xs.property⟩)

theorem table_mem {n : Nat} (t : Table n) : t ∈ tables n := by
  apply List.mem_map.mpr
  exact ⟨⟨t.val, (mem_permutations _ _).mpr t.property⟩, List.mem_attach _ _, rfl⟩

theorem table_length {n : Nat} (t : Table n) : t.val.length = n := by
  simpa using t.property.length_eq

theorem table_element_bound {n : Nat} (t : Table n) {i : Nat} (hi : i < n) :
    t.val.getD i 0 < n := by
  rw [getD_eq_getElem _ 0 (by rwa [table_length])]
  exact List.mem_range.mp (t.property.subset (List.getElem_mem _))

theorem table_index_bound {n : Nat} (t : Table n) {i : Nat} (hi : i < n) :
    t.val.idxOf i < n := by
  have hb := List.idxOf_lt_length_of_mem (t.property.symm.subset (List.mem_range.mpr hi))
  simpa only [table_length] using hb

theorem table_left_inverse {n : Nat} (t : Table n) {i : Nat} (hi : i < n) :
    t.val.idxOf (t.val.getD i 0) = i := by
  have hib : i < t.val.length := by rwa [table_length]
  rw [getD_eq_getElem _ 0 hib]
  exact (t.property.symm.nodup (range_nodup' n)).idxOf_getElem i hib

theorem table_right_inverse {n : Nat} (t : Table n) {i : Nat} (hi : i < n) :
    t.val.getD (t.val.idxOf i) 0 = i := by
  have hib : t.val.idxOf i < t.val.length := by
    rw [table_length]
    exact table_index_bound t hi
  rw [getD_eq_getElem _ 0 hib]
  exact List.getElem_idxOf hib

def tableRen {n : Nat} (t : Table n) : DRen n :=
  extendFinite n (fun i => t.val.getD i 0) t.val.idxOf
    (fun _ hi => table_element_bound t hi) (fun _ hi => table_index_bound t hi)
    (fun _ hi => table_left_inverse t hi) (fun _ hi => table_right_inverse t hi)

def renTable {n : Nat} (pi : DRen n) : Table n :=
  ⟨(List.range n).map pi.f, perm_of_nodup_membership
    (map_nodup_injective pi.f (fun x y he => by
      have e := congrArg pi.g he
      simpa only [pi.fg] using e) _ (range_nodup' n))
    (range_nodup' n) (fun i => by
      constructor
      · intro hi
        obtain ⟨j, hj, rfl⟩ := List.mem_map.mp hi
        exact List.mem_range.mpr (pi.fbound j (List.mem_range.mp hj))
      · intro hi
        exact List.mem_map.mpr ⟨pi.g i, List.mem_range.mpr (pi.gbound i (List.mem_range.mp hi)),
          pi.gf i⟩)⟩

theorem tableRen_renTable_f {n : Nat} (pi : DRen n) {i : Nat} (hi : i < n) :
    (tableRen (renTable pi)).f i = pi.f i := by
  change padF n (fun j => ((List.range n).map pi.f).getD j 0) i = pi.f i
  rw [padF_lt _ hi, List.getD_eq_getElem?_getD, List.getElem?_map]
  simp [hi]

theorem tableRen_renTable_g {n : Nat} (pi : DRen n) {i : Nat} (hi : i < n) :
    (tableRen (renTable pi)).g i = pi.g i := by
  let rho := tableRen (renTable pi)
  have e : pi.f (rho.g i) = i := by
    rw [← tableRen_renTable_f pi (rho.gbound i hi)]
    exact rho.gf i
  have e' := congrArg pi.g e
  simpa only [pi.fg] using e'

theorem relabel_congr (r : Regime) (hr : r.wf)
    (pi pi' : DRen r.data) (phi phi' : DRen r.forms.length)
    (hd : ∀ i, i < r.data → pi.f i = pi'.f i)
    (hf : ∀ i, i < r.forms.length → phi.f i = phi'.f i)
    (hg : ∀ i, i < r.forms.length → phi.g i = phi'.g i) :
    relabel r pi phi = relabel r pi' phi' := by
  refine Regime.ext' (r := relabel r pi phi) (s := relabel r pi' phi') rfl ?_ ?_ ?_ ?_
  · rw [relabel_forms, relabel_forms]
    apply List.map_congr_left
    intro j hj
    rw [hg j (List.mem_range.mp hj)]
  · rw [relabel_insts, relabel_insts, List.map_map, List.map_map]
    apply List.map_congr_left
    intro p hp
    change (phi.f p.1, p.2.map pi.f) = (phi'.f p.1, p.2.map pi'.f)
    rw [hf p.1 (hr.1 p hp).1]
    congr 1
    exact List.map_congr_left (fun a ha => hd a ((hr.1 p hp).2.2 a ha))
  · rw [relabel_rules, relabel_rules]
    exact List.map_congr_left (fun f hf' => hf f (hr.2.1 f hf'))
  · rw [relabel_reqs, relabel_reqs]
    apply List.map_congr_left
    intro q hq
    simp only [mapReq, hd q.1 (Nat.lt_trans (hr.2.2.1 q hq).1 (hr.2.2.1 q hq).2),
      hd q.2 (hr.2.2.1 q hq).2]

def candidateKeys (r : Regime) : List StructuralKey :=
  (tables r.data).flatMap (fun pi => (tables r.forms.length).map
    (fun phi => serializedRelabel r (tableRen pi) (tableRen phi)))

theorem mem_candidateKeys (r : Regime) (hr : r.wf) (key : StructuralKey) :
    key ∈ candidateKeys r ↔ OrbitKey r key := by
  constructor
  · intro hk
    obtain ⟨pi, _, hpi⟩ := List.mem_flatMap.mp hk
    obtain ⟨phi, _, he⟩ := List.mem_map.mp hpi
    exact ⟨tableRen pi, tableRen phi, he⟩
  · rintro ⟨pi, phi, he⟩
    refine List.mem_flatMap.mpr ⟨renTable pi, table_mem _, ?_⟩
    refine List.mem_map.mpr ⟨renTable phi, table_mem _, ?_⟩
    exact (congrArg structuralKey (relabel_congr r hr _ _ _ _
      (fun i hi => tableRen_renTable_f pi hi)
      (fun i hi => tableRen_renTable_f phi hi)
      (fun i hi => tableRen_renTable_g phi hi))).trans he

def minimum? {A : Type} [Ord A] : List A → Option A
  | [] => none
  | a :: xs => match minimum? xs with
    | none => some a
    | some b => some (if (compare a b).isLE then a else b)

theorem minimum_none_iff {A : Type} [Ord A] (xs : List A) :
    minimum? xs = none ↔ xs = [] := by
  cases xs with
  | nil => simp [minimum?]
  | cons a xs => cases he : minimum? xs <;> simp [minimum?, he]

theorem minimum_spec {A : Type} [Ord A] [Std.TransOrd A]
    (xs : List A) (k : A) (hk : minimum? xs = some k) :
    k ∈ xs ∧ ∀ a ∈ xs, (compare k a).isLE := by
  induction xs generalizing k with
  | nil => simp [minimum?] at hk
  | cons x xs ih =>
    cases he : minimum? xs with
    | none =>
      have hn := (minimum_none_iff xs).mp he
      subst xs
      have e : x = k := Option.some.inj hk
      subst k
      simp [Std.ReflOrd.compare_self]
    | some b =>
      have hb := ih b he
      simp only [minimum?, he] at hk
      by_cases hxb : (compare x b).isLE
      · simp only [if_pos hxb, Option.some.injEq] at hk
        subst k
        refine ⟨List.mem_cons_self .., ?_⟩
        intro a ha
        rcases List.mem_cons.mp ha with rfl | ha
        · simp [Std.ReflOrd.compare_self]
        · exact Std.TransOrd.isLE_trans hxb (hb.2 a ha)
      · simp only [if_neg hxb, Option.some.injEq] at hk
        subst k
        refine ⟨List.mem_cons_of_mem _ hb.1, ?_⟩
        intro a ha
        rcases List.mem_cons.mp ha with rfl | ha
        · have h := Std.OrientedCmp.lt_of_not_isLE hxb
          rw [h]
          rfl
        · exact hb.2 a ha

theorem minimum_exists_of_mem {A : Type} [Ord A] {xs : List A} {a : A}
    (ha : a ∈ xs) : ∃ k, minimum? xs = some k := by
  cases he : minimum? xs with
  | none => exact False.elim (List.not_mem_nil ((minimum_none_iff xs).mp he ▸ ha))
  | some k => exact ⟨k, rfl⟩

theorem minimum_eq_of_membership {A : Type} [Ord A] [Std.TransOrd A] [Std.LawfulEqOrd A]
    (xs ys : List A) (hm : ∀ a, a ∈ xs ↔ a ∈ ys) : minimum? xs = minimum? ys := by
  cases hx : minimum? xs with
  | none =>
    have hxs := (minimum_none_iff xs).mp hx
    have hys : ys = [] := by
      cases ys with
      | nil => rfl
      | cons y ys => exact False.elim (List.not_mem_nil (hxs ▸ (hm y).mpr (List.mem_cons_self ..)))
    simp only [hys, minimum?]
  | some x =>
    have hsx := minimum_spec xs x hx
    obtain ⟨y, hy⟩ := minimum_exists_of_mem ((hm x).mp hsx.1)
    have hsy := minimum_spec ys y hy
    have he : x = y := Std.LawfulEqOrd.compare_eq_iff_eq.mp
      (Std.OrientedCmp.isLE_antisymm (hsx.2 y ((hm y).mpr hsy.1)) (hsy.2 x ((hm x).mp hsx.1)))
    rw [hy, he]

/-- Exact finite exhaustive search; no orbit-choice premise is supplied. -/
def canonicalKey (r : Regime) : Option StructuralKey := minimum? (candidateKeys r)

theorem canonicalKey_attained (r : Regime) (hr : r.wf) :
    ∃ key, canonicalKey r = some key ∧ OrbitKey r key ∧
      ∀ other, OrbitKey r other → (compare key other).isLE := by
  have hc := (mem_candidateKeys r hr _).mpr (orbitKey_self r hr)
  obtain ⟨key, he⟩ := minimum_exists_of_mem hc
  have hspec := minimum_spec _ key he
  exact ⟨key, he, (mem_candidateKeys r hr _).mp hspec.1,
    fun other ho => hspec.2 other ((mem_candidateKeys r hr _).mpr ho)⟩

theorem canonicalKey_classification {r s : Regime}
    (hr : r.wf) (hs : s.wf) (nr : SetCollections r) (ns : SetCollections s) :
    canonicalKey r = canonicalKey s ↔ Nonempty (Iso r s) := by
  constructor
  · intro he
    obtain ⟨key, hk, hkr, _⟩ := canonicalKey_attained r hr
    have hks : minimum? (candidateKeys s) = some key := he.symm.trans hk
    exact (common_orbitKey_iff_iso hr hs nr ns).mp
      ⟨key, hkr, (mem_candidateKeys s hs _).mp (minimum_spec _ key hks).1⟩
  · rintro ⟨h⟩
    exact minimum_eq_of_membership _ _ (fun key =>
      (mem_candidateKeys r hr key).trans ((orbitKey_iso h hr hs nr ns key).trans
        (mem_candidateKeys s hs key).symm))

theorem canonicalBytes_classification {r s : Regime}
    (hr : r.wf) (hs : s.wf) (nr : SetCollections r) (ns : SetCollections s)
    (kr ks : StructuralKey) (hkr : canonicalKey r = some kr) (hks : canonicalKey s = some ks)
    (br : ∀ word ∈ Wire.structuralWords kr, word < 2 ^ 64)
    (bs : ∀ word ∈ Wire.structuralWords ks, word < 2 ^ 64) :
    Wire.portableBytes kr = Wire.portableBytes ks ↔ Nonempty (Iso r s) := by
  constructor
  · intro he
    have hk := Wire.portableBytes_injective br bs he
    exact (canonicalKey_classification hr hs nr ns).mp
      (hkr.trans ((congrArg some hk).trans hks.symm))
  · intro hi
    have he := (canonicalKey_classification hr hs nr ns).mpr hi
    have hk : kr = ks := Option.some.inj (hkr.symm.trans (he.trans hks))
    exact congrArg Wire.portableBytes hk

end GenesisPaper.Search
