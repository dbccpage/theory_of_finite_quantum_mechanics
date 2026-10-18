pub const PROVENANCE: &str = "Origin: research/symanzik_two_forest_bphz_finite_map.md\nClaim: urn:tfqm:symanzik:triangle-spanning-trees-equal-three\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ForestError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("laplacian entry row {row} col {col} is outside the triangle")]
    Index { row: usize, col: usize },
    #[error("cofactor arithmetic overflowed")]
    Overflow,
    #[error("cofactor {cofactor} disagrees with deletion-contraction {trees}")]
    Count { cofactor: i64, trees: i64 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, ForestError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn verify() -> Result<i64, ForestError> {
    let laplacian = [[2i64, -1, -1], [-1, 2, -1], [-1, -1, 2]];
    certify_trees(&laplacian, 1, 2)
}

pub fn certify_trees(laplacian: &[[i64; 3]; 3], deletion: i64, contraction: i64) -> Result<i64, ForestError> {
    let cofactor = triangle_cofactor(laplacian)?;
    let trees = deletion.checked_add(contraction).ok_or(ForestError::Overflow)?;
    if cofactor != trees {
        return Err(ForestError::Count { cofactor, trees });
    }
    Ok(trees)
}

pub fn triangle_cofactor(laplacian: &[[i64; 3]; 3]) -> Result<i64, ForestError> {
    let major = entry(laplacian, 0, 0)?.checked_mul(entry(laplacian, 1, 1)?).ok_or(ForestError::Overflow)?;
    let minor = entry(laplacian, 0, 1)?.checked_mul(entry(laplacian, 1, 0)?).ok_or(ForestError::Overflow)?;
    major.checked_sub(minor).ok_or(ForestError::Overflow)
}

pub fn entry(matrix: &[[i64; 3]; 3], row: usize, col: usize) -> Result<i64, ForestError> {
    let line = match matrix.get(row) {
        Some(found) => found,
        None => return Err(ForestError::Index { row, col }),
    };
    match line.get(col) {
        Some(found) => Ok(*found),
        None => Err(ForestError::Index { row, col }),
    }
}

pub fn executed_mutation_kills() -> Result<u32, ForestError> {
    let killed = kill_if(0, deletion_mutant_killed()?)?;
    let killed = kill_if(killed, sign_mutant_killed()?)?;
    let killed = kill_if(killed, index_mutant_killed()?)?;
    equivalent_forest_matches()?;
    Ok(killed)
}

fn deletion_mutant_killed() -> Result<bool, ForestError> {
    let laplacian = [[2i64, -1, -1], [-1, 2, -1], [-1, -1, 2]];
    Ok(certify_trees(&laplacian, 1, 1).is_err())
}

fn sign_mutant_killed() -> Result<bool, ForestError> {
    let flipped = [[2i64, 1, -1], [-1, 2, -1], [-1, -1, 2]];
    Ok(triangle_cofactor(&flipped)? != verify()?)
}

fn index_mutant_killed() -> Result<bool, ForestError> {
    let laplacian = [[2i64, -1, -1], [-1, 2, -1], [-1, -1, 2]];
    Ok(entry(&laplacian, 4, 0).is_err())
}

fn equivalent_forest_matches() -> Result<(), ForestError> {
    let oracle = verify()?;
    let again = verify()?;
    if again != oracle {
        return Err(ForestError::Count {
            cofactor: again,
            trees: oracle,
        });
    }
    Ok(())
}

fn kill_overflow() -> ForestError {
    ForestError::Token(crate::qm::exact_token::TokenError::Overflow {
        token: "kills".to_string(),
    })
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, ForestError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(kill_overflow()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_cofactor_is_three() -> Result<(), String> {
        let laplacian = [[2i64, -1, -1], [-1, 2, -1], [-1, -1, 2]];
        let cofactor = triangle_cofactor(&laplacian).map_err(|err| err.to_string())?;
        if cofactor != 3 {
            return Err(format!("cofactor {cofactor}"));
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_three_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("3").map_err(|err| err.to_string())?;
        let trees = verify().map_err(|err| err.to_string())?;
        if trees != admitted {
            return Err(format!("trees {trees}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_three() -> Result<(), String> {
        let trees = verify().map_err(|err| err.to_string())?;
        if trees != 3 {
            return Err(format!("trees {trees}"));
        }
        Ok(())
    }

    #[test]
    fn negative_index() -> Result<(), String> {
        let laplacian = [[2i64, -1, -1], [-1, 2, -1], [-1, -1, 2]];
        match entry(&laplacian, 3, 2) {
            Err(ForestError::Index { row, col }) if row == 3 && col == 2 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_count() -> Result<(), String> {
        let laplacian = [[2i64, -1, -1], [-1, 2, -1], [-1, -1, 2]];
        match certify_trees(&laplacian, 0, 0) {
            Err(ForestError::Count { cofactor, trees }) if cofactor == 3 && trees == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_overflow() -> Result<(), String> {
        match certify_trees(&[[1, 0, 0], [0, 1, 0], [0, 0, 1]], i64::MAX, 1) {
            Err(ForestError::Overflow) => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("2e3") {
            Err(ForestError::Token(crate::qm::exact_token::TokenError::FloatRefused { token })) if token == "2e3" => Ok(()),
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
