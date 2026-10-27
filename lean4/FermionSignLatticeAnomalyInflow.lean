module

public import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
public import Mathlib.Tactic

public section

/-!
AuthorityEffect: None. Finite regulator identities, not the Callan-Harvey theorem.
The matrix results hold over any commutative ring, hence over Q(i). The cochain
results use Q. Physical identification with an anomalous determinant is not assumed.
-/

namespace FermionSignLatticeAnomalyInflow

open Matrix

section Matrices
variable {K V m n p : Type*} [CommRing K]

/-- Transport between fixed bases with independently specified row/column charges. -/
def transport (g : m → Kˣ) (h : n → Kˣ) (A : Matrix m n K) : Matrix m n K :=
  fun i j => ↑(g i)⁻¹ * A i j * ↑(h j)

theorem transport_mul [Fintype n] (g : m → Kˣ) (h : n → Kˣ)
    (k : p → Kˣ) (A : Matrix m n K) (B : Matrix n p K) :
    transport g h A * transport h k B = transport g k (A * B) := by
  ext i j
  simp only [transport, Matrix.mul_apply, Finset.mul_sum, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro l _
  calc
    _ = ↑(g i)⁻¹ * A i l * (↑(h l) * ↑(h l)⁻¹) * B l j * ↑(k j) := by ring
    _ = _ := by simp [mul_assoc]

theorem transport_sub (g : m → Kˣ) (h : n → Kˣ) (A B : Matrix m n K) :
    transport g h (A - B) = transport g h A - transport g h B := by
  ext i j
  simp [transport, mul_sub, sub_mul]

theorem transport_one [DecidableEq n] (g : n → Kˣ) :
    transport g g (1 : Matrix n n K) = 1 := by
  ext i j
  by_cases hij : i = j
  · subst j; simp [transport]
  · simp [transport, hij]

/-- An inverse certificate stays valid under a change of gauge. -/
theorem transport_inverse [Fintype n] [DecidableEq n] (g : n → Kˣ)
    (C E : Matrix n n K) (hCE : C * E = 1) (hEC : E * C = 1) :
    transport g g C * transport g g E = 1 ∧
      transport g g E * transport g g C = 1 := by
  simp [transport_mul, hCE, hEC, transport_one]

def gaugeUnit [Fintype n] [DecidableEq n] (g : n → Kˣ) : (Matrix n n K)ˣ where
  val := diagonal (fun i => ↑(g i))
  inv := diagonal (fun i => ↑(g i)⁻¹)
  val_inv := by rw [diagonal_mul_diagonal]; simp
  inv_val := by rw [diagonal_mul_diagonal]; simp

theorem transport_eq_conjugate [Fintype n] [DecidableEq n]
    (g : n → Kˣ) (A : Matrix n n K) :
    transport g g A = (gaugeUnit g).inv * A * (gaugeUnit g).val := by
  ext i j
  simp [transport, gaugeUnit, Matrix.mul_diagonal, Matrix.diagonal_mul]

/-- Includes singular and empty matrices: no logarithm or determinant division. -/
theorem det_transport [Fintype n] [DecidableEq n]
    (g : n → Kˣ) (A : Matrix n n K) :
    (transport g g A).det = A.det := by
  rw [transport_eq_conjugate]
  exact Matrix.det_units_conj' (gaugeUnit g) A

/-- A fixed pair of chiral bases with the same site charges has no gauge anomaly. -/
theorem chiral_fixed_basis_det [Fintype n] [DecidableEq n]
    (g : V → Kˣ) (row col : n → m) (site : m → V)
    (hsite : ∀ i, site (row i) = site (col i)) (A : Matrix m m K) :
    ((transport (g ∘ site) (g ∘ site) A).submatrix row col).det =
      (A.submatrix row col).det := by
  have heq : (transport (g ∘ site) (g ∘ site) A).submatrix row col =
      transport (g ∘ site ∘ row) (g ∘ site ∘ row) (A.submatrix row col) := by
    ext i j
    simp [transport, Matrix.submatrix, hsite]
  rw [heq, det_transport]

/-- The inverse E is certified separately; this definition never inverts a singular block. -/
def schur [Fintype n] (A : Matrix m m K) (B : Matrix m n K)
    (C : Matrix n m K) (E : Matrix n n K) : Matrix m m K := A - B * E * C

theorem schur_covariant [Fintype n] (g : m → Kˣ) (h : n → Kˣ)
    (A : Matrix m m K) (B : Matrix m n K) (C : Matrix n m K) (E : Matrix n n K) :
    schur (transport g g A) (transport g h B) (transport h g C) (transport h h E) =
      transport g g (schur A B C E) := by
  simp only [schur, transport_mul, transport_sub]

/-- Entry form covering Wilson hopping with fixed spin/edge coefficients. -/
def hopping (onsite : m → K) (weight link : Matrix m m K) [DecidableEq m] :
    Matrix m m K := fun i j => (if i = j then onsite i else 0) + weight i j * link i j

theorem hopping_covariant [DecidableEq m] (g : m → Kˣ)
    (onsite : m → K) (weight link : Matrix m m K) :
    hopping onsite weight (transport g g link) = transport g g (hopping onsite weight link) := by
  ext i j
  by_cases hij : i = j
  · subst j
    simp only [hopping, transport, ite_true]
    calc
      _ = ↑(g i)⁻¹ * ↑(g i) * onsite i + ↑(g i)⁻¹ * (weight i i * link i i) * ↑(g i) := by simp; ring
      _ = _ := by ring
  · simp only [hopping, transport, hij, ite_false, zero_add]
    ring
end Matrices

section Cochains
variable {V : Type*}

def curvature (a : V → V → ℚ) (x y z : V) : ℚ := a y z - a x z + a x y
def gauge (a : V → V → ℚ) (α : V → ℚ) : V → V → ℚ :=
  fun x y => a x y + α y - α x

theorem curvature_gauge (a : V → V → ℚ) (α : V → ℚ) (x y z : V) :
    curvature (gauge a α) x y z = curvature a x y z := by
  simp only [curvature, gauge]; ring

theorem bianchi (a : V → V → ℚ) (w x y z : V) :
    curvature a x y z - curvature a w y z + curvature a w x z - curvature a w x y = 0 := by
  simp only [curvature]; ring

/-- Normalized, lifted level-one candidate: exp(2 pi i cs). No compact lift invariance. -/
def csCell (a : V → V → ℚ) (t : Fin 4 → V) : ℚ :=
  (1 / 2) * a (t 0) (t 1) * curvature a (t 1) (t 2) (t 3)

def boundaryCell (a : V → V → ℚ) (α : V → ℚ) (t : Fin 4 → V) : ℚ :=
  (1 / 2) * (α (t 1) * curvature a (t 1) (t 2) (t 3) -
    α (t 0) * curvature a (t 0) (t 2) (t 3) +
    α (t 0) * curvature a (t 0) (t 1) (t 3) -
    α (t 0) * curvature a (t 0) (t 1) (t 2))

theorem cs_cell_variation (a : V → V → ℚ) (α : V → ℚ) (t : Fin 4 → V) :
    csCell (gauge a α) t - csCell a t = boundaryCell a α t := by
  simp only [csCell, gauge, boundaryCell, curvature]; ring

/-- Every finite signed tetrahedral chain, including repeated cells and empty chains. -/
theorem cs_chain_variation {T : Type*} [Fintype T] (c : T → ℚ) (t : T → Fin 4 → V)
    (a : V → V → ℚ) (α : V → ℚ) :
    (∑ q, c q * csCell (gauge a α) (t q)) - (∑ q, c q * csCell a (t q)) =
      ∑ q, c q * boundaryCell a α (t q) := by
  rw [← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro q _
  rw [← mul_sub, cs_cell_variation]

theorem finite_variation_nonzero : (1 / 2 : ℚ) * (1 / 4) * (1 / 4) = 1 / 32 ∧
    (1 / 32 : ℚ) ≠ 0 := by norm_num

abbrev Vertex := Fin 3 → ℕ

/-- Six monotone tetrahedra in each unit cube, with the orientation of x,y,z. -/
def axisOrder : Fin 6 → Fin 3 → Fin 3 :=
  ![![0, 1, 2], ![0, 2, 1], ![1, 0, 2], ![1, 2, 0], ![2, 0, 1], ![2, 1, 0]]
def orientation : Fin 6 → ℚ := ![1, -1, -1, 1, 1, -1]
def tetra (layer : ℕ) (p : Fin 6) (corner : Fin 4) : Vertex := fun μ =>
  (if μ = 2 then layer else 0) +
    (if 0 < corner.val ∧ axisOrder p 0 = μ then 1 else 0) +
    (if 1 < corner.val ∧ axisOrder p 1 = μ then 1 else 0) +
    (if 2 < corner.val ∧ axisOrder p 2 = μ then 1 else 0)

/-- x,y,z path lift of the single active link (0,0,1) -> (0,1,1). -/
def slabPotential (v w : Vertex) : ℚ :=
  if w 0 = 0 ∧ v 1 = 0 ∧ w 1 = 1 ∧ v 2 = 1 then 1 / 4 else 0
def slabGauge (v : Vertex) : ℚ :=
  if v 0 = 0 ∧ v 1 = 0 ∧ v 2 = 0 then 1 / 4 else 0
def slabCS (height : ℕ) (a : Vertex → Vertex → ℚ) : ℚ :=
  ∑ k : Fin (height - 1), ∑ p : Fin 6, orientation p * csCell a (tetra k.val p)

theorem slab_three_cs : slabCS 3 slabPotential = 0 ∧
    slabCS 3 (gauge slabPotential slabGauge) = 1 / 32 := by
  norm_num [slabCS, csCell, curvature, gauge, slabPotential, slabGauge,
    tetra, orientation, axisOrder, Fin.sum_univ_succ]

theorem slab_four_cs : slabCS 4 slabPotential = 0 ∧
    slabCS 4 (gauge slabPotential slabGauge) = 1 / 32 := by
  norm_num [slabCS, csCell, curvature, gauge, slabPotential, slabGauge,
    tetra, orientation, axisOrder, Fin.sum_univ_succ]

/-- Exact obstruction for the independently computed phase in Q(zeta_32). -/
theorem phase_obstruction {K : Type*} [Field K] [CharZero K] (z : K)
    (hz : z ^ 16 + 1 = 0) : z ≠ 1 := by
  intro heq
  subst z
  norm_num at hz

theorem phase_times_det_ne {K : Type*} [Field K] [CharZero K] (z d : K)
    (hz : z ^ 16 + 1 = 0) (hd : d ≠ 0) : z * d ≠ d := by
  intro heq
  apply phase_obstruction z hz
  apply mul_right_cancel₀ hd
  simpa using heq
end Cochains

end FermionSignLatticeAnomalyInflow

#print axioms FermionSignLatticeAnomalyInflow.transport_mul
#print axioms FermionSignLatticeAnomalyInflow.transport_sub
#print axioms FermionSignLatticeAnomalyInflow.transport_one
#print axioms FermionSignLatticeAnomalyInflow.transport_inverse
#print axioms FermionSignLatticeAnomalyInflow.transport_eq_conjugate
#print axioms FermionSignLatticeAnomalyInflow.det_transport
#print axioms FermionSignLatticeAnomalyInflow.chiral_fixed_basis_det
#print axioms FermionSignLatticeAnomalyInflow.schur_covariant
#print axioms FermionSignLatticeAnomalyInflow.hopping_covariant
#print axioms FermionSignLatticeAnomalyInflow.curvature_gauge
#print axioms FermionSignLatticeAnomalyInflow.bianchi
#print axioms FermionSignLatticeAnomalyInflow.cs_cell_variation
#print axioms FermionSignLatticeAnomalyInflow.cs_chain_variation
#print axioms FermionSignLatticeAnomalyInflow.finite_variation_nonzero
#print axioms FermionSignLatticeAnomalyInflow.slab_three_cs
#print axioms FermionSignLatticeAnomalyInflow.slab_four_cs
#print axioms FermionSignLatticeAnomalyInflow.phase_obstruction
#print axioms FermionSignLatticeAnomalyInflow.phase_times_det_ne
