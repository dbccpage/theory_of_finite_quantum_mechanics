/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 5713213024bcd74fdadfb0dd0895b5efb13b35cd198e6a0328f9ad83f0c93223 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.Succession
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WitnessedDifference.WitnessedDifference.Core

/-!
# Typed succession paths and additive duration

The edge relation and edge weights are declared data. No continuum or clock
interpretation is inferred.
-/

namespace WitnessedDifference

inductive FinitePath {Vertex : Type _}
    (Next : Vertex → Vertex → Prop) : Vertex → Vertex → Type _ where
  | nil (vertex : Vertex) : FinitePath Next vertex vertex
  | cons {a b c : Vertex} (step : Next a b)
      (tail : FinitePath Next b c) : FinitePath Next a c

namespace FinitePath

def append {Vertex : Type _} {Next : Vertex → Vertex → Prop}
    {a b c : Vertex} :
    FinitePath Next a b → FinitePath Next b c → FinitePath Next a c
  | .nil _, suffix => suffix
  | .cons step tail, suffix => .cons step (append tail suffix)

theorem append_assoc
    {Vertex : Type _} {Next : Vertex → Vertex → Prop}
    {a b c d : Vertex}
    (first : FinitePath Next a b)
    (second : FinitePath Next b c)
    (third : FinitePath Next c d) :
    append (append first second) third =
      append first (append second third) := by
  induction first with
  | nil => rfl
  | cons step tail ih =>
      simp only [append]
      rw [ih]

def duration
    {Vertex R : Type _} {Next : Vertex → Vertex → Prop} [AddMonoid R]
    (weight : ∀ {a b : Vertex}, Next a b → R) :
    {a b : Vertex} → FinitePath Next a b → R
  | _, _, .nil _ => 0
  | _, _, .cons step tail => weight step + duration weight tail

theorem duration_append
    {Vertex R : Type _} {Next : Vertex → Vertex → Prop} [AddMonoid R]
    (weight : ∀ {a b : Vertex}, Next a b → R)
    {a b c : Vertex}
    (first : FinitePath Next a b) (second : FinitePath Next b c) :
    duration weight (append first second) =
      duration weight first + duration weight second := by
  induction first with
  | nil => simp [append, duration, AddMonoid.zero_add]
  | cons step tail ih =>
      simp [append, duration, ih, AddMonoid.add_assoc]

def potentialWeight
    {Vertex R : Type _} {Next : Vertex → Vertex → Prop} [Sub R]
    (potential : Vertex → R) {a b : Vertex} (_step : Next a b) : R :=
  potential b - potential a

theorem duration_potential
    {Vertex R : Type _} {Next : Vertex → Vertex → Prop} [AddCommGroup R]
    (potential : Vertex → R) {a b : Vertex}
    (path : FinitePath Next a b) :
    duration (potentialWeight potential) path = potential b - potential a := by
  induction path with
  | nil vertex =>
      change (0 : R) = potential vertex - potential vertex
      exact (AddCommGroup.sub_self (potential vertex)).symm
  | cons step tail ih =>
      simp only [duration, potentialWeight]
      rw [ih]
      exact AddCommGroup.telescope (potential _) (potential _) (potential _)

theorem exact_duration_path_independent
    {Vertex R : Type _} {Next : Vertex → Vertex → Prop} [AddCommGroup R]
    (potential : Vertex → R) {a b : Vertex}
    (first second : FinitePath Next a b) :
    duration (potentialWeight potential) first =
      duration (potentialWeight potential) second := by
  rw [duration_potential, duration_potential]

end FinitePath

/-!
# Constitutive succession and M3 separation

Mechanizes immediate incidence, K11 edge/join witnesses, M3 closed-witness refusal,
and immediate-succession signatures, proving separation between constitutive order
and immediate succession on the three-cut carrier Chain3.
-/

universe u

structure IncidencePacket (Cut : Type u) where
  immediate : Cut -> Cut -> Prop

inductive K11Witness {Cut : Type u} (P : IncidencePacket Cut) :
    Cut -> Cut -> Prop where
  | edge {a b : Cut} : P.immediate a b -> K11Witness P a b
  | join {a b c : Cut} :
      K11Witness P a b -> K11Witness P b c -> K11Witness P a c

def ConstitutiveOrder {Cut : Type u} (P : IncidencePacket Cut)
    (a b : Cut) : Prop :=
  Nonempty (K11Witness P a b)

structure M3 {Cut : Type u} (P : IncidencePacket Cut) : Prop where
  noSelf : forall a : Cut, Not (P.immediate a a)
  noClosed : forall a : Cut, Not (K11Witness P a a)

structure RecurrenceSignature {Cut : Type u} (P : IncidencePacket Cut) where
  regRec : Cut -> Cut -> Prop
  registration_grounded :
    forall {a b : Cut}, regRec a b -> P.immediate a b

def ImmediateSuccession {Cut : Type u} (P : IncidencePacket Cut)
    (Sigma : RecurrenceSignature P) (b a : Cut) : Prop :=
  Sigma.regRec a b

