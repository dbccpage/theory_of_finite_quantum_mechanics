pub const PROVENANCE: &str = "Origin: code/rust/src/wdp/derivation_controls/plan_qp_c3.rs\nClaim: PLAN-QP-C3 certifies the telescoping 3-cycle coboundary on vertices (3, 7, 11) is zero, records carrier 6 and secondary pair (0, 1), and refuses unpublished_zenodo_placeholder. Scope Fence: no authority is minted and no theorem beyond this cycle certificate is claimed.\nAuthorityEffect: None\nMutationKills: 3";

const DECLARED_CARRIER: i64 = 6;
const SECONDARY_NUM: i64 = 0;
const SECONDARY_DEN: i64 = 1;
const CYCLE_A0: i64 = 3;
const CYCLE_A1: i64 = 7;
const CYCLE_A2: i64 = 11;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Rational {
    pub num: i64,
    pub den: i64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Witness {
    pub carrier_val: i64,
    pub secondary_pair: (i64, i64),
    pub coboundary_cycle_zero: i64,
    pub authority: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ScopeError {
    OutOfScope { claim_flag: String },
    ZeroDenominator { num: i64 },
    CycleOverflow { op: &'static str, left: i64, right: i64 },
}

impl std::fmt::Display for ScopeError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::OutOfScope { claim_flag } => write!(
                f,
                "invariant out_of_scope_promotion control_id=PLAN-QP-C3 claim_flag={claim_flag}"
            ),
            Self::ZeroDenominator { num } => {
                write!(f, "invariant nonzero_denominator_refused num={num}")
            }
            Self::CycleOverflow { op, left, right } => {
                write!(f, "invariant checked_{op} left={left} right={right}")
            }
        }
    }
}

impl std::error::Error for ScopeError {}

fn overflow(op: &'static str, left: i64, right: i64) -> ScopeError {
    ScopeError::CycleOverflow { op, left, right }
}

fn nonneg_abs(value: i64) -> Result<i64, ScopeError> {
    match value.checked_abs() {
        Some(abs) => Ok(abs),
        None => Err(overflow("abs", value, 0)),
    }
}

fn gcd(mut a: i64, mut b: i64) -> Result<i64, ScopeError> {
    a = nonneg_abs(a)?;
    b = nonneg_abs(b)?;
    while b != 0 {
        let remainder = match a.checked_rem(b) {
            Some(value) => value,
            None => return Err(overflow("rem", a, b)),
        };
        a = b;
        b = remainder;
    }
    Ok(a)
}

fn checked_div(left: i64, right: i64) -> Result<i64, ScopeError> {
    match left.checked_div(right) {
        Some(value) => Ok(value),
        None => Err(overflow("div", left, right)),
    }
}

pub fn ratio(num: i64, den: i64) -> Result<Rational, ScopeError> {
    if den == 0 {
        return Err(ScopeError::ZeroDenominator { num });
    }
    let (num, den) = if den < 0 {
        let flipped_num = match num.checked_neg() {
            Some(value) => value,
            None => return Err(overflow("neg", num, 0)),
        };
        let flipped_den = match den.checked_neg() {
            Some(value) => value,
            None => return Err(overflow("neg", den, 0)),
        };
        (flipped_num, flipped_den)
    } else {
        (num, den)
    };
    let divisor = gcd(num, den)?;
    Ok(Rational {
        num: checked_div(num, divisor)?,
        den: checked_div(den, divisor)?,
    })
}

pub fn edge_delta(head: i64, tail: i64) -> Result<i64, ScopeError> {
    match head.checked_sub(tail) {
        Some(value) => Ok(value),
        None => Err(overflow("sub", head, tail)),
    }
}

fn add_delta(left: i64, right: i64) -> Result<i64, ScopeError> {
    match left.checked_add(right) {
        Some(value) => Ok(value),
        None => Err(overflow("add", left, right)),
    }
}

pub fn cycle_coboundary(a0: i64, a1: i64, a2: i64) -> Result<i64, ScopeError> {
    let d01 = edge_delta(a1, a0)?;
    let d12 = edge_delta(a2, a1)?;
    let d20 = edge_delta(a0, a2)?;
    let partial = match d01.checked_add(d12) {
        Some(value) => value,
        None => return Err(overflow("add", d01, d12)),
    };
    add_delta(partial, d20)
}

