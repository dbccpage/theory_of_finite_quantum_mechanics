/-!
# CODA-OR D01/D02: Records for Comparison Envelopes and Diagram Obstructions

Formalizes:
1. Weight classes W and Representation Regimes Reg_chi.
2. Comparison Objects X in Comp_W(Reg_chi).
3. Authority-Support Sieves Supp_Auth(X) with explicit target-binding invariants.
4. Enriched Comparison Complex E = (C0, C1, C2, d0, d1) with d1 circ d0 = 0.
5. Four-case square classification inductive type.

AuthorityEffect: None.
-/

namespace CodaOr

/-- Weight class specification for weighted limits and completions (OR-D3). -/
structure WeightClass where
  name : String
  is_finite : Bool
  deriving Repr, DecidableEq

/-- A certified representation regime A in Reg_chi (CODA-MUR). -/
structure RepresentationRegime where
  regime_id : String
  has_authority : Bool
  deriving Repr, DecidableEq

/-- A support arrow u: A -> X into comparison object X. -/
structure SupportArrow where
  source_id : String
  target_id : String
  source_has_authority : Bool
  has_descent_certificate : Bool
  deriving Repr, DecidableEq

/-- An arrow is validly in the certified authority-support sieve if source has authority
    and the descent compatibility certificate chi_u is valid. -/
def SupportArrow.is_auth_supporting (u : SupportArrow) : Bool :=
  u.source_has_authority && u.has_descent_certificate

/-- Target-bound support arrow: checks target agreement with declared target id. -/
def SupportArrow.is_auth_supporting_for (u : SupportArrow) (target : String) : Bool :=
  u.target_id == target && u.source_has_authority && u.has_descent_certificate

/-- Authority-support sieve Supp_Auth(X) as a collection of incoming certified arrows. -/
structure SupportSieve where
  target_id : String
  arrows : List SupportArrow
  deriving Repr

/-- Target-binding condition asserting all arrows in the sieve target the sieve's target. -/
def SupportSieve.targetBound (s : SupportSieve) : Prop :=
  ∀ u ∈ s.arrows, u.target_id = s.target_id

/-- A support sieve is empty if no incoming arrow is auth-supporting (OR-T5). -/
def SupportSieve.isEmpty (s : SupportSieve) : Prop :=
  ∀ u ∈ s.arrows, u.is_auth_supporting = false

/-- Comparison object X in Omega_O := Comp_W(Reg_chi) (OR-D3). -/
structure ComparisonObject where
  object_id : String
  weight_class : WeightClass
  support_sieve : SupportSieve
  has_local_terminalizer : Bool
  has_descent_triplet : Bool
  deriving Repr

/-- Object-sieve target binding asserting that the sieve target matches the comparison object id. -/
def ComparisonObject.sieveTargetBound (X : ComparisonObject) : Prop :=
  X.support_sieve.target_id = X.object_id ∧ X.support_sieve.targetBound

/-- Object-level authority declaration payload.
    NOTE (Claim Hygiene / Review Finding 5):
    This structure stores the witness string payloads emitted upon authorization.
    It is a declaration payload, NOT mathematical evidence that `HasAuthority X` holds.
    Standing is established solely by the predicate `HasAuthority X`. -/
structure AuthorityRecord (X : ComparisonObject) where
  descent_witness : String
  verifier_witness : String
  terminal_state : String

/-- Authority predicate on comparison objects (OR-D3 / OR-T5).
    Refinement Note: In Python, the default evaluator additionally checks
    `require_all_sources=true` (every listed arrow must carry standing).
    Lean `HasAuthority` requires that at least one arrow carries standing (non-empty sieve).
    For well-formed names and weight declarations, `require_all_sources=false` uses the same support and target-binding conditions. -/
def HasAuthority (X : ComparisonObject) : Prop :=
  ¬ X.support_sieve.isEmpty ∧
  X.has_local_terminalizer = true ∧
  X.has_descent_triplet = true ∧
  X.sieveTargetBound

/-- Four-case square defect classification (OR-D2, OR-T4). -/
inductive SquareStatus where
  | strict_commute
  | weak_commute_certified
  | h1_diagram_tear
  | open_diagram_obstruction
  deriving Repr, DecidableEq

/-- Enriched comparison environment complex E = (C0, C1, C2, d0, d1) with d1 circ d0 = 0. -/
structure EnrichedComplex (C0 C1 C2 : Type) where
  zero0 : C0
  zero1 : C1
  zero2 : C2
  d0 : C0 → C1
  d1 : C1 → C2
  d0_zero : d0 zero0 = zero1
  d1_zero : d1 zero1 = zero2
  complex_condition : ∀ x : C0, d1 (d0 x) = zero2

end CodaOr
