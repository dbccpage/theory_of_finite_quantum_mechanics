import BellOperad

/- Separator feasibility for binary 2x2 pair data, at a common integer scale.
   This module does not prove the general rational conditional-gluing formula.
   Origin: FQ-BELL-CLASSICAL-JOINT-EXTENSION. AuthorityEffect: None. -/
namespace QuantumMechanics.BellSeparatorExtension

structure PairCounts where
  d : Int
  a : Int
  c : Int
  b0 : Int
  b1 : Int
  x00 : Int
  x01 : Int
  x10 : Int
  x11 : Int

def PairPositive (d a b x : Int) : Prop :=
  0 ≤ x ∧ x ≤ a ∧ x ≤ b ∧ a + b - d ≤ x

-- The four cells are (d-a-b+x, b-x, a-x, x), so these hypotheses
-- encode positivity, common scale, and the shared one-party marginals.
def CompatiblePositive (p : PairCounts) : Prop :=
  0 < p.d ∧ PairPositive p.d p.a p.b0 p.x00 ∧
  PairPositive p.d p.a p.b1 p.x01 ∧ PairPositive p.d p.c p.b0 p.x10 ∧
  PairPositive p.d p.c p.b1 p.x11

def corr (d a b x : Int) : Int := d - 2*a - 2*b + 4*x

def FourCHSH (d e00 e01 e10 e11 : Int) : Prop :=
  (-2*d ≤ -e00+e01+e10+e11 ∧ -e00+e01+e10+e11 ≤ 2*d) ∧
  (-2*d ≤ e00-e01+e10+e11 ∧ e00-e01+e10+e11 ≤ 2*d) ∧
  (-2*d ≤ e00+e01-e10+e11 ∧ e00+e01-e10+e11 ≤ 2*d) ∧
  (-2*d ≤ e00+e01+e10-e11 ∧ e00+e01+e10-e11 ≤ 2*d)

def CHSHFamily (p : PairCounts) : Prop := FourCHSH p.d
  (corr p.d p.a p.b0 p.x00) (corr p.d p.a p.b1 p.x01)
  (corr p.d p.c p.b0 p.x10) (corr p.d p.c p.b1 p.x11)

def lower (d a c b x z : Int) : Int := max 0 (x+z-b) + max 0 (a+c-x-z-d+b)
def upper (a c x z : Int) : Int := min x z + min (a-x) (c-z)

def commonLower (p : PairCounts) : Int := max
  (lower p.d p.a p.c p.b0 p.x00 p.x10)
  (lower p.d p.a p.c p.b1 p.x01 p.x11)

def commonUpper (p : PairCounts) : Int := min
  (upper p.a p.c p.x00 p.x10) (upper p.a p.c p.x01 p.x11)

def HasSeparator (p : PairCounts) : Prop := ∃ r : Int,
  lower p.d p.a p.c p.b0 p.x00 p.x10 ≤ r ∧
  r ≤ upper p.a p.c p.x00 p.x10 ∧
  lower p.d p.a p.c p.b1 p.x01 p.x11 ≤ r ∧
  r ≤ upper p.a p.c p.x01 p.x11

theorem separator_iff_overlap (p : PairCounts) :
    HasSeparator p ↔ commonLower p ≤ commonUpper p := by
  unfold HasSeparator commonLower commonUpper
  constructor
  · rintro ⟨r,h⟩; omega
  · intro h
    refine ⟨max (lower p.d p.a p.c p.b0 p.x00 p.x10)
      (lower p.d p.a p.c p.b1 p.x01 p.x11), ?_⟩
    omega

-- The only remaining real-valued step toward a fully formal converse is NOT
-- hidden here: these are linear integer inequalities and a separator parameter,
-- not yet a normalized four-variable rational distribution.
theorem overlap_iff_chsh (p : PairCounts) (hp : CompatiblePositive p) :
    commonLower p ≤ commonUpper p ↔ CHSHFamily p := by
  simp only [CompatiblePositive, PairPositive] at hp
  simp only [commonLower, commonUpper, lower, upper, CHSHFamily, FourCHSH, corr]
  omega

theorem separator_iff_chsh (p : PairCounts) (hp : CompatiblePositive p) :
    HasSeparator p ↔ CHSHFamily p :=
  (separator_iff_overlap p).trans (overlap_iff_chsh p hp)

def TripleCellsPositive (d a c b x z r t : Int) : Prop :=
  0 ≤ t ∧ t ≤ x ∧ t ≤ z ∧ x+z-b ≤ t ∧
  0 ≤ r-t ∧ r-t ≤ a-x ∧ r-t ≤ c-z ∧
  a+c-x-z-d+b ≤ r-t

