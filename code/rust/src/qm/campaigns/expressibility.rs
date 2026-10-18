pub const PROVENANCE: &str = "Origin: papers/core/finite_quantum_mechanics_source_notes.md\nClaim: urn:tfqm:sp2-f2:generated-order-is-six-with-three-involutions-and-two-rotations\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ExprError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("permutation point {point} is outside three letters")]
    Index { point: usize },
    #[error("permutation sends {point} to {image}")]
    Image { point: usize, image: usize },
    #[error("generated order {found} is not {expected}")]
    Order { found: usize, expected: usize },
    #[error("census has {involutions} involutions and {rotations} rotations")]
    Shapes { involutions: usize, rotations: usize },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, ExprError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn apply_perm(perm: [usize; 3], point: usize) -> Result<usize, ExprError> {
    let image = match perm.get(point) {
        Some(image) => *image,
        None => return Err(ExprError::Index { point }),
    };
    if image > 2 {
        return Err(ExprError::Image { point, image });
    }
    Ok(image)
}

pub fn require_census(order: usize, involutions: usize, rotations: usize) -> Result<usize, ExprError> {
    if order != 6 {
        return Err(ExprError::Order {
            found: order,
            expected: 6,
        });
    }
    if involutions != 3 || rotations != 2 {
        return Err(ExprError::Shapes {
            involutions,
            rotations,
        });
    }
    Ok(order)
}

pub fn close_from(generators: [[usize; 3]; 2]) -> Result<usize, ExprError> {
    Ok(generate_from(generators)?.len())
}

pub fn verify() -> Result<usize, ExprError> {
    let transposition = [1usize, 0, 2];
    let cycle = [1usize, 2, 0];
    let group = generate_from([transposition, cycle])?;
    let involutions = count_order(&group, 2)?;
    let rotations = count_order(&group, 3)?;
    require_census(group.len(), involutions, rotations)
}

pub fn executed_mutation_kills() -> Result<u32, ExprError> {
    let killed = kill_if(0, transposition_only_killed()?)?;
    let killed = kill_if(killed, image_killed())?;
    let killed = kill_if(killed, shape_killed())?;
    equivalent_order_matches()?;
    Ok(killed)
}

fn transposition_only_killed() -> Result<bool, ExprError> {
    let transposition = [1usize, 0, 2];
    Ok(close_from([transposition, transposition])? != verify()?)
}

fn image_killed() -> bool {
    apply_perm([3, 0, 1], 0).is_err()
}

fn shape_killed() -> bool {
    require_census(6, 0, 2).is_err()
}

fn equivalent_order_matches() -> Result<(), ExprError> {
    let oracle = verify()?;
    let again = require_census(6, 3, 2)?;
    if again != oracle {
        return Err(ExprError::Order {
            found: again,
            expected: oracle,
        });
    }
    Ok(())
}

fn generate_from(generators: [[usize; 3]; 2]) -> Result<Vec<[usize; 3]>, ExprError> {
    let mut group = vec![[0usize, 1, 2]];
    let mut cursor = 0usize;
    while cursor < group.len() {
        let current = match group.get(cursor) {
            Some(perm) => *perm,
            None => return Err(ExprError::Index { point: cursor }),
        };
        cursor += 1;
        admit(&mut group, compose(generators[0], current)?)?;
        admit(&mut group, compose(generators[1], current)?)?;
    }
    Ok(group)
}

fn admit(group: &mut Vec<[usize; 3]>, next: [usize; 3]) -> Result<(), ExprError> {
    if group.contains(&next) {
        return Ok(());
    }
    group.push(next);
    Ok(())
}

fn compose(left: [usize; 3], right: [usize; 3]) -> Result<[usize; 3], ExprError> {
    Ok([
        apply_perm(left, right[0])?,
        apply_perm(left, right[1])?,
        apply_perm(left, right[2])?,
    ])
}

fn count_order(group: &[[usize; 3]], target: usize) -> Result<usize, ExprError> {
    let mut count = 0usize;
    for perm in group {
        if order_of(*perm)? == target {
            count += 1;
        }
    }
    Ok(count)
}

fn order_of(perm: [usize; 3]) -> Result<usize, ExprError> {
    let mut current = perm;
    let mut steps = 1usize;
    while current != [0, 1, 2] {
        if steps > 6 {
            return Err(ExprError::Order {
                found: steps,
                expected: 6,
            });
        }
        current = compose(perm, current)?;
        steps += 1;
    }
    Ok(steps)
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, ExprError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(ExprError::KillOverflow { killed }),
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
    fn unit_transposition_and_cycle_have_order_six() -> Result<(), String> {
        let order = close_from([[1, 0, 2], [1, 2, 0]]).map_err(|err| err.to_string())?;
        if order != 6 {
            return Err(order.to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_six_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("6").map_err(|err| err.to_string())?;
        if admitted != verify().map_err(|err| err.to_string())? as i64 {
            return Err("admit".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_six() -> Result<(), String> {
        if verify().map_err(|err| err.to_string())? != 6 {
            return Err("verify".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_index() -> Result<(), String> {
        match apply_perm([0, 1, 2], 3) {
            Err(ExprError::Index { point }) if point == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_image() -> Result<(), String> {
        match apply_perm([3, 0, 1], 0) {
            Err(ExprError::Image { point, image }) if point == 0 && image == 3 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_order() -> Result<(), String> {
        match require_census(2, 1, 0) {
            Err(ExprError::Order { found, expected }) if found == 2 && expected == 6 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_shapes() -> Result<(), String> {
        match require_census(6, 0, 2) {
            Err(ExprError::Shapes {
                involutions,
                rotations,
            }) if involutions == 0 && rotations == 2 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("1.5") {
            Err(ExprError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
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
            Err(ExprError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
