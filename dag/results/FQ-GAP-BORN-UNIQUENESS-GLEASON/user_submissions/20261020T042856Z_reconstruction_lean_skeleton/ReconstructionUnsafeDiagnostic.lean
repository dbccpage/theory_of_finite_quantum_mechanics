/-!
# FiniteQM.Reconstruction — Row 8 skeleton

Full operational reconstruction of finite-dimensional complex QM.

Status vocabulary (kernel-facing, see `#print axioms` at the end):

* `PROVED`       closed term, no `sorry`
* `AXIOM[cite]`  published theorem imported as an axiom, citation in docstring
* `AXIOM[elem]`  elementary argument sketched in the docstring, not yet formalized
* `ENCODED`      a classification carried by a datatype rather than asserted
* `OPAQUE`       a predicate whose content lives outside this file

Dependencies: core Lean 4 only. No Mathlib.
-/

namespace FiniteQM.Reconstruction

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

/-- **A0.** An operational system: compact convex finite-dimensional state space with
effects. The carrier is abstract; the two invariants every later step consumes are
explicit. `dim` is K, the real dimension of the span of Ω; `rank` is N, the maximal
size of a perfectly distinguishable family (information capacity). -/
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

/-- **A0 (composition).** A composite with bilinear product states and marginals.
Marginals *are* no-signalling. Product frames are frames, giving `rank_mul`. -/
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

/-! ## Part III — The five imported theorems -/

/-- `OPAQUE`. The state space of `A` is affinely isomorphic to the normalized-trace
state space of `J` (cone of squares, trace one). -/
axiom JordanIso : System → EJA → Prop

/-- `AXIOM[cite]` **T1.** Barnum–Hilgert 2019, *Strongly symmetric spectral convex
bodies are Jordan algebra state spaces*, arXiv:1904.03753 (closing the gap in
Barnum–Müller–Ududec, New J. Phys. 16 (2014) 123029). Engine: Koecher 1957 / Vinberg 1960
(homogeneous self-dual cones are the cones of squares of EJAs) and Alfsen–Shultz spectral
theory. Transitivity by the theory's own reversible group implies transitivity by the full
affine group, so no no-restriction hypothesis is needed here. -/
axiom jordan_of_spectral_strongSym (A : System) (h1 : Spectral A) (h2 : StronglySymmetric A) :
  ∃ J : EJA, JordanIso A J ∧ A.dim = J.dim ∧ A.rank = J.rank

/-- `AXIOM[cite]` **T2.** Alfsen–Shultz, *Geometry of State Spaces of Operator Algebras*
(Birkhäuser 2003): Jordan automorphisms preserve the center, hence permute the simple
summands. Consequence: a frame with two idempotents in one summand cannot be carried to a
frame split across two summands, so strong symmetry forces a single summand, or all
summands of rank 1 (classical, where permutations suffice). -/
axiom simple_or_classical (A : System) (h : StronglySymmetric A) (J : EJA) (hJ : JordanIso A J) :
  J.IsSimple ∨ J.IsClassical

/-- `AXIOM[cite]` **T3.** Barnum–Wilce 2014, *Local tomography and the Jordan structure of
quantum theory*, Found. Phys. 44, 192–212, via Hanche-Olsen 1983, *On the structure and
tensor products of JC-algebras*, Can. J. Math. 35, 1059–1074. In a locally tomographic
theory whose systems are Jordan and which contains a qubit, every system is a direct sum
of complex matrix algebras. The elementary necessary condition is `complex_dim_mul`
together with `real_not_multiplicative` and `quat_not_multiplicative`. -/
axiom complex_of_localTomo (T : Theory) (rep : T.Sys → EJA)
    (hrep : ∀ a, JordanIso (T.sys a) (rep a))
    (q : T.Sys) (s : SimpleEJA) (hq : (rep q).summands = [s]) (hs : s.IsQubitAlgebra) :
  ∀ a, ∀ t, t ∈ (rep a).summands → t.IsComplexType

