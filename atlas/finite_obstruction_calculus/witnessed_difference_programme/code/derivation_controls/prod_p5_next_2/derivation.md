# PROD-P5-NEXT-2

Goal id: PROD-P5-NEXT-2

Selected scope for PROD-P5-NEXT-2 is recorded in this note.

## Selected scope

`WdpCertificationService` (`omega_engine_applications/wdp_products/p5_claim_certification/adapter.py`) implementing `CertificationService` over `witnessed_difference.claims.validate_claim_map` and the WDP §21.11 topological dependency-order audit, verified in `omega_engine_applications/tests/test_p3_p5_adapters.py`.

## Hypotheses

H1. Under WDP Appendix D.3, a `ClaimNode` carries eight evidence pointer slots (`prose_statement`, `claim_ledger_row`, `implementation`, `tests`, `formal_theorem`, `axiom_or_import_report`, `source_revision_and_hash`, `release_artifact`), and any missing pointer (`None`) or missing implementation/test file reported by `validate_claim_map` counts as unknown (`Status.UNDETERMINED`), never as a pass (`WDP-CH20-D01`).

H2. Under WDP §21.11, status recomputation proceeds in topological dependency order: if a dependency $d \in \operatorname{depends\_on}(c)$ is not `Status.PROVED`, then $c$ cannot remain `Status.PROVED` and is demoted to `Status.UNDETERMINED`.

H3. Dependency cycles (`dependency_cycle`), duplicate claim IDs (`duplicate_claim_id`), and unknown dependencies (`unknown_dependency`) are refused with `TypedRefusal`.

## Derivation

1. **Topological 21.11 audit & `validate_claim_map` integration**:
   - Even when a ledger is supplied in reverse dependency order (`(C3, C2, C1, C_IND)` with `C3 -> C2 -> C1`), `WdpCertificationService.certify` topologically sorts the DAG (`C1`, `C2`, `C3`, `C_IND`).
   - When `C1` has a missing implementation file (`validate_claim_map` returns an issue) or a missing D.3 pointer, `C1` becomes `Status.UNDETERMINED`, which propagates to `C2` and `C3`, while `C_IND` remains `Status.PROVED`.

2. **Cycle refusal**:
   - Mutual dependency `A <-> B` is refused with `TypedRefusal(code="dependency_cycle", authority_effect="None")`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not equate profile-relative certification with absolute mathematical completeness (`WDP-CH20-N01`).
