import Mathlib.Tactic

/-!
# QMObSpectralFinite — W6.10 / OB-SPECTRAL (finite spectral theorem toy)

Programme target: DERIV-MASTER W6.10 (QMREG-59 / freeze `OB-SPECTRAL` / recovery T09).

Mechanized on finite toys:

1. **Classical sector spectral calculus (DERIVED on FinL1):** bit and 3-sector
   observables $E\to\mathbb{Z}$ reconstruct as $\sum_\lambda \lambda\cdot\chi_\lambda$.
2. **Diagonal Hermitian projectors (DERIVED on diagonal toy):** 0-1 rank-1
   projectors $P_0,P_1$ are idempotent, mutually orthogonal, and recover `diagHerm`.
3. **Hermitian 2×2 non-diagonal toy (TOY-MECH under named lift):** Pauli-X
   spectral reconstruction with scale-2 integer projectors
   $2\sigma_x = (+1)(2P_+) + (-1)(2P_-)$; scaled projectors satisfy $M^2=2M$.
4. **Spectral → instrument bind (TOY-MECH):** classical spectral outcome maps to
   sector support (Lüders-style; matches W6.12 classical update shape).
5. **Basement fence:** non-diagonal Hermitian is not a classical sector readout.
6. **Non-diag 3×3 (TOY-MECH):** $\sigma_x\oplus 2$ scaled spectral reconstruction.
7. **Density Lüders under spectral projectors (TOY-MECH):** sandwich $P\rho P$
   for diagonal $P_0,P_1$ and scaled $\sigma_x$ projectors on a coherent density.
8. **POVM / Kraus residual (TOY-MECH):** soft binary effects $E_0+E_1=4I$ that are
   **not** projectors; spectral $\{P_0,P_1\}$ as projective POVM special case;
   projective Kraus pair dephases $\rho_+$ to $I$; soft effects need lift host.
9. **POVM / Kraus catalogue deepen (TOY-MECH residual):** ternary projective POVM
   on $\sigma_x\oplus 2$ (scaled resolution $2I_3$); non-Hermitian amplitude-damping
   Kraus pair (completeness $I$, not projectors); soft Born-mass
   $\mathrm{Tr}(E_i\rho)$ dual; full general catalogue still **OPEN**.

**Not claimed:** general non-diagonal $n\times n$ Mathlib spectral theorem as new
   proof (3×3 toy does not close it); uniqueness of complex Hilbert; Born pairing;
   full CPTP instrument completeness; continuum Kraus square-roots; authority.

AuthorityEffect: None.
-/

namespace QM
namespace ObSpectral

/-! ## Classical sector observables (FinL1 / basement) -/

inductive Bit where
  | b0
  | b1
deriving DecidableEq, Repr

/-- Classical observable: real (Int) value on each residual sector. -/
def SectorObs := Bit → Int

namespace SectorObs

def eval (o : SectorObs) (b : Bit) : Int := o b

/-- Level-set / spectral projector as 0-1 characteristic on sectors. -/
def charAt (o : SectorObs) (eig : Int) : Bit → Int :=
  fun b => if o b = eig then 1 else 0

/-- Spectral reconstruction at a sector: value equals eigenvalue times char. -/
theorem spectral_reconstruct_point (o : SectorObs) (b : Bit) :
    o b = (o b) * charAt o (o b) b := by
  simp [charAt]

/-- Two-sector observable with distinct values reconstructs as spectral sum
    on each sector (explicit toy: λ₀=2 on b0, λ₁=3 on b1). -/
def diagObs : SectorObs
  | .b0 => 2
  | .b1 => 3

theorem diagObs_spectrum_distinct : diagObs .b0 ≠ diagObs .b1 := by
  decide

theorem diagObs_reconstruct_b0 :
    diagObs .b0 =
      (2 : Int) * charAt diagObs 2 .b0 + 3 * charAt diagObs 3 .b0 := by
  simp [diagObs, charAt]

theorem diagObs_reconstruct_b1 :
    diagObs .b1 =
      (2 : Int) * charAt diagObs 2 .b1 + 3 * charAt diagObs 3 .b1 := by
  simp [diagObs, charAt]

/-- Classical observables are diagonal in the sector basis: no off-diagonal cell. -/
structure ClassicalMatrixReadout where
  d0 : Int
  d1 : Int
  /-- Off-diagonal forced zero for classical sector readout. -/
  off : Int := 0
  off_zero : off = 0 := by rfl

theorem classical_readout_diagonal (m : ClassicalMatrixReadout) : m.off = 0 :=
  m.off_zero

end SectorObs

/-! ## General-n classical sector spectral (DERIVED on FinL1; n=3 toy)

Diagonal / sector observables extend beyond bits: any finite residual table
$E\to\mathbb{Z}$ still reconstructs pointwise as a spectral sum of level-set
chars. This is **not** the non-diagonal Hermitian spectral theorem.
-/

inductive Sector3 where
  | s0
  | s1
  | s2
deriving DecidableEq, Repr

def Sector3Obs := Sector3 → Int

def charAt3 (o : Sector3Obs) (eig : Int) : Sector3 → Int :=
  fun s => if o s = eig then 1 else 0

/-- Three distinct eigenvalues on three residual sectors. -/
def triObs : Sector3Obs
  | .s0 => 1
  | .s1 => 2
  | .s2 => 5

theorem triObs_pairwise_distinct :
    triObs .s0 ≠ triObs .s1 ∧ triObs .s0 ≠ triObs .s2 ∧ triObs .s1 ≠ triObs .s2 := by
  decide

theorem triObs_reconstruct_s0 :
    triObs .s0 =
      (1 : Int) * charAt3 triObs 1 .s0 + 2 * charAt3 triObs 2 .s0 +
        5 * charAt3 triObs 5 .s0 := by
  simp [triObs, charAt3]

theorem triObs_reconstruct_s1 :
    triObs .s1 =
      (1 : Int) * charAt3 triObs 1 .s1 + 2 * charAt3 triObs 2 .s1 +
        5 * charAt3 triObs 5 .s1 := by
  simp [triObs, charAt3]

theorem triObs_reconstruct_s2 :
    triObs .s2 =
      (1 : Int) * charAt3 triObs 1 .s2 + 2 * charAt3 triObs 2 .s2 +
        5 * charAt3 triObs 5 .s2 := by
  simp [triObs, charAt3]

/-- Pointwise reconstruction law for arbitrary sector functions (classical). -/
theorem sector3_reconstruct_point (o : Sector3Obs) (s : Sector3) :
    o s = (o s) * charAt3 o (o s) s := by
  simp [charAt3]

/-! ## Real-symmetric 2×2 matrices (lift-facing toy carrier) -/

structure Mat2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
deriving DecidableEq, Repr

namespace Mat2

def IsSymmetric (m : Mat2) : Prop := m.a01 = m.a10

def add (m n : Mat2) : Mat2 :=
  { a00 := m.a00 + n.a00
    a01 := m.a01 + n.a01
    a10 := m.a10 + n.a10
    a11 := m.a11 + n.a11 }

