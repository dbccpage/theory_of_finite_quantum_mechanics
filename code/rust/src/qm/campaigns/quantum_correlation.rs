//! Finite correlation experiments; all decisions use the canonical physics kernel.
use crate::linear_algebra::{
    elimination::{solve, LinearSolution},
    matrix,
};
use num_integer::Integer;
use num_traits::{One, Signed, Zero};
use omega_number_theory::cyclotomic_field::{sqrt_of_integer, Cyclotomic, CyclotomicNumber};
use omega_number_theory::cyclotomic_ordered::element_minimal_polynomial;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::quantum_correlation::{self, PlanarObservable};
use serde::{Deserialize, Serialize};
pub const HEIGHT_BOUND: usize = 5;
pub const DECLARED_CONDUCTORS: [usize; 5] = [1, 2, 4, 8, 12];
pub const TSIRELSON_VALUE_STR: &str = "2*sqrt(2)";
pub const TSIRELSON_MIN_POLY: &str = "x^2 - 8 = 0";
pub const Q1_MAX_AT_BOUND_STR: &str = "14/5";
pub const Q1_MIN_POLY: &str = "5*x - 14 = 0";
pub const Q1_DEFICIT_MIN_POLY: &str = "25*x^2 + 140*x - 4 = 0";
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StaircaseRow {
    pub conductor: usize,
    pub carrier: String,
    pub height_bound: usize,
    pub admissible_vectors_count: usize,
    pub max_chsh_exact: String,
    pub minimal_polynomial: String,
    pub tsirelson_attained: bool,
    pub distance_from_tsirelson_exact: String,
    pub distance_minimal_polynomial: String,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Q2Witness {
    pub witness_id: String,
    pub conductor: usize,
    pub carrier: String,
    pub exact_chsh_value: String,
    pub minimal_polynomial: String,
    pub attained: bool,
}
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Q1Witness {
    pub witness_id: String,
    pub conductor: usize,
    pub carrier: String,
    pub height_bound: usize,
    pub exact_chsh_value: String,
    pub minimal_polynomial: String,
    pub attained: bool,
    pub distance_from_tsirelson_exact: String,
    pub distance_minimal_polynomial: String,
}
fn scalar(q: Rational) -> Cyclotomic<24> {
    Cyclotomic::rational(q)
}
fn fraction(q: &Rational) -> String {
    if q.denom().is_one() {
        q.numer().to_string()
    } else {
        format!("{}/{}", q.numer(), q.denom())
    }
}

/// Exact quadratic formatting is presentation only. A scalar is first decomposed
/// by the canonical rational field solver, and the decomposition is replayed.
pub fn render_real(x: &Cyclotomic<24>) -> Result<String, String> {
    if let Some(q) = x.as_number().as_rational() {
        return Ok(fraction(&q));
    }
    for d in [2, 3, 6] {
        let root = sqrt_of_integer(24, &d.into()).map_err(|e| e.to_string())?;
        let one = CyclotomicNumber::one(24).map_err(|e| e.to_string())?;
        let rows = (0..x.coefficients().len())
            .map(|i| {
                vec![
                    one.coefficients()[i].clone(),
                    root.coefficients()[i].clone(),
                ]
            })
            .collect();
        let m = matrix::from_rows(rows).map_err(|e| e.to_string())?;
        if let LinearSolution::Consistent { particular, .. } =
            solve(&m, x.coefficients()).map_err(|e| e.to_string())?
        {
            let a = &particular[0];
            let b = &particular[1];
            let term = if b.denom().is_one() {
                if b.numer().is_one() {
                    format!("sqrt({d})")
                } else {
                    format!("{}*sqrt({d})", b.numer())
                }
            } else {
                format!("({})*sqrt({d})", fraction(b))
            };
            return Ok(if a.is_zero() {
                term
            } else if b.is_positive() {
                format!("{} + {}", fraction(a), term)
            } else {
                format!("{} - {}", fraction(a), term.trim_start_matches('-'))
            });
        }
    }
    Ok(x.as_number().to_string())
}

pub fn minimal_polynomial_string(x: &Cyclotomic<24>) -> Result<String, String> {
    let p = element_minimal_polynomial(x.as_number()).map_err(|e| e.to_string())?;
    let scale = p
        .coefficients()
        .iter()
        .fold(num_bigint::BigInt::one(), |s, q| s.lcm(q.denom()));
    let coeffs = p
        .coefficients()
        .iter()
        .map(|q| q.numer() * (&scale / q.denom()))
        .collect::<Vec<_>>();
    let mut out = String::new();
    for (degree, c) in coeffs.iter().enumerate().rev() {
        if c.is_zero() {
            continue;
        }
        let magnitude = c.abs();
        if out.is_empty() {
            if c.is_negative() {
                out.push('-');
            }
        } else {
            out.push_str(if c.is_negative() { " - " } else { " + " });
        }
        if degree == 0 {
            out.push_str(&magnitude.to_string());
        } else {
            if !magnitude.is_one() {
                out.push_str(&format!("{magnitude}*"));
            }
            out.push('x');
            if degree > 1 {
                out.push_str(&format!("^{degree}"));
            }
        }
    }
    Ok(format!("{out} = 0"))
}

pub fn optimize_chsh_at_bound(
    conductor: usize,
    height_bound: usize,
) -> Result<StaircaseRow, String> {
    let directions = quantum_correlation::generate_unit_vectors(conductor, height_bound)
        .map_err(|e| e.to_string())?;
    let maximum = quantum_correlation::finite_planar_chsh_max(&directions, true, 1_000_000)
        .map_err(|e| e.to_string())?;
    let target = quantum_correlation::tsirelson_value();
    let gap = &target - &maximum.value;
    Ok(StaircaseRow {
        conductor,
        carrier: format!("declared planar Hermitian directions in Q(zeta_{conductor})"),
        height_bound,
        admissible_vectors_count: directions.len(),
        max_chsh_exact: render_real(&maximum.value)?,
        minimal_polynomial: minimal_polynomial_string(&maximum.value)?,
        tsirelson_attained: maximum.value == target,
        distance_from_tsirelson_exact: render_real(&gap)?,
        distance_minimal_polynomial: minimal_polynomial_string(&gap)?,
    })
}

pub fn q2_optimal_witness() -> Q2Witness {
    let s = quantum_correlation::tsirelson_value().scale(&rq(1, 4));
    let u1 = PlanarObservable::new(scalar(ri(1)), scalar(ri(0)), "A1").expect("fixed axis");
    let u2 = PlanarObservable::new(scalar(ri(0)), scalar(ri(1)), "A2").expect("fixed axis");
    let v1 = PlanarObservable::new(s.clone(), s.clone(), "B1").expect("fixed unit direction");
    let v2 = PlanarObservable::new(s.clone(), -s, "B2").expect("fixed unit direction");
    let value = quantum_correlation::evaluate_planar_chsh(&u1, &u2, &v1, &v2)
        .expect("fixed valid strategy");
    Q2Witness {
        witness_id: "Q2".into(),
        conductor: 8,
        carrier: "Herm_4(Q(zeta_8))".into(),
        exact_chsh_value: render_real(&value).expect("fixed quadratic value"),
        minimal_polynomial: minimal_polynomial_string(&value).expect("fixed quadratic polynomial"),
        attained: value == quantum_correlation::tsirelson_value(),
    }
}

pub fn q1_bounded_witness(height_bound: usize) -> Result<Q1Witness, String> {
    if !(5..=128).contains(&height_bound) {
        return Err(
            "the declared height does not admit the fixed denominator-five strategy".into(),
        );
    }
    let directions = [
        (ri(1), ri(0)),
        (ri(0), ri(1)),
        (rq(4, 5), rq(3, 5)),
        (rq(3, 5), rq(-4, 5)),
    ]
    .into_iter()
    .map(|(x, y)| PlanarObservable::new(scalar(x), scalar(y), "denominator-five strategy"))
    .collect::<Result<Vec<_>, _>>()
    .map_err(|e| e.to_string())?;
    let value = quantum_correlation::evaluate_planar_chsh(
        &directions[0],
        &directions[1],
        &directions[2],
        &directions[3],
    )
    .map_err(|e| e.to_string())?;
    let target = quantum_correlation::tsirelson_value();
    let gap = &target - &value;
    Ok(Q1Witness {
        witness_id: "Q1".into(),
        conductor: 4,
        carrier: "Herm_4(Q(i))".into(),
        height_bound,
        exact_chsh_value: render_real(&value)?,
        minimal_polynomial: minimal_polynomial_string(&value)?,
        attained: value == target,
        distance_from_tsirelson_exact: render_real(&gap)?,
        distance_minimal_polynomial: minimal_polynomial_string(&gap)?,
    })
}

pub fn compute_staircase(
    conductors: &[usize],
    height_bound: usize,
) -> Result<Vec<StaircaseRow>, String> {
    conductors
        .iter()
        .map(|&c| optimize_chsh_at_bound(c, height_bound))
        .collect()
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_exact_radical_arithmetic() {
        let q = scalar(rq(14, 5));
        let r = quantum_correlation::tsirelson_value();
        assert_eq!(minimal_polynomial_string(&q).unwrap(), "5*x - 14 = 0");
        assert_eq!(minimal_polynomial_string(&r).unwrap(), "x^2 - 8 = 0");
        assert_eq!(
            minimal_polynomial_string(&(r - q)).unwrap(),
            "25*x^2 + 140*x - 4 = 0"
        );
    }
    #[test]
    fn test_washington_criterion() {
        for n in [1, 2, 4, 12] {
            assert!(!quantum_correlation::sqrt2_in_cyclotomic(n));
        }
        for n in [8, 16] {
            assert!(quantum_correlation::sqrt2_in_cyclotomic(n));
        }
    }
    #[test]
    fn test_q2_optimal_attainment() {
        let w = q2_optimal_witness();
        assert_eq!(w.exact_chsh_value, "2*sqrt(2)");
        assert!(w.attained);
    }
    #[test]
    fn test_q1_non_attainment() {
        let w = q1_bounded_witness(5).unwrap();
        assert_eq!(w.exact_chsh_value, "14/5");
        assert!(!w.attained);
        assert_eq!(w.distance_minimal_polynomial, "25*x^2 + 140*x - 4 = 0");
        assert!(q1_bounded_witness(4).is_err());
    }
    #[test]
    fn test_staircase_parity() {
        for row in compute_staircase(&DECLARED_CONDUCTORS, HEIGHT_BOUND).unwrap() {
            assert_eq!(
                row.max_chsh_exact,
                if row.conductor == 8 {
                    "2*sqrt(2)"
                } else {
                    "14/5"
                }
            );
            assert_eq!(row.tsirelson_attained, row.conductor == 8);
        }
    }
}
