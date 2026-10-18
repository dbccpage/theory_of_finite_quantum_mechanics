pub const PROVENANCE: &str = "Origin: research/qcd_beta0_wilson_confinement_finite_map.md\nClaim: urn:tfqm:qcd-beta0:three-by-three-lattice-betti-equals-four\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum QcdError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("lattice vertex count {vertices} or edge count {edges} is outside the declared range")]
    Range { vertices: i64, edges: i64 },
    #[error("lattice with {vertices} vertices and {edges} edges has Betti number {formula}")]
    Disconnected { vertices: i64, edges: i64, formula: i64 },
    #[error("Betti reading {got} is not the declared value {expected}")]
    Count { got: i64, expected: i64 },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, QcdError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn betti(vertices: i64, edges: i64) -> Result<i64, QcdError> {
    if vertices < 1 || edges < 0 {
        return Err(QcdError::Range { vertices, edges });
    }
    let formula = match edges.checked_sub(vertices).and_then(|gap| gap.checked_add(1)) {
        Some(value) => value,
        None => return Err(QcdError::Range { vertices, edges }),
    };
    if formula < 0 {
        return Err(QcdError::Disconnected {
            vertices,
            edges,
            formula,
        });
    }
    Ok(formula)
}

pub fn certify_declared(vertices: i64, edges: i64, expected: i64) -> Result<i64, QcdError> {
    let got = betti(vertices, edges)?;
    if got != expected {
        return Err(QcdError::Count { got, expected });
    }
    Ok(got)
}

pub fn verify() -> Result<i64, QcdError> {
    let value = certify_declared(9, 12, 4)?;
    let chords = match 12i64.checked_sub(8) {
        Some(chords) => chords,
        None => return Err(QcdError::Range { vertices: 9, edges: 12 }),
    };
    if chords != value {
        return Err(QcdError::Count {
            got: chords,
            expected: value,
        });
    }
    Ok(value)
}

pub fn executed_mutation_kills() -> Result<u32, QcdError> {
    let killed = kill_if(0, drop_plus_killed()?)?;
    let killed = kill_if(killed, tree_killed()?)?;
    let killed = kill_if(killed, empty_lattice_killed()?)?;
    equivalent_lattice_matches()?;
    Ok(killed)
}

fn drop_plus_killed() -> Result<bool, QcdError> {
    Ok(mutant_drop_plus() != verify()?)
}

fn tree_killed() -> Result<bool, QcdError> {
    Ok(mutant_tree_edges() != 8)
}

fn empty_lattice_killed() -> Result<bool, QcdError> {
    Ok(betti(5, 0).is_err())
}

fn equivalent_lattice_matches() -> Result<(), QcdError> {
    let oracle = verify()?;
    let again = betti(9, 12)?;
    if again != oracle {
        return Err(QcdError::Count {
            got: again,
            expected: oracle,
        });
    }
    Ok(())
}

fn mutant_drop_plus() -> i64 {
    12 - 9
}

fn mutant_tree_edges() -> i64 {
    9
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, QcdError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(QcdError::KillOverflow { killed }),
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
    fn unit_square_lattice_betti_is_four() -> Result<(), String> {
        if betti(9, 12).map_err(|err| err.to_string())? != 4 {
            return Err("betti".to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_four_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("4").map_err(|err| err.to_string())?;
        if admitted != verify().map_err(|err| err.to_string())? {
            return Err("admit".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_four() -> Result<(), String> {
        if verify().map_err(|err| err.to_string())? != 4 {
            return Err("verify".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_range() -> Result<(), String> {
        match betti(0, 12) {
            Err(QcdError::Range { vertices, edges }) if vertices == 0 && edges == 12 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_disconnected() -> Result<(), String> {
        match betti(5, 0) {
            Err(QcdError::Disconnected {
                vertices,
                edges,
                formula,
            }) if vertices == 5 && edges == 0 && formula == -4 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_count() -> Result<(), String> {
        match certify_declared(9, 12, 5) {
            Err(QcdError::Count { got, expected }) if got == 4 && expected == 5 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(QcdError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
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
            Err(QcdError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