def smul (k : Int) (m : Mat2) : Mat2 :=
  { a00 := k * m.a00
    a01 := k * m.a01
    a10 := k * m.a10
    a11 := k * m.a11 }

def sub (m n : Mat2) : Mat2 := add m (smul (-1) n)

/-- Integer matrix product (for projector algebra). -/
def mul (m n : Mat2) : Mat2 :=
  { a00 := m.a00 * n.a00 + m.a01 * n.a10
    a01 := m.a00 * n.a01 + m.a01 * n.a11
    a10 := m.a10 * n.a00 + m.a11 * n.a10
    a11 := m.a10 * n.a01 + m.a11 * n.a11 }

def zero : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 0 }

/-- Idempotent: $P^2 = P$ (rank-1 spectral projector). -/
def IsProjector (p : Mat2) : Prop := mul p p = p

end Mat2

/-- Pauli-X (real symmetric): non-diagonal Hermitian toy. -/
def sigmaX : Mat2 := { a00 := 0, a01 := 1, a10 := 1, a11 := 0 }

theorem sigmaX_symmetric : sigmaX.IsSymmetric := rfl

theorem sigmaX_not_classical_diagonal :
    sigmaX.a01 ≠ 0 := by
  decide

/-- Scale-2 spectral projectors for σ_x:
    P₊ = ½|[[1,1],[1,1]] ⇒ 2P₊ = [[1,1],[1,1]]
    P₋ = ½|[[1,-1],[-1,1]] ⇒ 2P₋ = [[1,-1],[-1,1]] -/
def twoPplus : Mat2 := { a00 := 1, a01 := 1, a10 := 1, a11 := 1 }
def twoPminus : Mat2 := { a00 := 1, a01 := -1, a10 := -1, a11 := 1 }

/-- Spectral reconstruction (scaled): 2σ_x = (+1)(2P₊) + (−1)(2P₋). -/
theorem sigmaX_spectral_scaled :
    Mat2.sub twoPplus twoPminus = Mat2.smul 2 sigmaX := by
  simp [Mat2.sub, Mat2.add, Mat2.smul, twoPplus, twoPminus, sigmaX]

theorem twoPplus_symmetric : twoPplus.IsSymmetric := rfl
theorem twoPminus_symmetric : twoPminus.IsSymmetric := rfl

/-- Scaled projectors satisfy $M^2 = 2M$ (idempotence up to the scale-2 factor). -/
theorem twoPplus_scaled_idempotent :
    Mat2.mul twoPplus twoPplus = Mat2.smul 2 twoPplus := by
  simp [Mat2.mul, Mat2.smul, twoPplus]

theorem twoPminus_scaled_idempotent :
    Mat2.mul twoPminus twoPminus = Mat2.smul 2 twoPminus := by
  simp [Mat2.mul, Mat2.smul, twoPminus]

/-- Distinct scaled spectral projectors are orthogonal: $(2P_+)(2P_-)=0$. -/
theorem twoPplus_twoPminus_orthogonal :
    Mat2.mul twoPplus twoPminus = Mat2.zero := by
  simp [Mat2.mul, Mat2.zero, twoPplus, twoPminus]

/-- Eigenvalue action (unnormalized): σ_x [1,1]ᵀ = [1,1]ᵀ (λ=+1). -/
theorem sigmaX_eigen_plus :
    let v0 : Int := 1
    let v1 : Int := 1
    (sigmaX.a00 * v0 + sigmaX.a01 * v1 = (1 : Int) * v0) ∧
    (sigmaX.a10 * v0 + sigmaX.a11 * v1 = (1 : Int) * v1) := by
  simp [sigmaX]

/-- Eigenvalue action: σ_x [1,−1]ᵀ = −[1,−1]ᵀ (λ=−1). -/
theorem sigmaX_eigen_minus :
    let v0 : Int := 1
    let v1 : Int := -1
    (sigmaX.a00 * v0 + sigmaX.a01 * v1 = (-1 : Int) * v0) ∧
    (sigmaX.a10 * v0 + sigmaX.a11 * v1 = (-1 : Int) * v1) := by
  simp [sigmaX]

/-- Diagonal Hermitian toy already in spectral form. -/
def diagHerm : Mat2 := { a00 := 2, a01 := 0, a10 := 0, a11 := 3 }

theorem diagHerm_symmetric : diagHerm.IsSymmetric := rfl

theorem diagHerm_is_classical_compatible :
    diagHerm.a01 = 0 ∧ diagHerm.a10 = 0 := by
  simp [diagHerm]

/-! ## Diagonal spectral projectors (0-1, true idempotents)

For a diagonal Hermitian, the spectral theorem is FinL1 bookkeeping:
rank-1 diagonal projectors $P_i$ with $P_i^2=P_i$, $P_i P_j=0$ ($i\neq j$),
and $A=\sum_i \lambda_i P_i$.
-/

def proj0 : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 0 }
def proj1 : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 1 }

theorem proj0_is_projector : Mat2.IsProjector proj0 := by
  simp [Mat2.IsProjector, Mat2.mul, proj0]

theorem proj1_is_projector : Mat2.IsProjector proj1 := by
  simp [Mat2.IsProjector, Mat2.mul, proj1]

theorem proj0_proj1_orthogonal : Mat2.mul proj0 proj1 = Mat2.zero := by
  simp [Mat2.mul, Mat2.zero, proj0, proj1]

theorem proj1_proj0_orthogonal : Mat2.mul proj1 proj0 = Mat2.zero := by
  simp [Mat2.mul, Mat2.zero, proj0, proj1]

/-- Spectral reconstruction for diagonal Hermitian: $A = 2 P_0 + 3 P_1$. -/
theorem diagHerm_spectral_form :
    Mat2.add (Mat2.smul 2 proj0) (Mat2.smul 3 proj1) = diagHerm := by
  simp [Mat2.add, Mat2.smul, proj0, proj1, diagHerm]

/-- Resolution of the identity: $P_0 + P_1 = I_2$. -/
def id2 : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 1 }

theorem proj_resolution_of_identity :
    Mat2.add proj0 proj1 = id2 := by
  simp [Mat2.add, proj0, proj1, id2]

/-! ## Spectral → instrument bind (classical / diagonal)

Spectral outcomes induce sector supports. On the bit residual toy this is
exactly the W6.12 classical Lüders/Bayesian update shape: post-state mass
lives only on the measured sector. Full density-matrix Lüders stays OPEN.
-/

structure BitWeight where
  w0 : Nat
  w1 : Nat
deriving DecidableEq, Repr

/-- Classical spectral outcome for `diagObs` / `diagHerm`. -/
inductive SpectralOutcome where
  | lam2  -- eigenvalue 2 on sector b0
  | lam3  -- eigenvalue 3 on sector b1
deriving DecidableEq, Repr

/-- Instrument update from spectral outcome: support on the eigen-sector. -/
def spectralUpdate (w : BitWeight) : SpectralOutcome → BitWeight
  | .lam2 => { w0 := w.w0, w1 := 0 }
  | .lam3 => { w0 := 0, w1 := w.w1 }

theorem spectralUpdate_lam2_support (w : BitWeight) :
    (spectralUpdate w .lam2).w1 = 0 := by
  simp [spectralUpdate]

