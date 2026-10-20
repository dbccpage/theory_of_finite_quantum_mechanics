/-!
# FiniteQM.ReconstructionConditional — Row 8 skeleton

Arithmetic tag classification and conditional assembly only. No geometric Jordan algebra or full operational reconstruction is formalized here.

Status vocabulary (kernel-facing, see `#print axioms` at the end):

* `PROVED`       closed term, no `sorry`
* `HYPOTHESIS`   a per-theory bridge field; no instance or published-theorem application is proved here
* `CONDITIONAL`  an implication from explicit fields, not a discharge of those fields
* `ENCODED`      a classification carried by a datatype rather than asserted
* `PARAMETER`    a predicate variable whose intended semantics are not formalized

Dependencies: core Lean 4 only. No Mathlib.
-/

namespace FiniteQM.ReconstructionConditional

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

/-! ## Part II — Operational side: A0–A4 -/

/-- Bare combinatorial interface copied from the proposal. No convex vector space,
compactness, affine action, operational effects, or semantic dimension is defined here.
The per-theory bridge fields below must be instantiated only after those obligations
are proved in a richer model. `Rev` is only a type and `act` only a function. -/
structure System where
  State : Type
  /-- reversible transformations and their action -/
  Rev   : Type
  act   : Rev → State → State
  pure  : State → Prop
  /-- `frame f`: the states in `f` are perfectly distinguishable -/
  frame : List State → Prop
  /-- `hull f ω`: ω is a convex combination of the states in `f` -/
  hull  : List State → State → Prop
  dim   : Nat
  rank  : Nat
  frame_le_rank : ∀ f, frame f → f.length ≤ rank
  rank_attained : ∃ f, frame f ∧ f.length = rank

/-- **A1. Spectrality** (Alfsen–Shultz sense). Every state is a mixture of perfectly
distinguishable pure states. Independent justification: states are classical lotteries
over an ideal alphabet. Fails for boxworld (the gbit square is not spectral). -/
structure Spectral (A : System) : Prop where
  decomp : ∀ ω : A.State, ∃ f, A.frame f ∧ (∀ x, x ∈ f → A.pure x) ∧ A.hull f ω

/-- **A2. Strong symmetry.** Any two frames of equal size are related by a reversible
transformation. Independent justification: relabeling invariance of equal-size
alphabets. This is the load-bearing axiom; see the audit in the text. -/
structure StronglySymmetric (A : System) : Prop where
  transitive : ∀ f g, A.frame f → A.frame g → f.length = g.length →
    ∃ r : A.Rev, f.map (A.act r) = g

/-- Set-level products with marginal sections and an assumed numerical rank bound.
Bilinearity, product effects, probabilities and operational no-signalling are not encoded. -/
structure Composite (A B AB : System) where
  prod      : A.State → B.State → AB.State
  margA     : AB.State → A.State
  margB     : AB.State → B.State
  marg_prod : ∀ a b, margA (prod a b) = a ∧ margB (prod a b) = b
  rank_mul  : A.rank * B.rank ≤ AB.rank

/-- A theory satisfying **A0–A4** with total composition. -/
structure Theory where
  Sys  : Type
  sys  : Sys → System
  comp : Sys → Sys → Sys
  composite : ∀ a b, Composite (sys a) (sys b) (sys (comp a b))
  /-- A1 -/
  spectral  : ∀ a, Spectral (sys a)
  /-- A2 -/
  strongSym : ∀ a, StronglySymmetric (sys a)
  /-- **A3. Local tomography.** Composite states are fixed by joint local statistics:
  K_AB = K_A · K_B. Independent justification: a global state is a finite record of local
  tests. Empirically testable; real QM violates it (Renou et al., Nature 600, 625, 2021). -/
  localTomo : ∀ a b, (sys (comp a b)).dim = (sys a).dim * (sys b).dim
  /-- **A4. A qubit exists.** Some capacity-2 system has three real parameters.
  Independent justification: Stokes 1852 — polarization has exactly three real
  parameters, seventy years before QM. (Among spectral strongly-symmetric rank-2 systems
  this pins V₃ ≅ Herm₂(ℂ); see `qubit_algebra`.) -/
  qubit : ∃ q, (sys q).rank = 2 ∧ (sys q).dim = 4


/-! ## Part III — Explicit per-theory import contract

These are proof PARAMETERS, not global axioms. No instance is supplied here.
The predicates are parameters too; their geometric/dynamical meaning is not defined.
A checked implication from this contract does not discharge any contract field.
Restricting fields to T.Sys avoids the submitted unrestricted theorem on every bare System.
-/