theorem constitutiveOrder_trans {Cut : Type u}
    (P : IncidencePacket Cut) {a b c : Cut} :
    ConstitutiveOrder P a b ->
    ConstitutiveOrder P b c ->
    ConstitutiveOrder P a c := by
  intro hab hbc
  rcases hab with ⟨wab⟩
  rcases hbc with ⟨wbc⟩
  exact ⟨K11Witness.join wab wbc⟩

theorem constitutiveOrder_irrefl_of_m3 {Cut : Type u}
    {P : IncidencePacket Cut} (hM3 : M3 P) (a : Cut) :
    Not (ConstitutiveOrder P a a) := by
  intro h
  rcases h with ⟨w⟩
  exact hM3.noClosed a w

theorem immediateSuccession_irrefl_of_m3 {Cut : Type u}
    {P : IncidencePacket Cut} (hM3 : M3 P)
    (Sigma : RecurrenceSignature P) (a : Cut) :
    Not (ImmediateSuccession P Sigma a a) := by
  intro h
  exact hM3.noSelf a (Sigma.registration_grounded h)

theorem immediateSuccession_asymm_of_m3 {Cut : Type u}
    {P : IncidencePacket Cut} (hM3 : M3 P)
    (Sigma : RecurrenceSignature P) {a b : Cut} :
    ImmediateSuccession P Sigma b a ->
    Not (ImmediateSuccession P Sigma a b) := by
  intro hba hab
  have wab : K11Witness P a b :=
    K11Witness.edge (Sigma.registration_grounded hba)
  have wba : K11Witness P b a :=
    K11Witness.edge (Sigma.registration_grounded hab)
  exact hM3.noClosed a (K11Witness.join wab wba)

theorem constitutive_arrow_under_closed_witness_free_admission {Cut : Type u}
    {P : IncidencePacket Cut} (hM3 : M3 P)
    (Sigma : RecurrenceSignature P) {a b : Cut} :
    ImmediateSuccession P Sigma b a ->
    Not (ImmediateSuccession P Sigma a b) :=
  immediateSuccession_asymm_of_m3 hM3 Sigma

inductive Chain3 where
  | alpha
  | beta
  | gamma
deriving DecidableEq, Repr

inductive ChainImmediate : Chain3 -> Chain3 -> Prop where
  | alpha_beta : ChainImmediate Chain3.alpha Chain3.beta
  | beta_gamma : ChainImmediate Chain3.beta Chain3.gamma

def chainPacket : IncidencePacket Chain3 where
  immediate := ChainImmediate

def chainSigma : RecurrenceSignature chainPacket where
  regRec := ChainImmediate
  registration_grounded := by
    intro a b h
    exact h

theorem chain_beta_succeeds_alpha :
    ImmediateSuccession chainPacket chainSigma Chain3.beta Chain3.alpha := by
  exact ChainImmediate.alpha_beta

theorem chain_gamma_succeeds_beta :
    ImmediateSuccession chainPacket chainSigma Chain3.gamma Chain3.beta := by
  exact ChainImmediate.beta_gamma

theorem chain_gamma_does_not_immediately_succeed_alpha :
    Not (ImmediateSuccession chainPacket chainSigma Chain3.gamma Chain3.alpha) := by
  intro h
  cases h

theorem immediateSuccession_not_transitive_witness :
    ImmediateSuccession chainPacket chainSigma Chain3.beta Chain3.alpha ∧
      ImmediateSuccession chainPacket chainSigma Chain3.gamma Chain3.beta ∧
      Not (ImmediateSuccession chainPacket chainSigma Chain3.gamma Chain3.alpha) := by
  exact ⟨chain_beta_succeeds_alpha, chain_gamma_succeeds_beta,
    chain_gamma_does_not_immediately_succeed_alpha⟩

def Chain3.rank : Chain3 -> Nat
  | Chain3.alpha => 0
  | Chain3.beta => 1
  | Chain3.gamma => 2

theorem chain_k11_rank_strictly_increases {a b : Chain3} :
    K11Witness chainPacket a b -> Chain3.rank a < Chain3.rank b := by
  intro w
  induction w with
  | edge h => cases h <;> decide
  | join _ _ ih1 ih2 => exact Nat.lt_trans ih1 ih2

theorem chainPacket_m3 : M3 chainPacket := by
  constructor
  · intro a h
    cases h
  · intro a w
    exact Nat.lt_irrefl (Chain3.rank a) (chain_k11_rank_strictly_increases w)

theorem chain_alpha_constitutively_precedes_gamma :
    ConstitutiveOrder chainPacket Chain3.alpha Chain3.gamma :=
  ⟨K11Witness.join
    (K11Witness.edge ChainImmediate.alpha_beta)
    (K11Witness.edge ChainImmediate.beta_gamma)⟩

theorem chain_constitutive_order_separates_immediate_succession :
    ConstitutiveOrder chainPacket Chain3.alpha Chain3.gamma ∧
      Not (ImmediateSuccession chainPacket chainSigma Chain3.gamma Chain3.alpha) :=
  ⟨chain_alpha_constitutively_precedes_gamma,
   chain_gamma_does_not_immediately_succeed_alpha⟩

end WitnessedDifference

