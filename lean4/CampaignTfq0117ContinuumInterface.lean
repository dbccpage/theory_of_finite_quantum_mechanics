import Mathlib.Data.Rat.Defs
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases

/-!
# Campaign Formalization: `TFQ-0117` (`CONTINUUM_INTERFACE`)
## Finite Cyclic Self-Duality, Exact $\mu_4$ Character Orthogonality, and Circle-Promotion Refusal Fences

This module formalizes the exact finite/algebraic counterpart and non-equivalence scope fences for
DAG node `TFQ-0117` (`GAP-F002-S001-001 remains open. Finite cyclic dual is not sold as a circle
group`):

1. **Finite Cyclic Self-Duality & Exponent-3 vs. Free-Integer Fence (`Z/NZ` Dual is `Z/NZ`, Not $U(1)$ or $\mathbb{Z}$)**:
   - On `Fin N` (`N > 0`), the character label set `Fin N` has finite cardinality `N`
     (`finite_cyclic_dual_cardinality`), and the modular pairing `cyclicPairing N k x = (k * x) % N`
     is annihilated by `N`-fold repetition `(N * k * x) % N = 0` (`finite_cyclic_periodicity`).
   - Discharges the `M3/M4` finite countermodel of `TFQ-0117`: `Fin 3` (`Z/3Z`) has cardinality `3`,
     is not exponent-2 (`(1 + 1) % 3 = 2 ≠ 0`), yet satisfies `(x + x + x) % 3 = 0` for all
     `x : Fin 3`, showing that a non-exponent-2 `N = 3` witness does not force the free integers
     $\mathbb{Z}$ or the continuous circle group $U(1)$ (`z3_not_exponent_two_yet_torsion_three_fence`).

2. **Exact Character Orthogonality Over $\mathbb{Q}[i]$ on $\mathbb{Z}/4\mathbb{Z}$ (`CharacterOrthogonality`)**:
   - Models Gaussian rationals `GaussRat` (`ℚ × ℚ`) with exact multiplication `gaussMul` and
     conjugation `gaussConj`, and the 4th-root-of-unity character family `chi4 (k x : Fin 4) : GaussRat`.
   - Proves that `mu4` is an exact group homomorphism under modular addition mod 4
     (`mu4_add_mod4_homomorphism`), every character value has unit Gaussian norm `normSq = 1`
     (`chi4_unit_gaussian_norm`), and the character inner product over `Fin 4` satisfies exact
     orthogonality: `chi4Inner k m = (4, 0)` if `k = m` and `(0, 0)` if `k ≠ m`
     (`z4_character_orthogonality_exact`).

3. **Promotion-Refusal Fences (`C_4` Cochain Syndrome, Sign-Fiber Gap, and Haar Period Independence)**:
   - Replays the `TFQ-0117` `M1/M4` finite witnesses: on $C_4$ with tree potentials `(200, -400, 300)`
     and chord potential `-300`, the oriented loop holonomy residual is `400`, and the $\mathbb{Z}_2$
     sign-fiber interference gap is `(1 + 1)^2 - (1 + (-1))^2 = 4`
     (`c4_cochain_syndrome_and_sign_fiber_gap_replay`).
   - Proves that unit-mass Haar normalization `(1 / P) * P = 1` holds for every nonzero period
     `P ≠ 0` and scales any interval length `L = α * P` to the period-independent fraction `α`, so
     Haar uniqueness of unit total mass does not select the angular period `2π`
     (`haar_normalization_period_independence_fence`, `haar_period_calibration_bijective`).
-/

namespace CampaignTfq0117ContinuumInterface

-- ============================================================================
-- 1. Finite Cyclic Self-Duality & `N = 3` Non-Exponent-2 Torsion Fence
-- ============================================================================

/-- Modular character pairing `(k * x) % N` on the finite cyclic carrier `Fin N`. -/
def cyclicPairing (N : Nat) (k x : Fin N) : Nat :=
  (k.val * x.val) % N

/-- Modular addition `(a + b) % N` on `Nat`. -/
def cyclicAdd (N a b : Nat) : Nat :=
  (a + b) % N

/-- Theorem 1: The dual character label carrier `Fin N` of the finite cyclic group of order `N` has
exact finite cardinality `N`, and for any `N1 ≠ N2`, their character duals have distinct finite
cardinalities. -/
theorem finite_cyclic_dual_cardinality (N1 N2 : Nat) (h : N1 ≠ N2) :
    Fintype.card (Fin N1) = N1 ∧
    Fintype.card (Fin N2) = N2 ∧
    Fintype.card (Fin N1) ≠ Fintype.card (Fin N2) := by
  simp [h]

