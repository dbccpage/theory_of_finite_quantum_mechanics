# Campaign C250 Certification & Score Reconciliation

**AuthorityEffect:** None.
**Citation:** `sealed-derivation-v1` (`3100c4e`).
**Receipt ID:** `CERT-C250-20260909-01`
**Date:** 2026-09-09
**Status:** `CERTIFIED_RECONCILED`
**Auditor Identity:** C250 Certification Auditor & Verification Engineer

---

## Executive Summary

This document certifies the formal Phase 1 audit and score reconciliation for Campaign C250 of `apps/finite_qm`.
All audits were conducted under strict zero-float discrete arithmetic rules, requiring exact string, rational, and integer equality matching.

Key audit findings:
1. **Sealed Bets Pre-Registration Integrity**: All 30 sealed bet files in private custody (`_private_bets/finite_qm_c250/`) underwent strict LF normalization (`\r\n` $\to$ `\n`, bare `\r` $\to$ `\n`). Exactly 30 of 30 SHA-256 digests match `SEALED_DIGESTS.txt` and `apps/finite_qm/campaigns/c250/sealed_targets.json`.
2. **Machine Clause Score Reconciliation**: Machine review of all 10 blocks (B01 through B10) across 191 machine clauses evaluates to exactly **94 HIT / 32 MISS / 65 OPEN**.
3. **Schema Drift Verification**: Every single one of the 65 `OPEN` verdicts carries the recorded reason `"field missing or null"`. Zero `OPEN` clauses are due to mathematical indecision; 100% are due to unaddressed fields from schema drift between bet prompt schemas and execution result formats.
4. **Unit Test Pass**: The official test suite `apps/finite_qm/code/tests/unit/test_campaign_seals.py` passes 5 of 5 tests cleanly without errors or warnings.

---

## 1. 30 Sealed Bets Digest Verification Table

All 30 sealed bet files from the private custody directory were verified against pre-registered targets:

