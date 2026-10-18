import Mathlib
import BasisExtensionObstruction
import ExtensionCurvatureObstruction
/-!
# The MUB-extension assembly: a mechanized reduction of MUB(d) ≤ 3

This module assembles the basis-level obstruction `Psi_basis`
(`MUB.BasisExtensionObstruction`) and the finite-cover machinery
(`MUB.ExtensionCurvatureObstruction`) into a single **conditional reduction**:

> `no_four_mub_of_psiVal_pos` : if the basis-level obstruction `psiVal` is strictly
> positive on **every** MU triple, then there is no fourth mutually-unbiased basis.

It is the Tao-style "isolate the hard lemma" step. The whole MUB(d) ≤ 3 question is
compressed onto the single positivity hypothesis `∀ T, 0 < psiVal T`; everything
*around* that hypothesis is proved here, axiom-clean.

The decomposition (each piece axiom-clean):

* **L-A** — `instance : CompactSpace (MUTriple d)`: the MU-triple space is a closed
  cut of the compact product of unitary groups (`unitaryGroup_compactSpace` ×
  Tychonoff).
* **L-B** — `continuous_psiVal`: `T ↦ psiVal T` is continuous (Berge / the parametric
  infimum `IsCompact.continuous_sInf` of a jointly-continuous mass).
* **reduction** — `no_four_mub_of_psiVal_pos`, via `Psi_basis_zero_iff_fourth_basis`.
* **finite-cover form** — `no_four_mub_of_finite_cover`, via `finite_cover_no_feasible`.
* **completeness** — `psiVal_uniform_of_pos`, via `uniform_pos_of_pointwise_pos`:
  when MU triples exist, pointwise positivity is equivalent to a uniform positive
  gap, so a *finite* certified cover loses nothing.

## Firewall (honest scope)

This is **NOT** a proof of MUB(d) ≤ 3 (for d = 6 the smallest open case of a
~20-year-open problem). It is a *reduction*: the open content is exactly the
hypothesis `∀ T : MUTriple d, 0 < psiVal T` (no fourth MU basis extends any triple),
which is left undischarged. `psiVal` is a diagnostic; it mints no authority. The
existence of MU triples (the `Nonempty (MUTriple d)` used by the completeness lemma)
is cited, not proved here (for d = 6 it holds via the Invariant-Systems canonical
triple).
-/

open Matrix Metric
open MUB.BasisExtensionObstruction
open MUB.ExtensionCurvatureObstruction

namespace MUB.TripleExtensionAssembly

variable {d : ℕ}

/-- Pairwise mutual-unbiasedness of three unitary bases: column `i` of basis `a`
and column `j` of basis `b` have squared overlap `1/d`. -/
def pairwiseMU (T : Fin 3 → Matrix.unitaryGroup (Fin d) ℂ) : Prop :=
  ∀ a b, a ≠ b → ∀ i j : Fin d,
    ‖∑ k, (starRingEnd ℂ) ((T a : Matrix (Fin d) (Fin d) ℂ) k i)
            * (T b : Matrix (Fin d) (Fin d) ℂ) k j‖ ^ 2 = 1 / (d : ℝ)

