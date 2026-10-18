//! Rejection-Ledger Guard Mining & Trace Verification (REV-SMRM-P3-MINE) exact verifier.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Candidate(pub u8, pub u8, pub u8);

pub fn is_valid(c: Candidate) -> bool {
    c.0 == 1 && c.1 != 0 && c.2 == 2
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Guard {
    FirstNotOne,
    SecondIsZero,
    ThirdNotTwo,
}

pub fn mine_guard(c: Candidate) -> Option<Guard> {
    if c.0 != 1 {
        Some(Guard::FirstNotOne)
    } else if c.1 == 0 {
        Some(Guard::SecondIsZero)
    } else if c.2 != 2 {
        Some(Guard::ThirdNotTwo)
    } else {
        None
    }
}

pub fn guard_rejects(g: Guard, c: Candidate) -> bool {
    match g {
        Guard::FirstNotOne => c.0 != 1,
        Guard::SecondIsZero => c.1 == 0,
        Guard::ThirdNotTwo => c.2 != 2,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mined_guards_never_reject_valid_candidates() {
        let mut universe = Vec::new();
        for a in 0..3 {
            for b in 0..3 {
                for c in 0..3 {
                    universe.push(Candidate(a, b, c));
                }
            }
        }
        for cand in &universe {
            if !is_valid(*cand) {
                let g = mine_guard(*cand).expect("invalid candidate must yield guard");
                assert!(guard_rejects(g, *cand));
                for v in universe.iter().copied().filter(|x| is_valid(*x)) {
                    assert!(!guard_rejects(g, v));
                }
            }
        }
    }
}