/-- `AXIOM[elem]` **T4.** The composite of a classical system of capacity ≥ 2 with a qubit
is not classical: if it were, its state space would be a simplex with finitely many
vertices, but δᵢ ⊗ σ for σ ranging over the qubit's continuum of pure states gives
infinitely many distinct pure product states (distinct because their marginals differ).
The *simple* branch is closed by `no_simple_dim4m_rank2m`; only the classical branch is
left to this axiom. Formalizing it needs the convex geometry abstracted away in `System`. -/
axiom no_classical_composite_with_qubit (T : Theory) (rep : T.Sys → EJA)
    (hrep : ∀ a, JordanIso (T.sys a) (rep a))
    (c q : T.Sys) (hc : (rep c).IsClassical) (hc2 : 2 ≤ (rep c).rank)
    (hq : (T.sys q).rank = 2 ∧ (T.sys q).dim = 4) :
  ¬ (rep (T.comp c q)).IsClassical

/-- `OPAQUE`. The dynamical and measurement half of the equivalence for a system of
capacity n: reversible maps are (anti)unitary conjugations with identity component PU(n),
one-parameter subgroups are ρ ↦ e^{-iHt} ρ e^{iHt}, effects are POVM elements, general
transformations are completely positive, and the Born rule is the duality pairing. -/
axiom DynamicsEquivalence : System → Nat → Prop

/-- `AXIOM[cite]` **T5.** Wigner 1931 / Kadison 1951 (affine automorphisms of D(ℂⁿ) are
(anti)unitary conjugations); Choi 1975 (positivity under every tensor extension is
complete positivity). The Lie-dimension step — transitivity on n-frames needs an orbit of
dimension n²−n, which no proper closed subgroup of PU(n) has — is elementary and not yet
formalized. -/
axiom dynamics_of_complex (A : System) (hss : StronglySymmetric A) (J : EJA) (hJ : JordanIso A J)
    (s : SimpleEJA) (hs : J.summands = [s]) (hc : s.IsComplexType) :
  DynamicsEquivalence A s.rank

/-! ## Part IV — Assembly: Row 8, state-space half -/

/-- **Reconstruction.** Under A0–A4 every system is a single complex matrix algebra
Herm_n(ℂ) with N = n and K = n², and carries the quantum dynamics and measurements.
Dependencies are listed by `#print axioms` below. -/
theorem reconstruction (T : Theory) :
    ∀ a, ∃ (J : EJA) (s : SimpleEJA),
      JordanIso (T.sys a) J ∧ J.summands = [s] ∧ s.IsComplexType ∧
      (T.sys a).rank = s.rank ∧ (T.sys a).dim = s.rank * s.rank ∧
      DynamicsEquivalence (T.sys a) s.rank := by
  -- T1: every system has a Jordan representative
  have hex : ∀ a, ∃ J : EJA, JordanIso (T.sys a) J ∧ (T.sys a).dim = J.dim ∧ (T.sys a).rank = J.rank :=
    fun a => jordan_of_spectral_strongSym _ (T.spectral a) (T.strongSym a)
  obtain ⟨rep, hrep⟩ := Classical.axiomOfChoice hex
  have hiso : ∀ a, JordanIso (T.sys a) (rep a) := fun a => (hrep a).1
  -- A4 → qubit algebra
  obtain ⟨q, hq2, hq4⟩ := T.qubit
  have hqr : (rep q).rank = 2 := by rw [← (hrep q).2.2]; exact hq2
  have hqd : (rep q).dim = 4 := by rw [← (hrep q).2.1]; exact hq4
  obtain ⟨sq, hsq, hsqq⟩ := qubit_algebra (rep q) hqr hqd
  -- T3: every summand everywhere is complex
  have hcx := complex_of_localTomo T rep hiso q sq hsq hsqq
  intro a
  -- single summand, by T2 + counting
  have hsingle : ∃ s, (rep a).summands = [s] := by
    rcases simple_or_classical (T.sys a) (T.strongSym a) (rep a) (hiso a) with hS | hC
    · exact hS
    · -- classical: rank 1 is fine, rank ≥ 2 contradicts the qubit
      by_cases hm : 2 ≤ (rep a).rank
      · exfalso
        let ab := T.comp a q
        rcases simple_or_classical (T.sys ab) (T.strongSym ab) (rep ab) (hiso ab) with hS' | hC'
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
        · exact no_classical_composite_with_qubit T rep hiso a q hC hm ⟨hq2, hq4⟩ hC'
      · have h1 := EJA.rank_pos (rep a)
        exact EJA.classical_rank_one_single (rep a) (by omega)
  obtain ⟨s, hs⟩ := hsingle
  have hsc : s.IsComplexType := hcx a s (by rw [hs]; simp)
  refine ⟨rep a, s, hiso a, hs, hsc, ?_, ?_, dynamics_of_complex _ (T.strongSym a) _ (hiso a) s hs hsc⟩
  · rw [(hrep a).2.2]; simp only [EJA.rank, hs, sumRank, Nat.add_zero]
  · rw [(hrep a).2.1]; simp only [EJA.dim, hs, sumDim, Nat.add_zero]
    exact SimpleEJA.complexType_dim s hsc

