/- These declarations are opaque and were not elaborated by Lake in this change. -/

import Gluing
import G1_Orbits

/-!
# Step 3B: Fourier-landing bypass formulation

AuthorityEffect: None
Firewall Line: NOT MUB(6)=3

Transition graph of a configuration `Fin 7 → Basis`. Edges are the unordered
pairs of distinct indices, enumerated as `{i j : Fin 7 | i < j}`. Each edge
carries a `Fin 6 × Fin 6` unitary transition. The pigeonhole is conditional
on an explicit non-landing count of at most 20. It does not assert that a
7-basis configuration exists, and it does not identify cyclic invariance
with the Fourier orbit of `F_6`.
-/

set_option autoImplicit false

namespace MUB6.Gluing

open MUB6.Gluing.Orbits

/-- Unitarity of a syntactic 6×6 phase matrix.
`UnitaryTransformation` acts on `Basis`; this predicate is the matrix condition. -/
opaque IsUnitary6 : ComplexMatrix6 → Prop

/-! ### 21 unordered edges -/

/-- Enumerated strict pairs `{i j : Fin 7 | i < j}`. -/
def enumeratedStrictPairs : List (Fin 7 × Fin 7) :=
  (List.finRange 7).flatMap fun i =>
    ((List.finRange 7).filter fun j => decide (i < j)).map fun j => (i, j)

theorem enumeratedStrictPairs_length :
    enumeratedStrictPairs.length = 21 := by
  decide

theorem enumeratedStrictPairs_length_binom :
    enumeratedStrictPairs.length = 7 * 6 / 2 := by
  decide

/-- Cardinality of the enumerated pairs `{i j : Fin 7 | i < j}`. -/
theorem strict_pair_cardinality :
    enumeratedStrictPairs.length = 21 ∧
      enumeratedStrictPairs.length = 7 * 6 / 2 := by
  decide

theorem enumeratedStrictPairs_nodup : enumeratedStrictPairs.Nodup := by
  decide

theorem mem_enumeratedStrictPairs (i j : Fin 7) :
    (i, j) ∈ enumeratedStrictPairs ↔ i < j := by
  constructor
  · intro h
    rw [enumeratedStrictPairs, List.mem_flatMap] at h
    rcases h with ⟨a, _, hmem⟩
    rw [List.mem_map] at hmem
    rcases hmem with ⟨b, hb, hab⟩
    rw [List.mem_filter] at hb
    cases hab
    exact of_decide_eq_true hb.2
  · intro hij
    rw [enumeratedStrictPairs, List.mem_flatMap]
    refine ⟨i, List.mem_finRange i, ?_⟩
    rw [List.mem_map]
    refine ⟨j, ?_, rfl⟩
    rw [List.mem_filter]
    exact ⟨List.mem_finRange j, decide_eq_true hij⟩

