/-!
Bounded FDA authority core.

This module defines the authority-facing five-field packet, the seven halt
guards, and the dependent authority witness. It formalizes definitional
firewalls: no packet, no authority-bearing terminalizer path, a refusal path,
or a generated candidate without that path cannot inhabit `Authority`.

It does not model FOC verifier soundness, construct an admissible packet,
derive the full trace-packet projection, or establish a categorical firewall.
-/

namespace GTFDA

universe u

/- Five-field authority-facing descent packet. -/

structure DescentPacket (Terminal : Type u) : Type (u + 1) where
  K : Type u
  E : K -> Type u
  V : (k : K) -> E k -> Type u
  tau : {k : K} -> {e : E k} -> V k e -> Terminal
  Lambda : {k : K} -> (e : E k) -> V k e -> Type u

/-- Countermodel to reading type-level packet emptiness as absent input. -/
def emptyCarrierPacket (Terminal : Type) : DescentPacket Terminal where
  K := Empty
  E := fun _ => Empty
  V := fun _ _ => Empty
  tau := fun {k} {_} _ => Empty.elim k
  Lambda := fun {k} _ _ => Empty.elim k

theorem packet_type_nonempty (Terminal : Type) : Nonempty (DescentPacket Terminal) :=
  ⟨emptyCarrierPacket Terminal⟩

/-
The richer eight-field FOC trace packet remains externally owned and opaque
here. A relationship to the FDA packet exists only when this projection
witness is explicitly supplied; field-name similarity creates no alias.
-/
structure DeclaredTraceProjection
    (TracePacket : Type u)
    (Terminal : Type u) : Type (u + 1) where
  project : TracePacket -> DescentPacket Terminal

/- Seven closed halt guards. -/

structure HaltGuards where
  accepted : Prop
  deterministic : Prop
  zeroResidualMass : Prop
  exhaustive : Prop
  skeletonPreserving : Prop
  noPendingLift : Prop
  noRefusal : Prop

def IsAuth (guards : HaltGuards) : Prop :=
  guards.accepted ∧
    guards.deterministic ∧
    guards.zeroResidualMass ∧
    guards.exhaustive ∧
    guards.skeletonPreserving ∧
    guards.noPendingLift ∧
    guards.noRefusal

abbrev SealedPipeline
    (Proposal Terminal Refusal : Type u) : Type (u + 1) :=
  DescentPacket Terminal -> Proposal -> Sum Terminal Refusal

/-
Authority is a terminal together with the exact pipeline path and the
seven-guard witness. The packet and proposal are indices, not fields that
can be omitted by a caller.
-/
structure Authority
    {Proposal Terminal Refusal : Type u}
    (pipeline : SealedPipeline Proposal Terminal Refusal)
    (guards : Terminal -> HaltGuards)
    (packet : DescentPacket Terminal)
    (proposal : Proposal) : Type (u + 1) where
  terminal : Terminal
  terminalizerPath : pipeline packet proposal = Sum.inl terminal
  isAuth : IsAuth (guards terminal)

/-
A generated candidate may carry a claimed terminal and even a valid guard
witness. It remains definitionally distinct from `Authority` because it has no
pipeline path.
-/
structure GeneratedCandidate
    (Terminal : Type u)
    (guards : Terminal -> HaltGuards) where
  terminal : Terminal
  isAuth : IsAuth (guards terminal)

/- An operational input may omit its packet. This records actual supplied
   input separately from existence of a value of the packet type. -/
structure SuppliedAuthority
    {Proposal Terminal Refusal : Type u}
    (pipeline : SealedPipeline Proposal Terminal Refusal)
    (guards : Terminal -> HaltGuards)
    (input : Option (DescentPacket Terminal))
    (proposal : Proposal) : Type (u + 1) where
  packet : DescentPacket Terminal
  supplied : input = some packet
  authority : Authority pipeline guards packet proposal

