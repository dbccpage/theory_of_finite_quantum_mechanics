
use num_traits::Signed;
use engine_number_theory::rational::{ri, Rational};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; CHSH/Tsirelson + Mermin-Peres cochain bridge face.";

pub type Q = Rational;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChshBounds {
    pub classical: Q,
    pub tsirelson_squared: Q,
    pub note: &'static str,
}

impl ChshBounds {
    pub fn standard() -> Self {
        Self {
            classical: ri(2),
            tsirelson_squared: &ri(2) * &ri(2) * &ri(2),
            note: "Tsirelson value 2√2 is not an element of ℚ; uniqueness of the bound \
                   is recorded via S² ≤ 8 for quantum, |S| ≤ 2 classical. Exact √2 \
                   residual OPEN on this rational face.",
        }
    }

    pub fn classify_s_squared(&self, s_sq: &Q) -> Result<ChshClass, &'static str> {
        if s_sq.is_negative() {
            return Err("a squared correlator cannot be negative");
        }
        let classical_sq = &self.classical * &self.classical;
        if s_sq <= &classical_sq {
            Ok(ChshClass::ClassicalCompatible)
        } else if s_sq <= &self.tsirelson_squared {
            Ok(ChshClass::QuantumCompatible)
        } else {
            Ok(ChshClass::BeyondTsirelson)
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ChshClass {
    ClassicalCompatible,
    QuantumCompatible,
    BeyondTsirelson,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChshExample {
    pub label: &'static str,
    pub s_squared: Q,
    pub class: ChshClass,
}

impl ChshExample {
    pub fn classical_max() -> Self {
        let bounds = ChshBounds::standard();
        let s_sq = &bounds.classical * &bounds.classical;
        Self::from_square("classical_max", s_sq, &bounds)
    }

    pub fn tsirelson_max_marker() -> Self {
        let bounds = ChshBounds::standard();
        let s_sq = bounds.tsirelson_squared.clone();
        Self::from_square("tsirelson_S2_eq_8", s_sq, &bounds)
    }

    pub fn pr_box() -> Self {
        let bounds = ChshBounds::standard();
        let s = &ri(2) + &ri(2);
        let s_sq = &s * &s;
        Self::from_square("pr_box", s_sq, &bounds)
    }

    fn from_square(label: &'static str, s_squared: Q, bounds: &ChshBounds) -> Self {
        let class = match bounds.classify_s_squared(&s_squared) {
            Ok(class) => class,
            Err(_) => ChshClass::BeyondTsirelson,
        };
        Self {
            label,
            s_squared,
            class,
        }
    }
}

pub fn chsh_value(correlators: &[Q; 4]) -> Q {
    &correlators[0] + &correlators[1] + &correlators[2] - &correlators[3]
}

pub fn chsh_square_two_ways(correlators: &[Q; 4]) -> Result<(Q, Q), &'static str> {
    let value = chsh_value(correlators);
    let direct = &value * &value;
    let expanded = expand_square(correlators);
    if direct != expanded {
        return Err("CHSH square readings disagree");
    }
    Ok((direct, expanded))
}

fn expand_square(correlators: &[Q; 4]) -> Q {
    let a = &correlators[0];
    let b = &correlators[1];
    let c = &correlators[2];
    let d = &correlators[3];
    let two = ri(2);
    a * a + b * b + c * c + d * d + &two * a * b + &two * a * c - &two * a * d + &two * b * c
        - &two * b * d
        - &two * c * d
}

pub fn mermin_square_has_no_noncontextual_assignment() -> Result<u32, &'static str> {
    let row_parity = 0u8 ^ 0 ^ 0;
    let col_parity = 0u8 ^ 0 ^ 1;
    if row_parity == col_parity {
        return Err("Mermin parity does not obstruct");
    }
    let mut found = 0u32;
    for mask in 0..512u32 {
        let bit = |index: u32| ((mask >> index) & 1) as u8;
        let rows = bit(0) ^ bit(1) ^ bit(2) == 0
            && bit(3) ^ bit(4) ^ bit(5) == 0
            && bit(6) ^ bit(7) ^ bit(8) == 0;
        let cols = bit(0) ^ bit(3) ^ bit(6) == 0
            && bit(1) ^ bit(4) ^ bit(7) == 0
            && bit(2) ^ bit(5) ^ bit(8) == 1;
        if rows && cols {
            found = found.saturating_add(1);
        }
    }
    if found != 0 {
        return Err("a noncontextual assignment exists");
    }
    Ok(found)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn chsh_classical_quantum_pr_separation() {
        let classical = ChshExample::classical_max();
        let quantum = ChshExample::tsirelson_max_marker();
        let pr = ChshExample::pr_box();
        let correlators = [ri(1), ri(1), ri(1), ri(-1)];
        let (direct, expanded) = match chsh_square_two_ways(&correlators) {
            Ok(pair) => pair,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        assert_eq!(direct, expanded);
        assert_eq!(pr.s_squared, direct);
        assert!(direct > ChshBounds::standard().tsirelson_squared);
        assert_eq!(classical.class, ChshClass::ClassicalCompatible);
        assert_eq!(quantum.class, ChshClass::QuantumCompatible);
        assert_eq!(pr.class, ChshClass::BeyondTsirelson);
        let assignments = match mermin_square_has_no_noncontextual_assignment() {
            Ok(count) => count,
            Err(error) => {
                assert!(false, "{error}");
                return;
            }
        };
        assert_eq!(assignments, 0);
    }

    #[test]
    fn negative_s_squared_is_refused_and_a_bound_is_not_membership() {
        assert!(ChshBounds::standard().classify_s_squared(&ri(-1)).is_err());
    }
}