/-- An **MU triple**: three unitary bases of `ℂ^d`, pairwise mutually unbiased.
Within-basis orthonormality is automatic from unitarity; this is the canonical
carrier for the extension question. -/
abbrev MUTriple (d : ℕ) := {T : Fin 3 → Matrix.unitaryGroup (Fin d) ℂ // pairwiseMU T}

/-- Forgetful adapter to the flat `3·d`-vector representation `Psi_basis` consumes.
Vector index `i : Fin (3*d)` splits as `(basis a, column c)`; the `k`-th component is
the `(k, c)` entry of unitary `a`. The flat list is a **compatibility interface** for
the existing `Psi_basis` machinery, not the primary carrier. -/
noncomputable def MUTriple.toFlat (T : MUTriple d) : Fin (3 * d) → (Fin d → ℂ) :=
  fun i k =>
    (T.val ((finProdFinEquiv (m := 3) (n := d)).symm i).1 : Matrix (Fin d) (Fin d) ℂ)
      k ((finProdFinEquiv (m := 3) (n := d)).symm i).2

/-- Entry continuity helper for the ambient product: `T ↦ (T a)_{k i}` is continuous. -/
theorem continuous_triple_entry (a : Fin 3) (k i : Fin d) :
    Continuous (fun T : Fin 3 → Matrix.unitaryGroup (Fin d) ℂ =>
      (T a : Matrix (Fin d) (Fin d) ℂ) k i) :=
  (continuous_subtype_val.comp (continuous_apply a)).matrix_elem k i

/-- **L-A: the MU-triple space is compact.** It is a closed subset (cut out by the
pairwise-MU equations) of the compact product of unitary groups. -/
instance : CompactSpace (MUTriple d) := by
  have hclosed : IsClosed {T : Fin 3 → Matrix.unitaryGroup (Fin d) ℂ | pairwiseMU T} := by
    have hset :
        {T : Fin 3 → Matrix.unitaryGroup (Fin d) ℂ | pairwiseMU T}
          = ⋂ a, ⋂ b, ⋂ (_ : a ≠ b), ⋂ i, ⋂ j,
              {T : Fin 3 → Matrix.unitaryGroup (Fin d) ℂ |
                ‖∑ k, (starRingEnd ℂ) ((T a : Matrix (Fin d) (Fin d) ℂ) k i)
                    * (T b : Matrix (Fin d) (Fin d) ℂ) k j‖ ^ 2 = 1 / (d : ℝ)} := by
      ext T
      simp only [pairwiseMU, Set.mem_setOf_eq, Set.mem_iInter]
    rw [hset]
    refine isClosed_iInter fun a => isClosed_iInter fun b => isClosed_iInter fun _ =>
      isClosed_iInter fun i => isClosed_iInter fun j => ?_
    refine isClosed_eq ?_ continuous_const
    refine (Continuous.norm ?_).pow 2
    refine continuous_finsetSum _ (fun k _ => ?_)
    exact (continuous_star.comp (continuous_triple_entry a k i)).mul
      (continuous_triple_entry b k j)
  exact isCompact_iff_compactSpace.mp hclosed.isCompact

/-- The attained minimum of an `ExtensionObstruction` equals the infimum of its mass
over the whole space. -/
theorem phi_eq_sInf {V : Type*} (O : ExtensionObstruction V) :
    O.phi = sInf (O.mass '' Set.univ) := by
  refine (IsLeast.csInf_eq ?_).symm
  refine ⟨?_, ?_⟩
  · obtain ⟨v, hv⟩ := O.phi_is_min.2
    exact ⟨v, Set.mem_univ v, hv.symm⟩
  · rintro y ⟨v, -, rfl⟩
    exact O.phi_is_min.1 v

/-- The basis-level obstruction value on a triple (via the flat adapter). `psiVal T = 0`
iff a fourth MU basis extends `T`. -/
noncomputable def psiVal (T : MUTriple d) : ℝ := (Psi_basis T.toFlat).phi

theorem continuous_toFlat_entry (i : Fin (3 * d)) (k : Fin d) :
    Continuous (fun T : MUTriple d => T.toFlat i k) := by
  unfold MUTriple.toFlat
  exact (continuous_subtype_val.comp
    ((continuous_apply _).comp continuous_subtype_val)).matrix_elem k _

/-- The deviation mass is jointly continuous in the triple and the candidate basis. -/
theorem continuous_uncurry_basisDeviation :
    Continuous (fun p : MUTriple d × Matrix.unitaryGroup (Fin d) ℂ =>
      basisDeviation p.1.toFlat p.2) := by
  unfold basisDeviation
  refine continuous_finsetSum _ (fun j _ => continuous_finsetSum _ (fun i _ => ?_))
  refine (Continuous.sub ?_ continuous_const).abs
  refine (Continuous.norm ?_).pow 2
  unfold overlap
  refine continuous_finsetSum _ (fun k _ => ?_)
  refine (continuous_star.comp ((continuous_toFlat_entry i k).comp continuous_fst)).mul ?_
  exact (continuous_subtype_val.comp continuous_snd).matrix_elem k j

/-- **L-B: the obstruction value `T ↦ psiVal T` is continuous** (Berge / parametric
infimum of a jointly-continuous mass over the compact unitary group). -/
theorem continuous_psiVal : Continuous (psiVal : MUTriple d → ℝ) := by
  have heq : (psiVal : MUTriple d → ℝ)
      = fun T => sInf ((fun U => basisDeviation T.toFlat U) '' Set.univ) := by
    funext T
    rw [psiVal, phi_eq_sInf]
    rfl
  rw [heq]
  exact isCompact_univ.continuous_sInf continuous_uncurry_basisDeviation

/-- **Four MUBs in ℂ^d**: an MU triple together with a fourth basis (unitary `U`)
mutually unbiased to all three (its orthonormal columns form the fourth basis). -/
def FourMUB (d : ℕ) : Prop :=
  ∃ T : MUTriple d, ∃ U : Matrix.unitaryGroup (Fin d) ℂ,
    ∀ j i, ‖overlap T.toFlat U i j‖ ^ 2 = 1 / (d : ℝ)

/-- **ASSEMBLY (the reduction).** If the basis-level obstruction `psiVal` is strictly
positive on every MU triple, then no four MUBs exist. The entire MUB(d) ≤ 3 question
is compressed onto the single hypothesis `∀ T, 0 < psiVal T`. -/
theorem no_four_mub_of_psiVal_pos (h : ∀ T : MUTriple d, 0 < psiVal T) :
    ¬ FourMUB d := by
  rintro ⟨T, U, hU⟩
  have hzero : psiVal T = 0 := by
    rw [psiVal, Psi_basis_zero_iff_fourth_basis]
    exact ⟨U, hU⟩
  exact absurd hzero (h T).ne'

/-- **ASSEMBLY (finite-cover form).** A finite certified cover of the triple space —
finitely many patches, each with a positive lower bound on `psiVal` — rules out four
MUBs. This is the computational target for the cover program. -/
theorem no_four_mub_of_finite_cover
    {ι : Type*} (s : Finset ι) (Uc : ι → Set (MUTriple d)) (ε : ι → ℝ)
    (hcover : ∀ T : MUTriple d, ∃ c ∈ s, T ∈ Uc c)
    (hbound : ∀ c ∈ s, ∀ T ∈ Uc c, ε c ≤ psiVal T)
    (hpos : ∀ c ∈ s, 0 < ε c) :
    ¬ FourMUB d := by
  refine no_four_mub_of_psiVal_pos (fun T => ?_)
  exact finite_cover_no_feasible s Uc psiVal Set.univ (fun T _ => hcover T) ε
    (fun c hc T hT => hbound c hc T hT) hpos T (Set.mem_univ T)

/-- **ASSEMBLY (completeness).** When MU triples exist, pointwise positivity of the
obstruction yields a *uniform* positive gap — so the finite-cover approach is
complete (a finite certified cover always exists when the reduction's hypothesis
holds). `Nonempty (MUTriple d)` is the cited existence of an MU triple (for d = 6 the
Invariant-Systems canonical triple). -/
theorem psiVal_uniform_of_pos [Nonempty (MUTriple d)]
    (h : ∀ T : MUTriple d, 0 < psiVal T) :
    ∃ ε, 0 < ε ∧ ∀ T : MUTriple d, ε ≤ psiVal T :=
  uniform_pos_of_pointwise_pos psiVal continuous_psiVal h

/-! ### The d = 6 instance (the smallest open case) -/

/-- The MU-triple space of ℂ⁶. -/
abbrev MUTriple6 := MUTriple 6

/-- Four MUBs in ℂ⁶. -/
abbrev FourMUB6 := FourMUB 6

/-- **The d = 6 reduction.** Strict positivity of `psiVal` on every MU triple of ℂ⁶
implies no four MUBs in ℂ⁶ (MUB(6) ≤ 3). The hypothesis is the open core. -/
theorem no_four_mub6_of_psiVal_pos (h : ∀ T : MUTriple6, 0 < psiVal T) :
    ¬ FourMUB6 :=
  no_four_mub_of_psiVal_pos h

end MUB.TripleExtensionAssembly

#print axioms MUB.TripleExtensionAssembly.no_four_mub_of_psiVal_pos
#print axioms MUB.TripleExtensionAssembly.continuous_psiVal
#print axioms MUB.TripleExtensionAssembly.no_four_mub_of_finite_cover
#print axioms MUB.TripleExtensionAssembly.psiVal_uniform_of_pos
#print axioms MUB.TripleExtensionAssembly.no_four_mub6_of_psiVal_pos
