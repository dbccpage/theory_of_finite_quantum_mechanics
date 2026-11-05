# PROD-P5

## Target
Bind **P5 Continuous Claim-Ledger Certification** (`PROD-P5`) to `omega_engine_woland` via `evaluate_claim_ledger_certification` and `WdpClaimLedgerCertificationAdapter`. Every claim's status is recomputed from its evidence pointers, dependency statuses, and `PROD-P2` numeric provenance gate using the exact 15-to-5 `ClaimStatus` lattice (`VERIFIED`, `BOUNDED_EXTERNAL`, `OPEN_DECLARED`, `UNVERIFIED_WRITTEN`, `INVALID_LINK`, from `PROD-P5-NEXT-1`, `PROD-P5-NEXT-2`, `PROD-P5-KILL`), treating missing pointers as unknown/invalid and attaching a `PROD-KERNEL` SHA-256 receipt.

## Mathematical Formulation

Let $\mathcal{L} = \{c_1, \dots, c_m\}$ be a finite claim ledger with dependency DAG $D(c_i) \subseteq \mathcal{L}$ and evidence pointers $E(c_i)$.
1. **15-to-5 Status Projection (`map_15_to_5_status`)**: Maps the 15 raw ledger statuses into the 5-status lattice $\mathcal{S}_5 = \{\text{VERIFIED}, \text{BOUNDED\_EXTERNAL}, \text{OPEN\_DECLARED}, \text{UNVERIFIED\_WRITTEN}, \text{INVALID\_LINK}\}$.
2. **Pointer & P2 Provenance Gate**: If any $p \in E(c_i)$ is missing from `available_pointers` or if $c_i$ requires numerical provenance (`requires_numeric_provenance = True`) when the `PROD-P2` gate is unverified, the pointer is marked non-existent and $c_i$ downgrades to `INVALID_LINK` / `UNVERIFIED_WRITTEN`.
3. **Dependency Propagation (`WdpLedgerCertifier.recompute`)**: A claim $c_i$ cannot retain `VERIFIED` if any dependency $d \in D(c_i)$ downgrades below `VERIFIED`.

## Verification Summary
- `evaluate_claim_ledger_certification` in `omega_engine_woland` certifies valid pointer-backed claims as `VERIFIED`, downgrades claims with missing pointers or downstream dependents when a pointer is removed, downgrades numeric claims when `p2_provenance_verified=False`, and emits a verified `PROD-KERNEL` receipt with `AuthorityEffect: None`.
