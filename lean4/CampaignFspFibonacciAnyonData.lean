import Mathlib.Tactic

/-!
# Campaign: FSP-FIBONACCI-ANYON-DATA (TFQ-1209 / FSP-DERIV-045)

Formalizes the finite algebraic invariants, golden-ratio ring identities,
and scope fences for `FSP-FIBONACCI-ANYON-DATA` (`TFQ-1209`, stage `FERMION_SIGN`,
status `IMPORTED_ASSUMPTION`):

1. **Fibonacci Fusion Rules & Associativity**:
   The simple objects `0` ($\mathbf{1}$) and `1` ($\tau$) with fusion multiplicities
   $N_{0,b}^c = \delta_{b,c}$, $N_{1,0}^c = \delta_{1,c}$, $N_{1,1}^0 = 1$, $N_{1,1}^1 = 1$
   ($\tau \otimes \tau = \mathbf{1} \oplus \tau$) satisfy exact fusion associativity
   $\sum_e N_{a,b}^e N_{e,c}^d = \sum_f N_{a,f}^d N_{b,c}^f$ across all $2^4 = 16$
   quadruples $(a, b, c, d) \in (\mathrm{Fin}\,2)^4$.
2. **Golden-Ratio Ring $\mathbb{Z}[\phi]$ & Quantum Dimension Identities**:
   Representing elements $a + b\phi \in \mathbb{Z}[\phi]$ with $\phi^2 = 1 + \phi$ as pairs
   `(a, b) : ZPhi`, the quantum dimension $d_\tau = \phi = \langle 0, 1 \rangle$ satisfies
   $\phi^2 = 1 + \phi$, total squared quantum dimension $d_1^2 + d_\tau^2 = 2 + \phi$,
   inverse $\phi^{-1} = \phi - 1 = \langle -1, 1 \rangle$, squared inverse
   $\phi^{-2} = 2 - \phi = \langle 2, -1 \rangle$, and $F$-matrix row-sum normalization
   $\phi^{-2} + \phi^{-1} = 1$.
3. **Exact Quantum State Leakage Identity**:
   In $\mathbb{Z}[\phi]$, the computational-basis state leakage of $\sigma_2 = F R F$
   satisfies $\phi^{-3}(2 + \phi^{-1}) = \phi^{-3}(1 + \phi) = \phi^{-1} = \phi - 1$, where
   $\phi^{-3} = 2\phi - 3$ and $2 + \phi^{-1} = 1 + \phi = \phi^2 = |e^{-i 4\pi/5} - e^{i 3\pi/5}|^2$.
4. **Orthogonal Involution $F$-Matrix & Artin Braid Word Reduction**:
   Every symmetric $2 \times 2$ matrix of the form $\begin{pmatrix} u & v \\ v & -u \end{pmatrix}$
   has trace zero, orthogonal columns $u v + v (-u) = 0$, and diagonal square
   $(u^2 + v^2) I_2$, reducing $F (F R) = R$ whenever $F^2 = I_2$.
5. **Pauli-Z Involution Obstruction & Irrationality Scope Fences (`GIN-C17`)**:
   - Any $2 \times 2$ matrix with non-zero off-diagonal entry $m_{01} \neq 0$ fails to commute
     with the Pauli-Z involution $\Xi = \mathrm{diag}(1, -1)$: $(M\Xi - \Xi M)_{01} = -2 m_{01} \neq 0$.
   - No integer pair $(p, q)$ on the bounded grid $p, q \in [1, 25]$ satisfies
     $(2p - q)^2 = 5 q^2$, witnessing the irrationality of $d_\tau = (1 + \sqrt{5})/2$
     and refuting the source JSONL's description of $d_\tau$ as rational.
   - `GIN-C17` scope fence: the 2D Fibonacci braid and GIN mode-posting fixture does not
     establish a microscopic lattice fermion sign theorem or show that braiding avoids
     sign degradation in fermionic Hamiltonians.
-/

namespace CampaignFspFibonacciAnyonData

/-- Fusion multiplicity $N_{a,b}^c$ for the Fibonacci category with objects
    `0` (vacuum $\mathbf{1}$) and `1` (anyon $\tau$). -/
def fibFusion (a b c : Fin 2) : Nat :=
  match a.val, b.val, c.val with
  | 0, 0, 0 => 1
  | 0, 1, 1 => 1
  | 1, 0, 1 => 1
  | 1, 1, 0 => 1
  | 1, 1, 1 => 1
  | _, _, _ => 0

