import GtfdaAuthorityCore

/-!
Axiom audit for the FDA authority-core firewall.
-/

#check GTFDA.DescentPacket
#check GTFDA.DeclaredTraceProjection
#check GTFDA.HaltGuards
#check GTFDA.IsAuth
#check GTFDA.Authority
#check GTFDA.GeneratedCandidate

#print axioms GTFDA.uniform_non_creation
#print axioms GTFDA.authority_non_construction
#print axioms GTFDA.refusal_non_creation
#print axioms GTFDA.authority_non_generation
#print axioms GTFDA.failed_guard_non_creation

#check GTFDA.SuppliedAuthority
#print axioms GTFDA.missing_supplied_packet_non_creation
