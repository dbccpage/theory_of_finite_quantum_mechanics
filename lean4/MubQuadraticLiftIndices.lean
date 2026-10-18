import MubQuadraticLiftDegree
import MubBoundedExportIndices

/-!
# Complete numbering for the full quadratic lift

AuthorityEffect: None.
-/
namespace MUB.QuadraticLiftIndices
open QuadraticLift QuadraticLiftPolynomials BoundedBlockChart
open BoundedExportIndices (bit index6 indices6 bools pairs entries6 components6)

def variableCode : Coord → Nat
  | (.inl s,b) => BoundedExportIndices.variableCode (s,b)
  | (.inr (.inl (i,j)),b) => 152 + 2 * (3 * i.val + j.val) + bit b
  | (.inr (.inr (a,i,j)),b) => 170 + 2 * (36 * a.val + 6 * index6 i + index6 j) + bit b

def equationCode : Equation → Nat
  | .inl (a,i,j) => 36 * a.val + 6 * index6 i + index6 j
  | .inr (.inl (a,i,j,b)) => 108 + 2 * (36 * a.val + 6 * index6 i + index6 j) + bit b
  | .inr (.inr (.inl (a,i,j,b))) => 324 + 2 * (36 * a.val + 6 * index6 i + index6 j) + bit b
  | .inr (.inr (.inr (a,i,j))) => 540 + 36 * a.val + 6 * index6 i + index6 j

def allSlots : List LiftSlot := BoundedExportIndices.allSlots.map Sum.inl ++
  (pairs 3 3).map (fun p => .inr (.inl p)) ++
  (entries6 3).map (fun p => .inr (.inr p))
def allVariables : List Coord := allSlots.flatMap fun s => bools.map fun b => (s,b)
def equations : List Equation := (entries6 3).map Sum.inl ++
  (components6 3).map (fun p => .inr (.inl p)) ++
  (components6 3).map (fun p => .inr (.inr (.inl p))) ++
  (entries6 3).map (fun p => .inr (.inr (.inr p)))

set_option maxRecDepth 10000 in
theorem variable_codes : allVariables.map variableCode = List.range 386 := by decide
set_option maxRecDepth 10000 in
theorem equation_codes : equations.map equationCode = List.range 648 := by decide

theorem mem_allSlots (s : LiftSlot) : s ∈ allSlots := by
  rcases s with s | p | p <;> simp [allSlots, List.mem_map]
theorem variables_complete (c : Coord) : c ∈ allVariables := by
  exact List.mem_flatMap.mpr ⟨c.1, mem_allSlots _,
    List.mem_map.mpr ⟨c.2, BoundedExportIndices.mem_bools _, rfl⟩⟩
theorem equations_complete (e : Equation) : e ∈ equations := by
  rcases e with p | p | p | p <;> simp [equations, List.mem_map]

theorem variableCode_injective : Function.Injective variableCode := by
  intro u v h
  exact List.inj_on_of_nodup_map (by rw [variable_codes]; exact List.nodup_range)
    (variables_complete u) (variables_complete v) h

theorem equationCode_injective : Function.Injective equationCode := by
  intro u v h
  exact List.inj_on_of_nodup_map (by rw [equation_codes]; exact List.nodup_range)
    (equations_complete u) (equations_complete v) h

theorem variableCode_lt (c : Coord) : variableCode c < 386 := by
  have h : variableCode c ∈ allVariables.map variableCode :=
    List.mem_map.mpr ⟨c, variables_complete c, rfl⟩
  rw [variable_codes] at h
  exact List.mem_range.mp h

theorem equationCode_lt (e : Equation) : equationCode e < 648 := by
  have h : equationCode e ∈ equations.map equationCode :=
    List.mem_map.mpr ⟨e, equations_complete e, rfl⟩
  rw [equation_codes] at h
  exact List.mem_range.mp h

def variableFin (c : Coord) : Fin 386 := ⟨variableCode c, variableCode_lt c⟩

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

noncomputable def variableEquiv : Coord ≃ Fin 386 :=
  Equiv.ofBijective variableFin variableFin_bijective

@[simp] theorem variableEquiv_apply (c : Coord) : variableEquiv c = variableFin c := rfl

def codeRadius (i : Nat) : Rat := if i < 170 then 1 else 3

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
  · have hn : ¬ 170 + 2 * (36 * a.val + 6 * index6 i + index6 j) + bit b < 170 := by omega
    simp [variableCode, codeRadius, radius, hn]

#print axioms variable_codes
#print axioms equation_codes
#print axioms variables_complete
#print axioms equations_complete
#print axioms variableCode_injective
#print axioms equationCode_injective
#print axioms variableFin_bijective
#print axioms radius_code
end MUB.QuadraticLiftIndices
