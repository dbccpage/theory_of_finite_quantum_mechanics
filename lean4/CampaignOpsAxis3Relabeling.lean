-- Campaign: OPS-AXIS3-RELABELING. Not a default target.
-- Composition step from a declared export. Hypotheses (i) and (ii) are not used.

def swap01 : Nat → Nat
  | 0 => 1
  | 1 => 0
  | n => n

theorem exportVerdictRelabel
    {Hist Export Verdict : Type}
    (exp : Hist → Export)
    (vbar : Export → Verdict)
    (sigma : Hist → Hist)
    (hExp : ∀ h, exp (sigma h) = exp h)
    (h : Hist) :
    vbar (exp (sigma h)) = vbar (exp h) := by
  rw [hExp h]

theorem lengthMapInvariant (xs : List Nat) (f : Nat → Nat) :
    (xs.map f).length = xs.length := by
  simp

theorem lengthVerdictRelabel
    {Verdict : Type}
    (vbar : Nat → Verdict)
    (xs : List Nat) :
    vbar ((xs.map swap01).length) = vbar xs.length := by
  have hExp : ∀ ys : List Nat, (ys.map swap01).length = ys.length :=
    fun ys => lengthMapInvariant ys swap01
  exact exportVerdictRelabel List.length vbar (List.map swap01) hExp xs

#print axioms exportVerdictRelabel
#print axioms lengthMapInvariant
#print axioms lengthVerdictRelabel
