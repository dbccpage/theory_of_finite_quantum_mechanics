# Lean 4 Claim Map — CODA-OR (Omniversal Re-Presentation)

**Package:** `coda_or`  
**Toolchain:** `leanprover/lean4:v4.34.0-rc1`  
**Axiom Whitelist:** axioms $\subseteq$ `{propext, Quot.sound, Classical.choice}`  

| Claim ID | Paper Statement | Lean 4 Module | Formal Name | Axiom Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OR-D1** | Pair compatibility condition | `Algebra` | `Coda.OR.pair_gluing` (type definition) | none | Mechanized |
| **OR-D2** | Four-case square defect classification inductive type | `D01D02Records` / `T01SquareClassification` | `CodaOr.SquareStatus`, `CodaOr.HasSquareStatus` | none | Mechanized |
| **OR-D3** | Standing of comparison object (sieve, terminalizer, descent triplet) | `D01D02Records` | `CodaOr.ComparisonObject`, `CodaOr.HasAuthority` | none | Mechanized |
| **OR-D4** | Limit candidate cone standing | `T02LimitAuthority` | `CodaOr.LimitCandidate.hasLimitAuthority` | none | Mechanized |
| **OR-T1** | Compatible pairs glue uniquely to a triple | `Algebra` (re-export) | `Coda.OR.pair_gluing` | axioms ⊆ {propext, Quot.sound} | Mechanized |
| **OR-T2** | A glue requires overlap | `Algebra` (re-export) | `Coda.OR.gluing_requires_overlap` | axioms ⊆ {propext, Quot.sound} | Mechanized |
| **OR-T3** | Incompatible countermodel has no glue | `Algebra` (re-export) | `Coda.OR.incompatible_countermodel` | axioms ⊆ {propext, Quot.sound} | Mechanized |
| **OR-T4** | Exact repairs are closed ($d_1(d_0 \alpha) = 0$) | `T01SquareClassification` | `CodaOr.exact_repair_is_closed`, `CodaOr.exact_implies_closed` | axioms ⊆ {propext, Quot.sound} | Mechanized |
| **OR-T5** | Empty support sieve implies zero comparison authority | `L02SupportSieve` | `CodaOr.empty_support_sieve_implies_zero_authority` | axioms ⊆ {propext, Quot.sound} | Mechanized |
| **OR-T6** | Envelope membership is not standing (uncredentialed witness) | `L01NonCreation` | `CodaOr.completion_reflector_does_not_create_authority`, `CodaOr.completion_membership_not_implies_authority` | axioms ⊆ {propext, Quot.sound} | Mechanized |
| **OR-T7** | Missing terminalizer or invalid leg blocks limit standing | `T02LimitAuthority` | `CodaOr.limit_missing_terminalizer_lacks_authority`, `CodaOr.limit_invalid_leg_lacks_authority` | axioms ⊆ {propext, Quot.sound} | Mechanized |
| **OR-T8** | Global omniversal comparison object is not assumed | `T02LimitAuthority` | `CodaOr.omniversal_not_assumed` | axioms ⊆ {propext, Quot.sound} | Mechanized |

OR-D3 includes `ComparisonObject.sieveTargetBound` in `HasAuthority`. The target-binding lemmas and concrete valid/invalid examples are in `L02SupportSieve.lean`. OR-T9 is an unmechanized scope fence and OR-T10 a declared application policy.
