//! Proof-Carrying Reasoning Kernel (PROD-KERNEL) exact arithmetic verifier.

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KernelOutcome {
    Accepted { step: String, digest: u64 },
    Refused { code: String, detail: String },
}

pub fn fnv1a_digest(step: &str, cost: u64, budget: u64, checks_ok: bool) -> u64 {
    let mut hash: u64 = 0xcbf29ce484222325;
    for b in step.as_bytes() {
        hash ^= *b as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    for b in &cost.to_le_bytes() {
        hash ^= *b as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    for b in &budget.to_le_bytes() {
        hash ^= *b as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash ^= if checks_ok { 1u64 } else { 0u64 };
    hash.wrapping_mul(0x100000001b3)
}

pub fn evaluate_kernel_step(step: &str, cost: u64, budget: u64, checks_ok: bool) -> KernelOutcome {
    if !checks_ok {
        return KernelOutcome::Refused {
            code: "INVALID_WITNESS".to_string(),
            detail: "Certificate check failed".to_string(),
        };
    }
    if cost > budget {
        return KernelOutcome::Refused {
            code: "BUDGET_EXCEEDED".to_string(),
            detail: format!("cost {} exceeds budget {}", cost, budget),
        };
    }
    let digest = fnv1a_digest(step, cost, budget, checks_ok);
    KernelOutcome::Accepted {
        step: step.to_string(),
        digest,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_prod_kernel_accepts_and_refuses_deterministically() {
        let ok = evaluate_kernel_step("certified_step", 2, 3, true);
        assert!(matches!(ok, KernelOutcome::Accepted { .. }));

        let refused_budget = evaluate_kernel_step("certified_step", 4, 3, true);
        assert_eq!(
            refused_budget,
            KernelOutcome::Refused {
                code: "BUDGET_EXCEEDED".to_string(),
                detail: "cost 4 exceeds budget 3".to_string(),
            }
        );

        let refused_witness = evaluate_kernel_step("certified_step", 2, 3, false);
        assert_eq!(
            refused_witness,
            KernelOutcome::Refused {
                code: "INVALID_WITNESS".to_string(),
                detail: "Certificate check failed".to_string(),
            }
        );
    }
}