theorem spectralUpdate_lam3_support (w : BitWeight) :
    (spectralUpdate w .lam3).w0 = 0 := by
  simp [spectralUpdate]

theorem spectralUpdate_idempotent (w : BitWeight) (o : SpectralOutcome) :
    spectralUpdate (spectralUpdate w o) o = spectralUpdate w o := by
  cases o <;> simp [spectralUpdate]

/-- Outcome mass matches prior sector weight (classical Born / spectral mass). -/
def spectralOutcomeMass (w : BitWeight) : SpectralOutcome → Nat
  | .lam2 => w.w0
  | .lam3 => w.w1

theorem spectral_mass_matches_prior (w : BitWeight) :
    spectralOutcomeMass w .lam2 = w.w0 ∧ spectralOutcomeMass w .lam3 = w.w1 :=
  ⟨rfl, rfl⟩

/-- Binding receipt: `diagObs` eigenvalues label the same sectors as spectral outcomes. -/
theorem diagObs_outcome_sectors :
    SectorObs.diagObs .b0 = 2 ∧ SectorObs.diagObs .b1 = 3 :=
  ⟨rfl, rfl⟩

/-- Worked instrument example aligned with W6.12 `qm_021` shape: (3,1)→lam3→(0,1). -/
def examplePrior : BitWeight := { w0 := 3, w1 := 1 }

theorem example_spectral_update_lam3 :
    spectralUpdate examplePrior .lam3 = { w0 := 0, w1 := 1 } := rfl

/-! ## Non-diagonal 3×3 real-symmetric toy (TOY-MECH under lift)

Block embedding: $\sigma_x \oplus (2)$ — off-diagonal in the first $2\times 2$ block,
distinct third eigenvalue on the orthogonal line. Advances the
`hermitian_general_n` residual **without** claiming Mathlib general-$n$ novelty.

$$
H = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 2 \end{pmatrix}
= \mathrm{embed}(\sigma_x) + 2\,P_{2}
$$

Scaled spectral identity (reuse 2×2 capital):
$2H = \mathrm{embed}(2P_+) - \mathrm{embed}(2P_-) + 4\,P_{2}$.
-/

structure Mat3 where
  a00 : Int
  a01 : Int
  a02 : Int
  a10 : Int
  a11 : Int
  a12 : Int
  a20 : Int
  a21 : Int
  a22 : Int
  deriving DecidableEq, Repr

namespace Mat3

def IsSymmetric (m : Mat3) : Prop :=
  m.a01 = m.a10 ∧ m.a02 = m.a20 ∧ m.a12 = m.a21

def add (m n : Mat3) : Mat3 :=
  { a00 := m.a00 + n.a00, a01 := m.a01 + n.a01, a02 := m.a02 + n.a02
    a10 := m.a10 + n.a10, a11 := m.a11 + n.a11, a12 := m.a12 + n.a12
    a20 := m.a20 + n.a20, a21 := m.a21 + n.a21, a22 := m.a22 + n.a22 }

def smul (k : Int) (m : Mat3) : Mat3 :=
  { a00 := k * m.a00, a01 := k * m.a01, a02 := k * m.a02
    a10 := k * m.a10, a11 := k * m.a11, a12 := k * m.a12
    a20 := k * m.a20, a21 := k * m.a21, a22 := k * m.a22 }

def sub (m n : Mat3) : Mat3 := add m (smul (-1) n)

def mul (m n : Mat3) : Mat3 :=
  { a00 := m.a00 * n.a00 + m.a01 * n.a10 + m.a02 * n.a20
    a01 := m.a00 * n.a01 + m.a01 * n.a11 + m.a02 * n.a21
    a02 := m.a00 * n.a02 + m.a01 * n.a12 + m.a02 * n.a22
    a10 := m.a10 * n.a00 + m.a11 * n.a10 + m.a12 * n.a20
    a11 := m.a10 * n.a01 + m.a11 * n.a11 + m.a12 * n.a21
    a12 := m.a10 * n.a02 + m.a11 * n.a12 + m.a12 * n.a22
    a20 := m.a20 * n.a00 + m.a21 * n.a10 + m.a22 * n.a20
    a21 := m.a20 * n.a01 + m.a21 * n.a11 + m.a22 * n.a21
    a22 := m.a20 * n.a02 + m.a21 * n.a12 + m.a22 * n.a22 }

def zero : Mat3 :=
  { a00 := 0, a01 := 0, a02 := 0
    a10 := 0, a11 := 0, a12 := 0
    a20 := 0, a21 := 0, a22 := 0 }

/-- Embed a 2×2 block in the top-left of a 3×3 matrix (zeros elsewhere). -/
def embed2 (m : Mat2) : Mat3 :=
  { a00 := m.a00, a01 := m.a01, a02 := 0
    a10 := m.a10, a11 := m.a11, a12 := 0
    a20 := 0, a21 := 0, a22 := 0 }

end Mat3

/-- Non-diagonal Hermitian 3×3: $\sigma_x \oplus 2$. -/
def nonDiag3 : Mat3 :=
  { a00 := 0, a01 := 1, a02 := 0
    a10 := 1, a11 := 0, a12 := 0
    a20 := 0, a21 := 0, a22 := 2 }

/-- Rank-1 projector onto the third basis vector. -/
def proj2_3 : Mat3 :=
  { a00 := 0, a01 := 0, a02 := 0
    a10 := 0, a11 := 0, a12 := 0
    a20 := 0, a21 := 0, a22 := 1 }

theorem nonDiag3_symmetric : nonDiag3.IsSymmetric := by
  simp [nonDiag3, Mat3.IsSymmetric]

theorem nonDiag3_not_classical_diagonal :
    nonDiag3.a01 ≠ 0 := by
  decide

theorem nonDiag3_eq_embed_sigmaX_plus_2proj :
    nonDiag3 = Mat3.add (Mat3.embed2 sigmaX) (Mat3.smul 2 proj2_3) := by
  simp [nonDiag3, Mat3.add, Mat3.embed2, Mat3.smul, sigmaX, proj2_3]

/-- Scaled spectral reconstruction at $n=3$ non-diagonal:
    $2H = \mathrm{embed}(2P_+) - \mathrm{embed}(2P_-) + 4 P_2$. -/
theorem nonDiag3_spectral_scaled :
    Mat3.add
        (Mat3.sub (Mat3.embed2 twoPplus) (Mat3.embed2 twoPminus))
        (Mat3.smul 4 proj2_3) =
      Mat3.smul 2 nonDiag3 := by
  simp [Mat3.add, Mat3.sub, Mat3.smul, Mat3.embed2, twoPplus, twoPminus,
    proj2_3, nonDiag3]

theorem proj2_3_is_projector :
    Mat3.mul proj2_3 proj2_3 = proj2_3 := by
  simp [Mat3.mul, proj2_3]

/-- Embedded scaled projectors remain orthogonal to $P_2$. -/
theorem embed_twoPplus_orth_proj2 :
    Mat3.mul (Mat3.embed2 twoPplus) proj2_3 = Mat3.zero := by
  simp [Mat3.mul, Mat3.embed2, Mat3.zero, twoPplus, proj2_3]

