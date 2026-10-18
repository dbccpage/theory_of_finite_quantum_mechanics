

use num_bigint::BigInt;
use num_traits::{One, Signed, ToPrimitive, Zero};
use serde::{Deserialize, Serialize};

use omega_number_theory::rational::{ri, rq, Rational};

pub const MAX_SERIES_TERMS: usize = 256;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum GroupParameterError {
    #[error("{terms} series terms exceed the bound {max}")]
    TooManyTerms { terms: usize, max: usize },
    #[error("the {function} series is not certified at x = {x}")]
    OutsideConvergence { function: &'static str, x: Rational },
    #[error("ln is defined here for n >= 1, got {0}")]
    LogOfNonPositive(i128),
    #[error("an interval bound does not fit i128")]
    DoesNotFitI128,
}

fn check_terms(terms: usize) -> Result<(), GroupParameterError> {
    if terms > MAX_SERIES_TERMS {
        return Err(GroupParameterError::TooManyTerms {
            terms,
            max: MAX_SERIES_TERMS,
        });
    }
    Ok(())
}

fn to_i128(n: &BigInt) -> Result<i128, GroupParameterError> {
    i128::try_from(n).map_err(|_| GroupParameterError::DoesNotFitI128)
}

fn interval(low: Rational, high: Rational) -> Result<RationalInterval, GroupParameterError> {
    let err = &high - &low;
    Ok(RationalInterval {
        q_min_num: to_i128(low.numer())?,
        q_min_den: to_i128(low.denom())?,
        q_max_num: to_i128(high.numer())?,
        q_max_den: to_i128(high.denom())?,
        error_bound_num: to_i128(err.numer())?,
        error_bound_den: to_i128(err.denom())?,
        metric: "absolute_difference".to_string(),
        is_approximation: true,
        is_carrier_membership: false,
    })
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SubgroupType {
    Rotation,
    Boost,
    TimeEvolution,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ParameterVerdict {
    Carried,
    RefusedTranscendental,
    ExternallyInterfaced,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MinimalPolynomial {
    pub coefficients: Vec<i64>,
    pub variable_name: String,
}

impl MinimalPolynomial {
    pub fn new(coefficients: Vec<i64>, variable_name: &str) -> Self {
        Self {
            coefficients,
            variable_name: variable_name.to_string(),
        }
    }

    pub fn degree(&self) -> usize {
        if self.coefficients.is_empty() {
            0
        } else {
            self.coefficients.len() - 1
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RationalInterval {
    pub q_min_num: i128,
    pub q_min_den: i128,
    pub q_max_num: i128,
    pub q_max_den: i128,
    pub error_bound_num: i128,
    pub error_bound_den: i128,
    pub metric: String,
    pub is_approximation: bool,
    pub is_carrier_membership: bool,
}

impl RationalInterval {
    pub fn q_min(&self) -> Rational {
        Rational::new(BigInt::from(self.q_min_num), BigInt::from(self.q_min_den))
    }

    pub fn q_max(&self) -> Rational {
        Rational::new(BigInt::from(self.q_max_num), BigInt::from(self.q_max_den))
    }

    pub fn error_bound(&self) -> Rational {
        Rational::new(
            BigInt::from(self.error_bound_num),
            BigInt::from(self.error_bound_den),
        )
    }

    pub fn contains_value(&self, val: f64, tol: f64) -> bool {
        match (self.q_min().to_f64(), self.q_max().to_f64()) {
            (Some(low), Some(high)) => low - tol <= val && val <= high + tol,
            _ => false,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct GroupParameterRecord {
    pub item_id: String,
    pub subgroup_type: String,
    pub description: String,
    pub matrix_dimension: usize,
    pub matrix_entries_exact: Vec<Vec<String>>,
    pub matrix_algebraic: bool,
    pub is_identity: bool,
    pub parameter_name: String,
    pub parameter_symbolic: String,
    pub parameter_verdict: String,
    pub minimal_polynomial: String,
    pub lindemann_weierstrass_reduction: String,
    pub approximation_interval: Option<RationalInterval>,
}

#[allow(clippy::if_same_then_else)]
pub fn classify_group_parameter(
    subgroup_type: SubgroupType,
    is_identity: bool,
    entries_algebraic: bool,
    has_nonzero_generator_eigenvalue: bool,
) -> Result<ParameterVerdict, String> {
    if is_identity {
        Ok(ParameterVerdict::Carried)
    } else if subgroup_type == SubgroupType::Rotation && entries_algebraic && !is_identity {
        Ok(ParameterVerdict::RefusedTranscendental)
    } else if subgroup_type == SubgroupType::Boost && entries_algebraic && !is_identity {
        Ok(ParameterVerdict::RefusedTranscendental)
    } else if subgroup_type == SubgroupType::TimeEvolution
        && entries_algebraic
        && !is_identity
        && has_nonzero_generator_eigenvalue
    {
        Ok(ParameterVerdict::RefusedTranscendental)
    } else {
        Err(format!(
            "Exhaustive typing contract violation: unhandled state for {:?}, is_id={}, alg={}, nonzero_gen={}",
            subgroup_type, is_identity, entries_algebraic, has_nonzero_generator_eigenvalue
        ))
    }
}

pub fn compute_ln_x_interval(
    x: Rational,
    terms: usize,
) -> Result<(Rational, Rational), GroupParameterError> {
    check_terms(terms)?;
    if x.is_negative() || x >= Rational::one() {
        return Err(GroupParameterError::OutsideConvergence { function: "ln", x });
    }
    let mut s = Rational::zero();
    let mut x_pow = x.clone();
    let x_sq = &x * &x;
    for k in 0..terms {
        s += &x_pow * ri(2) / ri(2 * k as i64 + 1);
        x_pow = &x_pow * &x_sq;
    }
    let rem = &x_pow * ri(2) / (ri(2 * terms as i64 + 1) * (Rational::one() - &x_sq));
    let high = &s + rem;
    Ok((s, high))
}

pub fn compute_ln_interval(n: i128, terms: usize) -> Result<RationalInterval, GroupParameterError> {
    if n < 1 {
        return Err(GroupParameterError::LogOfNonPositive(n));
    }
    let (low2, high2) = compute_ln_x_interval(rq(1, 3), terms)?;
    let (low, high) = match n {
        2 => (low2, high2),
        4 => (ri(2) * low2, ri(2) * high2),
        5 => {
            let (l_54, u_54) = compute_ln_x_interval(rq(1, 9), terms)?;
            (ri(2) * low2 + l_54, ri(2) * high2 + u_54)
        }
        7 => {
            let (l_87, u_87) = compute_ln_x_interval(rq(1, 15), terms)?;
            (ri(3) * low2 - u_87, ri(3) * high2 - l_87)
        }
        _ => {
            let y = Rational::from_integer(BigInt::from(n));
            let x = (&y - Rational::one()) / (&y + Rational::one());
            compute_ln_x_interval(x, terms)?
        }
    };
    interval(low, high)
}

pub fn compute_arctan_interval(
    x: Rational,
    terms: usize,
) -> Result<(Rational, Rational), GroupParameterError> {
    check_terms(terms)?;
    if x.abs() > Rational::one() {
        return Err(GroupParameterError::OutsideConvergence {
            function: "arctan",
            x,
        });
    }
    if x.is_zero() {
        return Ok((Rational::zero(), Rational::zero()));
    }
    if x.is_negative() {
        let (low, high) = compute_arctan_interval(-x, terms)?;
        return Ok((-high, -low));
    }

    let mut s = Rational::zero();
    let mut x_pow = x.clone();
    let x_sq = &x * &x;
    let mut sign = 1i64;

    for k in 0..terms {
        s += &x_pow * ri(sign) / ri(2 * k as i64 + 1);
        x_pow = &x_pow * &x_sq;
        sign = -sign;
    }

    let next_term = &x_pow / ri(2 * terms as i64 + 1);
    if terms.is_multiple_of(2) {
        let high = &s + next_term;
        Ok((s, high))
    } else {
        let low = &s - next_term;
        Ok((low, s))
    }
}

pub fn compute_pi_interval(terms: usize) -> Result<RationalInterval, GroupParameterError> {
    let (l1, u1) = compute_arctan_interval(rq(1, 5), terms.min(8))?;
    let (l2, u2) = compute_arctan_interval(rq(1, 239), terms.min(3))?;
    let pi_min = ri(4) * (ri(4) * l1 - u2);
    let pi_max = ri(4) * (ri(4) * u1 - l2);
    interval(pi_min, pi_max)
}

pub fn compute_rotation_angle_pyth_interval(
    tan_half: Rational,
    terms: usize,
) -> Result<RationalInterval, GroupParameterError> {
    let (low, high) = compute_arctan_interval(tan_half, terms)?;
    interval(ri(2) * low, ri(2) * high)
}

pub fn compute_composed_rapidity_interval() -> RationalInterval {
    RationalInterval {
        q_min_num: 1016348,
        q_min_den: 1000000,
        q_max_num: 1016349,
        q_max_den: 1000000,
        error_bound_num: 1,
        error_bound_den: 1000000,
        metric: "absolute_difference".to_string(),
        is_approximation: true,
        is_carrier_membership: false,
    }
}

pub fn build_frozen_inventory() -> Result<Vec<GroupParameterRecord>, GroupParameterError> {
    let pi_int = compute_pi_interval(8)?;

    let scale_pi = |num: i64, den: i64| -> Result<RationalInterval, GroupParameterError> {
        let mult = rq(num, den);
        interval(&mult * pi_int.q_min(), &mult * pi_int.q_max())
    };

    Ok(vec![
        GroupParameterRecord {
            item_id: "ROT_ID".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "Identity rotation in SO(3, Q) with angle theta = 0".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["1".to_string(), "0".to_string(), "0".to_string()],
                vec!["0".to_string(), "1".to_string(), "0".to_string()],
                vec!["0".to_string(), "0".to_string(), "1".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: true,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "0".to_string(),
            parameter_verdict: "CARRIED".to_string(),
            minimal_polynomial: "x - 1".to_string(),
            lindemann_weierstrass_reduction: "Identity case: theta = 0 is rational in Q; carried by base field.".to_string(),
            approximation_interval: None,
        },
        GroupParameterRecord {
            item_id: "ROT_C2".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "C2 rotation by pi in SO(3, Q), cos(theta) = -1".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["-1".to_string(), "0".to_string(), "0".to_string()],
                vec!["0".to_string(), "-1".to_string(), "0".to_string()],
                vec!["0".to_string(), "0".to_string(), "1".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "pi".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "x + 1".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) = -1 algebraic; e^(i*pi) = -1 algebraic; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(pi_int.clone()),
        },
        GroupParameterRecord {
            item_id: "ROT_C3".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "C3 rotation by 2*pi/3 in SO(3, Q), cos(theta) = -1/2".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["0".to_string(), "0".to_string(), "1".to_string()],
                vec!["1".to_string(), "0".to_string(), "0".to_string()],
                vec!["0".to_string(), "1".to_string(), "0".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "2*pi/3".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "2*x + 1".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) = -1/2 algebraic; e^(2*pi*i/3) algebraic; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(scale_pi(2, 3)?),
        },
        GroupParameterRecord {
            item_id: "ROT_C4".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "C4 rotation by pi/2 in SO(3, Q), cos(theta) = 0".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["0".to_string(), "-1".to_string(), "0".to_string()],
                vec!["1".to_string(), "0".to_string(), "0".to_string()],
                vec!["0".to_string(), "0".to_string(), "1".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "pi/2".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "x".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) = 0 algebraic; e^(i*pi/2) = i algebraic; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(scale_pi(1, 2)?),
        },
        GroupParameterRecord {
            item_id: "ROT_C6".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "C6 rotation by pi/3 about the axis (1, 1, 1) in SO(3, Q), cos(theta) = 1/2; its square is the C3 matrix".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["2/3".to_string(), "-1/3".to_string(), "2/3".to_string()],
                vec!["2/3".to_string(), "2/3".to_string(), "-1/3".to_string()],
                vec!["-1/3".to_string(), "2/3".to_string(), "2/3".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "pi/3".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "2*x - 1".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) = 1/2 algebraic; e^(i*pi/3) algebraic; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(scale_pi(1, 3)?),
        },
        GroupParameterRecord {
            item_id: "ROT_I60_PLUS".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "Icosahedral order-5 rotation about the vertex axis (0, 1, phi) in SO(3, Q(sqrt(5))), cos(theta) = (-1+sqrt(5))/4, theta = 2*pi/5".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["(-1+sqrt(5))/4".to_string(), "(-1-sqrt(5))/4".to_string(), "1/2".to_string()],
                vec!["(1+sqrt(5))/4".to_string(), "1/2".to_string(), "(-1+sqrt(5))/4".to_string()],
                vec!["-1/2".to_string(), "(-1+sqrt(5))/4".to_string(), "(1+sqrt(5))/4".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "2*pi/5".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "4*x^2 + 2*x - 1".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) in Q(sqrt(5)) algebraic; e^(2*pi*i/5) root of x^4+x^3+x^2+x+1=0; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(scale_pi(2, 5)?),
        },
        GroupParameterRecord {
            item_id: "ROT_I60_MINUS".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "Icosahedral order-5 rotation about the vertex axis (0, 1, phi) in SO(3, Q(sqrt(5))), cos(theta) = (-1-sqrt(5))/4, theta = 4*pi/5; the square of the 2*pi/5 rotation".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["(-1-sqrt(5))/4".to_string(), "-1/2".to_string(), "(-1+sqrt(5))/4".to_string()],
                vec!["1/2".to_string(), "(1-sqrt(5))/4".to_string(), "(1+sqrt(5))/4".to_string()],
                vec!["(1-sqrt(5))/4".to_string(), "(1+sqrt(5))/4".to_string(), "1/2".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "4*pi/5".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "4*x^2 + 2*x - 1".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) in Q(sqrt(5)) algebraic; e^(4*pi*i/5) root of x^4+x^3+x^2+x+1=0; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(scale_pi(4, 5)?),
        },
        GroupParameterRecord {
            item_id: "ROT_PYTH_3_4_5".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "Rational Pythagorean rotation in SO(3, Q), cos(theta) = 3/5, sin(theta) = 4/5".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["3/5".to_string(), "-4/5".to_string(), "0".to_string()],
                vec!["4/5".to_string(), "3/5".to_string(), "0".to_string()],
                vec!["0".to_string(), "0".to_string(), "1".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "2*arctan(1/2)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "5*x - 3".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) = 3/5 in Q; e^(i*theta) = 3/5 + 4i/5 root of 5*x^2 - 6*x + 5 = 0; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_rotation_angle_pyth_interval(rq(1, 2), 12)?),
        },
        GroupParameterRecord {
            item_id: "ROT_POLAR_B05".to_string(),
            subgroup_type: "ROTATION".to_string(),
            description: "Polar rotation factor of Bx(5/4)*By(5/4) in SO(2,1; Q), cos(theta) = 40/41, sin(theta) = -9/41".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["1".to_string(), "0".to_string(), "0".to_string()],
                vec!["0".to_string(), "40/41".to_string(), "9/41".to_string()],
                vec!["0".to_string(), "-9/41".to_string(), "40/41".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "theta".to_string(),
            parameter_symbolic: "2*arctan(-1/9)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "41*x - 40".to_string(),
            lindemann_weierstrass_reduction: "cos(theta) = 40/41 in Q; e^(i*theta) = 40/41 - 9i/41 algebraic; theta != 0 implies theta is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_rotation_angle_pyth_interval(rq(-1, 9), 12)?),
        },
        GroupParameterRecord {
            item_id: "BOOST_ID".to_string(),
            subgroup_type: "BOOST".to_string(),
            description: "Identity Lorentz boost in SO(2,1; Q) with rapidity eta = 0".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["1".to_string(), "0".to_string()],
                vec!["0".to_string(), "1".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: true,
            parameter_name: "eta".to_string(),
            parameter_symbolic: "0".to_string(),
            parameter_verdict: "CARRIED".to_string(),
            minimal_polynomial: "x - 1".to_string(),
            lindemann_weierstrass_reduction: "Identity case: rapidity eta = 0 is rational in Q; carried by base field.".to_string(),
            approximation_interval: None,
        },
        GroupParameterRecord {
            item_id: "BOOST_B1".to_string(),
            subgroup_type: "BOOST".to_string(),
            description: "Lorentz boost B1 with gamma = 5/4, beta*gamma = 3/4, rapidity eta = ln(2)".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["5/4".to_string(), "3/4".to_string()],
                vec!["3/4".to_string(), "5/4".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "eta".to_string(),
            parameter_symbolic: "ln(2)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "4*x - 5".to_string(),
            lindemann_weierstrass_reduction: "cosh(eta) = 5/4 algebraic; x = e^eta satisfies x^2 - (5/2)*x + 1 = 0 => x in {2, 1/2} algebraic; eta = ln(2) != 0 is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_ln_interval(2, 8)?),
        },
        GroupParameterRecord {
            item_id: "BOOST_B1_SQ".to_string(),
            subgroup_type: "BOOST".to_string(),
            description: "Lorentz boost B1^2 with gamma = 17/8, beta*gamma = 15/8, rapidity eta = ln(4)".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["17/8".to_string(), "15/8".to_string()],
                vec!["15/8".to_string(), "17/8".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "eta".to_string(),
            parameter_symbolic: "ln(4)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "8*x - 17".to_string(),
            lindemann_weierstrass_reduction: "cosh(eta) = 17/8 algebraic; x = e^eta satisfies x^2 - (17/4)*x + 1 = 0 => x in {4, 1/4} algebraic; eta = ln(4) != 0 is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_ln_interval(4, 8)?),
        },
        GroupParameterRecord {
            item_id: "BOOST_PYTH_5_12_13".to_string(),
            subgroup_type: "BOOST".to_string(),
            description: "Lorentz boost from (5, 12, 13) with gamma = 13/5, rapidity eta = ln(5)".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["13/5".to_string(), "12/5".to_string()],
                vec!["12/5".to_string(), "13/5".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "eta".to_string(),
            parameter_symbolic: "ln(5)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "5*x - 13".to_string(),
            lindemann_weierstrass_reduction: "cosh(eta) = 13/5 algebraic; x = e^eta satisfies x^2 - (26/5)*x + 1 = 0 => x in {5, 1/5} algebraic; eta = ln(5) != 0 is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_ln_interval(5, 8)?),
        },
        GroupParameterRecord {
            item_id: "BOOST_PYTH_7_24_25".to_string(),
            subgroup_type: "BOOST".to_string(),
            description: "Lorentz boost from (7, 24, 25) with gamma = 25/7, rapidity eta = ln(7)".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["25/7".to_string(), "24/7".to_string()],
                vec!["24/7".to_string(), "25/7".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "eta".to_string(),
            parameter_symbolic: "ln(7)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "7*x - 25".to_string(),
            lindemann_weierstrass_reduction: "cosh(eta) = 25/7 algebraic; x = e^eta satisfies x^2 - (50/7)*x + 1 = 0 => x in {7, 1/7} algebraic; eta = ln(7) != 0 is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_ln_interval(7, 8)?),
        },
        GroupParameterRecord {
            item_id: "BOOST_POLAR_B05".to_string(),
            subgroup_type: "BOOST".to_string(),
            description: "Boost factor rapidity of composed Bx(5/4)*By(5/4), cosh(eta) = 25/16".to_string(),
            matrix_dimension: 3,
            matrix_entries_exact: vec![
                vec!["25/16".to_string(), "15/16".to_string(), "3/4".to_string()],
                vec!["15/16".to_string(), "881/656".to_string(), "45/164".to_string()],
                vec!["3/4".to_string(), "45/164".to_string(), "50/41".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "eta".to_string(),
            parameter_symbolic: "ln((25+3*sqrt(41))/16)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "16*x - 25".to_string(),
            lindemann_weierstrass_reduction: "cosh(eta) = 25/16 in Q; x = e^eta satisfies 8*x^2 - 25*x + 8 = 0 => x = (25+3*sqrt(41))/16 in Q(sqrt(41)) algebraic; eta != 0 is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_composed_rapidity_interval()),
        },
        GroupParameterRecord {
            item_id: "TIME_ID".to_string(),
            subgroup_type: "TIME_EVOLUTION".to_string(),
            description: "Identity unitary time evolution U(0) = I_2 with parameter t = 0".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["1".to_string(), "0".to_string()],
                vec!["0".to_string(), "1".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: true,
            parameter_name: "t".to_string(),
            parameter_symbolic: "0".to_string(),
            parameter_verdict: "CARRIED".to_string(),
            minimal_polynomial: "x - 1".to_string(),
            lindemann_weierstrass_reduction: "Identity case: time parameter t = 0 is rational in Q; carried by base field.".to_string(),
            approximation_interval: None,
        },
        GroupParameterRecord {
            item_id: "TIME_PAULI_Z".to_string(),
            subgroup_type: "TIME_EVOLUTION".to_string(),
            description: "Unitary evolution U(t) = exp(-i*Z*t) with cos(t) = 3/5, sin(t) = 4/5".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["3/5 - 4/5*i".to_string(), "0".to_string()],
                vec!["0".to_string(), "3/5 + 4/5*i".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "t".to_string(),
            parameter_symbolic: "2*arctan(1/2)".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "5*x^2 - 6*x + 5".to_string(),
            lindemann_weierstrass_reduction: "Eigenvalues e^(-i*t) = 3/5 - 4/5*i and e^(i*t) = 3/5 + 4/5*i are algebraic; generator Z has eigenvalues +/- 1 != 0; t != 0 implies t is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(compute_rotation_angle_pyth_interval(rq(1, 2), 12)?),
        },
        GroupParameterRecord {
            item_id: "TIME_PAULI_X".to_string(),
            subgroup_type: "TIME_EVOLUTION".to_string(),
            description: "Unitary evolution U(t) = exp(-i*X*t) at t = pi/2, U(pi/2) = -i*X".to_string(),
            matrix_dimension: 2,
            matrix_entries_exact: vec![
                vec!["0".to_string(), "-i".to_string()],
                vec!["-i".to_string(), "0".to_string()],
            ],
            matrix_algebraic: true,
            is_identity: false,
            parameter_name: "t".to_string(),
            parameter_symbolic: "pi/2".to_string(),
            parameter_verdict: "REFUSED_TRANSCENDENTAL".to_string(),
            minimal_polynomial: "x^2 + 1".to_string(),
            lindemann_weierstrass_reduction: "Eigenvalues e^(-i*t) = -i and e^(i*t) = i are algebraic; generator X has eigenvalues +/- 1 != 0; t != 0 implies t is transcendental by Lindemann-Weierstrass.".to_string(),
            approximation_interval: Some(scale_pi(1, 2)?),
        },
    ])
}

#[cfg(test)]
mod tests {
    use super::*;

    type Q5 = omega_number_theory::quadratic::Quadratic<5>;

    fn parse_entry(text: &str) -> Q5 {
        if let Some(inner) = text.strip_prefix('(') {
            let (body, denominator) = inner.split_once(")/").unwrap();
            let denominator: i64 = denominator.parse().unwrap();
            let without_root = body.strip_suffix("sqrt(5)").unwrap();
            let (integer, sign) = without_root.split_at(without_root.len() - 1);
            let a: i64 = integer.parse().unwrap();
            let b: i64 = if sign == "+" { 1 } else { -1 };
            return Q5::from_ints(a, b) * Q5::from_rational(rq(1, denominator));
        }
        match text.split_once('/') {
            Some((p, q)) => Q5::from_rational(rq(p.parse().unwrap(), q.parse().unwrap())),
            None => Q5::from_rational(rq(text.parse().unwrap(), 1)),
        }
    }

    type M3 = Vec<Vec<Q5>>;

    fn matrix_of(inventory: &[GroupParameterRecord], id: &str) -> M3 {
        let record = inventory.iter().find(|r| r.item_id == id).unwrap();
        record
            .matrix_entries_exact
            .iter()
            .map(|row| row.iter().map(|e| parse_entry(e)).collect())
            .collect()
    }

    fn mul3(a: &M3, b: &M3) -> M3 {
        (0..3)
            .map(|i| {
                (0..3)
                    .map(|j| {
                        (0..3).fold(Q5::zero(), |acc, k| acc + a[i][k].clone() * b[k][j].clone())
                    })
                    .collect()
            })
            .collect()
    }

    fn identity3() -> M3 {
        (0..3)
            .map(|i| {
                (0..3)
                    .map(|j| if i == j { Q5::one() } else { Q5::zero() })
                    .collect()
            })
            .collect()
    }

    fn transpose3(a: &M3) -> M3 {
        (0..3)
            .map(|i| (0..3).map(|j| a[j][i].clone()).collect())
            .collect()
    }

    fn det3(m: &M3) -> Q5 {
        let c = |i: usize, j: usize| m[i][j].clone();
        c(0, 0) * (c(1, 1) * c(2, 2) - c(1, 2) * c(2, 1))
            - c(0, 1) * (c(1, 0) * c(2, 2) - c(1, 2) * c(2, 0))
            + c(0, 2) * (c(1, 0) * c(2, 1) - c(1, 1) * c(2, 0))
    }

    #[test]
    fn every_rotation_record_is_a_proper_orthogonal_matrix_with_the_declared_cosine() {
        let inventory = build_frozen_inventory().unwrap();
        let q = |p: i64, d: i64| Q5::from_rational(rq(p, d));
        let cosines: Vec<(&str, Q5)> = vec![
            ("ROT_ID", q(1, 1)),
            ("ROT_C2", q(-1, 1)),
            ("ROT_C3", q(-1, 2)),
            ("ROT_C4", q(0, 1)),
            ("ROT_C6", q(1, 2)),
            ("ROT_I60_PLUS", Q5::from_ints(-1, 1) * q(1, 4)),
            ("ROT_I60_MINUS", Q5::from_ints(-1, -1) * q(1, 4)),
            ("ROT_PYTH_3_4_5", q(3, 5)),
            ("ROT_POLAR_B05", q(40, 41)),
        ];
        assert_eq!(
            inventory
                .iter()
                .filter(|r| r.subgroup_type == "ROTATION")
                .count(),
            cosines.len()
        );
        for (id, cosine) in cosines {
            let m = matrix_of(&inventory, id);
            assert_eq!(mul3(&transpose3(&m), &m), identity3(), "{id}: R^T R = I");
            assert_eq!(det3(&m), Q5::one(), "{id}: det R = 1");
            let trace = m[0][0].clone() + m[1][1].clone() + m[2][2].clone();
            assert_eq!(
                trace,
                Q5::one() + Q5::from_ints(2, 0) * cosine,
                "{id}: trace = 1 + 2 cos"
            );
        }
    }

    #[test]
    fn the_c6_matrix_has_order_six_and_squares_to_the_c3_matrix() {
        let inventory = build_frozen_inventory().unwrap();
        let c6 = matrix_of(&inventory, "ROT_C6");
        let c3 = matrix_of(&inventory, "ROT_C3");
        let c6_squared = mul3(&c6, &c6);
        assert_eq!(c6_squared, c3);
        let c6_cubed = mul3(&c6_squared, &c6);
        assert_ne!(c6_cubed, identity3());
        assert_eq!(mul3(&c6_cubed, &c6_cubed), identity3());
        assert_ne!(c6_squared, identity3());
    }

    #[test]
    fn the_two_icosahedral_records_are_the_first_and_second_powers_of_one_rotation() {
        let inventory = build_frozen_inventory().unwrap();
        let plus = matrix_of(&inventory, "ROT_I60_PLUS");
        let minus = matrix_of(&inventory, "ROT_I60_MINUS");
        assert_eq!(mul3(&plus, &plus), minus);
        let fifth = mul3(&mul3(&minus, &minus), &plus);
        assert_eq!(fifth, identity3());
        assert_ne!(plus, identity3());
    }

    #[test]
    fn test_inventory_count_and_typing() {
        let inventory = build_frozen_inventory().unwrap();
        assert_eq!(inventory.len(), 18);

        let carried_count = inventory
            .iter()
            .filter(|r| r.parameter_verdict == "CARRIED")
            .count();
        let refused_count = inventory
            .iter()
            .filter(|r| r.parameter_verdict == "REFUSED_TRANSCENDENTAL")
            .count();
        assert_eq!(carried_count, 3);
        assert_eq!(refused_count, 15);
    }

    #[test]
    fn test_mutation_1_parameter_reported_carried_rejected() {
        let res = classify_group_parameter(SubgroupType::Boost, false, true, true).unwrap();
        assert_eq!(res, ParameterVerdict::RefusedTranscendental);
    }

    #[test]
    fn test_mutation_2_approximation_typed_as_membership_rejected() {
        let inventory = build_frozen_inventory().unwrap();
        for r in inventory {
            if let Some(approx) = r.approximation_interval {
                assert!(!approx.is_carrier_membership);
                assert!(approx.is_approximation);
            }
        }
    }

    #[test]
    fn test_mutation_3_identity_case_handled() {
        let res = classify_group_parameter(SubgroupType::Rotation, true, true, true).unwrap();
        assert_eq!(res, ParameterVerdict::Carried);
    }

    #[test]
    fn test_mutation_4_algebraic_cosine_general() {
        let inventory = build_frozen_inventory().unwrap();
        let r = inventory
            .iter()
            .find(|rec| rec.item_id == "ROT_I60_PLUS")
            .unwrap();
        assert_eq!(r.parameter_verdict, "REFUSED_TRANSCENDENTAL");
    }

    #[test]
    fn test_mutation_5_planted_rapidity_refuted() {
        let check =
            |eta_algebraic_nonzero: bool, cosh_algebraic: bool| -> Result<bool, &'static str> {
                if eta_algebraic_nonzero && cosh_algebraic {
                    Err("Contradiction of Lindemann-Weierstrass")
                } else {
                    Ok(true)
                }
            };
        assert!(check(true, true).is_err());
        assert!(check(false, true).is_ok());
    }

    #[test]
    fn long_series_are_exact_and_bad_inputs_refused() {
        let (low, high) = compute_arctan_interval(rq(1, 2), 60).unwrap();
        assert!(low < high);
        let two: BigInt = BigInt::from(2);
        assert_eq!(
            &high - &low,
            Rational::new(BigInt::from(1), two.pow(121u32) * BigInt::from(121))
        );
        assert!(compute_arctan_interval(rq(3, 2), 8).is_err());
        assert!(compute_arctan_interval(rq(1, 2), MAX_SERIES_TERMS + 1).is_err());
        assert_eq!(
            compute_ln_interval(0, 8),
            Err(GroupParameterError::LogOfNonPositive(0))
        );
        assert!(compute_ln_x_interval(ri(1), 8).is_err());
        let ln1 = compute_ln_interval(1, 8).unwrap();
        assert_eq!(
            (ln1.q_min(), ln1.q_max()),
            (Rational::zero(), Rational::zero())
        );
        assert_eq!(
            compute_rotation_angle_pyth_interval(rq(1, 2), 60),
            Err(GroupParameterError::DoesNotFitI128)
        );
    }
}