/-- An unordered edge, stored as the ordered pair with smaller index first. -/
abbrev ConfigEdge := {p : Fin 7 × Fin 7 // p.1 < p.2}

theorem fin21_lt_enum_length (k : Fin 21) : k.val < enumeratedStrictPairs.length := by
  rw [enumeratedStrictPairs_length]
  exact k.isLt

def edgePair (k : Fin 21) : Fin 7 × Fin 7 :=
  enumeratedStrictPairs[k.val]'(fin21_lt_enum_length k)

theorem edgePair_mem (k : Fin 21) : edgePair k ∈ enumeratedStrictPairs :=
  List.mem_of_getElem rfl

theorem edgePair_strict (k : Fin 21) : (edgePair k).1 < (edgePair k).2 :=
  (mem_enumeratedStrictPairs (edgePair k).1 (edgePair k).2).mp (edgePair_mem k)

/-- Edge `k` of the complete graph on `Fin 7`, under the bijection with `Fin 21`. -/
def edgeAt (k : Fin 21) : ConfigEdge :=
  ⟨edgePair k, edgePair_strict k⟩

theorem edgeAt_endpoints_ne (k : Fin 21) :
    (edgeAt k).val.1 ≠ (edgeAt k).val.2 := by
  intro h
  have hlt : (edgeAt k).val.1 < (edgeAt k).val.2 := (edgeAt k).property
  rw [h] at hlt
  exact Nat.lt_irrefl _ hlt

def indexOfEdge (e : ConfigEdge) : Fin 21 :=
  ⟨enumeratedStrictPairs.idxOf e.val, by
    have hmem : e.val ∈ enumeratedStrictPairs :=
      (mem_enumeratedStrictPairs e.val.1 e.val.2).mpr e.property
    have hlt := List.idxOf_lt_length_of_mem hmem
    rw [enumeratedStrictPairs_length] at hlt
    exact hlt⟩

theorem edgeAt_indexOfEdge (e : ConfigEdge) : edgeAt (indexOfEdge e) = e := by
  apply Subtype.ext
  change edgePair (indexOfEdge e) = e.val
  have hmem : e.val ∈ enumeratedStrictPairs :=
    (mem_enumeratedStrictPairs e.val.1 e.val.2).mpr e.property
  have hlt : enumeratedStrictPairs.idxOf e.val < enumeratedStrictPairs.length :=
    List.idxOf_lt_length_of_mem hmem
  have hget := List.getElem_idxOf (x := e.val) (xs := enumeratedStrictPairs) hlt
  simp [edgePair, indexOfEdge, hget]

theorem edgeAt_injective (k₁ k₂ : Fin 21) (h : edgeAt k₁ = edgeAt k₂) : k₁ = k₂ := by
  have hpair : edgePair k₁ = edgePair k₂ := congrArg Subtype.val h
  have hnodup := enumeratedStrictPairs_nodup
  have heq : enumeratedStrictPairs[k₁.val]'(fin21_lt_enum_length k₁) =
      enumeratedStrictPairs[k₂.val]'(fin21_lt_enum_length k₂) := by
    simpa [edgePair] using hpair
  have hidx :=
    (List.getElem_inj (h₀ := fin21_lt_enum_length k₁) (h₁ := fin21_lt_enum_length k₂) hnodup).mp heq
  exact Fin.eq_of_val_eq hidx

/-- The strict pairs are in bijection with `Fin 21`, and that set has `7 * 6 / 2` elements. -/
theorem strict_pairs_equiv_fin21 :
    (∀ i j : Fin 7, (i, j) ∈ enumeratedStrictPairs ↔ i < j) ∧
      enumeratedStrictPairs.length = 21 ∧
        enumeratedStrictPairs.length = 7 * 6 / 2 ∧
          (∀ k₁ k₂ : Fin 21, edgeAt k₁ = edgeAt k₂ → k₁ = k₂) ∧
            (∀ e : ConfigEdge, ∃ k : Fin 21, edgeAt k = e) := by
  refine ⟨mem_enumeratedStrictPairs, enumeratedStrictPairs_length,
    enumeratedStrictPairs_length_binom, edgeAt_injective, ?_⟩
  intro e
  exact ⟨indexOfEdge e, edgeAt_indexOfEdge e⟩

/-! ### Unitary transition on each edge -/

/-- A 6×6 unitary transition from `source` to `target`.
Entries are addressed by `Fin 6 × Fin 6` through `EdgeUnitaryTransition.entry`. -/
structure EdgeUnitaryTransition (source target : Basis) where
  matrix : ComplexMatrix6
  unitary : IsUnitary6 matrix

def EdgeUnitaryTransition.entry
    {source target : Basis} (T : EdgeUnitaryTransition source target)
    (jk : Fin 6 × Fin 6) : PhaseAngle :=
  T.matrix.entry jk.1 jk.2

/-- The 21 edge transitions of a configuration `B : Fin 7 → Basis`.
`trans k` runs between the bases at the endpoints of `edgeAt k`. -/
structure TransitionFamily (B : Fin 7 → Basis) where
  trans :
    (k : Fin 21) →
      EdgeUnitaryTransition (B (edgeAt k).val.1) (B (edgeAt k).val.2)

/-! ### Cyclic invariance, separate from the Fourier orbit -/

def cycShift (k r : Fin 6) : Fin 6 :=
  ⟨(k.val + r.val) % 6, Nat.mod_lt _ (by decide : 0 < 6)⟩

/-- A nonzero cyclic column shift fixes every row. -/
def NontrivialCyclicInvariance (H : ComplexMatrix6) : Prop :=
  ∃ r : Fin 6, r ≠ 0 ∧ ∀ j : Fin 6, ∀ k : Fin 6,
    H.entry j k = H.entry j (cycShift k r)

/-- Column-index marker. A nonzero shift moves the zero column. -/
def markerMatrix : ComplexMatrix6 where
  entry (_j : Fin 6) (k : Fin 6) := ⟨k.val⟩

theorem markerMatrix_not_nontrivial_cyclic :
    ¬ NontrivialCyclicInvariance markerMatrix := by
  intro h
  rcases h with ⟨r, hr, hfix⟩
  have h0 := hfix (0 : Fin 6) (0 : Fin 6)
  have hv : (0 : Fin 6).val = (cycShift (0 : Fin 6) r).val := by
    have h1 : PhaseAngle.mk (0 : Fin 6).val = PhaseAngle.mk (cycShift (0 : Fin 6) r).val := by
      simpa [markerMatrix] using h0
    injection h1 with hv
  have hshift : (cycShift (0 : Fin 6) r).val = r.val := by
    show ((0 : Fin 6).val + r.val) % 6 = r.val
    have h0v : (0 : Fin 6).val = 0 := rfl
    rw [h0v, Nat.zero_add]
    exact Nat.mod_eq_of_lt r.isLt
  have hr0 : r.val = (0 : Fin 6).val := by
    rw [hshift] at hv
    exact hv.symm
  exact hr (Fin.eq_of_val_eq hr0)

/-- The same non-landing marker on every edge `edgeAt k`. -/
def markerLabeling (_k : Fin 21) : ComplexMatrix6 :=
  markerMatrix

theorem markerLabeling_has_no_landing_edge :
    ¬ ∃ k : Fin 21,
        NontrivialCyclicInvariance (markerLabeling k) ∧
          MUB6.Gluing.Orbits.FourierOrbit (markerLabeling k) := by
  intro ⟨k, hc, _⟩
  exact markerMatrix_not_nontrivial_cyclic (by simpa [markerLabeling] using hc)

theorem marker_family_misses_conclusion
    (B : Fin 7 → Basis) (F : TransitionFamily B)
    (hmat : ∀ k : Fin 21, (F.trans k).matrix = markerMatrix) :
    ¬ ∃ k : Fin 21,
        NontrivialCyclicInvariance (F.trans k).matrix ∧
          MUB6.Gluing.Orbits.FourierOrbit (F.trans k).matrix := by
  intro ⟨k, hc, _⟩
  exact markerMatrix_not_nontrivial_cyclic (hmat k ▸ hc)

/-! ### Conditional pigeonhole -/

noncomputable section

open Classical

def landingBool (H : ComplexMatrix6) : Bool :=
  decide (NontrivialCyclicInvariance H ∧ MUB6.Gluing.Orbits.FourierOrbit H)

/-- Number of the 21 edge-matrices that miss cyclic invariance or the `F_6` orbit. -/
def nonLandingCount {B : Fin 7 → Basis} (F : TransitionFamily B) : Nat :=
  (List.ofFn fun k : Fin 21 => (F.trans k).matrix).countP fun H => ¬ landingBool H

theorem fourier_landing_pigeonhole
    (B : Fin 7 → Basis) (F : TransitionFamily B)
    (hNonLanding : nonLandingCount F ≤ 20) :
    ∃ k : Fin 21,
      NontrivialCyclicInvariance (F.trans k).matrix ∧
        MUB6.Gluing.Orbits.FourierOrbit (F.trans k).matrix := by
  let matrices := List.ofFn fun k : Fin 21 => (F.trans k).matrix
  have hsplit := List.length_eq_countP_add_countP landingBool (l := matrices)
  have hlen : matrices.length = 21 := List.length_ofFn
  have hnon : matrices.countP (fun H => ¬ landingBool H) = nonLandingCount F := rfl
  have hpos : 0 < matrices.countP landingBool := by
    rw [hlen] at hsplit
    omega
  rcases List.countP_pos_iff.mp hpos with ⟨H, hmem, hp⟩
  rcases List.mem_ofFn.mp hmem with ⟨k, hk⟩
  have hdecide : landingBool (F.trans k).matrix = true := by
    simpa [hk] using hp
  exact ⟨k, of_decide_eq_true (by simpa [landingBool] using hdecide)⟩

theorem landingBool_marker : landingBool markerMatrix = false := by
  have hnot : ¬ (NontrivialCyclicInvariance markerMatrix ∧
      MUB6.Gluing.Orbits.FourierOrbit markerMatrix) := by
    intro hc
    exact markerMatrix_not_nontrivial_cyclic hc.1
  simpa [landingBool] using decide_eq_false hnot

theorem marker_family_nonLandingCount
    (B : Fin 7 → Basis) (F : TransitionFamily B)
    (hmat : ∀ k : Fin 21, (F.trans k).matrix = markerMatrix) :
    nonLandingCount F = 21 := by
  let matrices := List.ofFn fun k : Fin 21 => (F.trans k).matrix
  have hfalse : ∀ H ∈ matrices, landingBool H = false := by
    intro H hH
    rcases List.mem_ofFn.mp hH with ⟨k, hk⟩
    rw [← hk, hmat k, landingBool_marker]
  have hzero : matrices.countP landingBool = 0 := by
    rw [List.countP_eq_zero]
    intro H hH
    rw [hfalse H hH]
    exact Bool.false_ne_true
  have hsplit := List.length_eq_countP_add_countP landingBool (l := matrices)
  have hlen : matrices.length = 21 := List.length_ofFn
  have hnon : matrices.countP (fun H => ¬ landingBool H) = nonLandingCount F := rfl
  omega

theorem marker_family_bound_fails
    (B : Fin 7 → Basis) (F : TransitionFamily B)
    (hmat : ∀ k : Fin 21, (F.trans k).matrix = markerMatrix) :
    ¬ nonLandingCount F ≤ 20 := by
  rw [marker_family_nonLandingCount B F hmat]
  omega

end

#print axioms strict_pair_cardinality
#print axioms fourier_landing_pigeonhole
#print axioms markerLabeling_has_no_landing_edge
#print axioms marker_family_misses_conclusion

end MUB6.Gluing