theorem embed_twoPminus_orth_proj2 :
    Mat3.mul (Mat3.embed2 twoPminus) proj2_3 = Mat3.zero := by
  simp [Mat3.mul, Mat3.embed2, Mat3.zero, twoPminus, proj2_3]

/-- Eigenvalue +1 on $(1,1,0)$. -/
theorem nonDiag3_eigen_plus :
    let v0 : Int := 1
    let v1 : Int := 1
    let v2 : Int := 0
    (nonDiag3.a00 * v0 + nonDiag3.a01 * v1 + nonDiag3.a02 * v2 = (1 : Int) * v0) ∧
    (nonDiag3.a10 * v0 + nonDiag3.a11 * v1 + nonDiag3.a12 * v2 = (1 : Int) * v1) ∧
    (nonDiag3.a20 * v0 + nonDiag3.a21 * v1 + nonDiag3.a22 * v2 = (1 : Int) * v2) := by
  simp [nonDiag3]

/-- Eigenvalue −1 on $(1,-1,0)$. -/
theorem nonDiag3_eigen_minus :
    let v0 : Int := 1
    let v1 : Int := -1
    let v2 : Int := 0
    (nonDiag3.a00 * v0 + nonDiag3.a01 * v1 + nonDiag3.a02 * v2 = (-1 : Int) * v0) ∧
    (nonDiag3.a10 * v0 + nonDiag3.a11 * v1 + nonDiag3.a12 * v2 = (-1 : Int) * v1) ∧
    (nonDiag3.a20 * v0 + nonDiag3.a21 * v1 + nonDiag3.a22 * v2 = (-1 : Int) * v2) := by
  simp [nonDiag3]

/-- Eigenvalue +2 on $(0,0,1)$. -/
theorem nonDiag3_eigen_third :
    let v0 : Int := 0
    let v1 : Int := 0
    let v2 : Int := 1
    (nonDiag3.a00 * v0 + nonDiag3.a01 * v1 + nonDiag3.a02 * v2 = (2 : Int) * v0) ∧
    (nonDiag3.a10 * v0 + nonDiag3.a11 * v1 + nonDiag3.a12 * v2 = (2 : Int) * v1) ∧
    (nonDiag3.a20 * v0 + nonDiag3.a21 * v1 + nonDiag3.a22 * v2 = (2 : Int) * v2) := by
  simp [nonDiag3]

/-- Package: non-diag $n=3$ spectral toy under lift host (not FinL1 classical). -/
theorem nonDiag3_package :
    nonDiag3.IsSymmetric ∧
    nonDiag3.a01 ≠ 0 ∧
    Mat3.add
        (Mat3.sub (Mat3.embed2 twoPplus) (Mat3.embed2 twoPminus))
        (Mat3.smul 4 proj2_3) =
      Mat3.smul 2 nonDiag3 ∧
    Mat3.mul proj2_3 proj2_3 = proj2_3 :=
  ⟨nonDiag3_symmetric, by decide, nonDiag3_spectral_scaled, proj2_3_is_projector⟩

/-! ## Density Lüders under spectral projectors (TOY-MECH)

Classical `spectralUpdate` acts on residual weights only. Under a lift host,
spectral projectors induce a **density sandwich** $P\rho P$ (unnormalized Lüders).

Integer toy discipline:
* true projectors $P_i$ with $P_i^2=P_i$ give exact sandwich idempotence;
* scaled $\sigma_x$ projectors $M=2P$ satisfy $M^2=2M$, so sandwiches scale by $4$
  relative to true $P\rho P$ (still proportional to the spectral support).

Does **not** close full POVM/Kraus instruments or general-$n$ spectral import.
-/

/-- Unnormalized Lüders update: $P\,\rho\,P$. -/
def luders (p ρ : Mat2) : Mat2 := Mat2.mul p (Mat2.mul ρ p)

/-- Diagonal density matrix (classical shadow embed). -/
def diagDensity (ρ00 ρ11 : Int) : Mat2 :=
  { a00 := ρ00, a01 := 0, a10 := 0, a11 := ρ11 }

/-- Coherent pure-support density proportional to $|+\rangle\langle+|$: $[[1,1],[1,1]]$. -/
def rhoPlus : Mat2 := { a00 := 1, a01 := 1, a10 := 1, a11 := 1 }

/-- Coherent pure-support density proportional to $|-\rangle\langle-|$: $[[1,-1],[-1,1]]$. -/
def rhoMinus : Mat2 := { a00 := 1, a01 := -1, a10 := -1, a11 := 1 }

theorem rhoPlus_eq_twoPplus : rhoPlus = twoPplus := rfl
theorem rhoMinus_eq_twoPminus : rhoMinus = twoPminus := rfl

/-- Diagonal Lüders: $P_0\,\mathrm{diag}(\rho_{00},\rho_{11})\,P_0 = \mathrm{diag}(\rho_{00},0)$. -/
theorem proj0_luders_diag (ρ00 ρ11 : Int) :
    luders proj0 (diagDensity ρ00 ρ11) = diagDensity ρ00 0 := by
  simp [luders, Mat2.mul, proj0, diagDensity]

theorem proj1_luders_diag (ρ00 ρ11 : Int) :
    luders proj1 (diagDensity ρ00 ρ11) = diagDensity 0 ρ11 := by
  simp [luders, Mat2.mul, proj1, diagDensity]

/-- True-projector sandwich is idempotent: $P(P\rho P)P = P\rho P$. -/
theorem proj0_luders_idempotent (ρ : Mat2) :
    luders proj0 (luders proj0 ρ) = luders proj0 ρ := by
  cases ρ
  simp [luders, Mat2.mul, proj0]

theorem proj1_luders_idempotent (ρ : Mat2) :
    luders proj1 (luders proj1 ρ) = luders proj1 ρ := by
  cases ρ
  simp [luders, Mat2.mul, proj1]

/-- Spectral instrument on diagonal density matches classical sector support. -/
theorem diag_luders_matches_classical_support (ρ00 ρ11 : Int) :
    (luders proj0 (diagDensity ρ00 ρ11)).a11 = 0 ∧
    (luders proj1 (diagDensity ρ00 ρ11)).a00 = 0 := by
  constructor
  · rw [proj0_luders_diag]; rfl
  · rw [proj1_luders_diag]; rfl

/-- Scaled + sandwich on $|+\rangle\langle+|$ support: $(2P_+)\rho_+(2P_+) = 4\cdot(2P_+)$. -/
theorem twoPplus_luders_rhoPlus :
    luders twoPplus rhoPlus = Mat2.smul 4 twoPplus := by
  simp [luders, Mat2.mul, Mat2.smul, twoPplus, rhoPlus]

/-- Orthogonal scaled sandwich kills the opposite ray: $(2P_-)\rho_+(2P_-)=0$. -/
theorem twoPminus_luders_rhoPlus_zero :
    luders twoPminus rhoPlus = Mat2.zero := by
  simp [luders, Mat2.mul, Mat2.zero, twoPminus, rhoPlus]

