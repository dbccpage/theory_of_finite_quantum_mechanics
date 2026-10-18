






import HWKernel
import H003ReversibilityGate
import H016ContinuousDynamicsFork
import H017Extras

namespace FableHilbertWalk20260819.H017ExtrasDropone

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H017Extras

inductive FrozenExtra
  | fieldC
  | spectral
  | gleasonUniqueness
  | cptp
  | uniqueTensor
  | circle
  | continuousTime
  | pythonDual
  deriving DecidableEq, Repr

inductive DropVerdict
  | lost
  | open
  deriving DecidableEq, Repr

def dropVerdict : FrozenExtra → DropVerdict
  | FrozenExtra.fieldC => DropVerdict.lost
  | FrozenExtra.spectral => DropVerdict.lost
  | FrozenExtra.gleasonUniqueness => DropVerdict.open
  | FrozenExtra.cptp => DropVerdict.open
  | FrozenExtra.uniqueTensor => DropVerdict.open
  | FrozenExtra.circle => DropVerdict.open
  | FrozenExtra.continuousTime => DropVerdict.lost
  | FrozenExtra.pythonDual => DropVerdict.open

def allExtras : List FrozenExtra :=
  [FrozenExtra.fieldC, FrozenExtra.spectral,
    FrozenExtra.gleasonUniqueness, FrozenExtra.cptp,
    FrozenExtra.uniqueTensor, FrozenExtra.circle,
    FrozenExtra.continuousTime, FrozenExtra.pythonDual]

def lostExtras : List FrozenExtra :=
  [FrozenExtra.fieldC, FrozenExtra.spectral,
    FrozenExtra.continuousTime]

def openExtras : List FrozenExtra :=
  [FrozenExtra.gleasonUniqueness, FrozenExtra.cptp,
    FrozenExtra.uniqueTensor, FrozenExtra.circle,
    FrozenExtra.pythonDual]

theorem extra_list_length : allExtras.length = 8 :=
  rfl

#print axioms extra_list_length

theorem lost_length : lostExtras.length = 3 :=
  rfl

#print axioms lost_length

theorem open_length : openExtras.length = 5 :=
  rfl

#print axioms open_length

theorem extras_complete (e : FrozenExtra) : e ∈ allExtras := by
  cases e <;> decide

#print axioms extras_complete

theorem extras_nodup : allExtras.Nodup := by
  decide

#print axioms extras_nodup

theorem lost_or_open (e : FrozenExtra) :
    dropVerdict e = DropVerdict.lost ∨
      dropVerdict e = DropVerdict.open := by
  cases e <;> decide

#print axioms lost_or_open

theorem mem_lost_iff (e : FrozenExtra) :
    e ∈ lostExtras ↔ dropVerdict e = DropVerdict.lost := by
  cases e <;> decide

#print axioms mem_lost_iff

theorem mem_open_iff (e : FrozenExtra) :
    e ∈ openExtras ↔ dropVerdict e = DropVerdict.open := by
  cases e <;> decide

#print axioms mem_open_iff

theorem drop_fieldC_loses_inverses :
    dropVerdict FrozenExtra.fieldC = DropVerdict.lost ∧
      ¬ IsFieldPack gaussPack :=
  ⟨rfl, gauss_not_a_field⟩

#print axioms drop_fieldC_loses_inverses

theorem drop_spectral_loses_gauss_eigenvalues :
    dropVerdict FrozenExtra.spectral = DropVerdict.lost ∧
      ¬ SpectralEigenvalueExtra enumBool :=
  ⟨rfl, spectral_eigenvalue_extra_fails_on_two_label⟩

#print axioms drop_spectral_loses_gauss_eigenvalues

theorem drop_continuousTime_loses_report_half_step :
    dropVerdict FrozenExtra.continuousTime = DropVerdict.lost ∧
      (¬ ∃ σ : Bool → Bool,
        ∀ q : Bool, σ (σ q) = FableHilbertWalk20260819.H003.toggle q) :=
  ⟨rfl, FableHilbertWalk20260819.H016.no_report_half_step⟩

