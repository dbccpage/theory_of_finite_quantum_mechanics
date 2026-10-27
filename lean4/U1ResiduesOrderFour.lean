-- DS-QM062-U1-RESIDUES-IMPORT. Not a default target.
-- Right-multiplication by the integer matrix J has order 4, and (k + 4) % 4 = k % 4.
-- Continuity, local tomography, and a U(1) fiber stay outside this module.

namespace U1ResiduesOrderFour

abbrev Mat := Int × Int × Int × Int

def mm : Mat → Mat → Mat
  | (a, b, c, d), (e, f, g, h) =>
    (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)

def eye : Mat := (1, 0, 0, 1)
def jay : Mat := (0, -1, 1, 0)
def jay2 : Mat := (-1, 0, 0, -1)
def jay3 : Mat := (0, 1, -1, 0)

def rep (r : Nat) : Mat :=
  if r = 0 then eye
  else if r = 1 then jay
  else if r = 2 then jay2
  else if r = 3 then jay3
  else eye

def pow : Nat → Mat
  | 0 => eye
  | Nat.succ n => mm (pow n) jay

theorem eye_entries : eye = (1, 0, 0, 1) := rfl
theorem jay_entries : jay = (0, -1, 1, 0) := rfl
theorem jay2_entries : jay2 = (-1, 0, 0, -1) := rfl
theorem jay3_entries : jay3 = (0, 1, -1, 0) := rfl

theorem alias4 (k : Nat) : (k + 4) % 4 = k % 4 :=
  Nat.add_mod_right k 4

theorem rem0 : (0 : Nat) % 4 = 0 := by decide
theorem rem1 : (1 : Nat) % 4 = 1 := by decide
theorem rem2 : (2 : Nat) % 4 = 2 := by decide
theorem rem3 : (3 : Nat) % 4 = 3 := by decide
theorem rem4 : (4 : Nat) % 4 = 0 := by decide

theorem stepNeg : (0 : Int) * 0 - 1 * 1 = -1 := by decide
theorem stepBack : (-1 : Int) * -1 = 1 := by decide

theorem sq : mm jay jay = jay2 := by decide
theorem cu : mm jay2 jay = jay3 := by decide
theorem fourth : mm jay3 jay = eye := by decide
theorem jayNe : jay ≠ eye := by decide
theorem jay2Ne : jay2 ≠ eye := by decide
theorem jay3Ne : jay3 ≠ eye := by decide

theorem mod_succ (k : Nat) : (k + 1) % 4 = (k % 4 + 1) % 4 := by
  rw [Nat.add_mod, rem1]

theorem rep_step (r : Nat) (hr : r < 4) : mm (rep r) jay = rep ((r + 1) % 4) := by
  match r with
  | 0 => decide
  | 1 => decide
  | 2 => decide
  | 3 => decide
  | n + 4 =>
      exfalso
      omega

theorem pow_rep (k : Nat) : pow k = rep (k % 4) := by
  induction k with
  | zero =>
      simp [pow, rep, Nat.zero_mod]
  | succ k ih =>
      have hk : k % 4 < 4 := Nat.mod_lt k (by decide : 0 < 4)
      calc
        pow (Nat.succ k) = mm (pow k) jay := by simp [pow]
        _ = mm (rep (k % 4)) jay := by rw [ih]
        _ = rep ((k % 4 + 1) % 4) := rep_step (k % 4) hk
        _ = rep ((k + 1) % 4) := by rw [← mod_succ k]
        _ = rep (Nat.succ k % 4) := by rw [Nat.succ_eq_add_one]

theorem rep_eye (r : Nat) (hr : r < 4) : rep r = eye ↔ r = 0 := by
  match r with
  | 0 => decide
  | 1 => decide
  | 2 => decide
  | 3 => decide
  | n + 4 =>
      exfalso
      omega

theorem pow_eye (k : Nat) : pow k = eye ↔ k % 4 = 0 := by
  rw [pow_rep]
  exact rep_eye (k % 4) (Nat.mod_lt k (by decide : 0 < 4))

theorem pow_period (k : Nat) : pow (k + 4) = pow k := by
  rw [pow_rep, pow_rep, alias4]

theorem pow1 : pow 1 = jay := by decide
theorem pow2 : pow 2 = jay2 := by decide
theorem pow3 : pow 3 = jay3 := by decide
theorem pow4 : pow 4 = eye := by decide

#print axioms alias4
#print axioms rem0
#print axioms rem1
#print axioms rem2
#print axioms rem3
#print axioms rem4
#print axioms stepNeg
#print axioms stepBack
#print axioms sq
#print axioms cu
#print axioms fourth
#print axioms jayNe
#print axioms jay2Ne
#print axioms jay3Ne
#print axioms eye_entries
#print axioms jay_entries
#print axioms jay2_entries
#print axioms jay3_entries
#print axioms mod_succ
#print axioms rep_step
#print axioms pow_rep
#print axioms rep_eye
#print axioms pow_eye
#print axioms pow_period
#print axioms pow1
#print axioms pow2
#print axioms pow3
#print axioms pow4

end U1ResiduesOrderFour
