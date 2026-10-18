pub const PROVENANCE: &str = "Origin: code/rust/src/wdp/derivation_controls/gen_wdp_o05.rs\nClaim: GEN-WDP-O05 admits only the declared integer carrier (4, 3, 1) on domain governance_jurisdiction_appeal_refinement and refuses unrestricted promotion. Scope Fence: no authority is minted and no theorem beyond this carrier check is claimed.\nAuthorityEffect: None\nMutationKills: 3";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Rational {
    pub num: i64,
    pub den: i64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AdmittedCarrier {
    pub control_id: &'static str,
    pub domain: &'static str,
    pub carrier: (i64, i64, i64),
    pub sum: i64,
    pub reduced: (Rational, Rational, Rational),
    pub authority: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ControlError {
    UnrestrictedPromotion {
        control_id: &'static str,
        observed: (i64, i64, i64),
    },
    InvariantMismatch {
        control_id: &'static str,
        expected: (i64, i64, i64),
        observed: (i64, i64, i64),
    },
    NonIntegerToken { token: String },
    ZeroDenominator { num: i64 },
    Overflow { op: &'static str, left: i64, right: i64 },
}

impl std::fmt::Display for ControlError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnrestrictedPromotion { control_id, observed } => write!(
                f,
                "invariant unrestricted_promotion_refused control_id={control_id} observed={observed:?}"
            ),
            Self::InvariantMismatch {
                control_id,
                expected,
                observed,
            } => write!(
                f,
                "invariant declared_carrier_mismatch control_id={control_id} expected={expected:?} observed={observed:?}"
            ),
            Self::NonIntegerToken { token } => {
                write!(f, "invariant integer_carrier_token_refused token={token}")
            }
            Self::ZeroDenominator { num } => {
                write!(f, "invariant nonzero_denominator_refused num={num}")
            }
            Self::Overflow { op, left, right } => {
                write!(f, "invariant checked_{op} left={left} right={right}")
            }
        }
    }
}

impl std::error::Error for ControlError {}

fn nonneg_abs(value: i64) -> Result<i64, ControlError> {
    value
        .checked_abs()
        .ok_or(ControlError::Overflow {
            op: "abs",
            left: value,
            right: 0,
        })
}

fn gcd(mut a: i64, mut b: i64) -> Result<i64, ControlError> {
    a = nonneg_abs(a)?;
    b = nonneg_abs(b)?;
    while b != 0 {
        let remainder = a.checked_rem(b).ok_or(ControlError::Overflow {
            op: "rem",
            left: a,
            right: b,
        })?;
        a = b;
        b = remainder;
    }
    Ok(a)
}

pub fn ratio(num: i64, den: i64) -> Result<Rational, ControlError> {
    if den == 0 {
        return Err(ControlError::ZeroDenominator { num });
    }
    let (num, den) = if den < 0 {
        (
            num.checked_neg().ok_or(ControlError::Overflow {
                op: "neg",
                left: num,
                right: 0,
            })?,
            den.checked_neg().ok_or(ControlError::Overflow {
                op: "neg",
                left: den,
                right: 0,
            })?,
        )
    } else {
        (num, den)
    };
    let divisor = gcd(num, den)?;
    let reduced_num = num.checked_div(divisor).ok_or(ControlError::Overflow {
        op: "div",
        left: num,
        right: divisor,
    })?;
    let reduced_den = den.checked_div(divisor).ok_or(ControlError::Overflow {
        op: "div",
        left: den,
        right: divisor,
    })?;
    Ok(Rational {
        num: reduced_num,
        den: reduced_den,
    })
}

pub fn carrier_sum(triple: (i64, i64, i64)) -> Result<i64, ControlError> {
    let (a, b, c) = triple;
    let ab = match a.checked_add(b) {
        Some(value) => value,
        None => {
            return Err(ControlError::Overflow {
                op: "add",
                left: a,
                right: b,
            })
        }
    };
    match ab.checked_add(c) {
        Some(value) => Ok(value),
        None => Err(ControlError::Overflow {
            op: "add",
            left: ab,
            right: c,
        }),
    }
}

fn reduce_one(value: i64) -> Result<Rational, ControlError> {
    ratio(value, 1)
}

fn reduce_triple(triple: (i64, i64, i64)) -> Result<(Rational, Rational, Rational), ControlError> {
    Ok((
        reduce_one(triple.0)?,
        reduce_one(triple.1)?,
        reduce_one(triple.2)?,
    ))
}

fn non_integer(token: &str) -> ControlError {
    ControlError::NonIntegerToken {
        token: token.to_string(),
    }
}

fn has_dot(token: &str) -> bool {
    token.contains(".")
}

fn has_exponent_mark(token: &str) -> bool {
    token.contains("e") || token.contains("E")
}

fn has_plus(token: &str) -> bool {
    token.contains("+")
}

fn token_rejected(token: &str) -> bool {
    token.is_empty() || has_dot(token) || has_exponent_mark(token) || has_plus(token)
}

fn parse_one(token: &str) -> Result<i64, ControlError> {
    if token_rejected(token) {
        return Err(non_integer(token));
    }
    match token.parse() {
        Ok(value) => Ok(value),
        Err(_) => Err(non_integer(token)),
    }
}