#print axioms drop_continuousTime_loses_report_half_step

theorem drop_gleasonUniqueness_necessity_open :
    dropVerdict FrozenExtra.gleasonUniqueness = DropVerdict.open :=
  rfl

#print axioms drop_gleasonUniqueness_necessity_open

theorem drop_cptp_necessity_open :
    dropVerdict FrozenExtra.cptp = DropVerdict.open :=
  rfl

#print axioms drop_cptp_necessity_open

theorem drop_uniqueTensor_necessity_open :
    dropVerdict FrozenExtra.uniqueTensor = DropVerdict.open :=
  rfl

#print axioms drop_uniqueTensor_necessity_open

theorem drop_circle_necessity_open :
    dropVerdict FrozenExtra.circle = DropVerdict.open :=
  rfl

#print axioms drop_circle_necessity_open

theorem drop_pythonDual_necessity_open :
    dropVerdict FrozenExtra.pythonDual = DropVerdict.open :=
  rfl

#print axioms drop_pythonDual_necessity_open

theorem drop_one_count :
    allExtras.length = 8 ∧
      allExtras.Nodup ∧
      (∀ e : FrozenExtra, e ∈ allExtras) ∧
      lostExtras.length = 3 ∧
      openExtras.length = 5 ∧
      (∀ e : FrozenExtra,
        e ∈ lostExtras ↔ dropVerdict e = DropVerdict.lost) ∧
      (∀ e : FrozenExtra,
        e ∈ openExtras ↔ dropVerdict e = DropVerdict.open) ∧
      (dropVerdict FrozenExtra.fieldC = DropVerdict.lost ∧
        ¬ IsFieldPack gaussPack) ∧
      (dropVerdict FrozenExtra.spectral = DropVerdict.lost ∧
        ¬ SpectralEigenvalueExtra enumBool) ∧
      (dropVerdict FrozenExtra.continuousTime = DropVerdict.lost ∧
        (¬ ∃ σ : Bool → Bool,
          ∀ q : Bool,
            σ (σ q) = FableHilbertWalk20260819.H003.toggle q)) ∧
      dropVerdict FrozenExtra.gleasonUniqueness = DropVerdict.open ∧
      dropVerdict FrozenExtra.cptp = DropVerdict.open ∧
      dropVerdict FrozenExtra.uniqueTensor = DropVerdict.open ∧
      dropVerdict FrozenExtra.circle = DropVerdict.open ∧
      dropVerdict FrozenExtra.pythonDual = DropVerdict.open :=
  ⟨extra_list_length, extras_nodup, extras_complete,
    lost_length, open_length, mem_lost_iff, mem_open_iff,
    drop_fieldC_loses_inverses, drop_spectral_loses_gauss_eigenvalues,
    drop_continuousTime_loses_report_half_step,
    drop_gleasonUniqueness_necessity_open, drop_cptp_necessity_open,
    drop_uniqueTensor_necessity_open, drop_circle_necessity_open,
    drop_pythonDual_necessity_open⟩

#print axioms drop_one_count

theorem drop_one_is_not_ordinary_mnC :
    dropVerdict FrozenExtra.gleasonUniqueness = DropVerdict.open ∧
      dropVerdict FrozenExtra.cptp = DropVerdict.open ∧
      dropVerdict FrozenExtra.uniqueTensor = DropVerdict.open ∧
      dropVerdict FrozenExtra.circle = DropVerdict.open ∧
      dropVerdict FrozenExtra.pythonDual = DropVerdict.open :=
  ⟨drop_gleasonUniqueness_necessity_open, drop_cptp_necessity_open,
    drop_uniqueTensor_necessity_open, drop_circle_necessity_open,
    drop_pythonDual_necessity_open⟩

#print axioms drop_one_is_not_ordinary_mnC

end FableHilbertWalk20260819.H017ExtrasDropone

private def l5aProvenance : String :=
  "Origin: lean4/H017ExtrasDropone.lean Claim: extra_list_length AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
