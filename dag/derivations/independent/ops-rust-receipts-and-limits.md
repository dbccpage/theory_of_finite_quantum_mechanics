Status: AI-drafted, awaiting human review.

# Ceiling arithmetic for OPS-RUST-RECEIPTS-AND-LIMITS

AuthorityEffect: None.

The ledger rows about the Rust module `empirical_presheaf` name a zero duality gap, tamper rejection, a rebuilt linear programme, and size ceilings. This note treats only the ceiling counts. It does not run the Rust tests.

## Bounds

Let G = 2^20 and L = 2^22.

Expanding the powers gives G = 1048576 and L = 4194304. The local-section count of one context of 21 binary measurements is 2^21 = 2097152.

## Above the global ceiling

2^64 > 2^20, and 2^21 > 2^20. The ledger reads 2^64 as the assignment count of 64 binary singletons and 2^21 as the section count of one 21-bit context. That reading is not a Lean object and is not re-run here.

## Inside both ceilings

10 * 2 = 20, 2^10 = 1024, and 20 * 1024 = 20480. Then 2^10 < 2^20 and 20480 < 2^22. The ledger reads 20 and 1024 as the outcome rows and assignment columns of ten binary singletons. That reading is not a Lean object and is not re-run here.

## What is proved

maxGlobal = 2^20 = 1048576, maxLp = 2^22 = 4194304, 2^21 = 2097152, 2^64 > maxGlobal, 2^21 > maxGlobal, 10 * 2 = 20, 2^10 = 1024, 20 * 1024 = 20480, 2^10 < maxGlobal, and 20 * 1024 < maxLp.

## What is assumed

Natural-number arithmetic. No identification of an exponent with a singleton census is assumed. No Rust execution, no linear programme, and no continuity or measure hypothesis.

## What is open

A zero duality gap, the dual inequality, tamper and shape rejection, rebuilding a linear programme, the PR box, the noisy boxes, and the Rust functions `verify_noncontextual_fraction` and `verify_l1_defect_receipt`. The in-repo module depends on `omega_solvers`, which is not a workspace member, so those tests are not run here.
