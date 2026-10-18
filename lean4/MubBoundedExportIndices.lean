import MubBoundedExpressions

/-!
# Complete coordinate and equation codes for bounded-quartet export

AuthorityEffect: None.
-/

namespace MUB.BoundedExportIndices
open BoundedCoordinates BoundedPolynomials BoundedBlockChart

def bit : Bool → Nat | false => 0 | true => 1
def index6 (i : I6) : Nat := (blockIndex i).val
def indices6 : List I6 := (List.finRange 6).map blockIndex.symm
def bools : List Bool := [false, true]

@[simp] theorem mem_indices6 (i : I6) : i ∈ indices6 := by
  apply List.mem_map.mpr
  exact ⟨blockIndex i, by simp, blockIndex.symm_apply_apply i⟩

def slotCode : Slot → Nat
  | .inl (i, j) => 2 * i.val + j.val
  | .inr (.inl (i, j)) => 4 + 3 * i.val + j.val
  | .inr (.inr (.inl (i, j))) => 10 + 2 * i.val + j.val
  | .inr (.inr (.inr (.inl (i, j)))) => 16 + 6 * i.val + index6 j
  | .inr (.inr (.inr (.inr (i, j)))) => 46 + 6 * i.val + index6 j

def variableCode (c : Coord) : Nat := 2 * slotCode c.1 + bit c.2

def equationCode : Equation → Nat
  | .inl (a, i, j) => 9 * a.val + 3 * i.val + j.val
  | .inr (.inl (i, j)) => 27 + 3 * i.val + j.val
  | .inr (.inr (.inl (a, i, j))) => 36 + 36 * a.val + 6 * index6 i + index6 j
  | .inr (.inr (.inr (.inl (a, i, j)))) => 108 + 36 * a.val + 6 * index6 i + index6 j
  | .inr (.inr (.inr (.inr (.inl (a, i, j, b))))) => 216 + 2 * (9 * a.val + 3 * i.val + j.val) + bit b
  | .inr (.inr (.inr (.inr (.inr (a, i, j, b))))) => 252 + 2 * (36 * a.val + 6 * index6 i + index6 j) + bit b

def pairs (n m : Nat) : List (Fin n × Fin m) :=
  (List.finRange n).flatMap fun i => (List.finRange m).map fun j => (i, j)
def basisSlots : List (Fin 5 × I6) :=
  (List.finRange 5).flatMap fun i => indices6.map fun j => (i, j)
def allSlots : List Slot :=
  (pairs 2 2).map Sum.inl ++ (pairs 2 3).map (fun p => .inr (.inl p)) ++
  (pairs 3 2).map (fun p => .inr (.inr (.inl p))) ++
  basisSlots.map (fun p => .inr (.inr (.inr (.inl p)))) ++
  basisSlots.map (fun p => .inr (.inr (.inr (.inr p))))
def allVariables : List Coord := allSlots.flatMap fun s => bools.map fun b => (s, b)

def entries3 (n : Nat) : List (Fin n × I3 × I3) :=
  (List.finRange n).flatMap fun a => (pairs 3 3).map fun (i, j) => (a, i, j)
def entries6 (n : Nat) : List (Fin n × I6 × I6) :=
  (List.finRange n).flatMap fun a => indices6.flatMap fun i => indices6.map fun j => (a, i, j)
def components3 (n : Nat) : List (Fin n × I3 × I3 × Bool) :=
  (entries3 n).flatMap fun (a, i, j) => bools.map fun b => (a, i, j, b)
def components6 (n : Nat) : List (Fin n × I6 × I6 × Bool) :=
  (entries6 n).flatMap fun (a, i, j) => bools.map fun b => (a, i, j, b)
def equations : List Equation :=
  (entries3 3).map Sum.inl ++ (pairs 3 3).map (fun p => .inr (.inl p)) ++
  (entries6 2).map (fun p => .inr (.inr (.inl p))) ++
  (entries6 3).map (fun p => .inr (.inr (.inr (.inl p)))) ++
  (components3 2).map (fun p => .inr (.inr (.inr (.inr (.inl p))))) ++
  (components6 2).map (fun p => .inr (.inr (.inr (.inr (.inr p)))))

set_option maxRecDepth 10000 in
theorem variable_codes : allVariables.map variableCode = List.range 152 := by decide
set_option maxRecDepth 10000 in
theorem equation_codes : equations.map equationCode = List.range 396 := by decide