/-- Composition is the tensor product on capacities: N_AB = N_A · N_B. `PROVED` from A3
and the reconstruction. -/
theorem composite_rank_mul (T : Theory) (a b : T.Sys) :
    (T.sys (T.comp a b)).rank = (T.sys a).rank * (T.sys b).rank := by
  obtain ⟨_, sa, _, _, _, hra, hda, _⟩ := reconstruction T a
  obtain ⟨_, sb, _, _, _, hrb, hdb, _⟩ := reconstruction T b
  obtain ⟨_, sab, _, _, _, hrab, hdab, _⟩ := reconstruction T (T.comp a b)
  have h := T.localTomo a b
  rw [hdab, hda, hdb, ← hra, ← hrb, ← hrab] at h
  -- h : N_AB * N_AB = N_A * N_A * (N_B * N_B)
  rw [← Nat.mul_mul_mul_comm] at h
  exact Nat.mul_self_inj.mp h

/-! ## Part V — Separation witnesses (`PROVED` where the model can see them)

| competing theory          | killed by | witness here                         |
|---------------------------|-----------|--------------------------------------|
| classical                 | A4        | `classical_bit_fails_A4`             |
| boxworld                  | A1        | not visible to the Jordan model      |
| real QM                   | A3, A4    | `real_not_multiplicative`, `rebit_is_disk` |
| quaternionic QM           | A3, A4    | `quat_not_multiplicative`, `quabit_is_5ball` |
| V_d (d ≠ 3), Herm₃(𝕆)     | A3        | `spin_no_composite`, `albert_no_composite` |
-/

theorem classical_bit_fails_A4 : sumDim [.realHerm 1, .realHerm 1] = 2 := by decide
theorem rebit_is_disk        : (SimpleEJA.realHerm 2).dim = 3 := by decide
theorem quabit_is_5ball      : (SimpleEJA.quatHerm 2).dim = 6 := by decide

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

end FiniteQM.Reconstruction

namespace FiniteQM.Reconstruction.Audit
open FiniteQM.Reconstruction

/-- A syntactically admissible one-state system with an ungrounded dimension field. -/
def phantom : System where
  State := Unit
  Rev := Unit
  act := fun _ _ => ()
  pure := fun _ => True
  frame := fun f => f = [()]
  hull := fun _ _ => True
  dim := 2
  rank := 1
  frame_le_rank := by
    intro f hf
    change f = [()] at hf
    subst f
    decide
  rank_attained := ⟨[()], rfl, rfl⟩

theorem phantom_spectral : Spectral phantom where
  decomp := by
    intro w
    refine ⟨[()], rfl, ?_, trivial⟩
    intro x hx
    trivial

theorem phantom_strongSym : StronglySymmetric phantom where
  transitive := by
    intro f g hf hg hlen
    change f = [()] at hf
    change g = [()] at hg
    refine ⟨(), ?_⟩
    rw [hf, hg]
    rfl

theorem rank_one_dim_one (J : EJA) (hr : J.rank = 1) : J.dim = 1 := by
  obtain ⟨s, hs⟩ := EJA.classical_rank_one_single J hr
  have hsr : s.rank = 1 := by
    simpa [EJA.rank, hs, sumRank] using hr
  have hw : s.wf := J.wf s (by rw [hs]; simp)
  have hd := SimpleEJA.rank_one_dim_one s hw hsr
  simpa [EJA.dim, hs, sumDim] using hd

/-- Diagnostic only: the unrestricted imported signature is inconsistent with System. -/
theorem unrestricted_bridge_derives_false : False := by
  obtain ⟨J, hIso, hd, hr⟩ :=
    jordan_of_spectral_strongSym phantom phantom_spectral phantom_strongSym
  have hjr : J.rank = 1 := by
    change 1 = J.rank at hr
    exact hr.symm
  have hjd := rank_one_dim_one J hjr
  change 2 = J.dim at hd
  omega

#print axioms phantom_spectral
#print axioms phantom_strongSym
#print axioms unrestricted_bridge_derives_false
end FiniteQM.Reconstruction.Audit
