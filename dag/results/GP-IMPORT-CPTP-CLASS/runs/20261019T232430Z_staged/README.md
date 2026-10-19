# GP-IMPORT-CPTP-CLASS

System-first bits index(q,ancilla)=2q+ancilla; ancilla startsfalse. Exhaust all24 permutations, retain exactly the reversible maps whose prepared outputs have systemfalse, and independently compute the reset channel Choi matrix, its output partial trace and reset action. These are constructive CP/TP controls, not claims that collapse noninvertibility obstructs CPTP. Output layout: count;four(map4,inverse4);Choi16;partial_trace4;reset_output4

Supported: Four actual reversible dilation maps/inverses and exact reset-channel Choi/TP/action arrays, with generic inverse and reset trace identities in Lean.

Remaining: Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential.

Every executed checkpoint retains an operad delta, source/candidate bindings and actual host results. This is local file-based PFP execution, not an external-provider transcript. No whole-repository or hosted-CI success is claimed. Awaiting the requested batch review. AuthorityEffect: None.
