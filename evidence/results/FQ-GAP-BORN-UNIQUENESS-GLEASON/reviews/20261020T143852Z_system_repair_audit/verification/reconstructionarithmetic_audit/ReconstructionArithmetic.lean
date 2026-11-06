/-!
Arithmetic-only extraction from the submitted reconstruction skeleton.
The datatypes encode rank/dimension formulas. No Jordan multiplication, state geometry,
actual disk/ball isomorphism, process theory or global bridge axiom is declared here.
Core Lean only; see the original attachment and review for provenance.
-/
namespace FiniteQM.ReconstructionArithmetic

/-! ## Part I — Jordan side

`ENCODED`: Jordan–von Neumann–Wigner 1934, Ann. Math. 35, 29–64.
The simple Euclidean Jordan algebras are exactly the five families below.
Coincidences: V₂ ≅ Herm₂(ℝ), V₃ ≅ Herm₂(ℂ), V₅ ≅ Herm₂(ℍ); Herm₁(𝔽) ≅ ℝ for every 𝔽.
The invariants `rank` (N, maximal frame size) and `dim` (K, real dimension) are
the only data consumed downstream.
-/

inductive SimpleEJA
  | realHerm    (n : Nat)   -- Herm_n(ℝ)
  | complexHerm (n : Nat)   -- Herm_n(ℂ)
  | quatHerm    (n : Nat)   -- Herm_n(ℍ)
  | spin        (d : Nat)   -- V_d, state space = d-ball
  | albert                  -- Herm_3(𝕆)
  deriving DecidableEq, Repr

namespace SimpleEJA

def rank : SimpleEJA → Nat
  | realHerm n | complexHerm n | quatHerm n => n
  | spin _ => 2
  | albert => 3

def dim : SimpleEJA → Nat
  | realHerm n    => n * (n + 1) / 2
  | complexHerm n => n * n
  | quatHerm n    => n * (2 * n - 1)
  | spin d        => d + 1
  | albert        => 27

/-- Well-formedness: the degenerate index values are excluded. -/
def wf : SimpleEJA → Prop
  | realHerm n | complexHerm n | quatHerm n => 1 ≤ n
  | spin d => 2 ≤ d
  | albert => True

/-- "Is a complex matrix algebra", modulo the JvNW coincidences. -/
def IsComplexType : SimpleEJA → Prop
  | complexHerm _ => True
  | realHerm n    => n = 1
  | quatHerm n    => n = 1
  | spin d        => d = 3
  | albert        => False

/-- The two spellings of the qubit algebra Herm₂(ℂ) ≅ V₃. -/
def IsQubitAlgebra (s : SimpleEJA) : Prop := s = complexHerm 2 ∨ s = spin 3

end SimpleEJA

def sumRank : List SimpleEJA → Nat
  | []     => 0
  | s :: t => s.rank + sumRank t

def sumDim : List SimpleEJA → Nat
  | []     => 0
  | s :: t => s.dim + sumDim t

/-- A Euclidean Jordan algebra = finite direct sum of simple ones. -/
structure EJA where
  summands : List SimpleEJA
  nonempty : summands ≠ []
  wf       : ∀ s, s ∈ summands → s.wf

namespace EJA

def rank (J : EJA) : Nat := sumRank J.summands
def dim  (J : EJA) : Nat := sumDim  J.summands

def IsSimple    (J : EJA) : Prop := ∃ s, J.summands = [s]
def IsClassical (J : EJA) : Prop := ∀ s, s ∈ J.summands → s.rank = 1

end EJA

/-! ### Elementary facts about the invariants — all `PROVED` -/

theorem two_dvd_mul_succ : ∀ n : Nat, 2 ∣ n * (n + 1)
  | 0 => ⟨0, rfl⟩
  | n + 1 => by
    have ih := two_dvd_mul_succ n
    have h : (n + 1) * (n + 1 + 1) = n * (n + 1) + 2 * (n + 1) := by
      simp only [Nat.add_mul, Nat.mul_add, Nat.mul_one, Nat.one_mul]
      omega
    rw [h]
    exact Nat.dvd_add ih (Nat.dvd_mul_right 2 (n + 1))

theorem SimpleEJA.wf_rank_pos (s : SimpleEJA) (h : s.wf) : 1 ≤ s.rank := by
  cases s <;> simp only [SimpleEJA.wf, SimpleEJA.rank] at * <;> omega

theorem SimpleEJA.rank_one_dim_one (s : SimpleEJA) (hw : s.wf) (h : s.rank = 1) : s.dim = 1 := by
  cases s with
  | realHerm n    => simp only [SimpleEJA.rank] at h; subst h; decide
  | complexHerm n => simp only [SimpleEJA.rank] at h; subst h; decide
  | quatHerm n    => simp only [SimpleEJA.rank] at h; subst h; decide
  | spin d        => simp only [SimpleEJA.rank] at h; omega
  | albert        => simp only [SimpleEJA.rank] at h; omega

