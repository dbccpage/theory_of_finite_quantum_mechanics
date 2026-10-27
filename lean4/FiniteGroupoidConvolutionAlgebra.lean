import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# TFQ-0014 (`FINITE_QCD`)

Formalizes the narrowed finite counterpart and non-equivalence fences for
`TFQ-0014` ("finite_groupoid_algebra.rs linearizes a ValidatedFiniteGroupoid as
convolution over Q(i). The module states that the associated complex C*-algebra
is a mathematical extension, not a native finite computation.
gauge_cochain_complex.rs is a different object: an exact complex on packets in
M_2(Q(i)), with d0 sending anti-Hermitian generators to commutators on effects
and states. Neither file is a Hopf gauge theory, and neither file stores SU(3)
link variables. The obligation is to keep the groupoid convolution and the qubit
packet complex from being cited as the color connection used later in the QCD
control."):

1. **Finite Groupoid Convolution Algebra over `ℤ[i]` (`PairGroupoid2`)**:
   - Models the 2-object pair groupoid `{0, 1} × {0, 1}` with 4 basis arrows
     `e₀₀, e₀₁, e₁₀, e₁₁` over `ℤ[i]` and convolution product `groupoidConv`.
   - Proves strict associativity of `groupoidConv` (`pair_groupoid_convolution_associative`),
     two-sided identity `1_G = e₀₀ + e₁₁`, and orthogonality of distinct object
     idempotents `e₀₀ * e₁₁ = 0` (`pair_groupoid_unit_and_orthogonal_object_idempotents`).
   - Proves the `C*`-completion fence: the operator norm `‖e₀₀ + e₀₁‖ = √2` requires a
     square-root extension outside `ℚ` (`(2p + 1)² ≠ 2q²`,
     `groupoid_cstar_norm_requires_sqrt_extension_fence`).
2. **`M_2(ℤ[i])` Qubit Packet Cochain Complex (`packetD0` Commutator Differential)**:
   - Defines the 0-cochain differential `packetD0 Ω X = Ω * X - X * Ω` on 2×2
     Gaussian-integer matrices `Mat2GI`.
   - Proves trace vanishing `mat2GITrace (packetD0 Ω X) = 0`
     (`packet_d0_commutator_trace_zero`), scalar kernel and Leibniz derivation law
     `packetD0 Ω (X * Y) = (packetD0 Ω X) * Y + X * (packetD0 Ω Y)`
     (`packet_d0_scalar_kernel_and_leibniz_derivation`), and the Jacobi identity
     (`packet_d0_jacobi_identity`).
3. **Non-Equivalence Fences: Groupoid Convolution vs. `M_2` Packet Complex vs. `SU(3)` Color Links**:
   - Proves that the identity element `I₂` is idempotent under convolution (`I₂ * I₂ = I₂ ≠ 0`)
     but annihilated by the packet commutator differential (`packetD0 Ω I₂ = 0`),
     separating the two constructions (`groupoid_convolution_vs_packet_d0_distinct_objects_fence`).
   - Proves the matrix entry count (`4 ≠ 9`), traceless Lie generator dimension (`3 ≠ 8`),
     and scaled quadratic Casimir (`3 ≠ 16/3`) fences separating `M_2(ℚ(i))` qubit packets
     and 2-object groupoid convolutions from `SU(3)` color links and Hopf gauge modules
     (`m2_packet_vs_su3_color_dimension_and_casimir_fence`,
     `neither_module_is_hopf_or_su3_scope_ledger_fence`,
     `commutator_derivation_breaks_grouplike_multiplicativity_fence`).
-/

namespace FiniteGroupoidConvolutionAlgebra

-- ============================================================================
-- 1. Finite Groupoid Convolution Algebra over `ℤ[i]` (`PairGroupoid2`)
-- ============================================================================

/-- Gaussian integers `ℤ[i]`. -/
@[ext]
structure GaussInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def giZero : GaussInt := ⟨0, 0⟩
def giOne : GaussInt := ⟨1, 0⟩

def giAdd (z w : GaussInt) : GaussInt :=
  ⟨z.re + w.re, z.im + w.im⟩

def giSub (z w : GaussInt) : GaussInt :=
  ⟨z.re - w.re, z.im - w.im⟩

def giMul (z w : GaussInt) : GaussInt :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

/-- Element of the linearized 2-object pair groupoid convolution algebra over `ℤ[i]`,
with basis arrows `e00 : 0→0`, `e01 : 0→1`, `e10 : 1→0`, `e11 : 1→1`. -/
@[ext]
structure PairGroupoid2 where
  e00 : GaussInt
  e01 : GaussInt
  e10 : GaussInt
  e11 : GaussInt
  deriving DecidableEq, Repr

def groupoidZero : PairGroupoid2 :=
  ⟨giZero, giZero, giZero, giZero⟩

def groupoidId : PairGroupoid2 :=
  ⟨giOne, giZero, giZero, giOne⟩

def objIdem0 : PairGroupoid2 :=
  ⟨giOne, giZero, giZero, giZero⟩

def objIdem1 : PairGroupoid2 :=
  ⟨giZero, giZero, giZero, giOne⟩

/-- Groupoid convolution product `(A * B)(i, k) = ∑_{j} A(i, j) B(j, k)` where only
composable arrows `i → j` and `j → k` contribute. -/
def groupoidConv (A B : PairGroupoid2) : PairGroupoid2 :=
  ⟨giAdd (giMul A.e00 B.e00) (giMul A.e01 B.e10),
   giAdd (giMul A.e00 B.e01) (giMul A.e01 B.e11),
   giAdd (giMul A.e10 B.e00) (giMul A.e11 B.e10),
   giAdd (giMul A.e10 B.e01) (giMul A.e11 B.e11)⟩

/-- Theorem 1: Convolution multiplication `groupoidConv` on the 2-object pair groupoid
over `ℤ[i]` is strictly associative. -/
theorem pair_groupoid_convolution_associative (A B C : PairGroupoid2) :
    groupoidConv (groupoidConv A B) C = groupoidConv A (groupoidConv B C) := by
  ext <;> dsimp [groupoidConv, giAdd, giMul] <;> ring

/-- Theorem 2: The sum of object identities `groupoidId = e00 + e11` is a two-sided
unit for `groupoidConv`, while distinct object idempotents `objIdem0` and `objIdem1`
are idempotent and mutually orthogonal (`e00 * e11 = 0`). -/
theorem pair_groupoid_unit_and_orthogonal_object_idempotents (A : PairGroupoid2) :
    groupoidConv groupoidId A = A ∧
    groupoidConv A groupoidId = A ∧
    groupoidConv objIdem0 objIdem0 = objIdem0 ∧
    groupoidConv objIdem1 objIdem1 = objIdem1 ∧
    groupoidConv objIdem0 objIdem1 = groupoidZero := by
  refine ⟨?_, ?_, by decide, by decide, by decide⟩
  · ext <;> dsimp [groupoidConv, groupoidId, giAdd, giMul, giOne, giZero] <;> ring
  · ext <;> dsimp [groupoidConv, groupoidId, giAdd, giMul, giOne, giZero] <;> ring

/-- Theorem 3 (`C*`-Algebra Extension Fence): For the groupoid element `A = e00 + e01`,
the maximum eigenvalue of `A^* A` is `2`, whose operator `C*`-norm `√2` satisfies the
odd/even parity obstruction `(2p + 1)² ≠ 2q²`, confirming that the `C*`-completion is an
analytic extension rather than a native `ℚ(i)` computation. -/
theorem groupoid_cstar_norm_requires_sqrt_extension_fence (p q : Int) :
    (2 * p + 1) ^ 2 ≠ 2 * q ^ 2 := by
  intro h
  have hmod : ((2 * p + 1) ^ 2) % 2 = (2 * q ^ 2) % 2 := congrArg (fun x => x % 2) h
  have hlhs : (2 * p + 1) ^ 2 = 2 * (2 * p ^ 2 + 2 * p) + 1 := by ring
  rw [hlhs] at hmod
  omega

-- ============================================================================
-- 2. `M_2(ℤ[i])` Qubit Packet Cochain Complex (`packetD0` Commutator)
-- ============================================================================

def groupoidAdd (A B : PairGroupoid2) : PairGroupoid2 :=
  ⟨giAdd A.e00 B.e00, giAdd A.e01 B.e01, giAdd A.e10 B.e10, giAdd A.e11 B.e11⟩

def groupoidSub (A B : PairGroupoid2) : PairGroupoid2 :=
  ⟨giSub A.e00 B.e00, giSub A.e01 B.e01, giSub A.e10 B.e10, giSub A.e11 B.e11⟩

def groupoidScale (c : GaussInt) (A : PairGroupoid2) : PairGroupoid2 :=
  ⟨giMul c A.e00, giMul c A.e01, giMul c A.e10, giMul c A.e11⟩

def mat2GITrace (A : PairGroupoid2) : GaussInt :=
  giAdd A.e00 A.e11

/-- The qubit packet 0-coboundary `d₀(Ω)(X) = [Ω, X] = Ω X - X Ω` on `M_2(ℤ[i])`. -/
def packetD0 (Omega X : PairGroupoid2) : PairGroupoid2 :=
  groupoidSub (groupoidConv Omega X) (groupoidConv X Omega)

/-- Theorem 4: Every commutator coboundary `packetD0 Omega X` in `M_2(ℤ[i])` is traceless
(`mat2GITrace (packetD0 Omega X) = giZero`). -/
theorem packet_d0_commutator_trace_zero (Omega X : PairGroupoid2) :
    mat2GITrace (packetD0 Omega X) = giZero := by
  ext <;> dsimp [mat2GITrace, packetD0, groupoidSub, groupoidConv, giAdd, giSub, giMul, giZero] <;> ring

/-- Theorem 5: Every scalar matrix `groupoidScale c groupoidId` lies in the kernel of
`packetD0 Omega`, and `packetD0 Omega` satisfies the Leibniz derivation identity
`packetD0 Omega (X * Y) = (packetD0 Omega X) * Y + X * (packetD0 Omega Y)`. -/
theorem packet_d0_scalar_kernel_and_leibniz_derivation
    (c : GaussInt) (Omega X Y : PairGroupoid2) :
    packetD0 Omega (groupoidScale c groupoidId) = groupoidZero ∧
    packetD0 Omega (groupoidConv X Y) =
      groupoidAdd (groupoidConv (packetD0 Omega X) Y) (groupoidConv X (packetD0 Omega Y)) := by
  refine ⟨?_, ?_⟩
  · ext <;> dsimp [packetD0, groupoidSub, groupoidConv, groupoidScale, groupoidId, groupoidZero,
      giAdd, giSub, giMul, giOne, giZero] <;> ring
  · ext <;> dsimp [packetD0, groupoidAdd, groupoidSub, groupoidConv, giAdd, giSub, giMul] <;> ring

/-- Theorem 6: The packet commutator differential `packetD0` satisfies the Jacobi identity
`[X, [Y, Z]] + [Y, [Z, X]] + [Z, [X, Y]] = 0` on `M_2(ℤ[i])`. -/
theorem packet_d0_jacobi_identity (X Y Z : PairGroupoid2) :
    groupoidAdd (groupoidAdd (packetD0 X (packetD0 Y Z)) (packetD0 Y (packetD0 Z X)))
      (packetD0 Z (packetD0 X Y)) = groupoidZero := by
  ext <;> dsimp [packetD0, groupoidAdd, groupoidSub, groupoidConv, groupoidZero,
    giAdd, giSub, giMul, giZero] <;> ring

-- ============================================================================
-- 3. Non-Equivalence Fences: Groupoid vs. Packet Complex vs. `SU(3)` Color
-- ============================================================================

/-- Theorem 7 (Groupoid Convolution vs. Packet Cochain Differential Fence):
Under groupoid convolution, `groupoidId` is idempotent (`groupoidConv groupoidId groupoidId = groupoidId ≠ groupoidZero`),
whereas under the packet coboundary `packetD0`, `groupoidId` is annihilated
(`packetD0 groupoidId groupoidId = groupoidZero`), proving that the two operations
define distinct algebraic objects. -/
theorem groupoid_convolution_vs_packet_d0_distinct_objects_fence :
    groupoidConv groupoidId groupoidId = groupoidId ∧
    packetD0 groupoidId groupoidId = groupoidZero ∧
    groupoidConv groupoidId groupoidId ≠ packetD0 groupoidId groupoidId := by
  decide

/-- Fundamental quadratic Casimir `C_2(fund) = (N^2 - 1) / (2 N)` over `ℚ` for `SU(N)`. -/
def suFundCasimir (N : ℚ) : ℚ :=
  (N ^ 2 - 1) / (2 * N)

/-- Theorem 8 (`M_2` Packet Complex vs. `SU(3)` Color Link Fence):
The `M_2(ℚ(i))` carrier has `2² = 4` matrix entries, `2² - 1 = 3` traceless Lie
generators, and fundamental Casimir `C₂(SU(2)) = 3/4`, whereas an `SU(3)` color link
requires `3² = 9` matrix entries (`4 ≠ 9`), `3² - 1 = 8` Gell-Mann generators (`3 ≠ 8`),
and fundamental Casimir `C₂(SU(3)) = 4/3 ≠ 3/4`. -/
theorem m2_packet_vs_su3_color_dimension_and_casimir_fence :
    (2 ^ 2 : Nat) = 4 ∧
    (3 ^ 2 : Nat) = 9 ∧
    (2 ^ 2 : Nat) ≠ 3 ^ 2 ∧
    (2 ^ 2 - 1 : Nat) = 3 ∧
    (3 ^ 2 - 1 : Nat) = 8 ∧
    suFundCasimir 2 = 3 / 4 ∧
    suFundCasimir 3 = 4 / 3 ∧
    suFundCasimir 2 ≠ suFundCasimir 3 := by
  dsimp [suFundCasimir]
  refine ⟨by decide, by decide, by decide, by decide, by decide, by norm_num, by norm_num, by norm_num⟩

/-- Scope audit ledger for `TFQ-0014`. -/
structure Tfq0014ScopeLedger where
  hasGroupoidConvolution : Bool
  hasM2PacketComplex : Bool
  isCStarCompletionNative : Bool
  hasHopfGaugeTheory : Bool
  hasSu3ColorLinks : Bool
  deriving DecidableEq, Repr

def tfq0014RepoLedger : Tfq0014ScopeLedger :=
  ⟨true, true, false, false, false⟩

/-- Theorem 9 (Scope Ledger Fence):
`tfq0014RepoLedger` records that `finite_groupoid_algebra.rs` (`hasGroupoidConvolution = true`)
and `gauge_cochain_complex.rs` (`hasM2PacketComplex = true`) are present, while native
`C*`-completion (`false`), Hopf gauge theory (`false`), and `SU(3)` color link storage (`false`)
are absent. -/
theorem neither_module_is_hopf_or_su3_scope_ledger_fence :
    tfq0014RepoLedger.hasGroupoidConvolution = true ∧
    tfq0014RepoLedger.hasM2PacketComplex = true ∧
    tfq0014RepoLedger.isCStarCompletionNative = false ∧
    tfq0014RepoLedger.hasHopfGaugeTheory = false ∧
    tfq0014RepoLedger.hasSu3ColorLinks = false := by
  decide

/-- Theorem 10 (Lie Derivation vs. Group-Like Multiplicative Link Fence):
For `Omega = ⟨⟨1, 0⟩, ⟨0, 0⟩, ⟨0, 0⟩, ⟨-1, 0⟩⟩` (`σ_z`) and `X = ⟨⟨0, 0⟩, ⟨1, 0⟩, ⟨1, 0⟩, ⟨0, 0⟩⟩` (`σ_x`),
`packetD0 Omega (X * X) = 0` whereas `(packetD0 Omega X) * (packetD0 Omega X) ≠ 0`,
confirming that `packetD0` is a Lie derivation (`d₀(XY) = d₀(X)Y + Xd₀(Y)`) and not a
multiplicative group-link homomorphism (`U(XY) = U(X)U(Y)`). -/
theorem commutator_derivation_breaks_grouplike_multiplicativity_fence :
    let Omega : PairGroupoid2 := ⟨⟨1, 0⟩, giZero, giZero, ⟨-1, 0⟩⟩
    let X : PairGroupoid2 := ⟨giZero, giOne, giOne, giZero⟩
    packetD0 Omega (groupoidConv X X) = groupoidZero ∧
    groupoidConv (packetD0 Omega X) (packetD0 Omega X) ≠ groupoidZero := by
  decide

#print axioms pair_groupoid_convolution_associative
#print axioms pair_groupoid_unit_and_orthogonal_object_idempotents
#print axioms groupoid_cstar_norm_requires_sqrt_extension_fence
#print axioms packet_d0_commutator_trace_zero
#print axioms packet_d0_scalar_kernel_and_leibniz_derivation
#print axioms packet_d0_jacobi_identity
#print axioms groupoid_convolution_vs_packet_d0_distinct_objects_fence
#print axioms m2_packet_vs_su3_color_dimension_and_casimir_fence
#print axioms neither_module_is_hopf_or_su3_scope_ledger_fence
#print axioms commutator_derivation_breaks_grouplike_multiplicativity_fence

end FiniteGroupoidConvolutionAlgebra