| Bet ID | Block | Actor | Raw Size (B) | LF Size (B) | SHA-256 Digest | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BET-CLAUDE-C250-B01` | `block_01` | CLAUDE | 3590 | 3590 | `1637e0e6b847e8bff05e823a7fbe290621d4f4dd55c751fb14cabf1f2f0f5674` | MATCH |
| `BET-GEMINI-C250-B01` | `block_01` | GEMINI | 2823 | 2823 | `c9dbf34d85e4aabf137e938922fea385096c1c5fd55eebc5100a7c3700f8a167` | MATCH |
| `BET-JC-C250-B01` | `block_01` | JC | 3260 | 3260 | `67695ab9a07aecda5a5294fe5fdf32635a51daec00d90b46f670d0880beb8893` | MATCH |
| `BET-CLAUDE-C250-B02` | `block_02` | CLAUDE | 3358 | 3358 | `46eccf7d1b44a42a72f812704164273ebb07e05e21fd95184e32584fb9a05789` | MATCH |
| `BET-GEMINI-C250-B02` | `block_02` | GEMINI | 2764 | 2764 | `20802087e0ce44a43d8cb10964c27d03ea29b369c1f950e86582e3c5956fcb5f` | MATCH |
| `BET-JC-C250-B02` | `block_02` | JC | 2998 | 2998 | `6e8752b2a920cc5efd45794635c9a4d6846c49253507a85e01b731945427c8f6` | MATCH |
| `BET-CLAUDE-C250-B03` | `block_03` | CLAUDE | 3262 | 3262 | `eba2fe358d731b62ba39bb096d8f6c3c62111fe1880ccbc8957f78bec7004a03` | MATCH |
| `BET-GEMINI-C250-B03` | `block_03` | GEMINI | 2822 | 2822 | `86123c1aacf824859533f0e205186ea2983e2c4f19bb40de89584fd3c517d1c3` | MATCH |
| `BET-JC-C250-B03` | `block_03` | JC | 3119 | 3119 | `edd10729c4f100c50d8be1ff565943f3fe9b55f5561a120a3dc9a1860f969e47` | MATCH |
| `BET-CLAUDE-C250-B04` | `block_04` | CLAUDE | 3890 | 3890 | `29e3dea56217a57644146fb54581a338f6994be461eac6f996a2e3b95ae546bb` | MATCH |
| `BET-GEMINI-C250-B04` | `block_04` | GEMINI | 2593 | 2593 | `7cd3a1c7a0b03bcac5fccd3fab671fc2abdd0a326ce53fd50849cf4c1a1adbcd` | MATCH |
| `BET-JC-C250-B04` | `block_04` | JC | 2850 | 2850 | `0986014d02001d38fd82ef279e3ece7bbc2397575c10eb5ef14ad1f2ffd77574` | MATCH |
| `BET-CLAUDE-C250-B05` | `block_05` | CLAUDE | 3146 | 3146 | `512ee55bcabfe6cd9460562d88e62fbbd34c7c7f3779eb3e1ec59d1c5973017e` | MATCH |
| `BET-GEMINI-C250-B05` | `block_05` | GEMINI | 2506 | 2506 | `7fdc1378e07ac2ca720abdf5b59bc6355254adfa787b1a269185bd7a2b74dff1` | MATCH |
| `BET-JC-C250-B05` | `block_05` | JC | 2877 | 2877 | `46a4a1923aad69c4ea563a3d558471dd74b69dc00e9d8b61a3073145d6f0381a` | MATCH |
| `BET-CLAUDE-C250-B06` | `block_06` | CLAUDE | 3234 | 3234 | `b8a34edde0380e0e7ea2b0f3ec43d4d0b0226548d575f54a9f3d97a6433e1554` | MATCH |
| `BET-GEMINI-C250-B06` | `block_06` | GEMINI | 2648 | 2648 | `548e488e74f465eace8c504e65019e2e6f5ef6749ee827c8f10f823d050d4b3a` | MATCH |
| `BET-JC-C250-B06` | `block_06` | JC | 2682 | 2682 | `55ea5c63f97638144104d71a5787acf86b347cadbfdfe89893a63994bb62ca15` | MATCH |
| `BET-CLAUDE-C250-B07` | `block_07` | CLAUDE | 2766 | 2766 | `e6306a2c24aeee209964ff5f4fa2b06649f662b8fd792f86e1291e337a14d8aa` | MATCH |
| `BET-GEMINI-C250-B07` | `block_07` | GEMINI | 2642 | 2642 | `49891123f8b552c518b7f51b1bb33f93073043b8f0af6f42c5b4fb1ed405389e` | MATCH |
| `BET-JC-C250-B07` | `block_07` | JC | 2861 | 2861 | `62b03ee98d8a1aedfc6215937786660413974e9a4e117b581277d76dff0c6587` | MATCH |
| `BET-CLAUDE-C250-B08` | `block_08` | CLAUDE | 3261 | 3261 | `15b62e9b2e1ec22094729f53374548eb46e4f2075c798a6fbf97f9ea6f5e9f8e` | MATCH |
| `BET-GEMINI-C250-B08` | `block_08` | GEMINI | 2709 | 2709 | `37bd90881b5cde9a65f8304a51eaca72ea817e3be9a71c6db9a27be8cde11846` | MATCH |
| `BET-JC-C250-B08` | `block_08` | JC | 3071 | 3071 | `791358cb1f9d67835382caf11767b9305f4d706da0578e16d725a0a5734f8c1c` | MATCH |
| `BET-CLAUDE-C250-B09` | `block_09` | CLAUDE | 3144 | 3144 | `3a2291061dffce01543d8ec81b57e6770fc81ccd568baa1597fcd9bad82c4125` | MATCH |
| `BET-GEMINI-C250-B09` | `block_09` | GEMINI | 2724 | 2724 | `0c35199a2cae03b6488da75c7100bd3f0a3c68481cb8c56318de0483f7392009` | MATCH |
| `BET-JC-C250-B09` | `block_09` | JC | 2963 | 2963 | `661cf536b4a0c70dd6d136f257fcbe7fd93983cd42a33fa19c43ec46aa8056ef` | MATCH |
| `BET-CLAUDE-C250-B10` | `block_10` | CLAUDE | 4118 | 4118 | `7b3838e2dd924b98b50e6ebfee9b871f26525b462df18375f5bfc257dce5e3a3` | MATCH |
| `BET-GEMINI-C250-B10` | `block_10` | GEMINI | 2999 | 2999 | `093ebd4c1a11bfbe7dc584787d2f9d169e6b900cd912ed50593daa04cc3bd1a4` | MATCH |
| `BET-JC-C250-B10` | `block_10` | JC | 3617 | 3617 | `8d6855fb09f4afb567e5f8b267f09f7dee670378a8e9b126f89f4e1097b328a7` | MATCH |

**Verification Result**: 30 of 30 matching (10 Claude, 10 Gemini, 10 JC). All digests match `SEALED_DIGESTS.txt` and `sealed_targets.json`.

---

## 2. Review Custody & Lineage Verification

The custody registration in `apps/finite_qm/evidence/c250_review_custody_20260907.json` records:
- **AuthorityEffect**: `None`
- **Original Git Head**: `22824045918194a72a9557b9410bf5d2e5380b93`
- **Total Tracked Files**: 60 files (30 bet files, 10 result JSON files, 10 RESULT markdown files, 10 SCORE markdown files).
- **Lineage Integrity**: The reviewed head in PR #207 integrates with CODA `main` at `7df073e3f61130b51e905d035cbbcc2cb2eea856`.

---

## 3. Machine Evaluation & Score Reconciliation

Audit of `apps/finite_qm/evidence/c250_machine_review_20260907.json` over 191 machine clauses across blocks B01–B10:

### 3.1 Campaign Totals
- **HIT**: 94
- **MISS**: 32
- **OPEN**: 65
- **TOTAL**: 191

### 3.2 Breakdown by Actor

| Actor | HIT | MISS | OPEN | Total Clauses | Hit Rate (Scored) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLAUDE** | 30 | 11 | 21 | 62 | 73.17% (30/41) |
| **GEMINI** | 34 | 10 | 23 | 67 | 77.27% (34/44) |
| **JC** | 30 | 11 | 21 | 62 | 73.17% (30/41) |
| **TOTAL** | **94** | **32** | **65** | **191** | **74.60% (94/126)** |

### 3.3 Breakdown by Block

| Block | HIT | MISS | OPEN | Total Clauses |
| :--- | :--- | :--- | :--- | :--- |
| **block_01** | 7 | 5 | 12 | 24 |
| **block_02** | 9 | 0 | 9 | 18 |
| **block_03** | 9 | 3 | 9 | 21 |
| **block_04** | 18 | 0 | 3 | 21 |
| **block_05** | 9 | 0 | 6 | 15 |
| **block_06** | 1 | 6 | 10 | 17 |
| **block_07** | 13 | 0 | 3 | 16 |
| **block_08** | 15 | 6 | 0 | 21 |
| **block_09** | 6 | 0 | 13 | 19 |
| **block_10** | 7 | 12 | 0 | 19 |
| **TOTAL** | **94** | **32** | **65** | **191** |

---

## 4. Schema Drift Analysis for OPEN Clauses

Every one of the 65 `OPEN` verdicts was checked for its recorded detail:
- **`"field missing or null"`**: 65 of 65 clauses (100.0%).
- **Other reasons**: 0.

As documented in `apps/finite_qm/evidence/C250_SCHEMA_CONFORMANCE_AUDIT_20260907.md`, these `OPEN` verdicts do not reflect mathematical ambiguity or computational failure. Rather, the bets were formulated against prompt schema fields that were subsequently omitted, renamed, or unpopulated in the execution results (e.g., `lean_dimensions_proved`, `residual_declaration_count`, `nonmonotone_additive_counterexample_found`).

---

## 5. Automated Unit Test Verification

The unit test suite `apps/finite_qm/code/tests/unit/test_campaign_seals.py` was executed:

```powershell
python -m pytest apps/finite_qm/code/tests/unit/test_campaign_seals.py -v --basetemp=C:\Users\a343o\source\repos\CODA\scratch\pytest_c250
```

Results:
- `test_sealed_targets_file_exists_and_declares_none_authority`: **PASSED**
- `test_c250_cl_and_jc_target_digests`: **PASSED**
- `test_revealed_plaintext_digests_match_when_present`: **PASSED**
- `test_executor_block_01_seal_integrity`: **PASSED**
- `test_c250_block_02_pre_registered_digests`: **PASSED**

**Overall Test Result**: 5 passed in 0.40s (100% pass rate).

---

## 6. Claim Hygiene & Formal Bounds

In accordance with repository claim hygiene standards:

1. **What this certification supports**:
   - Supports exact pre-registration custody and digest match for all 30 C250 bet files across Claude, Gemini, and JC.
   - Supports exact mechanical reconciliation of 191 machine evaluation clauses to 94 HIT, 32 MISS, and 65 OPEN.
   - Supports the finding that all 65 OPEN clauses are caused by schema drift (`"field missing or null"`).
2. **What this certification does NOT support**:
   - Does not support mathematical validity of unscored prose bets.
   - Does not support terminal derivation of quantum mechanics from finite operational models alone.
   - Does not establish unproved physical necessity or general continuous lifts.
3. **Narrowest Defensible Claim**:
   - The private custody bet plaintexts are byte-authentic to the pre-registered SHA-256 targets; machine evaluation scores reconcile to 94 HIT, 32 MISS, and 65 OPEN; and all OPEN clauses represent unanswered fields due to schema drift.
4. **Next Test Needed**:
   - Pre-flight schema conformance enforcement (`campaigns/check_result_schema.py`) must be wired into future campaign runners (C500, C750, C1000) prior to execution.

---

## 7. Formal Certification Declaration

Campaign C250 is hereby certified as mechanically verified, audit-reconciled, and sealed under exact discrete rational standards.

```
Status: CERTIFIED_RECONCILED
AuthorityEffect: None
Citation: sealed-derivation-v1 (3100c4e)
```