/-- Theorem 2: Every modular character pairing is annihilated after `N` steps (`(N * (k * x)) % N = 0`),
witnessing finite torsion order dividing `N` rather than free-integer $\mathbb{Z}$ grading. -/
theorem finite_cyclic_periodicity (N : Nat) (k x : Fin N) :
    (N * (k.val * x.val)) % N = 0 := by
  exact Nat.mul_mod_right N (k.val * x.val)

/-- Theorem 3 (`M3/M4` `Z/3Z` Countermodel Fence): On `Fin 3` (`N = 3`), the carrier has cardinality
`3`, is not exponent-2 (`cyclicAdd 3 1 1 = 2 ≠ 0`), yet every element `x : Fin 3` has 3-fold modular
sum `(x + x + x) % 3 = 0`—showing that a non-exponent-2 witness at `N = 3` is satisfied by a finite
torsion group and does not force $\mathbb{Z}$ or the circle $U(1)$. -/
theorem z3_not_exponent_two_yet_torsion_three_fence :
    Fintype.card (Fin 3) = 3 ∧
    cyclicAdd 3 1 1 = 2 ∧
    cyclicAdd 3 1 1 ≠ 0 ∧
    (∀ x : Fin 3, (x.val + x.val + x.val) % 3 = 0) := by
  decide

-- ============================================================================
-- 2. Exact Character Orthogonality Over $\mathbb{Q}[i]$ on $\mathbb{Z}/4\mathbb{Z}$
-- ============================================================================

/-- Gaussian integer/rational unit-lattice element `re + i * im` over `Int`. -/
@[ext]
structure GaussRat where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def gaussZero : GaussRat := ⟨0, 0⟩
def gaussOne : GaussRat := ⟨1, 0⟩

def gaussAdd (z w : GaussRat) : GaussRat :=
  ⟨z.re + w.re, z.im + w.im⟩

def gaussMul (z w : GaussRat) : GaussRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

def gaussConj (z : GaussRat) : GaussRat :=
  ⟨z.re, -z.im⟩

def gaussNormSq (z : GaussRat) : Int :=
  z.re ^ 2 + z.im ^ 2

/-- The 4th roots of unity `μ_4 = {1, i, -1, -i}` indexed by `Fin 4`. -/
def mu4 (n : Fin 4) : GaussRat :=
  match n.val with
  | 0 => ⟨1, 0⟩
  | 1 => ⟨0, 1⟩
  | 2 => ⟨-1, 0⟩
  | _ => ⟨0, -1⟩

/-- Character `χ_k(x) = μ_4((k * x) mod 4)` of `Z/4Z`. -/
def chi4 (k x : Fin 4) : GaussRat :=
  mu4 ⟨(k.val * x.val) % 4, Nat.mod_lt _ (by decide)⟩

/-- Unnormalized inner product `∑_{x ∈ Fin 4} χ_k(x) * conj(χ_m(x))` on `Z/4Z`. -/
def chi4Inner (k m : Fin 4) : GaussRat :=
  let t0 := gaussMul (chi4 k 0) (gaussConj (chi4 m 0))
  let t1 := gaussMul (chi4 k 1) (gaussConj (chi4 m 1))
  let t2 := gaussMul (chi4 k 2) (gaussConj (chi4 m 2))
  let t3 := gaussMul (chi4 k 3) (gaussConj (chi4 m 3))
  gaussAdd (gaussAdd t0 t1) (gaussAdd t2 t3)

/-- Theorem 4: `mu4` is an exact group homomorphism from `(Fin 4, + mod 4)` into `(GaussRat, gaussMul)`. -/
theorem mu4_add_mod4_homomorphism (a b : Fin 4) :
    mu4 ⟨(a.val + b.val) % 4, Nat.mod_lt _ (by decide)⟩ =
      gaussMul (mu4 a) (mu4 b) := by
  revert a b
  decide

/-- Theorem 5: Every character value `chi4 k x` lies on the rational unit circle `re^2 + im^2 = 1`
and satisfies `gaussMul (chi4 k x) (gaussConj (chi4 k x)) = gaussOne`. -/
theorem chi4_unit_gaussian_norm (k x : Fin 4) :
    gaussNormSq (chi4 k x) = 1 ∧
    gaussMul (chi4 k x) (gaussConj (chi4 k x)) = gaussOne := by
  revert k x
  decide

/-- Theorem 6: Exact character orthogonality on `Z/4Z`: for all `k, m : Fin 4`,
`chi4Inner k m = ⟨4, 0⟩` when `k = m` and `chi4Inner k m = ⟨0, 0⟩` when `k ≠ m`. -/
theorem z4_character_orthogonality_exact (k m : Fin 4) :
    chi4Inner k m = (if k = m then ⟨4, 0⟩ else gaussZero) := by
  revert k m
  decide