pub fn witness() -> Result<Witness, ScopeError> {
    let cycle = cycle_coboundary(CYCLE_A0, CYCLE_A1, CYCLE_A2)?;
    Ok(Witness {
        carrier_val: DECLARED_CARRIER,
        secondary_pair: (SECONDARY_NUM, SECONDARY_DEN),
        coboundary_cycle_zero: cycle,
        authority: "AuthorityEffect: None",
    })
}

fn is_named_refusal(flag: &str) -> bool {
    flag == "unpublished_zenodo_placeholder"
}

fn is_generic_refusal(flag: &str) -> bool {
    flag == "promote_unrestricted" || flag == "bypass_guard"
}

fn is_refused(flag: &str) -> bool {
    is_named_refusal(flag) || is_generic_refusal(flag)
}

pub fn reject_unpublished_zenodo_placeholder(claim_flag: &str) -> Result<(), ScopeError> {
    if is_refused(claim_flag) {
        return Err(ScopeError::OutOfScope {
            claim_flag: claim_flag.to_string(),
        });
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn show(error: ScopeError) -> String {
        error.to_string()
    }

    #[test]
    fn unit_cycle_telescopes_to_zero() -> Result<(), String> {
        let cycle = cycle_coboundary(CYCLE_A0, CYCLE_A1, CYCLE_A2).map_err(show)?;
        if cycle != 0 {
            return Err(format!("cycle {cycle}"));
        }
        Ok(())
    }

    #[test]
    fn integration_witness_matches_cycle() -> Result<(), String> {
        let found = witness().map_err(show)?;
        let cycle = cycle_coboundary(3, 7, 11).map_err(show)?;
        if found.coboundary_cycle_zero != cycle {
            return Err(format!("cycle {}", found.coboundary_cycle_zero));
        }
        let admitted = reject_unpublished_zenodo_placeholder("admissible_scoped_control");
        if admitted.is_err() {
            return Err("admissible refused".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_declared_witness_contract() -> Result<(), String> {
        let found = witness().map_err(show)?;
        if found.carrier_val != 6 {
            return Err(format!("carrier {}", found.carrier_val));
        }
        if found.secondary_pair != (0, 1) {
            return Err(format!("pair {:?}", found.secondary_pair));
        }
        if found.coboundary_cycle_zero != 0 {
            return Err("cycle".to_string());
        }
        if found.authority != "AuthorityEffect: None" {
            return Err(found.authority.to_string());
        }
        if !PROVENANCE.contains("Origin: code/rust/src/wdp/derivation_controls/plan_qp_c3.rs") {
            return Err("origin".to_string());
        }
        if !PROVENANCE.contains("Claim: ") || !PROVENANCE.contains("AuthorityEffect: None") {
            return Err("provenance".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_named_and_generic_refusals() -> Result<(), String> {
        match reject_unpublished_zenodo_placeholder("unpublished_zenodo_placeholder") {
            Err(ScopeError::OutOfScope { claim_flag }) if claim_flag == "unpublished_zenodo_placeholder" => {}
            other => return Err(format!("named {other:?}")),
        }
        match reject_unpublished_zenodo_placeholder("promote_unrestricted") {
            Err(ScopeError::OutOfScope { claim_flag }) if claim_flag == "promote_unrestricted" => {}
            other => return Err(format!("promote {other:?}")),
        }
        match reject_unpublished_zenodo_placeholder("bypass_guard") {
            Err(ScopeError::OutOfScope { claim_flag }) if claim_flag == "bypass_guard" => Ok(()),
            other => Err(format!("bypass {other:?}")),
        }
    }

    #[test]
fn unit_secondary_ratio() -> Result<(), String> {
    let reduced = ratio(0, 1).map_err(show)?;
    if reduced.num != 0 || reduced.den != 1 {
        return Err(format!("ratio {reduced:?}"));
    }
    match ratio(1, 0) {
        Err(ScopeError::ZeroDenominator { num }) if num == 1 => Ok(()),
        other => Err(format!("den {other:?}")),
    }
}


    #[test]
    fn negative_cycle_overflow() -> Result<(), String> {
        match edge_delta(i64::MIN, 1) {
            Err(ScopeError::CycleOverflow { op, left, right })
                if op == "sub" && left == i64::MIN && right == 1 =>
            {
                Ok(())
            }
            other => Err(format!("overflow {other:?}")),
        }
    }
}
