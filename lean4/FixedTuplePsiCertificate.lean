import Mathlib
import BasisExtensionObstruction
import ExtensionCurvatureObstruction
import FiniteBasisCover
/-!
# MUB6 fixed-tuple `Ψ_basis` certificate adapter (packet section 11)

Lean reflection of the Rust binding layer
`omega_mub::omega_native::mub6_basis_extension_packet` (`Mub6OdpInstance`). A
`FixedTuplePsiCertificate.Cert e` is the *typed receipt* that the basis-level
obstruction of a fixed set `e` is strictly positive — its single field is exactly the
lower bound that the Rust instance leaves **OPEN** (`lower_bound_epsilon = none`,
`terminal = OpenResidual`).

* **With** that receipt, the no-extension conclusion is immediate
  (`no_fourth_basis_of_cert`, reusing `Psi_basis_pos_iff_no_fourth_basis`).
* **Without** it, the terminal is `OpenResidual`: all that is available is
  `0 ≤ Ψ_basis(e)` (`open_residual_only_nonneg`), never upgraded to `0 < _`.

**Where the receipt comes from.** This file does *not* re-prove the cover→no-go logic —
that is `MUB.FiniteVectorCover` (vector cover) and `MUB.FiniteBasisCover` (basis cover),
which route `finite_cover_no_feasible` into `Ψ_basis`. The `Cert.of…` constructors below are
thin adapters that turn each of those canonical bridges' conclusions into the packet receipt:

* `Cert.ofBasisCover` — from a completed exact **basis** cover
  (`FiniteBasisCover.psi_basis_pos_of_cover`, the ℓ² mass the Rust cover engine lower-bounds);
* `Cert.ofNoMuVector` — from a completed exact **vector** cover: no fourth MU *vector* a
  fortiori means no fourth MU *basis* (`FiniteBasisCover.psi_basis_pos_of_no_mu_vector`). This
  is the wire from the machine-run `gauge_fixed_5_torus_cover_certificate` (910,338 boxes,
  `complete = true`, exact `BigRational`) to the basis-level certificate;
* `Cert.ofPointwisePos` — from a pointwise-positive basis deviation.

cover is the open frontier). It only adapts the cover bridges to the packet's seal.
-/

open MUB.BasisExtensionObstruction
open MUB.ExtensionCurvatureObstruction

namespace MUB
namespace FixedTuplePsiCertificate

/-- A verified fixed-tuple certificate. Its single field is the basis-level lower bound
`0 < Ψ_basis(e)` — the Rust `lower_bound_*`, which is OPEN there. It carries no global
MUB claim; it is just the typed hypothesis under which the terminal target fires. -/
structure Cert {N d : ℕ} (e : Fin N → (Fin d → ℂ)) : Prop where
  psi_basis_pos : 0 < (Psi_basis e).phi

/-- **Section-11 target.** A verified `Ψ_basis(e) > 0` certificate implies no fourth MU
basis extends the fixed set `e` (the columns of a unitary `U` all mutually unbiased to
`e`). This is the packet's terminal-target theorem, stated as a clean implication from
the lower bound. -/
theorem no_fourth_basis_of_cert {N d : ℕ} (e : Fin N → (Fin d → ℂ)) (c : Cert e) :
    ¬ ∃ U : Matrix.unitaryGroup (Fin d) ℂ,
        ∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (d : ℝ) :=
  (Psi_basis_pos_iff_no_fourth_basis e).mp c.psi_basis_pos

/-- The d = 6 instance (`N = 18`, target `1/6`): a verified certificate for the
canonical-triple problem yields "no fourth MU basis extends the 18 fixed vectors". -/
theorem no_fourth_basis_of_cert_d6 (e : Fin 18 → (Fin 6 → ℂ)) (c : Cert e) :
    ¬ ∃ U : Matrix.unitaryGroup (Fin 6) ℂ,
        ∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (6 : ℝ) :=
  no_fourth_basis_of_cert e c

/-- **Pointwise-positive ⇒ `Ψ_basis > 0`.** If the basis-level deviation is strictly
positive at *every* unitary, then its compact minimum `Ψ_basis(e)` is strictly positive:
the minimum is attained (`phi_is_min`) at some `U`, where the deviation is `> 0`. -/
theorem psi_basis_pos_of_pointwise_pos {N d : ℕ} (e : Fin N → (Fin d → ℂ))
    (h : ∀ U : Matrix.unitaryGroup (Fin d) ℂ, 0 < basisDeviation e U) :
    0 < (Psi_basis e).phi := by
  obtain ⟨U, hU⟩ := (Psi_basis e).phi_is_min.2
  rw [hU]
  exact h U

