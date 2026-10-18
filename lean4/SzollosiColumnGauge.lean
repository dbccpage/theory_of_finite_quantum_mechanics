import SzollosiQuadraticSystem
import SzollosiExecutableSystem

/-!
# Column gauge reduction for both additional bases

AuthorityEffect: None.

Independent unit column phases preserve every Gram norm and both raw unitary
identities. Conjugating the first-row entries fixes that row to one. The family
matrix and all eight phase parameters stay fixed. Every actual quartet therefore
has a solution of the same 618 equations with 24 prescribed real coordinates.
Both additional bases are retained. No variety emptiness, cell coverage or
curvature certificate is asserted.
-/

noncomputable section
namespace MUB.SzollosiColumnGauge
open Matrix
open scoped BigOperators
open ConcreteMubPolynomialSystem SzollosiTwoCirculant SzollosiQuartetSystem
open SzollosiQuadraticSystem

def columnRephase (U : Candidate) (c : Fin 6 → ℂ) : Candidate :=
  fun i j => U i j * c j

theorem columnRephase_one (U : Candidate) : columnRephase U (fun _ => 1) = U := by
  ext i j
  simp [columnRephase]

theorem columnRephase_gram (U V : Candidate) (c d : Fin 6 → ℂ) :
    (columnRephase U c).conjTranspose * columnRephase V d =
      fun i j => star (c i) * (U.conjTranspose * V) i j * d j := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.conjTranspose_apply, columnRephase]
  rw [Finset.mul_sum, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro k _
  simp only [star_mul]
  ring

theorem columnRephase_unitary (U : Candidate) (c : Fin 6 → ℂ)
    (hc : ∀ j, Complex.normSq (c j) = 1)
    (hU : U.conjTranspose * U = (6 : ℂ) • (1 : Candidate)) :
    (columnRephase U c).conjTranspose * columnRephase U c =
      (6 : ℂ) • (1 : Candidate) := by
  rw [columnRephase_gram, hU]
  ext i j
  by_cases hij : i = j
  · subst j
    have hu : star (c i) * c i = 1 := by
      rw [mul_comm]
      exact (normSq_unit_iff _).mp (hc i)
    simp only [Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul, mul_one]
    calc
      star (c i) * 6 * c i = 6 * (star (c i) * c i) := by ring
      _ = 6 := by rw [hu]; ring
  · simp [Matrix.smul_apply, hij]

theorem columnRephase_entry_unit (U : Candidate) (c : Fin 6 → ℂ)
    (hc : ∀ j, Complex.normSq (c j) = 1)
    (hU : ∀ i j, Complex.normSq (U i j) = 1) :
    ∀ i j, Complex.normSq (columnRephase U c i j) = 1 := by
  intro i j
  simp [columnRephase, Complex.normSq_mul, hU i j, hc j]

theorem columnRephase_rawPairMU (U V : Candidate) (c d : Fin 6 → ℂ)
    (hc : ∀ j, Complex.normSq (c j) = 1)
    (hd : ∀ j, Complex.normSq (d j) = 1) (h : RawPairMU U V) :
    RawPairMU (columnRephase U c) (columnRephase V d) := by
  intro i j
  rw [columnRephase_gram]
  simp only [Complex.normSq_mul, Complex.star_def, Complex.normSq_conj, hc i, hd j]
  simpa using h i j

def firstRowPhase (U : Candidate) (j : Fin 6) : ℂ := star (U 0 j)
def firstRowDephase (U : Candidate) : Candidate := columnRephase U (firstRowPhase U)

theorem firstRowPhase_unit (U : Candidate) (hU : ∀ i j, Complex.normSq (U i j) = 1) :
    ∀ j, Complex.normSq (firstRowPhase U j) = 1 := by
  intro j
  simpa [firstRowPhase, Complex.star_def, Complex.normSq_conj] using hU 0 j

theorem firstRowDephase_row (U : Candidate) (hU : ∀ i j, Complex.normSq (U i j) = 1) :
    ∀ j, firstRowDephase U 0 j = 1 := by
  intro j
  exact (normSq_unit_iff (U 0 j)).mp (hU 0 j)

theorem rawCandidates_firstRowDephase (H U V : Candidate) (h : RawCandidates H U V) :
    RawCandidates H (firstRowDephase U) (firstRowDephase V) := by
  rcases h with ⟨hU,heU,hHU,hV,heV,hHV,hUV⟩
  have hc := firstRowPhase_unit U heU
  have hd := firstRowPhase_unit V heV
  have hone : ∀ j : Fin 6, Complex.normSq (1 : ℂ) = 1 := by norm_num
  refine ⟨columnRephase_unitary U _ hc hU, columnRephase_entry_unit U _ hc heU,
    ?_, columnRephase_unitary V _ hd hV, columnRephase_entry_unit V _ hd heV, ?_,
    columnRephase_rawPairMU U V _ _ hc hd hUV⟩
  · simpa only [columnRephase_one, firstRowDephase] using
      columnRephase_rawPairMU H U (fun _ => 1) _ hone hc hHU
  · simpa only [columnRephase_one, firstRowDephase] using
      columnRephase_rawPairMU H V (fun _ => 1) _ hone hd hHV

def gaugeBases (r : Variable → ℝ) : Fin 3 → Candidate :=
  ![basis r 0, firstRowDephase (basis r 1), firstRowDephase (basis r 2)]
def gaugeProducts (r : Variable → ℝ) : Fin 3 → Candidate :=
  fun a => (gaugeBases r (pairLeft a)).conjTranspose * gaugeBases r (pairRight a)
def gaugeSolution (r : Variable → ℝ) : Variable → ℝ :=
  encode (parameters r) (gaugeBases r) (gaugeProducts r)

def FirstRowGauge (r : Variable → ℝ) : Prop :=
  ∀ a : Fin 2, ∀ j, basis r (candidateIndex a) 0 j = 1

theorem gaugeSolution_parameters (r : Variable → ℝ) :
    parameters (gaugeSolution r) = parameters r := rfl

theorem gaugeSolution_equations (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) :
    ∀ e, realEval (gaugeSolution r) (equationPolynomial e) = 0 := by
  have hr := (all_equations_zero_iff r).mp h
  have hp := solution_parameter_equations r hr
  have hc := rawCandidates_firstRowDephase _ _ _ (solution_rawCandidates r hr)
  apply (all_equations_zero_iff _).mpr
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simpa only [gaugeSolution, phase_encode] using (parameter_equations_iff _).mp hp
  · rw [gaugeSolution, basis_encode, rawFamily_eq_parameter, parameters_encode]
    exact hr.2.1.trans (rawFamily_eq_parameter r)
  · intro a
    rw [gaugeSolution, basis_encode]
    fin_cases a
    · exact hc.1
    · exact hc.2.2.2.1
  · intro a i j
    rw [gaugeSolution, basis_encode]
    fin_cases a
    · exact hc.2.1 i j
    · exact hc.2.2.2.2.1 i j
  · intro a
    rw [gaugeSolution, product_encode, basis_encode, basis_encode]
    rfl
  · intro a i j
    rw [gaugeSolution, product_encode]
    fin_cases a
    · exact hc.2.2.1 i j
    · exact hc.2.2.2.2.2.1 i j
    · exact hc.2.2.2.2.2.2 i j

theorem gaugeSolution_firstRow (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) : FirstRowGauge (gaugeSolution r) := by
  have hr := (all_equations_zero_iff r).mp h
  intro a j
  rw [gaugeSolution, basis_encode]
  fin_cases a
  · exact firstRowDephase_row _ (hr.2.2.2.1 0) j
  · exact firstRowDephase_row _ (hr.2.2.2.1 1) j

/-- Twenty-four real coordinates of the two variable bases are prescribed. -/
theorem firstRowGauge_coordinate (r : Variable → ℝ) (hg : FirstRowGauge r)
    (a : Fin 2) (j : Fin 6) (b : Bool) :
    r (.inr (.inl (candidateIndex a, 0, j, b))) = if b then 0 else 1 := by
  have h := hg a j
  cases b
  · simpa [basis, basisPolynomial, complexEval, realEval] using congrArg Complex.re h
  · simpa [basis, basisPolynomial, complexEval, realEval] using congrArg Complex.im h

/-- The family parameter stays fixed in the existence reduction. -/
theorem exists_gauged_solution_with_parameters_iff (p : ParameterCoord → ℝ)
    (hp : ∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) :
    (∃ r, parameters r = p ∧ (∀ e, realEval r (equationPolynomial e) = 0) ∧
      FirstRowGauge r) ↔ ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  constructor
  · rintro ⟨r,hr,hz,_⟩
    exact (exists_solution_with_parameters_iff p hp).mp ⟨r,hr,hz⟩
  · intro hq
    rcases (exists_solution_with_parameters_iff p hp).mpr hq with ⟨r,hr,hz⟩
    exact ⟨gaugeSolution r, hr, gaugeSolution_equations r hz, gaugeSolution_firstRow r hz⟩

/-- The reduced search retains a representative of every constructed-family quartet. -/
theorem exists_gauged_bounded_solution_iff_quartet :
    (∃ r : Variable → ℝ, (∀ e, realEval r (equationPolynomial e) = 0) ∧
      FirstRowGauge r ∧ ∀ i, -(radius i : ℝ) ≤ r i ∧ r i ≤ (radius i : ℝ)) ↔
      ∃ p : ParameterCoord → ℝ, (∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) ∧
        ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  rw [← exists_solution_iff_quartet]
  constructor
  · rintro ⟨r,hr,_,_⟩
    exact ⟨r,hr⟩
  · rintro ⟨r,hr⟩
    have hz := gaugeSolution_equations r hr
    exact ⟨gaugeSolution r,hz,gaugeSolution_firstRow r hr,solution_in_full_box _ hz⟩


/-- Point bounds on both additional first rows; all other radii are unchanged. -/
def gaugePoint : Variable → Option ℚ
  | .inr (.inl (a,i,_,b)) => if a = 0 ∨ i ≠ 0 then none else some (if b then 0 else 1)
  | _ => none

def gaugeLower (v : Variable) : ℚ := (gaugePoint v).getD (-radius v)
def gaugeUpper (v : Variable) : ℚ := (gaugePoint v).getD (radius v)

theorem gauged_solution_in_box (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) (hg : FirstRowGauge r) :
    ∀ v, (gaugeLower v : ℝ) ≤ r v ∧ r v ≤ (gaugeUpper v : ℝ) := by
  have hfull := solution_in_full_box r h
  intro v
  rcases v with q | q
  · simpa [gaugeLower,gaugeUpper,gaugePoint] using hfull (.inl q)
  rcases q with q | q
  · rcases q with ⟨a,i,j,b⟩
    by_cases hf : a = 0 ∨ i ≠ 0
    · simpa [gaugeLower,gaugeUpper,gaugePoint,hf,radius] using
        hfull (.inr (.inl (a,i,j,b)))
    · have hi : i = 0 := by tauto
      subst i
      fin_cases a
      · exact (hf (Or.inl rfl)).elim
      · have hc := firstRowGauge_coordinate r hg 0 j b
        cases b <;> simpa [gaugeLower,gaugeUpper,gaugePoint,candidateIndex] using
          (And.intro (le_of_eq hc.symm) (le_of_eq hc))
      · have hc := firstRowGauge_coordinate r hg 1 j b
        cases b <;> simpa [gaugeLower,gaugeUpper,gaugePoint,candidateIndex] using
          (And.intro (le_of_eq hc.symm) (le_of_eq hc))
  · simpa [gaugeLower,gaugeUpper,gaugePoint] using hfull (.inr (.inr q))

/-- Membership in the point box itself supplies the first-row equalities. -/
theorem gauge_box_firstRow (r : Variable → ℝ)
    (hb : ∀ v, (gaugeLower v : ℝ) ≤ r v ∧ r v ≤ (gaugeUpper v : ℝ)) : FirstRowGauge r := by
  intro a j
  have ha : candidateIndex a ≠ 0 := by
    intro h
    have hv := congrArg Fin.val h
    simp [candidateIndex] at hv
  have hre := hb (.inr (.inl (candidateIndex a,0,j,false)))
  have him := hb (.inr (.inl (candidateIndex a,0,j,true)))
  simp [gaugeLower,gaugeUpper,gaugePoint,ha] at hre him
  apply Complex.ext
  · simpa [basis,basisPolynomial,complexEval,realEval] using le_antisymm hre.2 hre.1
  · simpa [basis,basisPolynomial,complexEval,realEval] using le_antisymm him.2 him.1

/-- Restriction to the explicit point box preserves existence at each parameter. -/
theorem exists_gauge_box_solution_with_parameters_iff (p : ParameterCoord → ℝ)
    (hp : ∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) :
    (∃ r, parameters r = p ∧ (∀ e, realEval r (equationPolynomial e) = 0) ∧
      ∀ v, (gaugeLower v : ℝ) ≤ r v ∧ r v ≤ (gaugeUpper v : ℝ)) ↔
      ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  rw [← exists_gauged_solution_with_parameters_iff p hp]
  constructor
  · rintro ⟨r,hp,hr,hb⟩
    exact ⟨r,hp,hr,gauge_box_firstRow r hb⟩
  · rintro ⟨r,hp,hr,hg⟩
    exact ⟨r,hp,hr,gauged_solution_in_box r hr hg⟩

def gaugePointCodes : List (Nat × Rat) :=
  SzollosiExecutableSystem.allVariables.filterMap fun v =>
    (gaugePoint v).map fun q => (SzollosiExecutableSystem.variableCode v, q)

set_option maxRecDepth 10000 in
/-- Exact native wire coordinates for the two prescribed first rows. -/
theorem gaugePointCodes_checked : gaugePointCodes =
  [(80, 1), (81, 0), (82, 1), (83, 0), (84, 1), (85, 0), (86, 1), (87, 0), (88, 1), (89, 0), (90, 1), (91, 0), (152, 1), (153, 0), (154, 1), (155, 0), (156, 1), (157, 0), (158, 1), (159, 0), (160, 1), (161, 0), (162, 1), (163, 0)] := by rfl

#print axioms gaugePointCodes_checked

#print axioms gauge_box_firstRow
#print axioms gauged_solution_in_box
#print axioms exists_gauge_box_solution_with_parameters_iff

#print axioms columnRephase_gram
#print axioms columnRephase_unitary
#print axioms columnRephase_rawPairMU
#print axioms rawCandidates_firstRowDephase
#print axioms gaugeSolution_equations
#print axioms gaugeSolution_firstRow
#print axioms firstRowGauge_coordinate
#print axioms exists_gauged_solution_with_parameters_iff
#print axioms exists_gauged_bounded_solution_iff_quartet
end MUB.SzollosiColumnGauge
