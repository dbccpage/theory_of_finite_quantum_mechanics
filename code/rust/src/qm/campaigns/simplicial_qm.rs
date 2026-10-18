pub const PROVENANCE: &str = "Origin: lean4/FiniteCochain.lean\nClaim: urn:tfqm:FiniteCochain:d1-d0-vanishes-on-the-declared-triangle\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum StokesError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("checked {op} overflowed from {left} and {right}")]
    Overflow { op: &'static str, left: i64, right: i64 },
    #[error("Stokes pairing {pairing} is not zero")]
    Stokes { pairing: i64 },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, StokesError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn coboundary(v0: i64, v1: i64, v2: i64) -> Result<[i64; 3], StokesError> {
    Ok([sub(v1, v0)?, sub(v2, v1)?, sub(v0, v2)?])
}

pub fn evaluate_face(edges: [i64; 3]) -> Result<i64, StokesError> {
    add(add(edges[0], edges[1])?, edges[2])
}

pub fn require_pairing(pairing: i64) -> Result<i64, StokesError> {
    if pairing != 0 {
        return Err(StokesError::Stokes { pairing });
    }
    Ok(pairing)
}

pub fn certify_vertices(v0: i64, v1: i64, v2: i64) -> Result<i64, StokesError> {
    let pairing = evaluate_face(coboundary(v0, v1, v2)?)?;
    require_pairing(pairing)
}

pub fn verify() -> Result<i64, StokesError> {
    certify_vertices(4, -2, 5)
}

pub fn executed_mutation_kills() -> Result<u32, StokesError> {
    let killed = kill_if(0, flipped_edge_killed()?)?;
    let killed = kill_if(killed, dropped_edge_killed()?)?;
    let killed = kill_if(killed, overflow_killed())?;
    equivalent_pairing_matches()?;
    Ok(killed)
}

fn flipped_edge_killed() -> Result<bool, StokesError> {
    Ok(mutant_flip_first(4, -2, 5)? != verify()?)
}

fn dropped_edge_killed() -> Result<bool, StokesError> {
    let edges = coboundary(4, -2, 5)?;
    Ok(mutant_drop_last(edges)? != 0)
}

fn overflow_killed() -> bool {
    sub(i64::MIN, 1).is_err()
}

fn equivalent_pairing_matches() -> Result<(), StokesError> {
    let oracle = verify()?;
    let again = certify_vertices(4, -2, 5)?;
    if again != oracle {
        return Err(StokesError::Stokes { pairing: again });
    }
    Ok(())
}

fn mutant_flip_first(v0: i64, v1: i64, v2: i64) -> Result<i64, StokesError> {
    evaluate_face([sub(v0, v1)?, sub(v2, v1)?, sub(v0, v2)?])
}

fn mutant_drop_last(edges: [i64; 3]) -> Result<i64, StokesError> {
    add(edges[0], edges[1])
}

fn add(left: i64, right: i64) -> Result<i64, StokesError> {
    match left.checked_add(right) {
        Some(sum) => Ok(sum),
        None => Err(StokesError::Overflow {
            op: "add",
            left,
            right,
        }),
    }
}

fn sub(left: i64, right: i64) -> Result<i64, StokesError> {
    match left.checked_sub(right) {
        Some(diff) => Ok(diff),
        None => Err(StokesError::Overflow {
            op: "sub",
            left,
            right,
        }),
    }
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, StokesError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(StokesError::KillOverflow { killed }),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn provenance_lists_authority() -> Result<(), String> {
        if PROVENANCE.contains("Origin:")
            && PROVENANCE.contains("Claim:")
            && PROVENANCE.contains("AuthorityEffect: None")
        {
            return Ok(());
        }
        Err(PROVENANCE.to_string())
    }

    #[test]
    fn unit_declared_triangle_pairs_to_zero() -> Result<(), String> {
        if certify_vertices(4, -2, 5).map_err(|err| err.to_string())? != 0 {
            return Err("pairing".to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_zero_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("0").map_err(|err| err.to_string())?;
        if admitted != verify().map_err(|err| err.to_string())? {
            return Err("admit".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_zero() -> Result<(), String> {
        if verify().map_err(|err| err.to_string())? != 0 {
            return Err("verify".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_overflow() -> Result<(), String> {
        match sub(i64::MIN, 1) {
            Err(StokesError::Overflow { op, left, right })
                if op == "sub" && left == i64::MIN && right == 1 =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_stokes() -> Result<(), String> {
        match require_pairing(4) {
            Err(StokesError::Stokes { pairing }) if pairing == 4 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(StokesError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
                if token == "1.5" =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_kill_overflow() -> Result<(), String> {
        match kill_if(u32::MAX, true) {
            Err(StokesError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn mutation_record_matches_execution() -> Result<(), String> {
        let killed = executed_mutation_kills().map_err(|err| err.to_string())?;
        let marked = format!("killed={killed}");
        if MUTATION_KILL_RECORD != marked {
            return Err(format!("record {MUTATION_KILL_RECORD} executed {marked}"));
        }
        Ok(())
    }
}