/-- Build the packet `Cert` from a pointwise-positive basis deviation. -/
theorem Cert.ofPointwisePos {N d : ℕ} (e : Fin N → (Fin d → ℂ))
    (h : ∀ U : Matrix.unitaryGroup (Fin d) ℂ, 0 < basisDeviation e U) :
    Cert e :=
  ⟨psi_basis_pos_of_pointwise_pos e h⟩

/-- Build the packet `Cert` from a completed **exact basis cover** — the canonical wiring is
`MUB.FiniteBasisCover.psi_basis_pos_of_cover` (the ℓ² basis mass the Rust cover engine
lower-bounds per box). A completed cover discharges the `OpenResidual` seal. -/
theorem Cert.ofBasisCover {N d : ℕ} {ι : Type*} (e : Fin N → (Fin d → ℂ))
    (s : Finset ι) (Uc : ι → Set (Matrix.unitaryGroup (Fin d) ℂ))
    (K : Set (Matrix.unitaryGroup (Fin d) ℂ))
    (hcover : ∀ U ∈ K, ∃ j ∈ s, U ∈ Uc j) (ε : ι → ℝ)
    (hbound : ∀ j ∈ s, ∀ U ∈ Uc j, ε j ≤ FiniteBasisCover.basisCurvatureMass e (1 / (d : ℝ)) U)
    (hpos : ∀ j ∈ s, 0 < ε j)
    (hK : ∀ U, (∀ j i, ‖overlap e U i j‖ ^ 2 = 1 / (d : ℝ)) → U ∈ K) :
    Cert e :=
  ⟨FiniteBasisCover.psi_basis_pos_of_cover s Uc K e hcover ε hbound hpos hK⟩

/-- Build the packet `Cert` from a completed **exact vector cover**: no fourth MU *vector*
a fortiori means no fourth MU *basis* (a candidate unitary's first column would be such a
vector), via `MUB.FiniteBasisCover.psi_basis_pos_of_no_mu_vector`. This is the wire from the
machine-run exact cover `gauge_fixed_5_torus_cover_certificate` to the basis-level receipt. -/
theorem Cert.ofNoMuVector {N d : ℕ} [NeZero d] (e : Fin N → (Fin d → ℂ))
    (hv : ¬ ∃ w : Fin d → ℂ, ∀ i, ‖∑ k, (starRingEnd ℂ) (e i k) * w k‖ ^ 2 = 1 / (d : ℝ)) :
    Cert e :=
  ⟨FiniteBasisCover.psi_basis_pos_of_no_mu_vector e hv⟩

/-- **`OpenResidual`, typed.** Absent the lower-bound field, both a fourth-basis
extension and its negation remain possible: the basis-level obstruction is only known
to be `0 ≤ Ψ_basis(e)` (`phi_nonneg`), with no proof of strict positivity. The Rust
`terminal = OpenResidual` / `lower_bound_epsilon = none` is exactly this `0 ≤ _`,
never upgraded to `0 < _`. -/
theorem open_residual_only_nonneg {N d : ℕ} (e : Fin N → (Fin d → ℂ)) :
    0 ≤ (Psi_basis e).phi :=
  (Psi_basis e).phi_nonneg

end FixedTuplePsiCertificate
end MUB

-- Axiom hygiene: the receipt and its constructors rest only on the standard kernel axioms.
#print axioms MUB.FixedTuplePsiCertificate.no_fourth_basis_of_cert
#print axioms MUB.FixedTuplePsiCertificate.no_fourth_basis_of_cert_d6
#print axioms MUB.FixedTuplePsiCertificate.psi_basis_pos_of_pointwise_pos
#print axioms MUB.FixedTuplePsiCertificate.Cert.ofPointwisePos
#print axioms MUB.FixedTuplePsiCertificate.Cert.ofBasisCover
#print axioms MUB.FixedTuplePsiCertificate.Cert.ofNoMuVector
#print axioms MUB.FixedTuplePsiCertificate.open_residual_only_nonneg
