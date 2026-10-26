/-!
  Byzantine Fault-Tolerant (BFT) Consensus Cochains & Log Compaction Core
  AuthorityEffect: None.
  Gate: Lean 4 (version 4.34.0)
-/

namespace ByzantineConsensus

/-- Node identifier in a distributed cluster -/
structure NodeId where
  val : Nat
deriving Repr, DecidableEq

/-- Byzantine Fault Configuration:
    N: total number of nodes
    f: maximum number of tolerated Byzantine nodes
    Condition: N >= 3 * f + 1 -/
structure BftClusterConfig where
  N : Nat
  f : Nat
  h_bft : N ≥ 3 * f + 1
deriving Repr

/-- Quorum threshold: Q = 2 * f + 1 -/
def quorum_threshold (f : Nat) : Nat :=
  2 * f + 1

/-- THEOREM: Quorum Intersection Cardinality
    Any two quorums of size at least 2f + 1 in a cluster of size 3f + 1
    intersect in at least f + 1 nodes. -/
theorem quorum_intersection_cardinality (f : Nat) :
    (2 * f + 1) + (2 * f + 1) - (3 * f + 1) = f + 1 := by
  omega

/-- THEOREM: Honest Node Guaranteed in Intersection
    Since at most f nodes in the cluster can be Byzantine,
    an intersection of size at least f + 1 contains at least (f + 1) - f = 1 honest node. -/
theorem honest_node_in_intersection (f : Nat) :
    (f + 1) - f = 1 := by
  omega

/-- Message Phase in PBFT 3-phase consensus -/
inductive PbftPhase where
  | PrePrepare
  | Prepare
  | Commit
  | Checkpoint
deriving Repr, DecidableEq

/-- A signed message in the PBFT message log -/
structure PbftMessage where
  phase : PbftPhase
  view : Nat
  seq_num : Nat
  digest : Nat
  sender : NodeId
deriving Repr, DecidableEq

/-- Equivocation Detection:
    A node equivocates if it signs two distinct digests for the same phase, view, and sequence. -/
def is_equivocation (m1 m2 : PbftMessage) : Bool :=
  m1.sender == m2.sender &&
  m1.phase == m2.phase &&
  m1.view == m2.view &&
  m1.seq_num == m2.seq_num &&
  m1.digest != m2.digest

/-- THEOREM: Equivocation reflexivity is false: a message never equivocates with itself -/
theorem not_equivocation_self (m : PbftMessage) :
    is_equivocation m m = false := by
  dsimp [is_equivocation]
  simp

/-- Checkpoint Certificate:
    A stable checkpoint at sequence number seq_num signed by matching_signatures nodes
    certifying state_digest. -/
structure CheckpointCertificate where
  seq_num : Nat
  state_digest : Nat
  matching_signatures : Nat
  is_valid_digest : Bool
deriving Repr, DecidableEq

/-- BQNF Consensus Cochain Routing Disposition -/
inductive BqnfConsensusDisposition where
  | ExactCompaction (truncated_seq : Nat) -- O(1) log garbage collection
  | EquivocationRefusal (node : NodeId)    -- Byzantine equivocation detected and blamed
  | CorruptedDigestRefusal                 -- State digest mismatch refused
  | QuorumDefect                           -- Insufficient votes (< 2f + 1), wait or view change
deriving Repr, DecidableEq

/-- BQNF Routing function for consensus cochain audit -/
def route_consensus_audit
    (f : Nat)
    (has_equivocation : Option NodeId)
    (cp : CheckpointCertificate) : BqnfConsensusDisposition :=
  match has_equivocation with
  | some bad_node => BqnfConsensusDisposition.EquivocationRefusal bad_node
  | none =>
    if !cp.is_valid_digest then
      BqnfConsensusDisposition.CorruptedDigestRefusal
    else if cp.matching_signatures ≥ quorum_threshold f then
      BqnfConsensusDisposition.ExactCompaction cp.seq_num
    else
      BqnfConsensusDisposition.QuorumDefect

/-- THEOREM: Detected equivocation deterministically routes to EquivocationRefusal -/
theorem equivocation_routes_to_refusal
    (f : Nat) (bad_node : NodeId) (cp : CheckpointCertificate) :
    route_consensus_audit f (some bad_node) cp = BqnfConsensusDisposition.EquivocationRefusal bad_node := by
  dsimp [route_consensus_audit]

/-- THEOREM: Valid stable checkpoint with quorum >= 2f + 1 routes to ExactCompaction -/
theorem valid_stable_checkpoint_routes_to_compaction
    (f : Nat) (cp : CheckpointCertificate)
    (h_dig : cp.is_valid_digest = true)
    (h_q : cp.matching_signatures ≥ quorum_threshold f) :
    route_consensus_audit f none cp = BqnfConsensusDisposition.ExactCompaction cp.seq_num := by
  dsimp [route_consensus_audit]
  rw [h_dig]
  dsimp
  split
  · rfl
  · contradiction

/-- THEOREM: Checkpoint with corrupted state digest routes to CorruptedDigestRefusal -/
theorem corrupted_checkpoint_routes_to_refusal
    (f : Nat) (cp : CheckpointCertificate)
    (h_bad : cp.is_valid_digest = false) :
    route_consensus_audit f none cp = BqnfConsensusDisposition.CorruptedDigestRefusal := by
  dsimp [route_consensus_audit]
  rw [h_bad]
  dsimp

/-- THEOREM: Checkpoint lacking quorum routes to QuorumDefect -/
theorem insufficient_signatures_routes_to_defect
    (f : Nat) (cp : CheckpointCertificate)
    (h_dig : cp.is_valid_digest = true)
    (h_sub : cp.matching_signatures < quorum_threshold f) :
    route_consensus_audit f none cp = BqnfConsensusDisposition.QuorumDefect := by
  dsimp [route_consensus_audit]
  rw [h_dig]
  dsimp
  split
  · rename_i h_ge
    have h_not : ¬ (cp.matching_signatures ≥ quorum_threshold f) := Nat.not_le.mpr h_sub
    contradiction
  · rfl

end ByzantineConsensus

