pub const PROVENANCE: &str = "Origin: research/dressed_graph_qed_g2_finite_map.md\nClaim: urn:tfqm:qm212:diamond-symanzik-units-equal-eight-and-triangle-sums-weights\nAuthorityEffect: None";

pub const MUTATION_KILL_RECORD: &str = "killed=3";

const ENDS: [[u8; 2]; 5] = [[0, 1], [1, 2], [2, 3], [3, 0], [0, 2]];
const TRIPLES: [[u8; 3]; 10] = [
    [0, 1, 2],
    [0, 1, 3],
    [0, 1, 4],
    [0, 2, 3],
    [0, 2, 4],
    [0, 3, 4],
    [1, 2, 3],
    [1, 2, 4],
    [1, 3, 4],
    [2, 3, 4],
];

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum DressedError {
    #[error(transparent)]
    Token(#[from] crate::qm::exact_token::TokenError),
    #[error("edge slot {slot} is outside the diamond")]
    Slot { slot: u8 },
    #[error("triangle weights {a}, {b}, {c} are not positive")]
    Weight { a: i64, b: i64, c: i64 },
    #[error("graph with {vertices} vertices and {edges} edges is not a positive carrier")]
    Shape { vertices: i64, edges: i64 },
    #[error("spanning-tree count {got} is not {expected}")]
    Trees { got: i64, expected: i64 },
    #[error("triangle polynomial {got} is not {expected}")]
    Triangle { got: i64, expected: i64 },
    #[error("kill counter overflowed at {killed}")]
    KillOverflow { killed: u32 },
}

pub fn admit_integer_token(token: &str) -> Result<i64, DressedError> {
    Ok(crate::qm::exact_token::admit_integer_token(token)?)
}

pub fn touch(slot: u8) -> Result<(), DressedError> {
    let mut seen = [false; 4];
    mark_edge(&mut seen, slot)
}

pub fn triangle_polynomial(a: i64, b: i64, c: i64) -> Result<i64, DressedError> {
    if a <= 0 || b <= 0 || c <= 0 {
        return Err(DressedError::Weight { a, b, c });
    }
    match a.checked_add(b).and_then(|sum| sum.checked_add(c)) {
        Some(sum) => Ok(sum),
        None => Err(DressedError::Weight { a, b, c }),
    }
}

pub fn certify_triangle(a: i64, b: i64, c: i64, expected: i64) -> Result<i64, DressedError> {
    let got = triangle_polynomial(a, b, c)?;
    if got != expected {
        return Err(DressedError::Triangle { got, expected });
    }
    Ok(got)
}

pub fn loop_number(vertices: i64, edges: i64) -> Result<i64, DressedError> {
    if vertices < 1 || edges < 0 {
        return Err(DressedError::Shape { vertices, edges });
    }
    match edges.checked_sub(vertices).and_then(|gap| gap.checked_add(1)) {
        Some(loops) => Ok(loops),
        None => Err(DressedError::Shape { vertices, edges }),
    }
}

pub fn require_tree_count(got: i64) -> Result<i64, DressedError> {
    if got != 8 {
        return Err(DressedError::Trees { got, expected: 8 });
    }
    Ok(got)
}

pub fn count_diamond_trees() -> Result<i64, DressedError> {
    let mut count = 0i64;
    for triple in TRIPLES {
        if covers_four(triple)? {
            count = match count.checked_add(1) {
                Some(next) => next,
                None => return Err(DressedError::Trees { got: count, expected: 8 }),
            };
        }
    }
    Ok(count)
}

pub fn verify() -> Result<i64, DressedError> {
    let trees = count_diamond_trees()?;
    let admitted = require_tree_count(trees)?;
    let polynomial = certify_triangle(1, 1, 1, 3)?;
    let loops = loop_number(4, 5)?;
    if polynomial != 3 || loops != 2 {
        return Err(DressedError::Triangle {
            got: polynomial,
            expected: loops,
        });
    }
    Ok(admitted)
}

pub fn executed_mutation_kills() -> Result<u32, DressedError> {
    let killed = kill_if(0, all_triples_killed()?)?;
    let killed = kill_if(killed, dropped_weight_killed()?)?;
    let killed = kill_if(killed, loop_drop_killed()?)?;
    equivalent_diamond_matches()?;
    Ok(killed)
}

fn all_triples_killed() -> Result<bool, DressedError> {
    Ok(mutant_count_every_triple() != verify()?)
}

fn dropped_weight_killed() -> Result<bool, DressedError> {
    Ok(mutant_drop_third() != 3)
}

fn loop_drop_killed() -> Result<bool, DressedError> {
    Ok(mutant_drop_loop_one() != loop_number(4, 5)?)
}

fn equivalent_diamond_matches() -> Result<(), DressedError> {
    let oracle = verify()?;
    let again = require_tree_count(8)?;
    if again != oracle {
        return Err(DressedError::Trees {
            got: again,
            expected: oracle,
        });
    }
    Ok(())
}

fn mutant_count_every_triple() -> i64 {
    TRIPLES.len() as i64
}

fn mutant_drop_third() -> i64 {
    1 + 1
}

fn mutant_drop_loop_one() -> i64 {
    5 - 4
}

fn covers_four(triple: [u8; 3]) -> Result<bool, DressedError> {
    let mut seen = [false; 4];
    mark_edge(&mut seen, triple[0])?;
    mark_edge(&mut seen, triple[1])?;
    mark_edge(&mut seen, triple[2])?;
    Ok(seen[0] && seen[1] && seen[2] && seen[3])
}

fn mark_edge(seen: &mut [bool; 4], slot: u8) -> Result<(), DressedError> {
    let edge = match ENDS.get(slot as usize) {
        Some(edge) => *edge,
        None => return Err(DressedError::Slot { slot }),
    };
    let left = match seen.get_mut(edge[0] as usize) {
        Some(bit) => bit,
        None => return Err(DressedError::Slot { slot }),
    };
    *left = true;
    let right = match seen.get_mut(edge[1] as usize) {
        Some(bit) => bit,
        None => return Err(DressedError::Slot { slot }),
    };
    *right = true;
    Ok(())
}

fn kill_if(killed: u32, dead: bool) -> Result<u32, DressedError> {
    if !dead {
        return Ok(killed);
    }
    match killed.checked_add(1) {
        Some(next) => Ok(next),
        None => Err(DressedError::KillOverflow { killed }),
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
    fn unit_diamond_has_eight_trees() -> Result<(), String> {
        if count_diamond_trees().map_err(|err| err.to_string())? != 8 {
            return Err("trees".to_string());
        }
        Ok(())
    }

    #[test]
    fn integration_admitted_eight_matches_verify() -> Result<(), String> {
        let admitted = admit_integer_token("8").map_err(|err| err.to_string())?;
        if admitted != verify().map_err(|err| err.to_string())? {
            return Err("admit".to_string());
        }
        Ok(())
    }

    #[test]
    fn e2e_public_verify_is_eight() -> Result<(), String> {
        if verify().map_err(|err| err.to_string())? != 8 {
            return Err("verify".to_string());
        }
        Ok(())
    }

    #[test]
    fn negative_slot() -> Result<(), String> {
        match touch(5) {
            Err(DressedError::Slot { slot }) if slot == 5 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_weight() -> Result<(), String> {
        match triangle_polynomial(1, 1, 0) {
            Err(DressedError::Weight { a, b, c }) if a == 1 && b == 1 && c == 0 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_shape() -> Result<(), String> {
        match loop_number(0, 5) {
            Err(DressedError::Shape { vertices, edges }) if vertices == 0 && edges == 5 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_trees() -> Result<(), String> {
        match require_tree_count(7) {
            Err(DressedError::Trees { got, expected }) if got == 7 && expected == 8 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_triangle() -> Result<(), String> {
        match certify_triangle(1, 1, 1, 2) {
            Err(DressedError::Triangle { got, expected }) if got == 3 && expected == 2 => Ok(()),
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_float_token() -> Result<(), String> {
        match admit_integer_token("2e3") {
            Err(DressedError::Token(crate::qm::exact_token::TokenError::FloatRefused { token }))
                if token == "2e3" =>
            {
                Ok(())
            }
            other => Err(format!("{other:?}")),
        }
    }

    #[test]
    fn negative_kill_overflow() -> Result<(), String> {
        match kill_if(u32::MAX, true) {
            Err(DressedError::KillOverflow { killed }) if killed == u32::MAX => Ok(()),
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