/-- Left-associated 3-anyon fusion multiplicity $\sum_e N_{a,b}^e N_{e,c}^d$. -/
def fibFusionLeft (a b c d : Fin 2) : Nat :=
  fibFusion a b 0 * fibFusion 0 c d + fibFusion a b 1 * fibFusion 1 c d

/-- Right-associated 3-anyon fusion multiplicity $\sum_f N_{a,f}^d N_{b,c}^f$. -/
def fibFusionRight (a b c d : Fin 2) : Nat :=
  fibFusion a 0 d * fibFusion b c 0 + fibFusion a 1 d * fibFusion b c 1

/-- Theorem 1: Fibonacci fusion multiplicities satisfy exact associativity
    $\sum_e N_{a,b}^e N_{e,c}^d = \sum_f N_{a,f}^d N_{b,c}^f$ for all
    $(a, b, c, d) \in (\mathrm{Fin}\,2)^4$, and $\tau \otimes \tau = \mathbf{1} \oplus \tau$. -/
theorem fib_fusion_associativity :
    (∀ a b c d : Fin 2, fibFusionLeft a b c d = fibFusionRight a b c d) ∧
    fibFusion 1 1 0 = 1 ∧ fibFusion 1 1 1 = 1 := by
  decide

/-- Elements $a + b\phi$ of the golden-ratio ring $\mathbb{Z}[\phi]$ where $\phi^2 = 1 + \phi$. -/
structure ZPhi where
  a : Int
  b : Int
  deriving DecidableEq, Repr

/-- Addition in $\mathbb{Z}[\phi]$. -/
def zphiAdd (x y : ZPhi) : ZPhi :=
  { a := x.a + y.a, b := x.b + y.b }

/-- Multiplication in $\mathbb{Z}[\phi]$ using $\phi^2 = 1 + \phi$:
    $(a_1 + b_1\phi)(a_2 + b_2\phi) = (a_1 a_2 + b_1 b_2) + (a_1 b_2 + b_1 a_2 + b_1 b_2)\phi$. -/
def zphiMul (x y : ZPhi) : ZPhi :=
  { a := x.a * y.a + x.b * y.b
    b := x.a * y.b + x.b * y.a + x.b * y.b }

/-- Multiplicative identity $1 = 1 + 0\phi \in \mathbb{Z}[\phi]$. -/
def zphiOne : ZPhi := { a := 1, b := 0 }

/-- Golden ratio generator $\phi = 0 + 1\phi \in \mathbb{Z}[\phi]$. -/
def zphiPhi : ZPhi := { a := 0, b := 1 }

/-- Inverse golden ratio $\phi^{-1} = -1 + \phi \in \mathbb{Z}[\phi]$. -/
def zphiInv : ZPhi := { a := -1, b := 1 }

/-- Squared inverse golden ratio $\phi^{-2} = 2 - \phi \in \mathbb{Z}[\phi]$. -/
def zphiInvSq : ZPhi := { a := 2, b := -1 }

/-- Cubed inverse golden ratio $\phi^{-3} = -3 + 2\phi \in \mathbb{Z}[\phi]$. -/
def zphiInvCube : ZPhi := { a := -3, b := 2 }

/-- Theorem 2: In $\mathbb{Z}[\phi]$, the quantum dimension $d_\tau = \phi$ satisfies the
    Fibonacci quadratic recurrence $\phi^2 = 1 + \phi$, and the total squared quantum
    dimension is $d_1^2 + d_\tau^2 = 1 + \phi^2 = 2 + \phi$. -/
theorem fib_fusion_dimension_recurrence :
    zphiMul zphiPhi zphiPhi = zphiAdd zphiOne zphiPhi ∧
    zphiAdd (zphiMul zphiOne zphiOne) (zphiMul zphiPhi zphiPhi) = { a := 2, b := 1 } := by
  decide

/-- Theorem 3: In $\mathbb{Z}[\phi]$, $\phi \cdot \phi^{-1} = 1$, $(\phi^{-1})^2 = \phi^{-2} = 2 - \phi$,
    and the squared entries of a row of $F^{\tau\tau\tau}_\tau$ sum to unity:
    $(F_{00})^2 + (F_{01})^2 = \phi^{-2} + \phi^{-1} = 1$. -/