-- The two ++B slice counts t and r-t determine all eight triple cells.
-- This establishes existence of nonnegative cells with the requested two-pair
-- marginals and shared ++ separator count, without dividing by a separator.
theorem split_triple_exists (d a c b x z r : Int)
    (h0 : PairPositive d a b x) (h1 : PairPositive d c b z)
    (hr : lower d a c b x z ≤ r ∧ r ≤ upper a c x z) :
    ∃ t : Int, TripleCellsPositive d a c b x z r t := by
  simp only [PairPositive] at h0 h1
  simp only [lower, upper] at hr
  refine ⟨max 0 (max (x+z-b) (max (r-a+x) (r-c+z))), ?_⟩
  unfold TripleCellsPositive
  omega

theorem chsh_has_two_triples (p : PairCounts) (hp : CompatiblePositive p)
    (hc : CHSHFamily p) : ∃ r t0 t1 : Int,
    TripleCellsPositive p.d p.a p.c p.b0 p.x00 p.x10 r t0 ∧
    TripleCellsPositive p.d p.a p.c p.b1 p.x01 p.x11 r t1 := by
  obtain ⟨r,h0,h1,h2,h3⟩ := (separator_iff_chsh p hp).mpr hc
  obtain ⟨_,h00,_,h10,_⟩ := hp
  have h01 : PairPositive p.d p.a p.b1 p.x01 := hp.2.2.1
  have h11 : PairPositive p.d p.c p.b1 p.x11 := hp.2.2.2.2
  obtain ⟨t0,ht0⟩ := split_triple_exists p.d p.a p.c p.b0 p.x00 p.x10 r h00 h10 ⟨h0,h1⟩
  obtain ⟨t1,ht1⟩ := split_triple_exists p.d p.a p.c p.b1 p.x01 p.x11 r h01 h11 ⟨h2,h3⟩
  exact ⟨r,t0,t1,ht0,ht1⟩

open BellClassicalJointExtension BellOperad DerivationDagQMClosure

inductive Facet where
  | minus00 | minus01 | minus10 | minus11

def facetLinear (f : Facet) (e : Four) : Int := match f with
  | .minus00 => -e 0+e 1+e 2+e 3
  | .minus01 => e 0-e 1+e 2+e 3
  | .minus10 => e 0+e 1-e 2+e 3
  | .minus11 => e 0+e 1+e 2-e 3

theorem deterministic_facet_bound (f : Facet) (a : Assignment) :
    -2 ≤ facetLinear f (products a) ∧ facetLinear f (products a) ≤ 2 := by
  rcases a with ⟨a0,a1,b0,b1⟩
  cases f <;> cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide

theorem facet_expectation (f : Facet) (table : Assignment → Four)
    (law : List (Nat × Assignment)) :
    facetLinear f (expect4 table law) = weighted (fun a => facetLinear f (table a)) law := by
  induction law with
  | nil => cases f <;> rfl
  | cons p rest ih =>
    rcases p with ⟨w,a⟩
    cases f <;> simp only [facetLinear, expect4, weighted, Int.mul_add, Int.mul_sub,
      Int.mul_neg] at ih ⊢ <;> omega

theorem full_family_joint_necessity (f : Facet) (law : List (Nat × Assignment)) :
    -2 * mass law ≤ facetLinear f (expect4 products law) ∧
    facetLinear f (expect4 products law) ≤ 2 * mass law := by
  let ws := law.map fun p => (p.1, facetLinear f (products p.2))
  have hb : ∀ p ∈ ws, -2 ≤ p.2 ∧ p.2 ≤ 2 := by
    intro p hp
    obtain ⟨x,_,rfl⟩ := List.mem_map.mp hp
    exact deterministic_facet_bound f x.2
  have hs : weightedChshSum ws = weighted (fun a => facetLinear f (products a)) law := by
    induction law with
    | nil => rfl
    | cons p rest ih => simpa only [ws, List.map_cons, weightedChshSum, weighted] using congrArg ((p.1 : Int) * facetLinear f (products p.2) + ·) ih
  have hm : totalWeight ws = mass law := by
    induction law with
    | nil => rfl
    | cons p rest ih => simpa only [ws, List.map_cons, totalWeight, mass, rows] using congrArg ((p.1 : Int) + ·) ih
  have h := (fq_bell_classical_joint_extension_convex_bound ws hb).2
  rw [hs,hm,← facet_expectation f products law] at h
  exact h

end QuantumMechanics.BellSeparatorExtension

#print axioms QuantumMechanics.BellSeparatorExtension.separator_iff_chsh
#print axioms QuantumMechanics.BellSeparatorExtension.split_triple_exists
#print axioms QuantumMechanics.BellSeparatorExtension.chsh_has_two_triples
#print axioms QuantumMechanics.BellSeparatorExtension.full_family_joint_necessity