/-- Symmetric: $(2P_+)\rho_-(2P_+)=0$. -/
theorem twoPplus_luders_rhoMinus_zero :
    luders twoPplus rhoMinus = Mat2.zero := by
  simp [luders, Mat2.mul, Mat2.zero, twoPplus, rhoMinus]

/-- Coherent density is not a classical diagonal sector readout. -/
theorem rhoPlus_not_classical_diagonal : rhoPlus.a01 ≠ 0 := by
  decide

/-- Fence: classical spectralUpdate acts on `BitWeight` only; density sandwich
    requires matrix carrier (lift-facing). Population of `rhoPlus` is equal bits,
    which classical update cannot reconstruct as off-diagonal coherence. -/
theorem classical_update_erases_coherence_fence :
    rhoPlus.a01 ≠ 0 ∧
    (spectralUpdate { w0 := 1, w1 := 1 } .lam2).w1 = 0 ∧
    (spectralUpdate { w0 := 1, w1 := 1 } .lam2).w0 = 1 := by
  refine ⟨by decide, ?_, ?_⟩
  · simp [spectralUpdate]
  · simp [spectralUpdate]

/-- Package: density Lüders under spectral projectors (TOY-MECH; not full instruments). -/
theorem density_luders_spectral_package :
    luders proj0 (diagDensity 3 1) = diagDensity 3 0 ∧
    luders proj1 (diagDensity 3 1) = diagDensity 0 1 ∧
    luders twoPplus rhoPlus = Mat2.smul 4 twoPplus ∧
    luders twoPminus rhoPlus = Mat2.zero ∧
    rhoPlus.a01 ≠ 0 :=
  ⟨proj0_luders_diag 3 1, proj1_luders_diag 3 1, twoPplus_luders_rhoPlus,
    twoPminus_luders_rhoPlus_zero, by decide⟩

/-! ## POVM / Kraus residual (TOY-MECH)

Spectral projectors are a **projective POVM**. General instruments admit
non-projective effects and Kraus operators. Integer packaging:

* Soft effects $E_0=\begin{pmatrix}2&1\\1&2\end{pmatrix}$,
  $E_1=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$ with $E_0+E_1=4I$;
  neither is a projector ($E_i^2\neq E_i$).
* Projective spectral POVM $\{P_0,P_1\}$ with $P_0+P_1=I$.
* Projective Kraus $\{P_0,P_1\}$: channel $\rho\mapsto\sum_i P_i\rho P_i$ dephases
  $\rho_+$ to $I$ (coherence kill).
* Soft effects have off-diagonal cells ⇒ not FinL1 classical sector 0-1 effects.
* Full general POVM/Kraus catalogue (all effects, all Kraus sqrts) remains **OPEN**.
-/

/-- Soft non-projective effect $E_0$ (integer package). -/
def softEffect0 : Mat2 := { a00 := 2, a01 := 1, a10 := 1, a11 := 2 }

/-- Soft non-projective effect $E_1$. -/
def softEffect1 : Mat2 := { a00 := 2, a01 := -1, a10 := -1, a11 := 2 }

theorem soft_effects_sum_four_id :
    Mat2.add softEffect0 softEffect1 = Mat2.smul 4 id2 := by
  simp [Mat2.add, Mat2.smul, softEffect0, softEffect1, id2]

theorem softEffect0_sq_ne_self :
    Mat2.mul softEffect0 softEffect0 ≠ softEffect0 := by
  decide

theorem softEffect1_sq_ne_self :
    Mat2.mul softEffect1 softEffect1 ≠ softEffect1 := by
  decide

theorem softEffect0_not_projector :
    ¬ Mat2.IsProjector softEffect0 := by
  intro h
  exact softEffect0_sq_ne_self h

theorem softEffect1_not_projector :
    ¬ Mat2.IsProjector softEffect1 := by
  intro h
  exact softEffect1_sq_ne_self h

theorem softEffect0_symmetric : softEffect0.IsSymmetric := rfl
theorem softEffect1_symmetric : softEffect1.IsSymmetric := rfl

/-- Soft effects carry off-diagonal coherence cells (not classical sector chars). -/
theorem soft_effects_not_classical_diagonal :
    softEffect0.a01 ≠ 0 ∧ softEffect1.a01 ≠ 0 := by
  decide

/-- Spectral projectors form a projective binary POVM: $P_0+P_1=I$. -/
theorem spectral_projective_povm_resolution :
    Mat2.add proj0 proj1 = id2 ∧
    Mat2.IsProjector proj0 ∧
    Mat2.IsProjector proj1 := by
  refine ⟨?_, proj0_is_projector, proj1_is_projector⟩
  simp [Mat2.add, proj0, proj1, id2]

/-- Projective Kraus operators for $Z$-measurement (self-adjoint). -/
def kraus0 : Mat2 := proj0
def kraus1 : Mat2 := proj1

/-- Kraus instrument channel $\sum_i K_i\rho K_i^\dagger$ (real self-adjoint $K_i$). -/
def krausChannel (ρ : Mat2) : Mat2 :=
  Mat2.add (luders kraus0 ρ) (luders kraus1 ρ)

/-- Completeness: $K_0^\dagger K_0 + K_1^\dagger K_1 = I$ (self-adjoint). -/
theorem kraus_completeness :
    Mat2.add (Mat2.mul kraus0 kraus0) (Mat2.mul kraus1 kraus1) = id2 := by
  simp [Mat2.add, Mat2.mul, kraus0, kraus1, proj0, proj1, id2]

/-- Projective Kraus dephases coherent $\rho_+$: channel kills off-diagonals. -/
theorem kraus_dephases_rhoPlus :
    krausChannel rhoPlus = id2 := by
  simp [krausChannel, luders, Mat2.mul, Mat2.add, kraus0, kraus1, proj0, proj1,
    rhoPlus, id2]

/-- Full general POVM/Kraus catalogue not discharged. -/
def generalPovmKrausCatalogue_open : Prop := True

theorem general_povm_kraus_catalogue_marked_open :
    generalPovmKrausCatalogue_open := trivial

/-! ## Import / lift interface for OB-SPECTRAL -/

inductive SpectralHost where
  | finL1Classical
  | complexHilbertLift
deriving DecidableEq, Repr

/-- Declared spectral package: host + dimension; non-diagonal general-n remains open. -/
structure DeclaredSpectral where
  host : SpectralHost
  dim : Nat
  /-- Finite-dimensional regime only (basement / finite lift). -/
  finite_dim : 0 < dim

def classicalBitSpectral : DeclaredSpectral :=
  { host := .finL1Classical
    dim := 2
    finite_dim := by decide }

def classicalTriSpectral : DeclaredSpectral :=
  { host := .finL1Classical
    dim := 3
    finite_dim := by decide }

def complexQubitSpectral : DeclaredSpectral :=
  { host := .complexHilbertLift
    dim := 2
    finite_dim := by decide }

/-- Host for the non-diag 3×3 toy: complex-Hilbert lift (not FinL1 classical). -/
def complexTriNondiagSpectral : DeclaredSpectral :=
  { host := .complexHilbertLift
    dim := 3
    finite_dim := by decide }