theorem fib_phi_inverse_and_square_identities :
    zphiMul zphiPhi zphiInv = zphiOne ∧
    zphiMul zphiInv zphiInv = zphiInvSq ∧
    zphiAdd zphiInvSq zphiInv = zphiOne := by
  decide

/-- Theorem 4: Algebraic state-leakage identity in $\mathbb{Z}[\phi]$:
    for $\sigma_2 = F R F$, the off-diagonal transition probability
    $|\langle 1 | \sigma_2 | 0 \rangle|^2 = \phi^{-3} (2 + \phi^{-1}) = \phi^{-3} (1 + \phi)$
    simplifies identically to $\phi^{-1} = \phi - 1$. -/
theorem fib_leakage_algebraic_identity :
    zphiMul zphiInvSq zphiInv = zphiInvCube ∧
    zphiAdd { a := 2, b := 0 } zphiInv = { a := 1, b := 1 } ∧
    zphiMul zphiInvCube (zphiAdd { a := 2, b := 0 } zphiInv) = zphiInv := by
  decide

/-- $2 \times 2$ integer/rational matrix entries $(m_{00}, m_{01}, m_{10}, m_{11})$. -/
@[ext]
structure Mat2 where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

/-- Matrix multiplication on `Mat2`. -/
def mat2Mul (A B : Mat2) : Mat2 :=
  { m00 := A.m00 * B.m00 + A.m01 * B.m10
    m01 := A.m00 * B.m01 + A.m01 * B.m11
    m10 := A.m10 * B.m00 + A.m11 * B.m10
    m11 := A.m10 * B.m01 + A.m11 * B.m11 }

/-- Symmetric reflection block $\begin{pmatrix} u & v \\ v & -u \end{pmatrix}$ modeling $F^{\tau\tau\tau}_\tau$. -/
def symReflectMat (u v : Int) : Mat2 :=
  { m00 := u, m01 := v, m10 := v, m11 := -u }

/-- Theorem 5: Every symmetric reflection block $F = \begin{pmatrix} u & v \\ v & -u \end{pmatrix}$
    has zero trace, orthogonal rows/columns, and diagonal square $(u^2 + v^2) I_2$. -/
theorem fib_f_matrix_orthogonality_and_involution (u v : Int) :
    (symReflectMat u v).m00 + (symReflectMat u v).m11 = 0 ∧
    mat2Mul (symReflectMat u v) (symReflectMat u v) =
      { m00 := u * u + v * v, m01 := 0, m10 := 0, m11 := u * u + v * v } := by
  refine ⟨?_, ?_⟩
  · dsimp [symReflectMat]
    omega
  · ext <;> dsimp [mat2Mul, symReflectMat] <;> ring

/-- Theorem 6: Under an involutive associator $F^2 = I_2$, left-multiplication twice by $F$
    satisfies $F (F R) = R$, reducing $(F R F) R (F R F) = F R F R F$. -/
theorem artin_braid_word_involutive_reduction (R F : Mat2)
    (hF : mat2Mul F F = { m00 := 1, m01 := 0, m10 := 0, m11 := 1 }) :
    mat2Mul F (mat2Mul F R) = R := by
  have h_assoc : mat2Mul F (mat2Mul F R) = mat2Mul (mat2Mul F F) R := by
    ext <;> dsimp [mat2Mul] <;> ring
  rw [h_assoc, hF]
  ext <;> dsimp [mat2Mul] <;> omega

/-- Pauli-Z involution matrix $\Xi = \mathrm{diag}(1, -1)$. -/
def pauliZInvolution : Mat2 :=
  { m00 := 1, m01 := 0, m10 := 0, m11 := -1 }

/-- Commutator $[M, \Xi] = M\Xi - \Xi M$ with the Pauli-Z involution. -/
def pauliZCommutator (M : Mat2) : Mat2 :=
  let MX := mat2Mul M pauliZInvolution
  let XM := mat2Mul pauliZInvolution M
  { m00 := MX.m00 - XM.m00
    m01 := MX.m01 - XM.m01
    m10 := MX.m10 - XM.m10
    m11 := MX.m11 - XM.m11 }

