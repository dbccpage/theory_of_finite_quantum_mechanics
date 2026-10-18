/-
  H017ExtrasDropone -- declared census of the frozen remaining
  extras for ordinary M_n(C).
  AuthorityEffect: None. Candidate only. Not PROVEN.

  Frozen extra list: paper §7.2 items 1–8 at merge SHA
  dba1434b398153fefeb7a8277b0a9e7b6f59602a. H017Extras names
  seven English remaining extras; a Python dual is a prohibition
  there, not an eighth remaining extra of that file. Paper §7.2
  counts the Python dual as extra 8. Item 9 of that section is
  this census, not an extra. Do not add extras. Do not count
  SUSY or SU(3)×SU(2)×U(1). Do not write a Python dual here.

  dropVerdict is a declared classification table, not an
  assumption-removal interface. For each extra: classified lost
  with current-host obstruction evidence, or OPEN that necessity
  was not shown. Necessity is not a prose table.

  Classified lost, with host obstruction (three):
    field C — invertibility of nonzero scalars (1+i has no inverse);
    spectral extra — every self-adjoint GaussInt matrix has a
      GaussInt eigenvalue (notSpectral has none);
    continuous time — a report-level square root of the toggle.
  Completeness of C is not the invertibility theorem. Unitary
  diagonalization over C is not the GaussInt-eigenvalue theorem.
  Stone / topology is not the half-step theorem.

  OPEN necessity (five): Gleason uniqueness at n ≥ 3; CPTP;
  uniqueness of Hilbert tensor as a combining rule; the circle
  group; a Python dual. Host obstructions already recorded in
  H017Extras (cardinality surrogate, dumpRight rival, sign-exclusion
  survivors) are not these necessity claims.

  This is not M_n(C). The census does not import the extras.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H003ReversibilityGate
import H016ContinuousDynamicsFork
import H017Extras

namespace FableHilbertWalk20260819.H017ExtrasDropone

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H017Extras

/-- Frozen extra list, paper §7.2 items 1–8 at
    dba1434b398153fefeb7a8277b0a9e7b6f59602a. -/
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

/-- Declared census label: classified lost with current-host
    obstruction evidence, or OPEN. Not an assumption-removal
    interface. -/
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

/-- Classified lost with current-host obstruction evidence:
    GaussInt is not a field. Completeness of C is not this. -/
theorem drop_fieldC_loses_inverses :
    dropVerdict FrozenExtra.fieldC = DropVerdict.lost ∧
      ¬ IsFieldPack gaussPack :=
  ⟨rfl, gauss_not_a_field⟩

#print axioms drop_fieldC_loses_inverses

/-- Classified lost with current-host obstruction evidence: a
    self-adjoint GaussInt matrix need not have a GaussInt
    eigenvalue. Unitary diagonalization over C is not this. -/
theorem drop_spectral_loses_gauss_eigenvalues :
    dropVerdict FrozenExtra.spectral = DropVerdict.lost ∧
      ¬ SpectralEigenvalueExtra enumBool :=
  ⟨rfl, spectral_eigenvalue_extra_fails_on_two_label⟩

#print axioms drop_spectral_loses_gauss_eigenvalues

/-- Classified lost with current-host obstruction evidence: the
    toggle has no report-level square root. Topology, a
    one-parameter group, and Stone are not this. -/
theorem drop_continuousTime_loses_report_half_step :
    dropVerdict FrozenExtra.continuousTime = DropVerdict.lost ∧
      (¬ ∃ σ : Bool → Bool,
        ∀ q : Bool, σ (σ q) = FableHilbertWalk20260819.H003.toggle q) :=
  ⟨rfl, FableHilbertWalk20260819.H016.no_report_half_step⟩

#print axioms drop_continuousTime_loses_report_half_step

/-- OPEN: Gleason uniqueness at n ≥ 3 is not shown necessary.
    The two-label cardinality surrogate is H017Gleason, not this. -/
theorem drop_gleasonUniqueness_necessity_open :
    dropVerdict FrozenExtra.gleasonUniqueness = DropVerdict.open :=
  rfl

#print axioms drop_gleasonUniqueness_necessity_open

/-- OPEN: CPTP is not shown necessary. H015 prices collapse
    without a channel class. -/
theorem drop_cptp_necessity_open :
    dropVerdict FrozenExtra.cptp = DropVerdict.open :=
  rfl

#print axioms drop_cptp_necessity_open

/-- OPEN: uniqueness of Hilbert tensor is not shown necessary.
    The weaker CombiningEmbed rival is H014Interface, not this. -/
theorem drop_uniqueTensor_necessity_open :
    dropVerdict FrozenExtra.uniqueTensor = DropVerdict.open :=
  rfl

#print axioms drop_uniqueTensor_necessity_open

/-- OPEN: the circle group is not shown necessary. Sign-exclusion
    survivors are H011Circle, not this. -/
theorem drop_circle_necessity_open :
    dropVerdict FrozenExtra.circle = DropVerdict.open :=
  rfl

#print axioms drop_circle_necessity_open

/-- OPEN: a Python dual is not shown necessary. This run does not
    write one. -/
theorem drop_pythonDual_necessity_open :
    dropVerdict FrozenExtra.pythonDual = DropVerdict.open :=
  rfl

#print axioms drop_pythonDual_necessity_open

/-- Punchline: declared census of eight extras, no duplicates,
    every extra appears. Three are classified lost with
    current-host obstruction evidence. Five are OPEN. Not an
    assumption-removal interface. This is not M_n(C). -/
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

/-- The count does not recover ordinary M_n(C): five extras remain
    OPEN as necessity, and the extras themselves are not imported. -/
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