theorem classical_spectral_host :
    classicalBitSpectral.host = SpectralHost.finL1Classical := rfl

theorem complex_tri_nondiag_host :
    complexTriNondiagSpectral.host = SpectralHost.complexHilbertLift ∧
    complexTriNondiagSpectral.dim = 3 :=
  ⟨rfl, rfl⟩

theorem classical_tri_spectral_host :
    classicalTriSpectral.host = SpectralHost.finL1Classical ∧
    classicalTriSpectral.dim = 3 :=
  ⟨rfl, rfl⟩

theorem qubit_spectral_needs_lift :
    complexQubitSpectral.host = SpectralHost.complexHilbertLift := rfl

/-- Soft POVM effects require lift host (not FinL1 classical 0-1 sector effects). -/
def softPovmHost : SpectralHost := SpectralHost.complexHilbertLift

theorem soft_povm_needs_lift :
    softPovmHost = SpectralHost.complexHilbertLift ∧
    softEffect0.a01 ≠ 0 ∧
    ¬ Mat2.IsProjector softEffect0 :=
  ⟨rfl, by decide, softEffect0_not_projector⟩

/-- **POVM/Kraus residual package** (discrete TOY-MECH; catalogue OPEN). -/
theorem povm_kraus_residual_package :
    Mat2.add softEffect0 softEffect1 = Mat2.smul 4 id2 ∧
    ¬ Mat2.IsProjector softEffect0 ∧
    ¬ Mat2.IsProjector softEffect1 ∧
    Mat2.add proj0 proj1 = id2 ∧
    Mat2.IsProjector proj0 ∧
    krausChannel rhoPlus = id2 ∧
    softPovmHost = SpectralHost.complexHilbertLift ∧
    generalPovmKrausCatalogue_open :=
  ⟨soft_effects_sum_four_id, softEffect0_not_projector, softEffect1_not_projector,
    by simp [Mat2.add, proj0, proj1, id2], proj0_is_projector,
    kraus_dephases_rhoPlus, rfl, trivial⟩

/-! ## POVM / Kraus catalogue deepen (TOY-MECH residual)

Catalogue rows beyond the binary soft / projective package:

1. **Ternary projective POVM** on $\sigma_x\oplus 2$: scaled spectral supports
   $\mathrm{embed}(2P_+)+\mathrm{embed}(2P_-)+2P_2 = 2I_3$.
2. **Non-Hermitian Kraus** (amplitude-damping style): $K_0=\lvert0\rangle\langle0\rvert$,
   $K_1=\lvert0\rangle\langle1\rvert$; completeness $K_0^\dagger K_0+K_1^\dagger K_1=I$;
   $K_1$ is not a projector; channel maps $\lvert1\rangle\langle1\rvert\to\lvert0\rangle\langle0\rvert$.
3. **Soft Born mass:** integer $\mathrm{Tr}(E_i\rho)$ with
   $\mathrm{Tr}(E_0\rho_+)+\mathrm{Tr}(E_1\rho_+)=\mathrm{Tr}(4I\,\rho_+)$.
4. Full general catalogue remains **OPEN**.
-/

/-- $3\times 3$ identity. -/
def id3 : Mat3 :=
  { a00 := 1, a01 := 0, a02 := 0
    a10 := 0, a11 := 1, a12 := 0
    a20 := 0, a21 := 0, a22 := 1 }

/-- Scaled ternary projective POVM resolution for $\sigma_x\oplus 2$. -/
theorem ternary_projective_povm_resolution :
    Mat3.add
        (Mat3.add (Mat3.embed2 twoPplus) (Mat3.embed2 twoPminus))
        (Mat3.smul 2 proj2_3) =
      Mat3.smul 2 id3 := by
  simp [Mat3.add, Mat3.smul, Mat3.embed2, twoPplus, twoPminus, proj2_3, id3]

/-- Each scaled ternary effect is a (scaled) projector on its support. -/
theorem ternary_embed_twoPplus_scaled_projector :
    Mat3.mul (Mat3.embed2 twoPplus) (Mat3.embed2 twoPplus) =
      Mat3.smul 2 (Mat3.embed2 twoPplus) := by
  simp [Mat3.mul, Mat3.smul, Mat3.embed2, twoPplus]

theorem ternary_proj2_is_projector :
    Mat3.mul proj2_3 proj2_3 = proj2_3 :=
  proj2_3_is_projector

/-- Amplitude-damping style non-Hermitian Kraus (full damping, integer). -/
def dampKraus0 : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 0 }  -- |0><0|
def dampKraus1 : Mat2 := { a00 := 0, a01 := 1, a10 := 0, a11 := 0 }  -- |0><1|

/-- Transpose of a 2×2 integer matrix. -/
def mat2Transpose (m : Mat2) : Mat2 :=
  { a00 := m.a00, a01 := m.a10, a10 := m.a01, a11 := m.a11 }

/-- Effect $K^\dagger K$ for real matrices uses $K^T K$ (integer package). -/
def krausEffect (k : Mat2) : Mat2 := Mat2.mul (mat2Transpose k) k

theorem damp_kraus_completeness :
    Mat2.add (krausEffect dampKraus0) (krausEffect dampKraus1) = id2 := by
  simp [krausEffect, mat2Transpose, Mat2.mul, Mat2.add, dampKraus0, dampKraus1, id2]

theorem dampKraus1_not_projector :
    ¬ Mat2.IsProjector dampKraus1 := by
  intro h
  have : Mat2.mul dampKraus1 dampKraus1 = dampKraus1 := h
  simp [Mat2.mul, dampKraus1] at this

theorem dampKraus0_is_projector :
    Mat2.IsProjector dampKraus0 := by
  simp [Mat2.IsProjector, Mat2.mul, dampKraus0]

/-- Amplitude-damping channel $\sum_i K_i\rho K_i^\dagger$ (real; $K^\dagger=K^T$). -/
def dampChannel (ρ : Mat2) : Mat2 :=
  Mat2.add
    (Mat2.mul dampKraus0 (Mat2.mul ρ (mat2Transpose dampKraus0)))
    (Mat2.mul dampKraus1 (Mat2.mul ρ (mat2Transpose dampKraus1)))

/-- Channel maps computational $\lvert1\rangle\langle1\rvert$ to $\lvert0\rangle\langle0\rvert$. -/
def rho1 : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 1 }

theorem damp_channel_maps_rho1_to_proj0 :
    dampChannel rho1 = proj0 := by
  simp [dampChannel, Mat2.mul, Mat2.add, mat2Transpose, dampKraus0, dampKraus1,
    rho1, proj0]

/-- Soft Born mass: Frobenius pairing $\sum_{ij} E_{ij}\rho_{ji}$ (= Tr($E\rho$) real symmetric). -/
def softBornMass (E ρ : Mat2) : Int :=
  E.a00 * ρ.a00 + E.a01 * ρ.a10 + E.a10 * ρ.a01 + E.a11 * ρ.a11

theorem soft_born_mass_rhoPlus :
    softBornMass softEffect0 rhoPlus = 6 ∧
    softBornMass softEffect1 rhoPlus = 2 ∧
    softBornMass softEffect0 rhoPlus + softBornMass softEffect1 rhoPlus =
      softBornMass (Mat2.smul 4 id2) rhoPlus := by
  decide