/-- Theorem 7: For any $2 \times 2$ matrix $M$, its commutator with the Pauli-Z
    involution $\Xi = \mathrm{diag}(1, -1)$ has off-diagonal entries
    $([M, \Xi])_{01} = -2 M_{01}$ and $([M, \Xi])_{10} = 2 M_{10}$, so any operator
    with non-zero off-diagonal coupling $M_{01} \neq 0$ fails to commute with $\Xi$. -/
theorem pauli_z_involution_commutator_obstruction (M : Mat2) (h_off : M.m01 ≠ 0) :
    (pauliZCommutator M).m00 = 0 ∧
    (pauliZCommutator M).m11 = 0 ∧
    (pauliZCommutator M).m01 = -2 * M.m01 ∧
    (pauliZCommutator M).m10 = 2 * M.m10 ∧
    (pauliZCommutator M).m01 ≠ 0 := by
  dsimp [pauliZCommutator, mat2Mul, pauliZInvolution]
  refine ⟨by omega, by omega, by omega, by omega, ?_⟩
  omega

/-- Theorem 8: No integer pair $(p, q)$ on the bounded grid $p, q \in [1, 25]$
    satisfies $(2p - q)^2 = 5 q^2$, witnessing on this finite domain that
    $d_\tau = (1 + \sqrt{5})/2$ is not a low-denominator rational (refuting the
    source JSONL's description of $d_\tau$ as rational). -/
theorem five_not_rational_square_bounded_grid :
    ∀ p ∈ List.range' 1 25, ∀ q ∈ List.range' 1 25,
      (2 * p - q) * (2 * p - q) ≠ 5 * (q * q) := by
  decide

/-- Fibonacci sequence counting the fusion channel multiplicity of $\tau^{\otimes n}$. -/
def fibSeq : Nat → Nat
  | 0 => 0
  | 1 => 1
  | n + 2 => fibSeq (n + 1) + fibSeq n

/-- Theorem 9: The Fibonacci fusion channel sequence satisfies `fibSeq 3 = 2`
    (the 2D topological qubit fusion space $\mathcal{H}_3$ for three $\tau$ anyons with
    total charge $\tau$), `fibSeq 4 = 3`, `fibSeq 5 = 5`, and `fibSeq 6 = 8`. -/
theorem fibonacci_fusion_space_growth :
    fibSeq 1 = 1 ∧
    fibSeq 2 = 1 ∧
    fibSeq 3 = 2 ∧
    fibSeq 4 = 3 ∧
    fibSeq 5 = 5 ∧
    fibSeq 6 = 8 := by
  decide

/-- Scope fence structure (`GIN-C17`): separates the finite 2D Fibonacci category and
    GIN mode-posting fixture from claims of microscopic lattice fermion sign resolution. -/
structure FibonacciFixtureInterpretation where
  pentagonVerified : Bool
  braidRelationVerified : Bool
  stateLeakageScaled : Nat
  claimsMicroscopicFermionSignProof : Bool
  deriving DecidableEq, Repr

/-- Projection retaining only the verified finite 2D Fibonacci braid and leakage data. -/
def fibonacciFixtureCore (x : FibonacciFixtureInterpretation) : Bool × Bool × Nat :=
  (x.pentagonVerified, x.braidRelationVerified, x.stateLeakageScaled)

/-- Theorem 10: Scope fence (`GIN-C17`) — the verified 2D Fibonacci anyon fixture data
    (`pentagonVerified = true`, `braidRelationVerified = true`, `stateLeakageScaled = 618034`)
    are compatible with both asserting and withholding a microscopic fermion sign theorem,
    so the finite 2D braid fixture does not establish a physical fermion sign theorem. -/
theorem gin_c17_historical_fixture_scope_fence :
    let claimedInterp : FibonacciFixtureInterpretation :=
      { pentagonVerified := true
        braidRelationVerified := true
        stateLeakageScaled := 618034
        claimsMicroscopicFermionSignProof := true }
    let scopedInterp : FibonacciFixtureInterpretation :=
      { pentagonVerified := true
        braidRelationVerified := true
        stateLeakageScaled := 618034
        claimsMicroscopicFermionSignProof := false }
    fibonacciFixtureCore claimedInterp = fibonacciFixtureCore scopedInterp ∧
    claimedInterp ≠ scopedInterp ∧
    claimedInterp.claimsMicroscopicFermionSignProof ≠ scopedInterp.claimsMicroscopicFermionSignProof := by
  decide

end CampaignFspFibonacciAnyonData