theorem missing_supplied_packet_non_creation
    {Proposal Terminal Refusal : Type u}
    (pipeline : SealedPipeline Proposal Terminal Refusal)
    (guards : Terminal -> HaltGuards) (proposal : Proposal) :
    ¬ Nonempty (SuppliedAuthority pipeline guards none proposal) := by
  rintro ⟨standing⟩
  cases standing.supplied

/- Historical type-existence implication. Its premise is never satisfied:
   DescentPacket permits an empty K. It does not model a missing input. -/

theorem uniform_non_creation
    {Proposal Terminal Refusal : Type u}
    (pipeline : SealedPipeline Proposal Terminal Refusal)
    (guards : Terminal -> HaltGuards)
    (hNoPacket : ¬ Nonempty (DescentPacket Terminal)) :
    ¬ ∃ packet : DescentPacket Terminal,
        ∃ proposal : Proposal,
          Nonempty (Authority pipeline guards packet proposal) := by
  rintro ⟨packet, _, _⟩
  exact hNoPacket ⟨packet⟩

/- No authority value exists when every terminal path is absent. -/
theorem authority_non_construction
    {Proposal Terminal Refusal : Type u}
    {pipeline : SealedPipeline Proposal Terminal Refusal}
    {guards : Terminal -> HaltGuards}
    {packet : DescentPacket Terminal}
    {proposal : Proposal}
    (hNoTerminalPath :
      ∀ terminal : Terminal, pipeline packet proposal ≠ Sum.inl terminal) :
    ¬ Nonempty (Authority pipeline guards packet proposal) := by
  rintro ⟨authority⟩
  exact hNoTerminalPath authority.terminal authority.terminalizerPath

/- Encode/decode canary: a refusal branch cannot be authority. -/
theorem refusal_non_creation
    {Proposal Terminal Refusal : Type u}
    {pipeline : SealedPipeline Proposal Terminal Refusal}
    {guards : Terminal -> HaltGuards}
    {packet : DescentPacket Terminal}
    {proposal : Proposal}
    (refusal : Refusal)
    (hRefusal : pipeline packet proposal = Sum.inr refusal) :
    ¬ Nonempty (Authority pipeline guards packet proposal) := by
  apply authority_non_construction
  intro terminal hTerminal
  have hAbsurd :
      (Sum.inr refusal : Sum Terminal Refusal) = Sum.inl terminal :=
    hRefusal.symm.trans hTerminal
  nomatch hAbsurd

/-
Bounded core: even a generated candidate with valid guards cannot be
identified with authority when its exact terminalizer path is absent.
-/
theorem authority_non_generation
    {Proposal Terminal Refusal : Type u}
    {pipeline : SealedPipeline Proposal Terminal Refusal}
    {guards : Terminal -> HaltGuards}
    {packet : DescentPacket Terminal}
    {proposal : Proposal}
    (candidate : GeneratedCandidate Terminal guards)
    (hNoPath : pipeline packet proposal ≠ Sum.inl candidate.terminal) :
    ¬ ∃ authority : Authority pipeline guards packet proposal,
        authority.terminal = candidate.terminal := by
  rintro ⟨authority, hTerminal⟩
  apply hNoPath
  exact authority.terminalizerPath.trans
    (congrArg
      (fun terminal : Terminal => (Sum.inl terminal : Sum Terminal Refusal))
      hTerminal)

/- Seven-guard negative canary, independent of terminalizer-path failure. -/
theorem failed_guard_non_creation
    {Proposal Terminal Refusal : Type u}
    {pipeline : SealedPipeline Proposal Terminal Refusal}
    {guards : Terminal -> HaltGuards}
    {packet : DescentPacket Terminal}
    {proposal : Proposal}
    (terminal : Terminal)
    (hFailed : ¬ IsAuth (guards terminal)) :
    ¬ ∃ authority : Authority pipeline guards packet proposal,
        authority.terminal = terminal := by
  rintro ⟨authority, hTerminal⟩
  apply hFailed
  exact hTerminal ▸ authority.isAuth

end GTFDA
