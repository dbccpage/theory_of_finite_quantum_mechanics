/-
Narrowed boundary for TFQ-0031.
The identities are the strong-coupling formulae on a 3 by 3 lattice.
This module does not read the finite-map note and does not discharge a continuum gap.
-/

def latticeV : Nat := 3 * 3
def latticeE : Nat := 3 * 2 + 3 * 2

def beta0Num (n : Nat) : Int := 33 - 2 * n
def beta1Num (n : Nat) : Int := 306 - 38 * n

def beta0Window : List Int := (List.range 17).map beta0Num

theorem tfq0031_vertex_count : latticeV = 9 := rfl

theorem tfq0031_edge_count : latticeE = 12 := rfl

theorem tfq0031_tree_edges : latticeV - 1 = 8 := rfl

theorem tfq0031_betti : latticeE - latticeV + 1 = 4 := rfl

theorem tfq0031_beta_tilde : (2 : Int) * (3 * 3) = 18 := by
  decide

theorem tfq0031_beta_tilde_reduced : (2 : Int) = 1 * 2 ∧ (2 : Int) * (3 * 3) = 9 * 2 := by
  decide

theorem tfq0031_area_exponent (r t : Nat) :
    (r + 1) * (t + 1) + r * t = (r + 1) * t + r * (t + 1) + 1 := by
  calc
    (r + 1) * (t + 1) + r * t
        = ((r + 1) * t + (r + 1)) + r * t := by rw [Nat.mul_succ]
    _ = (r + 1) * t + ((r + 1) + r * t) := by rw [Nat.add_assoc]
    _ = (r + 1) * t + (r + (1 + r * t)) := by rw [Nat.add_assoc]
    _ = (r + 1) * t + (r + (r * t + 1)) := by rw [Nat.add_comm 1 (r * t)]
    _ = (r + 1) * t + ((r + r * t) + 1) := by rw [← Nat.add_assoc r (r * t) 1]
    _ = (r + 1) * t + ((r * t + r) + 1) := by rw [Nat.add_comm r (r * t)]
    _ = (r + 1) * t + (r * (t + 1) + 1) := by rw [← Nat.mul_succ]
    _ = (r + 1) * t + r * (t + 1) + 1 := by rw [← Nat.add_assoc]

theorem tfq0031_side_shift (r t : Nat) : (r + 1) + t = r + (t + 1) := by
  rw [Nat.add_assoc, Nat.add_comm 1 t]

theorem tfq0031_perim_exponent (r t : Nat) :
    2 * ((r + 1) + (t + 1)) + 2 * (r + t) =
      2 * ((r + 1) + t) + 2 * (r + (t + 1)) := by
  calc
    2 * ((r + 1) + (t + 1)) + 2 * (r + t)
        = 2 * (((r + 1) + t) + 1) + 2 * (r + t) := by rw [← Nat.add_assoc (r + 1) t 1]
    _ = (2 * ((r + 1) + t) + 2 * 1) + 2 * (r + t) := by rw [Nat.mul_succ]
    _ = 2 * ((r + 1) + t) + (2 * 1 + 2 * (r + t)) := by rw [Nat.add_assoc]
    _ = 2 * ((r + 1) + t) + 2 * (1 + (r + t)) := by rw [← Nat.mul_add]
    _ = 2 * ((r + 1) + t) + 2 * ((r + t) + 1) := by rw [Nat.add_comm 1 (r + t)]
    _ = 2 * ((r + 1) + t) + 2 * (r + (t + 1)) := by rw [Nat.add_assoc r t 1]

theorem tfq0031_area_pair_22 :
    (2 : Nat) * 2 + 1 * 1 = 2 * 1 + 1 * 2 + 1 := by
  decide

theorem tfq0031_area_pair_23 :
    (2 : Nat) * 3 + 1 * 2 = 2 * 2 + 1 * 3 + 1 := by
  decide

theorem tfq0031_area_pair_32 :
    (3 : Nat) * 2 + 2 * 1 = 3 * 1 + 2 * 2 + 1 := by
  decide

theorem tfq0031_area_pair_33 :
    (3 : Nat) * 3 + 2 * 2 = 3 * 2 + 2 * 3 + 1 := by
  decide

theorem tfq0031_perim_pair_22 :
    2 * ((2 : Nat) + 2) + 2 * (1 + 1) = 2 * (2 + 1) + 2 * (1 + 2) := by
  decide

theorem tfq0031_perim_pair_23 :
    2 * ((2 : Nat) + 3) + 2 * (1 + 2) = 2 * (2 + 2) + 2 * (1 + 3) := by
  decide

theorem tfq0031_perim_pair_32 :
    2 * ((3 : Nat) + 2) + 2 * (2 + 1) = 2 * (3 + 1) + 2 * (2 + 2) := by
  decide

theorem tfq0031_perim_pair_33 :
    2 * ((3 : Nat) + 3) + 2 * (2 + 2) = 2 * (3 + 2) + 2 * (2 + 3) := by
  decide

theorem tfq0031_beta0_samples :
    beta0Num 0 = 11 * 3 ∧ beta0Num 3 = 9 * 3 ∧ beta0Num 5 = 23 ∧
      beta0Num 6 = 7 * 3 ∧ beta0Num 16 = 1 ∧ beta0Num 17 = -1 := by
  decide

theorem tfq0031_beta0_window :
    beta0Window = [33, 31, 29, 27, 25, 23, 21, 19, 17, 15, 13, 11, 9, 7, 5, 3, 1] := by
  decide

theorem tfq0031_beta1_16 : beta1Num 16 = -302 := by
  decide

theorem tfq0031_banks_zaks : -beta0Num 16 * 302 = beta1Num 16 := by
  decide

#print axioms tfq0031_vertex_count
#print axioms tfq0031_edge_count
#print axioms tfq0031_tree_edges
#print axioms tfq0031_betti
#print axioms tfq0031_beta_tilde
#print axioms tfq0031_beta_tilde_reduced
#print axioms tfq0031_area_exponent
#print axioms tfq0031_side_shift
#print axioms tfq0031_perim_exponent
#print axioms tfq0031_area_pair_22
#print axioms tfq0031_area_pair_23
#print axioms tfq0031_area_pair_32
#print axioms tfq0031_area_pair_33
#print axioms tfq0031_perim_pair_22
#print axioms tfq0031_perim_pair_23
#print axioms tfq0031_perim_pair_32
#print axioms tfq0031_perim_pair_33
#print axioms tfq0031_beta0_samples
#print axioms tfq0031_beta0_window
#print axioms tfq0031_beta1_16
#print axioms tfq0031_banks_zaks