/-- Theorem 7: For any non-trivial character `k ≠ 0` of `Z/4Z`, the sum of character values over the
4 group elements vanishes identically (`chi4Inner k 0 = gaussZero`). -/
theorem z4_nontrivial_character_sum_zero (k : Fin 4) (hk : k ≠ 0) :
    chi4Inner k 0 = gaussZero := by
  rw [z4_character_orthogonality_exact]
  simp [hk]

-- ============================================================================
-- 3. Promotion-Refusal Fences (`C_4` Cochain Syndrome, Sign-Fiber, & Haar Period)
-- ============================================================================

/-- Oriented 4-cycle loop holonomy `e01 + e12 + e23 - e03` from tree potentials `(e01, e12, e23)`
and chord potential `e03`. -/
def c4LoopHolonomy (e01 e12 e23 e03 : Int) : Int :=
  e01 + e12 + e23 - e03

/-- Squared amplitude `(s1 + s2)^2` of two `±1` sign-fiber paths. -/
def signFiberIntensity (s1 s2 : Int) : Int :=
  (s1 + s2) ^ 2

/-- Theorem 8: Exact replay of the `TFQ-0117` `M1/M4` finite witnesses:
(1) for `tree_potentials = (200, -400, 300)` and `chord_potential = -300`, the loop holonomy
`c4LoopHolonomy 200 (-400) 300 (-300)` equals `400`;
(2) constructive vs. destructive sign-fiber interference gives `signFiberIntensity 1 1 = 4`,
`signFiberIntensity 1 (-1) = 0`, and gap `4 - 0 = 4`. -/
theorem c4_cochain_syndrome_and_sign_fiber_gap_replay :
    c4LoopHolonomy 200 (-400) 300 (-300) = 400 ∧
    signFiberIntensity 1 1 = 4 ∧
    signFiberIntensity 1 (-1) = 0 ∧
    signFiberIntensity 1 1 - signFiberIntensity 1 (-1) = 4 := by
  decide

/-- Normalized uniform measure `(1 / P) * L` of an interval of length `L` on a periodic domain of
period `P`. -/
def normalizedHaarIntervalMass (P L : ℚ) : ℚ :=
  (1 / P) * L

/-- Theorem 9 (Haar Uniqueness Does Not Select Period `2π`): For any nonzero angular period `P ≠ 0`
(whether `P = 1`, `P = 44/7`, or `P = 360`) and any fractional arc `α : ℚ`, normalizing the uniform
measure by `1 / P` assigns total mass `1` to the full period `L = P` and mass `α` to the sub-arc
`L = α * P`, completely independent of `P`. -/
theorem haar_normalization_period_independence_fence
    (P α : ℚ) (hP : P ≠ 0) :
    normalizedHaarIntervalMass P P = 1 ∧
    normalizedHaarIntervalMass P (α * P) = α := by
  refine ⟨?_, ?_⟩
  · dsimp [normalizedHaarIntervalMass]; field_simp [hP]
  · dsimp [normalizedHaarIntervalMass]; field_simp [hP]

/-- Theorem 10: For any fixed nonzero arc length `L ≠ 0`, distinct nonzero period normalizations
`P1 ≠ P2` assign distinct normalized masses `normalizedHaarIntervalMass P1 L ≠ normalizedHaarIntervalMass P2 L`. -/
theorem haar_period_calibration_injective
    (L P1 P2 : ℚ) (hL : L ≠ 0) (hP1 : P1 ≠ 0) (hP2 : P2 ≠ 0)
    (heq : normalizedHaarIntervalMass P1 L = normalizedHaarIntervalMass P2 L) :
    P1 = P2 := by
  dsimp [normalizedHaarIntervalMass] at heq
  field_simp [hL, hP1, hP2] at heq
  linarith

end CampaignTfq0117ContinuumInterface

#print axioms CampaignTfq0117ContinuumInterface.finite_cyclic_dual_cardinality
#print axioms CampaignTfq0117ContinuumInterface.finite_cyclic_periodicity
#print axioms CampaignTfq0117ContinuumInterface.z3_not_exponent_two_yet_torsion_three_fence
#print axioms CampaignTfq0117ContinuumInterface.mu4_add_mod4_homomorphism
#print axioms CampaignTfq0117ContinuumInterface.chi4_unit_gaussian_norm
#print axioms CampaignTfq0117ContinuumInterface.z4_character_orthogonality_exact
#print axioms CampaignTfq0117ContinuumInterface.z4_nontrivial_character_sum_zero
#print axioms CampaignTfq0117ContinuumInterface.c4_cochain_syndrome_and_sign_fiber_gap_replay
#print axioms CampaignTfq0117ContinuumInterface.haar_normalization_period_independence_fence
#print axioms CampaignTfq0117ContinuumInterface.haar_period_calibration_injective

private def l5aProvenance : String :=
  "Origin: lean4/CampaignTfq0117ContinuumInterface.lean Claim: TFQ-0117 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
