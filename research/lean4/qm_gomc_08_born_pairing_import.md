namespace QM.GOMC08

/--
A two-sector readout is only the simplex-shaped output data: two
nonnegative weights whose total is one. This is deliberately weaker than a
Born pairing with declared effects.
-/
structure TwoSectorReadout where
  p0 : Nat
  p1 : Nat
  sum_one : p0 + p1 = 1

/-- One declared simplex-shaped readout. -/
def l1NormalizedReadout : TwoSectorReadout where
  p0 := 0
  p1 := 1
  sum_one := rfl

/--
A second simplex-shaped readout, representing an explicitly different
declared pairing/readout rule over the same two-sector carrier.
-/
def declaredAlternativeReadout : TwoSectorReadout where
  p0 := 1
  p1 := 0
  sum_one := rfl

/--
GOMC-08: L1 normalization gives simplex-shaped sector weights, but the
simplex shape alone does not select a unique Born-style pairing/readout.

This is a finite counterexample theorem, not a reconstruction theorem: it
shows non-selection at the bookkeeping layer and forces any Born pairing to be
declared/imported by extra structure.
-/
theorem born_pairing_requires_import :
    ∃ a b : TwoSectorReadout, a ≠ b := by
  refine ⟨l1NormalizedReadout, declaredAlternativeReadout, ?_⟩
  intro h
  have hp0 : (0 : Nat) = 1 := congrArg TwoSectorReadout.p0 h
  exact Nat.zero_ne_one hp0

#print axioms QM.GOMC08.born_pairing_requires_import

end QM.GOMC08
