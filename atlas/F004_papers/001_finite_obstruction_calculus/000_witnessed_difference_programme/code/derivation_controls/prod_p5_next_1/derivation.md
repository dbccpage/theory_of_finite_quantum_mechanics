# PROD-P5-NEXT-1

Goal id: PROD-P5-NEXT-1

Selected scope for PROD-P5-NEXT-1 is recorded in this note.

## Selected scope

`WdpCertificationService` and `map_claim_status` / `route_claim_to_ch20_status` (`omega_engine_applications/wdp_products/p5_claim_certification/adapter.py`) implementing the `CertificationService` protocol (`omega_engine_applications/wdp_products/p5_claim_certification/contracts.py`) and mapping `relative_status.ClaimStatus` onto Chapter 20's five `Status` values, with parity and negative-control tests (`omega_engine_applications/tests/test_p3_p5_adapters.py`).

## Hypotheses

H1. `relative_status.ClaimStatus` defines fifteen claim statuses across algebraic, operational, and structural categories (`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/relative_status/status.py`).

H2. Chapter 20 (`Status` in `omega_engine_applications/wdp_products/p5_claim_certification/contracts.py`) defines five evaluable outcome classes (`PROVED`, `REFUTED`, `UNDETERMINED`, `OUTSIDE_PROFILE`, `REFUSED`).

H3. Every `ClaimCert` requires a concrete witness digest (`PROVED`), counterexample digest (`REFUTED`), remaining-case count (`UNDETERMINED`), profile reason (`OUTSIDE_PROFILE`), or refusal code (`REFUSED`), and structural/non-evaluable `ClaimStatus` labels (`DEFINITION`, `NONCLAIM`, `SYNTHESIS_CONCLUSION`, `INTERPRETIVE`) must be refused with a `TypedRefusal` rather than collapsed into an algebraic truth status (`WDP-CHS-N04`, `WDP-CHS-N06`).

## Derivation

1. **Exhaustive 15-value partition (`CLAIM_STATUS_TO_CH20_STATUS` and `UNMAPPED_CLAIM_STATUSES`)**:
   - `PROVED` $\leftarrow \{\text{EXACT\_ALGEBRAIC\_THEOREM}, \text{WITNESSED\_CONSTRUCTIVE\_EXISTENCE}, \text{FINITE\_EXHAUSTIVE\_VERIFICATION}, \text{REPLAY\_CERTIFIED\_COMPUTATION}, \text{PROTOCOL\_REPLAY\_PASS}\}$.
   - `REFUTED` $\leftarrow \{\text{WITNESSED\_COUNTEREXAMPLE}\}$.
   - `UNDETERMINED` $\leftarrow \{\text{BOUNDED\_EMPIRICAL\_FINDING}, \text{SIMULATION\_OBSERVATION}, \text{CONJECTURE\_FALSIFIABLE}\}$.
   - `OUTSIDE_PROFILE` $\leftarrow \{\text{CONDITIONAL\_IMPLICATION}\}$.
   - `REFUSED` $\leftarrow \{\text{STRUCTURAL\_ABSENCE\_RESULT}\}$.
   - Refused via `TypedRefusal(code="unmapped_claim_status", ...)` $\leftarrow \{\text{DEFINITION}, \text{NONCLAIM}, \text{SYNTHESIS\_CONCLUSION}, \text{INTERPRETIVE}\}$.

2. **Certification service (`WdpCertificationService.certify`)**:
   - Validates `Assumptions` and rejects uncertified claims (`cert.status == Status.PROVED and not cert.witness_digest`) or unknown status codes via `TypedRefusal`.
   - Emits a `ClaimCert` with `authority_effect="None"` when all required status-specific fields are populated.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not promote structural or interpretive statements into Chapter 20 truth statuses.
- It does not permit `PROVED` without a non-empty `witness_digest` or `REFUTED` without a non-empty `counterexample_digest`.