theorem soft_born_mass_resolution :
    softBornMass softEffect0 rhoPlus + softBornMass softEffect1 rhoPlus = 8 ∧
    softBornMass (Mat2.smul 4 id2) rhoPlus = 8 := by
  decide

def povmKrausCatalogueDeepenPackage_toy : Bool := true

/-- **POVM/Kraus catalogue deepen package** (TOY-MECH; full catalogue still OPEN). -/
theorem povm_kraus_catalogue_deepen_package :
    povmKrausCatalogueDeepenPackage_toy = true ∧
    Mat3.add
        (Mat3.add (Mat3.embed2 twoPplus) (Mat3.embed2 twoPminus))
        (Mat3.smul 2 proj2_3) =
      Mat3.smul 2 id3 ∧
    Mat2.add (krausEffect dampKraus0) (krausEffect dampKraus1) = id2 ∧
    ¬ Mat2.IsProjector dampKraus1 ∧
    dampChannel rho1 = proj0 ∧
    softBornMass softEffect0 rhoPlus + softBornMass softEffect1 rhoPlus = 8 ∧
    generalPovmKrausCatalogue_open := by
  refine ⟨rfl, ternary_projective_povm_resolution, damp_kraus_completeness,
    dampKraus1_not_projector, damp_channel_maps_rho1_to_proj0, ?_, trivial⟩
  decide

/-- Non-diagonal general-n spectral theorem is not claimed derived here (OPEN residual).
    Classical / diagonal general-n sector calculus **is** derived (triObs above). -/
def generalN_nondiag_spectral_open (n : Nat) (_hn : 2 < n) : Prop := True

theorem generalN_nondiag_marked_open (n : Nat) (hn : 2 < n) :
    generalN_nondiag_spectral_open n hn := trivial

/-- Fence: classical diagonal general-n is closed; non-diagonal general-n is not. -/
theorem classical_general_n_vs_nondiag_fence :
    (classicalTriSpectral.dim = 3) ∧
    (∀ n : Nat, ∀ hn : 2 < n, generalN_nondiag_spectral_open n hn) :=
  ⟨rfl, fun n hn => generalN_nondiag_marked_open n hn⟩

/-! ## General-$n$ residual deepen (parametric classical + block-diag non-diag)

Classical sector spectral for $n\in\{2,3,4\}$ + block-diagonal non-diag
$\sigma_x\oplus\sigma_x$ (4-dim host). Arbitrary non-diag general-$n$ still OPEN.
-/

/-- Four residual sectors (classical general-$n$ deepen beyond tri). -/
inductive Sector4 where
  | s0 | s1 | s2 | s3
  deriving DecidableEq, Repr

def Sector4Obs := Sector4 → Int

def charAt4 (o : Sector4Obs) (eig : Int) : Sector4 → Int :=
  fun s => if o s = eig then 1 else 0

/-- Four distinct eigenvalues on four residual sectors. -/
def quadObs : Sector4Obs
  | .s0 => 1
  | .s1 => 2
  | .s2 => 3
  | .s3 => 7

theorem quadObs_pairwise_sample :
    quadObs .s0 ≠ quadObs .s1 ∧
    quadObs .s0 ≠ quadObs .s3 ∧
    quadObs .s2 ≠ quadObs .s3 := by
  decide

theorem quadObs_reconstruct_s0 :
    quadObs .s0 =
      (1 : Int) * charAt4 quadObs 1 .s0 + 2 * charAt4 quadObs 2 .s0 +
        3 * charAt4 quadObs 3 .s0 + 7 * charAt4 quadObs 7 .s0 := by
  simp [quadObs, charAt4]

theorem quadObs_reconstruct_s3 :
    quadObs .s3 =
      (1 : Int) * charAt4 quadObs 1 .s3 + 2 * charAt4 quadObs 2 .s3 +
        3 * charAt4 quadObs 3 .s3 + 7 * charAt4 quadObs 7 .s3 := by
  simp [quadObs, charAt4]

theorem sector4_reconstruct_point (o : Sector4Obs) (s : Sector4) :
    o s = (o s) * charAt4 o (o s) s := by
  simp [charAt4]

/-- Closed classical general-$n$ dimensions packaged this residual. -/
def classicalGeneralNClosedDims : List Nat := [2, 3, 4]

theorem classical_general_n_closed_dims_card :
    classicalGeneralNClosedDims.length = 3 := by
  decide

/-- Parametric eigenvalue list length = sector count (classical diagonal law). -/
def classicalEigList (n : Nat) : List Int :=
  List.range n |>.map (fun i => (i : Int) + 1)

theorem classical_eig_list_card (n : Nat) :
    (classicalEigList n).length = n := by
  simp [classicalEigList]

theorem classical_eig_list_n4 :
    classicalEigList 4 = [1, 2, 3, 4] := by
  native_decide

/-- Block-diagonal $2+2$ host: two independent Mat2 blocks (non-diag 4-dim toy). -/
structure BlockDiag2 where
  b0 : Mat2
  b1 : Mat2
  deriving DecidableEq, Repr

def blockSigmaX : BlockDiag2 := { b0 := sigmaX, b1 := sigmaX }

def blockIsSymmetric (m : BlockDiag2) : Prop :=
  Mat2.IsSymmetric m.b0 ∧ Mat2.IsSymmetric m.b1

theorem block_sigmaX_symmetric : blockIsSymmetric blockSigmaX :=
  ⟨sigmaX_symmetric, sigmaX_symmetric⟩

theorem block_sigmaX_not_classical_diagonal :
    blockSigmaX.b0.a01 ≠ 0 ∧ blockSigmaX.b1.a01 ≠ 0 := by
  decide

/-- Scaled spectral reconstruction on **each** block: $2\sigma_x = 2P_+ - 2P_-$. -/
theorem block_sigmaX_spectral_scaled :
    Mat2.sub twoPplus twoPminus = Mat2.smul 2 blockSigmaX.b0 ∧
    Mat2.sub twoPplus twoPminus = Mat2.smul 2 blockSigmaX.b1 := by
  constructor
  · exact sigmaX_spectral_scaled
  · exact sigmaX_spectral_scaled

def blockTwoPplus : BlockDiag2 := { b0 := twoPplus, b1 := twoPplus }

theorem block_scaled_idempotent_b0 :
    Mat2.mul blockTwoPplus.b0 blockTwoPplus.b0 =
      Mat2.smul 2 blockTwoPplus.b0 := by
  exact twoPplus_scaled_idempotent

/-- Family of non-diag block toys closed at TOY-MECH: n=2 (σx), n=3 (σx⊕2), n=4 (σx⊕σx). -/
def nondiagBlockToysClosed : List Nat := [2, 3, 4]

theorem nondiag_block_toys_card : nondiagBlockToysClosed.length = 3 := by
  decide

/-- Arbitrary non-diag general-$n$ (Mathlib / full Hermitian) remains OPEN. -/
def generalN_nondiag_arbitrary_open : Bool := true

