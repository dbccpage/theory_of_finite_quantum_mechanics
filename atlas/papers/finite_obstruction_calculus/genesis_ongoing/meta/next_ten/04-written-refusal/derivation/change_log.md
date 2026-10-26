# Change Log: Problem 04 (Written Refusal)

1. **Initialization**:
   - Received Problem 04 assignment (`meta/next_ten/04-written-refusal`) under parent derivation `twentyfirst`.
   - Recorded dispatch and established persistent memory in `.agents/teamwork/worker_p04/DISPATCH.md` and `BRIEFING.md`.

2. **Model Implementation (`model.py`)**:
   - Implemented literal written state representation with `same_written`.
   - Formalized refusal semantics: `refused` detects loops; `refusal_result` ensures under the declared definitions identity invariance ($s \mapsto s$).
   - Implemented `explore_written_refusal` with exact wave generation, refusal tracking, and frontier exit logging.
   - Formulated independent census calculations ($2^{n(n-1)}$ for FREE; multiplier of 2 for ANCHORED $n \ge 2$).
   - Added differential comparison harnesses against Eighteenth and Twentyfirst.

3. **Test Suite (`test_derivation.py`)**:
   - Implemented 11 comprehensive unit and integration tests.
   - Verified branch coverage of 97.26% across the derivation package (exceeding the 95% floor).
   - Validated orbit-stabilizer theorem, census matches, and round-by-round closure equivalence.

4. **Evidence Generation (`evidence.py`)**:
   - Created deterministic evidence pipeline generating `evidence/summary.json` and `evidence/MANIFEST.sha256`.
   - Verified byte-identical regeneration with `python evidence.py --check`.

5. **Lean 4 Formalization (`Derivation.lean`)**:
   - Proved `written_step_preserves_legal`, `refusal_invariant`, `identify_given_refused`, and `adding_self_loop_refused`.
   - Constructed concrete, certified splitting witnesses (`freeW1 ≠ freeW2`, `anchoredW1 ≠ anchoredW2`).
   - Verified zero use of `sorry`, `admit`, or non-standard axioms.

6. **Documentation and Scientific Artifacts**:
   - Authored `paper.md` following claim hygiene standards.
   - Formulated `claim_ledger.md` mapping claims to statuses and proof evidence.
   - Documented the refutation of the core hypothesis in `resolution.md`.

7. **Review repair (2026-10-19)**:
   - Fresh B=3, R=12 evidence replay agrees with the stored summary. Corrected the two `bra=True` wave vectors in both `paper.md` and `resolution.md`; totals were unchanged.
   - Added checks of every numeric table cell against fresh model output and the stored summary, plus missing/duplicate cohort, Boolean/float coercion, incorrect count/wave and reading mutations for both table formats. The original documents fail two table checks; the corrected source passes all 32 tests. Scoped model/evidence coverage exceeds 95% for both lines and branches, and `evidence.py` has complete coverage.
   - Added Lean proofs that identity extensions preserve reachability within each round budget and first-discovery depth, including the bounded list-state relation. Pinned Lean 4.33.1 checks all four closure/discovery declarations without axioms. A non-identity extra edge supplies a checked counterexample to dropping the identity premise.
   - Corrected the impossible assertion-addition witness, separated the finite replay from the shared-relation theorem, and added the still-open Python/Lean representation and transition transport obligation to the ledger. No historical archive or release artifact was changed; this source repair is not deposit certification.