structure ReconstructionImports (T : Theory)
    (JordanIso : System → EJA → Prop)
    (DynamicsEquivalence : System → Nat → Prop) : Prop where
  jordan_of_spectral_strongSym : ∀ a : T.Sys,
    ∃ J : EJA, JordanIso (T.sys a) J ∧ (T.sys a).dim = J.dim ∧ (T.sys a).rank = J.rank
  simple_or_classical : ∀ (a : T.Sys) (J : EJA),
    JordanIso (T.sys a) J → J.IsSimple ∨ J.IsClassical
  complex_of_localTomo : ∀ (rep : T.Sys → EJA),
    (∀ a, JordanIso (T.sys a) (rep a)) →
    ∀ (q : T.Sys) (s : SimpleEJA), (rep q).summands = [s] → s.IsQubitAlgebra →
    ∀ a, ∀ t, t ∈ (rep a).summands → t.IsComplexType
  no_classical_composite_with_qubit : ∀ (rep : T.Sys → EJA),
    (∀ a, JordanIso (T.sys a) (rep a)) →
    ∀ c q, (rep c).IsClassical → 2 ≤ (rep c).rank →
    ((T.sys q).rank = 2 ∧ (T.sys q).dim = 4) → ¬ (rep (T.comp c q)).IsClassical
  dynamics_of_complex : ∀ (a : T.Sys) (J : EJA),
    JordanIso (T.sys a) J → ∀ s, J.summands = [s] → s.IsComplexType →
    DynamicsEquivalence (T.sys a) s.rank

/-! ## Part IV — Assembly: Row 8, state-space half -/

/-- Conditional assembly of encoded tags and a parameterized dynamics predicate.
This theorem assumes all five fields of ReconstructionImports explicitly. It constructs
neither a concrete Jordan algebra isomorphism nor an operational theory equivalence. -/
theorem reconstruction (T : Theory)
    (JordanIso : System → EJA → Prop) (DynamicsEquivalence : System → Nat → Prop)
    (imports : ReconstructionImports T JordanIso DynamicsEquivalence) :
    ∀ a, ∃ (J : EJA) (s : SimpleEJA),
      JordanIso (T.sys a) J ∧ J.summands = [s] ∧ s.IsComplexType ∧
      (T.sys a).rank = s.rank ∧ (T.sys a).dim = s.rank * s.rank ∧
      DynamicsEquivalence (T.sys a) s.rank := by
  -- T1: every system has a Jordan representative
  have hex : ∀ a, ∃ J : EJA, JordanIso (T.sys a) J ∧ (T.sys a).dim = J.dim ∧ (T.sys a).rank = J.rank :=
    fun a => imports.jordan_of_spectral_strongSym a
  obtain ⟨rep, hrep⟩ := Classical.axiomOfChoice hex
  have hiso : ∀ a, JordanIso (T.sys a) (rep a) := fun a => (hrep a).1
  -- A4 → qubit algebra
  obtain ⟨q, hq2, hq4⟩ := T.qubit
  have hqr : (rep q).rank = 2 := by rw [← (hrep q).2.2]; exact hq2
  have hqd : (rep q).dim = 4 := by rw [← (hrep q).2.1]; exact hq4
  obtain ⟨sq, hsq, hsqq⟩ := qubit_algebra (rep q) hqr hqd
  -- T3: every summand everywhere is complex
  have hcx := imports.complex_of_localTomo rep hiso q sq hsq hsqq
  intro a
  -- single summand, by T2 + counting
  have hsingle : ∃ s, (rep a).summands = [s] := by
    rcases imports.simple_or_classical a (rep a) (hiso a) with hS | hC
    · exact hS
    · -- classical: rank 1 is fine, rank ≥ 2 contradicts the qubit
      by_cases hm : 2 ≤ (rep a).rank
      · exfalso
        let ab := T.comp a q
        rcases imports.simple_or_classical ab (rep ab) (hiso ab) with hS' | hC'
        · obtain ⟨t, ht⟩ := hS'
          have hdimA : (T.sys a).dim = (rep a).rank := by
            rw [(hrep a).2.1]; exact EJA.classical_dim_eq_rank _ hC
          have hdimAB : (T.sys ab).dim = (rep a).rank * 4 := by
            rw [T.localTomo a q, hdimA, hq4]
          have htd : t.dim = 4 * (rep a).rank := by
            have h := (hrep ab).2.1
            rw [hdimAB] at h
            simp only [EJA.dim, ht, sumDim, Nat.add_zero] at h
            rw [← h, Nat.mul_comm]
          have htr : 2 * (rep a).rank ≤ t.rank := by
            have h1 := (T.composite a q).rank_mul
            rw [hq2, (hrep a).2.2, (hrep ab).2.2] at h1
            simp only [EJA.rank, ht, sumRank, Nat.add_zero] at h1
            rw [Nat.mul_comm] at h1; exact h1
          exact no_simple_dim4m_rank2m _ hm t ((rep ab).wf t (by rw [ht]; simp)) htd htr
        · exact imports.no_classical_composite_with_qubit rep hiso a q hC hm ⟨hq2, hq4⟩ hC'
      · have h1 := EJA.rank_pos (rep a)
        exact EJA.classical_rank_one_single (rep a) (by omega)
  obtain ⟨s, hs⟩ := hsingle
  have hsc : s.IsComplexType := hcx a s (by rw [hs]; simp)
  refine ⟨rep a, s, hiso a, hs, hsc, ?_, ?_, imports.dynamics_of_complex a (rep a) (hiso a) s hs hsc⟩
  · rw [(hrep a).2.2]; simp only [EJA.rank, hs, sumRank, Nat.add_zero]
  · rw [(hrep a).2.1]; simp only [EJA.dim, hs, sumDim, Nat.add_zero]
    exact SimpleEJA.complexType_dim s hsc