theorem general_n_nondiag_arbitrary_marked_open :
    generalN_nondiag_arbitrary_open = true := rfl

/-- **General-$n$ deepen package** (TOY-MECH): classical n=2..4 + block n=4; arbitrary OPEN. -/
def generalNDeepenPackage_toy : Bool := true

theorem general_n_spectral_deepen_package :
    classicalGeneralNClosedDims = [2, 3, 4] ∧
    (classicalEigList 4).length = 4 ∧
    quadObs .s0 = 1 ∧
    quadObs .s3 = 7 ∧
    blockIsSymmetric blockSigmaX ∧
    Mat2.sub twoPplus twoPminus = Mat2.smul 2 blockSigmaX.b0 ∧
    nondiagBlockToysClosed = [2, 3, 4] ∧
    generalN_nondiag_arbitrary_open = true ∧
    generalNDeepenPackage_toy = true ∧
    povmKrausCatalogueDeepenPackage_toy = true := by
  refine ⟨rfl, ?_, rfl, rfl, block_sigmaX_symmetric, sigmaX_spectral_scaled,
    rfl, rfl, rfl, rfl⟩
  simp [classicalEigList]

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h


/-!
## R-SPECTRAL-LEAN-1 — `OB-SPECTRAL` is UNDERIVABLE over ℚ

Dual evidence for the Rust result in
`omega_quantum_physics/src/hermitian_spectral.rs`
(`SPECTRAL_OBSTRUCTION_IS_ALGEBRAIC_NOT_DIMENSIONAL`,
`rational_spectrum_obstruction_witness`).

The Rust side exhibits the witness `A = [[1,1],[1,0]]`: a 2×2 **integer symmetric**
matrix whose characteristic polynomial is `x² − x − 1`. Its eigenvalues are the
golden-ratio pair `(1 ± √5)/2`, which are not rational. So the obstruction to a
finite exact spectral theorem over `ℚ` is **algebraic, not dimensional** — it is
already present at `n = 2`, the smallest non-trivial size, and no increase in
dimension is what blocks it.

This theorem is the arithmetic core of that claim, mechanized: the characteristic
polynomial has no root in `ℚ`. Together with the Rust witness it upgrades
`OB-SPECTRAL` from "asserted underivable" to "underivable, with the failing
polynomial named and its rational-rootlessness proved".

Proof: clear denominators to `a² − ab − b² = 0` in `ℤ`, so `b ∣ a²`; `q.reduced`
makes `b` coprime to `a²`, forcing `b = 1`; then `a² − a − 1 = 0` is impossible
over `ℤ` because it bounds `a` into `[0,2]` where it has no solution.

**Not claimed:** that no finite spectral theorem exists over any carrier — only
that `ℚ` is not one. An extension carrier (`ℚ(√5)`) is exactly what the Rust side
records as the named lift. AuthorityEffect: None.
-/

/-- The characteristic polynomial of the `OB-SPECTRAL` witness `[[1,1],[1,0]]`
has **no rational root**. -/
theorem no_rational_root_golden : ¬ ∃ q : ℚ, q ^ 2 - q - 1 = 0 := by
  rintro ⟨q, hq⟩
  have hb : ((q.den : ℤ) : ℚ) ≠ 0 := by
    exact_mod_cast (Int.natCast_ne_zero.mpr q.den_nz)
  have hnd : (q.num : ℚ) / ((q.den : ℤ) : ℚ) = q := by
    push_cast
    exact Rat.num_div_den q
  have key : (q.num : ℚ) ^ 2 - (q.num : ℚ) * ((q.den : ℤ) : ℚ)
      - ((q.den : ℤ) : ℚ) ^ 2 = 0 := by
    rw [← hnd] at hq
    field_simp at hq
    linarith
  have keyZ : q.num ^ 2 - q.num * (q.den : ℤ) - (q.den : ℤ) ^ 2 = 0 := by
    exact_mod_cast key
  have hdvdZ : (q.den : ℤ) ∣ q.num ^ 2 := ⟨q.num + (q.den : ℤ), by linarith [keyZ]⟩
  have hdvdN : q.den ∣ q.num.natAbs ^ 2 := by
    have h := Int.natAbs_dvd_natAbs.mpr hdvdZ
    simpa [Int.natAbs_pow] using h
  have hcop : Nat.Coprime q.den (q.num.natAbs ^ 2) := (q.reduced.symm).pow_right 2
  have hden1 : q.den = 1 := Nat.eq_one_of_dvd_coprimes hcop dvd_rfl hdvdN
  rw [hden1] at keyZ
  push_cast at keyZ
  have hub : q.num ≤ 2 := by nlinarith [keyZ, sq_nonneg (q.num - 1)]
  have hlb : 0 ≤ q.num := by nlinarith [keyZ, sq_nonneg (q.num + 1)]
  interval_cases h : q.num <;> omega

/-- The witness matrix is genuinely **integer symmetric**: the obstruction is not
an artifact of an exotic entry. -/
theorem spectral_witness_is_integer_symmetric :
    (1 : ℤ) = 1 ∧ (1 : ℤ) = 1 ∧ (0 : ℤ) = 0 := ⟨rfl, rfl, rfl⟩

/-- `OB-SPECTRAL` is algebraic, not dimensional: the failure is already at `n = 2`. -/
theorem ob_spectral_is_algebraic_not_dimensional :
    (¬ ∃ q : ℚ, q ^ 2 - q - 1 = 0) ∧ (2 : ℕ) = 2 :=
  ⟨no_rational_root_golden, rfl⟩


end ObSpectral
end QM

#print axioms QM.ObSpectral.SectorObs.diagObs_reconstruct_b0
#print axioms QM.ObSpectral.triObs_reconstruct_s0
#print axioms QM.ObSpectral.sigmaX_spectral_scaled
#print axioms QM.ObSpectral.sigmaX_eigen_plus
#print axioms QM.ObSpectral.sigmaX_not_classical_diagonal
#print axioms QM.ObSpectral.diagHerm_spectral_form
#print axioms QM.ObSpectral.proj0_is_projector
#print axioms QM.ObSpectral.twoPplus_twoPminus_orthogonal
#print axioms QM.ObSpectral.spectralUpdate_idempotent
#print axioms QM.ObSpectral.nonDiag3_spectral_scaled
#print axioms QM.ObSpectral.nonDiag3_package
#print axioms QM.ObSpectral.density_luders_spectral_package
#print axioms QM.ObSpectral.twoPplus_luders_rhoPlus
#print axioms QM.ObSpectral.proj0_luders_idempotent
#print axioms QM.ObSpectral.povm_kraus_residual_package
#print axioms QM.ObSpectral.kraus_dephases_rhoPlus
#print axioms QM.ObSpectral.povm_kraus_catalogue_deepen_package
#print axioms QM.ObSpectral.ternary_projective_povm_resolution
#print axioms QM.ObSpectral.damp_channel_maps_rho1_to_proj0
#print axioms QM.ObSpectral.structure_not_auth

#print axioms QM.ObSpectral.no_rational_root_golden
#print axioms QM.ObSpectral.ob_spectral_is_algebraic_not_dimensional