theorem SimpleEJA.rank_one_complexType (s : SimpleEJA) (hw : s.wf) (h : s.rank = 1) :
    s.IsComplexType := by
  cases s with
  | realHerm n    => simp only [SimpleEJA.rank] at h; simp only [SimpleEJA.IsComplexType]; exact h
  | complexHerm n => trivial
  | quatHerm n    => simp only [SimpleEJA.rank] at h; simp only [SimpleEJA.IsComplexType]; exact h
  | spin d        => simp only [SimpleEJA.rank] at h; omega
  | albert        => simp only [SimpleEJA.rank] at h; omega

theorem SimpleEJA.complexType_dim (s : SimpleEJA) (h : s.IsComplexType) :
    s.dim = s.rank * s.rank := by
  cases s with
  | realHerm n    => simp only [SimpleEJA.IsComplexType] at h; subst h; decide
  | complexHerm n => rfl
  | quatHerm n    => simp only [SimpleEJA.IsComplexType] at h; subst h; decide
  | spin d        => simp only [SimpleEJA.IsComplexType] at h; subst h; decide
  | albert        => simp only [SimpleEJA.IsComplexType] at h

theorem sumDim_eq_sumRank : ∀ (l : List SimpleEJA),
    (∀ s, s ∈ l → s.wf) → (∀ s, s ∈ l → s.rank = 1) → sumDim l = sumRank l
  | [], _, _ => rfl
  | s :: t, hwf, h => by
    simp only [sumDim, sumRank]
    have hs : s.rank = 1 := h s (by simp)
    rw [SimpleEJA.rank_one_dim_one s (hwf s (by simp)) hs, hs,
        sumDim_eq_sumRank t (fun u hu => hwf u (by simp [hu])) (fun u hu => h u (by simp [hu]))]

theorem EJA.classical_dim_eq_rank (J : EJA) (h : J.IsClassical) : J.dim = J.rank :=
  sumDim_eq_sumRank J.summands J.wf h

/-- Local tomography counting, complex case: K(N_A N_B) = K(N_A) K(N_B). `PROVED`. -/
theorem complex_dim_mul (n k : Nat) :
    (SimpleEJA.complexHerm (n * k)).dim
      = (SimpleEJA.complexHerm n).dim * (SimpleEJA.complexHerm k).dim := by
  simp only [SimpleEJA.dim]
  exact Nat.mul_mul_mul_comm n k n k

/-- Real QM is not locally tomographic: K(2)=3 but K(4)=10 ≠ 9 (Hardy–Wootters 2012). `PROVED`. -/
theorem real_not_multiplicative :
    (SimpleEJA.realHerm (2 * 2)).dim ≠ (SimpleEJA.realHerm 2).dim * (SimpleEJA.realHerm 2).dim := by
  decide

/-- Quaternionic QM is not locally tomographic: K(2)=6 but K(4)=28 ≠ 36. `PROVED`. -/
theorem quat_not_multiplicative :
    (SimpleEJA.quatHerm (2 * 2)).dim ≠ (SimpleEJA.quatHerm 2).dim * (SimpleEJA.quatHerm 2).dim := by
  decide

/-- **The counting lemma (step 3).** No simple EJA has K = 4m and N ≥ 2m once m ≥ 2.
This is what kills a classical system of capacity m sitting next to a qubit, in the
branch where their composite is simple. `PROVED`. -/
theorem no_simple_dim4m_rank2m (m : Nat) (hm : 2 ≤ m) (s : SimpleEJA) (hwf : s.wf)
    (hdim : s.dim = 4 * m) (hrank : 2 * m ≤ s.rank) : False := by
  cases s with
  | realHerm n =>
    simp only [SimpleEJA.dim, SimpleEJA.rank] at hdim hrank
    have h2 : 2 * (n * (n + 1) / 2) = n * (n + 1) := Nat.mul_div_cancel' (two_dvd_mul_succ n)
    have h4 : 4 ≤ n := by omega
    have h5 : 4 * (n + 1) ≤ n * (n + 1) := Nat.mul_le_mul_right (n + 1) h4
    omega
  | complexHerm n =>
    simp only [SimpleEJA.dim, SimpleEJA.rank] at hdim hrank
    have h4 : 4 ≤ n := by omega
    have h5 : 4 * n ≤ n * n := Nat.mul_le_mul_right n h4
    omega
  | quatHerm n =>
    simp only [SimpleEJA.dim, SimpleEJA.rank] at hdim hrank
    have h4 : 4 ≤ n := by omega
    have h5 : 4 * (2 * n - 1) ≤ n * (2 * n - 1) := Nat.mul_le_mul_right (2 * n - 1) h4
    omega
  | spin d =>
    simp only [SimpleEJA.rank] at hrank; omega
  | albert =>
    simp only [SimpleEJA.rank] at hrank; omega