fn push_part(parts: &mut Vec<String>, part: String, text: &str) -> Result<(), ControlError> {
    if parts.len() == 3 {
        return Err(non_integer(text));
    }
    parts.push(part);
    Ok(())
}

fn pop_part(parts: &mut Vec<String>, text: &str) -> Result<String, ControlError> {
    match parts.pop() {
        Some(value) => Ok(value),
        None => Err(non_integer(text)),
    }
}

fn split_carrier(text: &str) -> Result<(String, String, String), ControlError> {
    let mut parts = Vec::new();
    for part in text.split(",") {
        push_part(&mut parts, part.to_string(), text)?;
    }
    if parts.len() != 3 {
        return Err(non_integer(text));
    }
    let third = pop_part(&mut parts, text)?;
    let second = pop_part(&mut parts, text)?;
    let first = pop_part(&mut parts, text)?;
    Ok((first, second, third))
}

pub fn parse_carrier(text: &str) -> Result<(i64, i64, i64), ControlError> {
    let (first, second, third) = split_carrier(text)?;
    Ok((parse_one(&first)?, parse_one(&second)?, parse_one(&third)?))
}


pub fn evaluate_gen_wdp_o05(
    candidate: (i64, i64, i64),
    promote: bool,
) -> Result<AdmittedCarrier, ControlError> {
    if promote {
        return Err(ControlError::UnrestrictedPromotion {
            control_id: "GEN-WDP-O05",
            observed: candidate,
        });
    }
    let expected = (4, 3, 1);
    if candidate != expected {
        return Err(ControlError::InvariantMismatch {
            control_id: "GEN-WDP-O05",
            expected,
            observed: candidate,
        });
    }
    let sum = carrier_sum(expected)?;
    let reduced = reduce_triple(expected)?;
    Ok(AdmittedCarrier {
        control_id: "GEN-WDP-O05",
        domain: "governance_jurisdiction_appeal_refinement",
        carrier: expected,
        sum,
        reduced,
        authority: "AuthorityEffect: None",
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn show(error: ControlError) -> String {
        error.to_string()
    }

    #[test]
    fn unit_reduced_declared_carrier() -> Result<(), String> {
        let reduced = ratio(4, 1).map_err(show)?;
        if reduced.num != 4 || reduced.den != 1 {
            return Err(format!("reduced {reduced:?}"));
        }
        let sum = carrier_sum((4, 3, 1)).map_err(show)?;
        if sum != 8 {
            return Err(format!("sum {sum}"));
        }
        Ok(())
    }

    #[test]
    fn integration_parse_then_admit() -> Result<(), String> {
        let parsed = parse_carrier("4,3,1").map_err(show)?;
        let admitted = evaluate_gen_wdp_o05(parsed, false).map_err(show)?;
        if admitted.carrier != (4, 3, 1) {
            return Err(format!("carrier {:?}", admitted.carrier));
        }
        if admitted.domain != "governance_jurisdiction_appeal_refinement" {
            return Err(admitted.domain.to_string());
        }
        if !PROVENANCE.contains("Origin: code/rust/src/wdp/derivation_controls/gen_wdp_o05.rs") {
            return Err("origin missing".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_contract() -> Result<(), String> {
        let admitted = evaluate_gen_wdp_o05((4, 3, 1), false).map_err(show)?;
        if admitted.control_id != "GEN-WDP-O05" {
            return Err(admitted.control_id.to_string());
        }
        if admitted.sum != 8 {
            return Err(format!("sum {}", admitted.sum));
        }
        if admitted.authority != "AuthorityEffect: None" {
            return Err(admitted.authority.to_string());
        }
        if !PROVENANCE.contains("Claim: ") || !PROVENANCE.contains("AuthorityEffect: None") {
            return Err("provenance".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_promotion_records_observed_carrier() -> Result<(), String> {
        match evaluate_gen_wdp_o05((4, 3, 1), true) {
            Err(ControlError::UnrestrictedPromotion { observed, control_id })
                if observed == (4, 3, 1) && control_id == "GEN-WDP-O05" =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_mismatch_records_both_triples() -> Result<(), String> {
        let drifted = (4_i64.checked_add(1).ok_or("drift overflow")?, 3, 1);
        match evaluate_gen_wdp_o05(drifted, false) {
            Err(ControlError::InvariantMismatch {
                expected,
                observed,
                ..
            }) if expected == (4, 3, 1) && observed == drifted => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token_is_refused() -> Result<(), String> {
        match parse_carrier("1.5,3,1") {
            Err(ControlError::NonIntegerToken { token }) if token == "1.5" => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_zero_denominator_and_overflow() -> Result<(), String> {
        match ratio(1, 0) {
            Err(ControlError::ZeroDenominator { num }) if num == 1 => {}
            other => return Err(format!("den {other:?}")),
        }
        match carrier_sum((i64::MAX, 1, 0)) {
            Err(ControlError::Overflow { op, left, right })
                if op == "add" && left == i64::MAX && right == 1 =>
            {
                Ok(())
            }
            other => Err(format!("overflow {other:?}")),
        }
    }
}