@[simp] theorem mem_bools (b : Bool) : b ∈ bools := by cases b <;> simp [bools]

@[simp] theorem mem_pairs {n m : Nat} (p : Fin n × Fin m) : p ∈ pairs n m := by
  exact List.mem_flatMap.mpr ⟨p.1, by simp, List.mem_map.mpr ⟨p.2, by simp, rfl⟩⟩

@[simp] theorem mem_basisSlots (p : Fin 5 × I6) : p ∈ basisSlots := by
  exact List.mem_flatMap.mpr ⟨p.1, by simp, List.mem_map.mpr ⟨p.2, mem_indices6 _, rfl⟩⟩

@[simp] theorem mem_allSlots (s : Slot) : s ∈ allSlots := by
  rcases s with p | p | p | p | p <;> simp [allSlots, List.mem_map]

theorem variables_complete (c : Coord) : c ∈ allVariables := by
  exact List.mem_flatMap.mpr ⟨c.1, mem_allSlots _, List.mem_map.mpr ⟨c.2, mem_bools _, rfl⟩⟩

@[simp] theorem mem_entries3 {n : Nat} (p : Fin n × I3 × I3) : p ∈ entries3 n := by
  exact List.mem_flatMap.mpr ⟨p.1, by simp, List.mem_map.mpr ⟨p.2, mem_pairs _, rfl⟩⟩

@[simp] theorem mem_entries6 {n : Nat} (p : Fin n × I6 × I6) : p ∈ entries6 n := by
  exact List.mem_flatMap.mpr ⟨p.1, by simp, List.mem_flatMap.mpr
    ⟨p.2.1, mem_indices6 _, List.mem_map.mpr ⟨p.2.2, mem_indices6 _, rfl⟩⟩⟩

@[simp] theorem mem_components3 {n : Nat} (p : Fin n × I3 × I3 × Bool) : p ∈ components3 n := by
  exact List.mem_flatMap.mpr ⟨(p.1, p.2.1, p.2.2.1), mem_entries3 _,
    List.mem_map.mpr ⟨p.2.2.2, mem_bools _, rfl⟩⟩

@[simp] theorem mem_components6 {n : Nat} (p : Fin n × I6 × I6 × Bool) : p ∈ components6 n := by
  exact List.mem_flatMap.mpr ⟨(p.1, p.2.1, p.2.2.1), mem_entries6 _,
    List.mem_map.mpr ⟨p.2.2.2, mem_bools _, rfl⟩⟩

theorem equations_complete (e : Equation) : e ∈ equations := by
  rcases e with p | p | p | p | p | p <;> simp [equations, List.mem_map]

theorem variableCode_injective : Function.Injective variableCode := by
  intro u v h
  exact List.inj_on_of_nodup_map (by rw [variable_codes]; exact List.nodup_range)
    (variables_complete u) (variables_complete v) h

theorem equationCode_injective : Function.Injective equationCode := by
  intro u v h
  exact List.inj_on_of_nodup_map (by rw [equation_codes]; exact List.nodup_range)
    (equations_complete u) (equations_complete v) h

theorem variableCode_lt (c : Coord) : variableCode c < 152 := by
  have h : variableCode c ∈ allVariables.map variableCode :=
    List.mem_map.mpr ⟨c, variables_complete c, rfl⟩
  rw [variable_codes] at h
  exact List.mem_range.mp h

theorem equationCode_lt (e : Equation) : equationCode e < 396 := by
  have h : equationCode e ∈ equations.map equationCode :=
    List.mem_map.mpr ⟨e, equations_complete e, rfl⟩
  rw [equation_codes] at h
  exact List.mem_range.mp h

def variableFin (c : Coord) : Fin 152 := ⟨variableCode c, variableCode_lt c⟩

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

noncomputable def variableEquiv : Coord ≃ Fin 152 :=
  Equiv.ofBijective variableFin variableFin_bijective

@[simp] theorem variableEquiv_apply (c : Coord) : variableEquiv c = variableFin c := rfl

#print axioms variable_codes
#print axioms equation_codes
#print axioms variables_complete
#print axioms equations_complete
#print axioms variableCode_injective
#print axioms equationCode_injective
#print axioms variableCode_lt
#print axioms equationCode_lt
#print axioms variableFin_bijective
end MUB.BoundedExportIndices