/-- Numeric capacity multiplicativity: N_AB = N_A · N_B. Conditional on the explicit bridge contract and A3
and the reconstruction. -/
theorem composite_rank_mul (T : Theory)
    (JordanIso : System → EJA → Prop) (DynamicsEquivalence : System → Nat → Prop)
    (imports : ReconstructionImports T JordanIso DynamicsEquivalence) (a b : T.Sys) :
    (T.sys (T.comp a b)).rank = (T.sys a).rank * (T.sys b).rank := by
  obtain ⟨_, sa, _, _, _, hra, hda, _⟩ := reconstruction T JordanIso DynamicsEquivalence imports a
  obtain ⟨_, sb, _, _, _, hrb, hdb, _⟩ := reconstruction T JordanIso DynamicsEquivalence imports b
  obtain ⟨_, sab, _, _, _, hrab, hdab, _⟩ := reconstruction T JordanIso DynamicsEquivalence imports (T.comp a b)
  have h := T.localTomo a b
  rw [hdab, hda, hdb, ← hra, ← hrb, ← hrab] at h
  -- h : N_AB * N_AB = N_A * N_A * (N_B * N_B)
  rw [← Nat.mul_mul_mul_comm] at h
  exact Nat.mul_self_inj.mp h

/-! ## Part V — Numeric tag witnesses only (not disk/ball or categorical constructions)

| competing theory          | killed by | witness here                         |
|---------------------------|-----------|--------------------------------------|
| classical                 | A4        | `classical_two_tag_dim_two`             |
| boxworld                  | A1        | not visible to the Jordan model      |
| real QM                   | A3, A4    | `real_not_multiplicative`, `real_rank_two_dim_three` |
| quaternionic QM           | A3, A4    | `quat_not_multiplicative`, `quaternionic_rank_two_dim_six` |
| V_d (d ≠ 3), Herm₃(𝕆)     | A3        | `spin_no_composite`, `albert_no_composite` |
-/

theorem classical_two_tag_dim_two : sumDim [.realHerm 1, .realHerm 1] = 2 := by decide
theorem real_rank_two_dim_three        : (SimpleEJA.realHerm 2).dim = 3 := by decide
theorem quaternionic_rank_two_dim_six      : (SimpleEJA.quatHerm 2).dim = 6 := by decide

/-- A composite of two rank-2 systems needs rank ≥ 4; no spin factor has it. -/
theorem spin_no_composite (d : Nat) : ¬ (4 ≤ (SimpleEJA.spin d).rank) := by
  simp only [SimpleEJA.rank]; omega

/-- The Albert algebra has rank 3 and so cannot host any composite of two rank-2 systems. -/
theorem albert_no_composite : ¬ (4 ≤ SimpleEJA.albert.rank) := by decide

/-! ## Kernel receipt -/

#print axioms reconstruction
#print axioms composite_rank_mul
#print axioms no_simple_dim4m_rank2m
#print axioms qubit_algebra

end FiniteQM.ReconstructionConditional

namespace FiniteQM.ReconstructionConditional.GeometryInterface

/-- A finite generating list for the supplied hull relation. The relation is a parameter. -/
def HasFiniteHull {X : Type} (hull : List X → X → Prop) : Prop :=
  ∃ vertices : List X, ∀ x : X, hull vertices x

/-- Affine hull transport plus surjectivity sends finite generation to finite generation. -/
theorem finite_hull_image {X Y : Type}
    (hullX : List X → X → Prop) (hullY : List Y → Y → Prop)
    (f : X → Y) (surj : ∀ y, ∃ x, f x = y)
    (transport : ∀ vertices x, hullX vertices x → hullY (vertices.map f) (f x))
    (finiteX : HasFiniteHull hullX) : HasFiniteHull hullY := by
  obtain ⟨vertices, hvertices⟩ := finiteX
  refine ⟨vertices.map f, ?_⟩
  intro y
  obtain ⟨x, rfl⟩ := surj y
  exact transport vertices x (hvertices x)

/-- The geometry needed for classical exclusion is exposed instead of hidden in a global axiom. -/
theorem no_finite_hull_composite_with_nonpolytope_marginal
    (A B AB : System) (comp : Composite A B AB) (a0 : A.State)
    (transport : ∀ vertices x,
      AB.hull vertices x → B.hull (vertices.map comp.margB) (comp.margB x))
    (finiteAB : HasFiniteHull AB.hull) (nonpolyB : ¬ HasFiniteHull B.hull) : False := by
  apply nonpolyB
  exact finite_hull_image AB.hull B.hull comp.margB
    (fun b => ⟨comp.prod a0 b, (comp.marg_prod a0 b).2⟩) transport finiteAB

#print axioms finite_hull_image
#print axioms no_finite_hull_composite_with_nonpolytope_marginal
end FiniteQM.ReconstructionConditional.GeometryInterface