/-- A4 in Jordan terms: capacity 2 with three real parameters is the qubit algebra,
in either spelling. `PROVED`. -/
theorem qubit_algebra (J : EJA) (hr : J.rank = 2) (hd : J.dim = 4) :
    ∃ s, J.summands = [s] ∧ s.IsQubitAlgebra := by
  obtain ⟨l, hne, hwf⟩ := J
  simp only [EJA.rank, EJA.dim] at hr hd
  match l, hne, hwf with
  | [], h, _ => exact absurd rfl h
  | [s], _, hwf =>
    refine ⟨s, rfl, ?_⟩
    simp only [sumRank, sumDim, Nat.add_zero] at hr hd
    cases s with
    | realHerm n    => simp only [SimpleEJA.rank] at hr; subst hr; simp [SimpleEJA.dim] at hd
    | complexHerm n => simp only [SimpleEJA.rank] at hr; subst hr; exact Or.inl rfl
    | quatHerm n    => simp only [SimpleEJA.rank] at hr; subst hr; simp [SimpleEJA.dim] at hd
    | spin d        =>
      simp only [SimpleEJA.dim] at hd
      have : d = 3 := by omega
      subst this; exact Or.inr rfl
    | albert        => simp only [SimpleEJA.rank] at hr; omega
  | s :: t :: rest, _, hwf =>
    exfalso
    simp only [sumRank, sumDim] at hr hd
    have h1 := SimpleEJA.wf_rank_pos s (hwf s (by simp))
    have h2 := SimpleEJA.wf_rank_pos t (hwf t (by simp))
    have hs : s.rank = 1 := by omega
    have ht : t.rank = 1 := by omega
    cases rest with
    | nil =>
      simp only [sumDim] at hd
      rw [SimpleEJA.rank_one_dim_one s (hwf s (by simp)) hs,
          SimpleEJA.rank_one_dim_one t (hwf t (by simp)) ht] at hd
      omega
    | cons u rest' =>
      have := SimpleEJA.wf_rank_pos u (hwf u (by simp))
      simp only [sumRank] at hr
      omega

theorem EJA.rank_pos (J : EJA) : 1 ≤ J.rank := by
  obtain ⟨l, hne, hwf⟩ := J
  simp only [EJA.rank]
  cases l with
  | nil => exact absurd rfl hne
  | cons s t =>
    simp only [sumRank]
    have := SimpleEJA.wf_rank_pos s (hwf s (by simp))
    omega

theorem EJA.classical_rank_one_single (J : EJA) (hr : J.rank = 1) : ∃ s, J.summands = [s] := by
  obtain ⟨l, hne, hwf⟩ := J
  simp only [EJA.rank] at hr
  match l, hne, hwf with
  | [], h, _ => exact absurd rfl h
  | [s], _, _ => exact ⟨s, rfl⟩
  | s :: t :: _, _, hwf =>
    exfalso
    simp only [sumRank] at hr
    have := SimpleEJA.wf_rank_pos s (hwf s (by simp))
    have := SimpleEJA.wf_rank_pos t (hwf t (by simp))
    omega

theorem classical_two_tag_dim_two : sumDim [.realHerm 1, .realHerm 1] = 2 := by decide
theorem real_rank_two_dim_three        : (SimpleEJA.realHerm 2).dim = 3 := by decide
theorem quaternionic_rank_two_dim_six      : (SimpleEJA.quatHerm 2).dim = 6 := by decide

/-- A composite of two rank-2 systems needs rank ≥ 4; no spin factor has it. -/
theorem spin_no_composite (d : Nat) : ¬ (4 ≤ (SimpleEJA.spin d).rank) := by
  simp only [SimpleEJA.rank]; omega

/-- The Albert algebra has rank 3 and so cannot host any composite of two rank-2 systems. -/
theorem albert_no_composite : ¬ (4 ≤ SimpleEJA.albert.rank) := by decide


#print axioms two_dvd_mul_succ
#print axioms SimpleEJA.wf_rank_pos
#print axioms SimpleEJA.rank_one_dim_one
#print axioms SimpleEJA.rank_one_complexType
#print axioms SimpleEJA.complexType_dim
#print axioms sumDim_eq_sumRank
#print axioms EJA.classical_dim_eq_rank
#print axioms complex_dim_mul
#print axioms real_not_multiplicative
#print axioms quat_not_multiplicative
#print axioms no_simple_dim4m_rank2m
#print axioms qubit_algebra
#print axioms EJA.rank_pos
#print axioms EJA.classical_rank_one_single
#print axioms classical_two_tag_dim_two
#print axioms real_rank_two_dim_three
#print axioms quaternionic_rank_two_dim_six
#print axioms spin_no_composite
#print axioms albert_no_composite
end FiniteQM.ReconstructionArithmetic
