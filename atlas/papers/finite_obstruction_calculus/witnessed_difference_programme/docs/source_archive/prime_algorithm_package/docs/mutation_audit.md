# Mutation audit

AuthorityEffect: None. Reproduce with `python scripts/mutation_audit.py`.

Each mutation disables exactly one law in a copy of `code/` and runs the
suite. The unchanged 35-test algorithm suite must pass in the same isolated
environment before any mutation is assessed. Each mutant must return pytest
exit code 1 and a valid JUnit report containing test failures and no test
errors to count as KILLED. A green mutant marks an untested law; a collection,
runner or report failure aborts the audit and does not count as a kill.

| Law | Result |
|---|---|
| Measurement requires admission gate | KILLED |
| Measurement admitted defaults to False | KILLED |
| CanContinue requires obligation | KILLED |
| CanContinue requires witness | KILLED |
| CanContinue requires next carrier declared | KILLED |
| CanContinue requires adapter sound | KILLED |
| CanContinue requires detector adequate | KILLED |
| CanContinue requires minimal lift | KILLED |
| CanContinue requires skeleton preserved | KILLED |
| CanContinue requires budget remains | KILLED |
| CanContinue requires not GTLA refusal | KILLED |
| Declaration order requires grounding hash | KILLED |
| Declaration order requires valid carrier | KILLED |
| Declaration order requires observer | KILLED |
| Declaration order requires witness certificate | KILLED |
| Intake evaluation refuses missing carrier | KILLED |
| Intake evaluation refuses missing witness | KILLED |
| Terminalization requires zero residual | KILLED |
| Terminalization refuses blind observer | KILLED |
| Merkle tape verifies entry hash mismatch | KILLED |

Result: 20/20 mutations killed. Rechecked on 2026-10-02 after updating the
carrier-validation anchor; see [deposit validation](deposit_validation_2026_10_02.md).
