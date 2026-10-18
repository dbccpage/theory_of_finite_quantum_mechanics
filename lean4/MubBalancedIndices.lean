import MubBalancedQuadraticPolynomials

/-!
# Complete numbering for the balanced quadratic model

AuthorityEffect: None.
-/
namespace MUB.BalancedIndices
open BalancedQuadraticLift BoundedBlockChart
open BoundedExportIndices (bit bools pairs)

def variableCode : Coord → Nat
  | (.inl s,b) => BoundedExportIndices.variableCode (s,b)
  | (.inr (.inl (i,j)),b) => 152 + 2 * (3 * i.val + j.val) + bit b
  | (.inr (.inr (a,i,j)),b) => 170 + 2 * (25 * a.val + 5 * i.val + j.val) + bit b

def coreSlots : List (Fin 3 × Fin 5 × Fin 5) :=
  (List.finRange 3).flatMap fun a => (pairs 5 5).map fun (i,j) => (a,i,j)

def allSlots : List Slot := BoundedExportIndices.allSlots.map Sum.inl ++
  (pairs 3 3).map (fun p => .inr (.inl p)) ++
  coreSlots.map (fun p => .inr (.inr p))

def allVariables : List Coord := allSlots.flatMap fun s => bools.map fun b => (s,b)

set_option maxRecDepth 10000 in
theorem variable_codes : allVariables.map variableCode = List.range 320 := by decide

@[simp] theorem mem_coreSlots (p : Fin 3 × Fin 5 × Fin 5) : p ∈ coreSlots := by
  exact List.mem_flatMap.mpr ⟨p.1, by simp, List.mem_map.mpr ⟨p.2, by simp, rfl⟩⟩

theorem mem_allSlots (s : Slot) : s ∈ allSlots := by
  rcases s with s | p | p <;> simp [allSlots, List.mem_map]

theorem variables_complete (c : Coord) : c ∈ allVariables := by
  exact List.mem_flatMap.mpr ⟨c.1, mem_allSlots _,
    List.mem_map.mpr ⟨c.2, BoundedExportIndices.mem_bools _, rfl⟩⟩

theorem variableCode_injective : Function.Injective variableCode := by
  intro u v h
  exact List.inj_on_of_nodup_map (by rw [variable_codes]; exact List.nodup_range)
    (variables_complete u) (variables_complete v) h

theorem variableCode_lt (c : Coord) : variableCode c < 320 := by
  have h : variableCode c ∈ allVariables.map variableCode :=
    List.mem_map.mpr ⟨c, variables_complete c, rfl⟩
  rw [variable_codes] at h
  exact List.mem_range.mp h

def variableFin (c : Coord) : Fin 320 := ⟨variableCode c, variableCode_lt c⟩

theorem variableFin_bijective : Function.Bijective variableFin := by
  constructor
  · intro c d h
    exact variableCode_injective (congrArg Fin.val h)
  · intro i
    have h : i.val ∈ allVariables.map variableCode := by
      rw [variable_codes]
      exact List.mem_range.mpr i.isLt
    obtain ⟨c, _, hc⟩ := List.mem_map.mp h
    exact ⟨c, Fin.ext hc⟩

noncomputable def variableEquiv : Coord ≃ Fin 320 :=
  Equiv.ofBijective variableFin variableFin_bijective

@[simp] theorem variableEquiv_apply (c : Coord) : variableEquiv c = variableFin c := rfl

def codeRadius (i : Nat) : Rat := if i < 170 then 1 else QuadraticLiftNarrowBox.transitionRadius

theorem radius_code (c : Coord) : (codeRadius (variableCode c) : ℝ) = radius c.1 := by
  rcases c with ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · have h := BoundedExportIndices.variableCode_lt (s,b)
    have h' : variableCode (.inl s,b) < 170 := by
      change BoundedExportIndices.variableCode (s,b) < 170
      omega
    rw [codeRadius, if_pos h']
    norm_num [radius]
  · have hi := i.isLt
    have hj := j.isLt
    cases b <;> simp [variableCode, codeRadius, radius, bit, show 152 + 2 * (3 * i.val + j.val) < 170 by omega,
      show 152 + 2 * (3 * i.val + j.val) + 1 < 170 by omega]
  · have hn : ¬ 170 + 2 * (25 * a.val + 5 * i.val + j.val) + bit b < 170 := by omega
    simp [variableCode, codeRadius, radius, hn]

#print axioms variable_codes
#print axioms variables_complete
#print axioms variableCode_injective
#print axioms variableFin_bijective
#print axioms radius_code
end MUB.BalancedIndices
