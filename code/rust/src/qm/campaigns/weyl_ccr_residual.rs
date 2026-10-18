use crate::linear_algebra::{matrix as mx, ExactFieldError};
use omega_lie_theory::heisenberg::{
    prime_characteristic_ccr, trace_obstruction, HeisenbergError, WeylHeisenberg,
};
use omega_lie_theory::scalar::is_unitary;
use omega_number_theory::cyclotomic_field::{normalized_conductor, Cyclotomic, CyclotomicError};
use omega_number_theory::polynomial::{self, PolynomialError};
use omega_number_theory::rational::rq;
use serde_json::{json, Value};
use std::collections::BTreeMap;
#[derive(Debug, thiserror::Error)]
pub enum WeylReceiptError {
    #[error("dimension is outside the declared campaign set")]
    Dimension,
    #[error("lambda must have a nonzero denominator")]
    ZeroDenominator,
    #[error(transparent)]
    Heisenberg(#[from] HeisenbergError),
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
    #[error(transparent)]
    Polynomial(#[from] PolynomialError),
    #[error(transparent)]
    Cyclotomic(#[from] CyclotomicError),
}
pub const TESTED_DIMENSIONS: [usize; 9] = [2, 3, 4, 5, 6, 7, 8, 12, 24];
fn evaluate<const C: usize>(
    d: usize,
    lambda_num: i64,
    lambda_den: i64,
) -> Result<(Value, Value), WeylReceiptError> {
    if lambda_den == 0 {
        return Err(WeylReceiptError::ZeroDenominator);
    }
    let omega = Cyclotomic::<C>::zeta((C / d) as i64);
    let system = if d % 2 == 1 {
        WeylHeisenberg::new(d, omega)?
    } else {
        WeylHeisenberg::with_phase_root(d, omega, Cyclotomic::<C>::zeta((C / (2 * d)) as i64))?
    };
    let x = system.shift()?;
    let z = system.clock()?;
    let relations = system.verify_relations()?;
    let minimal = (1..d).all(|k| {
        mx::power(&x, k as u64)
            .and_then(|m| mx::is_identity_matrix(&m))
            .map(|b| !b)
            .unwrap_or(false)
            && mx::power(&z, k as u64)
                .and_then(|m| mx::is_identity_matrix(&m))
                .map(|b| !b)
                .unwrap_or(false)
    });
    let lambda = Cyclotomic::<C>::rational(rq(lambda_num, lambda_den));
    let obstruction = trace_obstruction(d, &lambda)?;
    let comm = mx::commutator(&x, &z)?;
    let residual = mx::sub(&comm, &mx::scale(&mx::identity(d)?, &lambda)?)?;
    let trace = mx::trace(&residual)?;
    Ok((
        json!({"dimension":d,"is_X_unitary":is_unitary(&x)?,"is_Z_unitary":is_unitary(&z)?,
        "twisted_commutation_holds":relations,"minimal_orders_verified":minimal}),
        json!({"dimension":d,"lambda":rq(lambda_num,lambda_den).to_string(),
        "residual_trace":format!("{:?}",trace),"predicted_trace_verified":trace==obstruction.residual_trace,
        "obstruction_holds":obstruction.obstructed,
        "normalized_frobenius_square_lower_bound":format!("{:?}",obstruction.normalized_frobenius_square_lower_bound)}),
    ))
}
fn dispatch(d: usize, n: i64, q: i64) -> Result<(Value, Value), WeylReceiptError> {
    match d {
        2 => evaluate::<4>(d, n, q),
        3 => evaluate::<3>(d, n, q),
        4 => evaluate::<8>(d, n, q),
        5 => evaluate::<5>(d, n, q),
        6 => evaluate::<12>(d, n, q),
        7 => evaluate::<7>(d, n, q),
        8 => evaluate::<16>(d, n, q),
        12 => evaluate::<24>(d, n, q),
        24 => evaluate::<48>(d, n, q),
        _ => Err(WeylReceiptError::Dimension),
    }
}
pub fn verify_weyl_algebra_properties(d: usize) -> Result<Value, WeylReceiptError> {
    Ok(dispatch(d, 1, 1)?.0)
}
pub fn verify_trace_obstruction(d: usize, n: i64, q: i64) -> Result<Value, WeylReceiptError> {
    Ok(dispatch(d, n, q)?.1)
}
pub fn char_p_weyl_representation(p: usize) -> Result<Value, WeylReceiptError> {
    let model = prime_characteristic_ccr(p)?;
    let field = omega_number_theory::finite_field::FiniteField::prime_field(p)
        .ok_or(WeylReceiptError::Dimension)?;
    let identity = (0..p).all(|r| {
        (0..p).all(|c| {
            model.commutator.as_slice()[r * p + c]
                == if r == c { field.one() } else { field.zero() }
        })
    });
    Ok(
        json!({"characteristic":p,"dimension":p,"commutator_is_identity_mod_p":identity,
        "trace_identity_mod_p":model.identity_trace.coeffs[0],"obstruction_evaporates_in_char_p":model.identity_trace.is_zero()}),
    )
}
pub fn compute_dimension_table() -> Result<Vec<Value>, WeylReceiptError> {
    TESTED_DIMENSIONS.iter().map(|&d| {
        let polynomial=polynomial::cyclotomic_polynomial(d)?;
        let conductor=normalized_conductor(d)?;
        Ok(json!({"dimension":d,"euler_phi":polynomial::euler_phi(d),"conductor":conductor,
            "cyclotomic_poly_coeffs":polynomial.coefficients().iter().map(ToString::to_string).collect::<Vec<_>>(),
            "scalar_characteristic":0,"symmetric_displacement_conductor":if d%2==0 {2*d}else{d}}))
    }).collect()
}
pub fn generate_canonical_block01_receipt() -> Result<Value, WeylReceiptError> {
    let mut weyl = BTreeMap::new();
    let mut ccr = BTreeMap::new();
    for &d in &TESTED_DIMENSIONS {
        weyl.insert(format!("d_{d}"), verify_weyl_algebra_properties(d)?);
        ccr.insert(format!("d_{d}"), verify_trace_obstruction(d, 1, 1)?);
    }
    Ok(
        json!({"campaign":"C500","block":"block_01","weyl_results":weyl,"obstruction_results":ccr,
        "char_p_results":[char_p_weyl_representation(2)?,char_p_weyl_representation(3)?,char_p_weyl_representation(5)?],
        "dimension_table":compute_dimension_table()?}),
    )
}
