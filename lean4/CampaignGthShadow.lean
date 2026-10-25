/-
Campaign narrowing of GTH-SHADOW.

One triangle, one reach map, and one pair of parallel edges.
Status stays OPEN. This stage keeps the node lean list empty.
-/

def face2 : Nat × Nat := (0, 1)
def face1 : Nat × Nat := (0, 2)
def face0 : Nat × Nat := (1, 2)

def src (e : Nat × Nat) : Nat := e.1
def tgt (e : Nat × Nat) : Nat := e.2

theorem face_id_01 : tgt face1 = 2 ∧ tgt face0 = 2 ∧ tgt face1 = tgt face0 := by
  decide

theorem face_id_02 : tgt face2 = 1 ∧ src face0 = 1 ∧ tgt face2 = src face0 := by
  decide

theorem face_id_12 : src face2 = 0 ∧ src face1 = 0 ∧ src face2 = src face1 := by
  decide

def reach (_v : Nat) : Nat := 0

theorem reach_collapses : reach 0 = 0 ∧ reach 1 = 0 ∧ (reach 0, reach 1) = (0, 0) := by
  decide

theorem reach_pair_differs : (reach 0, reach 1) ≠ face2 := by
  decide

def edgeSource (_e : Nat) : Nat := 0
def edgeTarget (_e : Nat) : Nat := 1

theorem parallel_edges :
    edgeSource 0 = 0 ∧ edgeSource 1 = 0 ∧ edgeTarget 0 = 1 ∧ edgeTarget 1 = 1 ∧
      edgeSource 0 = edgeSource 1 ∧ edgeTarget 0 = edgeTarget 1 := by
  decide

#print axioms face_id_01
#print axioms face_id_02
#print axioms face_id_12
#print axioms reach_collapses
#print axioms reach_pair_differs
#print axioms parallel_edges
