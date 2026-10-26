# Derivation Control: PLAN-7D-DAY-5

**AuthorityEffect:** None.

## Scope and Claim

This finite control (`PLAN-7D-DAY-5`) certifies the Day 5 integration gate across the staged PFP repair and operator-reuse episodes (`SG-40` and `SG-48`) under a non-reset fuel ledger and the Lane E protected subgroup character quotient dependency closure (`PQ-1` through `PQ-6`):

1. **Staged PFP Repair & Operator Reuse Under Non-Reset Fuel Ledger**:
   - Executes `PLAN-7D-NEXT-3` (`SG-40` admission followed by `SG-48` reuse) under a single monotone fuel ledger (`fuel_cap = 20`, `sg40_spent = 6`, `sg48_ep1_spent = 5`, `sg48_ep2_spent = 3`, `remaining = 6`), retaining seed digests, raw proposals, stage-execution flags, and witness-bound decisions.
2. **Lane E Dependency Closure (`docs/protected_subgroup_character_quotients.md`, `PQ-1`..`PQ-6`)**:
   - Verifies the Chinese Remainder Theorem idempotent residues $a_n \in \mathbb{Z}/6^n\mathbb{Z}$ satisfying $a_n \equiv 0 \pmod{2^n}$ and $a_n \equiv 1 \pmod{3^n}$ for $n \in \{1, 2, 3, 4\}$.
   - Verifies the dyadic approximation discrepancy $x_n = \frac{1}{3} - \frac{\lfloor 2^n / 3 \rfloor}{2^n} = \frac{r_n}{3 \cdot 2^n} < 2^{-n}$ ($r_n \in \{1, 2\}$), whose $3$-primary character evaluation remains $\frac{1}{3} > \frac{1}{4}$.
3. **Adversarial & Refusal Controls**:
   - Resetting the fuel ledger between episodes, dropping raw proposal logs, or supplying a residue $a_n$ violating $a_n \equiv 0 \pmod{2^n}$ or $a_n \equiv 1 \pmod{3^n}$ is refused.

## Non-Claims

- This finite control does not claim infinite locally compact group duality or paid live provider dispatch.
