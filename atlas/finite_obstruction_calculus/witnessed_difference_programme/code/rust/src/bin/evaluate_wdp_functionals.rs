//! JSON transport to the canonical exact functional evaluators.
//!
//! This binary admits data and serializes results. Functional arithmetic is
//! implemented in omega_functional; the solver proposes primal and dual data.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use omega_functional::gamma2::{DegreeOneResidualQ, ExactCochainComplexQ, Gamma2Functional};
use omega_functional::phi1::{ExactPhi1Certificate, Phi1Functional};
use omega_solvers::solver_lp_exact_simplex::solve_weighted_l1_projection;
use serde::Deserialize;
use serde_json::{json, Value};
use std::io::{self, Read};
use std::str::FromStr;

#[derive(Debug, Deserialize)]
#[serde(tag = "operation", rename_all = "snake_case", deny_unknown_fields)]
enum Request {
    SolvePhi1 {
        matrix: Vec<Vec<String>>,
        columns: usize,
        delta: Vec<String>,
        weights: Vec<String>,
        max_pivots: usize,
    },
    EvaluatePhi1 {
        matrix: Vec<Vec<String>>, columns: usize, delta: Vec<String>, weights: Vec<String>,
        potential: Vec<String>, dual: Vec<String>,
    },
    VerifyPhi1 {
        matrix: Vec<Vec<String>>,
        columns: usize,
        delta: Vec<String>,
        weights: Vec<String>,
        potential: Vec<String>,
        residual: Vec<String>,
        dual: Vec<String>,
        value: String,
    },
    SquaredL2 {
        residual: Vec<String>,
    },
    PolyhedralGauge {
        facets: Vec<Vec<String>>, residual: Vec<String>,
    },
    DualBound {
        matrix: Vec<Vec<String>>, columns: usize, delta: Vec<String>,
        weights: Vec<String>, dual: Vec<String>,
    },
    RepresentativeMass {
        residual: Vec<String>,
        weights: Vec<String>,
    },
    Closure {
        d0: Vec<Vec<String>>,
        c0_dim: usize,
        d1: Vec<Vec<String>>,
        residual: Vec<String>,
    },
}

fn rational(text: &str) -> Result<BigRational, String> {
    let (numerator, denominator) = text.split_once('/').unwrap_or((text, "1"));
    let n = BigInt::from_str(numerator).map_err(|e| e.to_string())?;
    let d = BigInt::from_str(denominator).map_err(|e| e.to_string())?;
    if d.is_zero() {
        return Err("zero rational denominator".into());
    }
    let result = BigRational::new(n, d);
    if result.to_string() != text {
        return Err("rational strings must be canonical integers or fractions".into());
    }
    Ok(result)
}

fn vector(values: &[String]) -> Result<Vec<BigRational>, String> {
    values.iter().map(|x| rational(x)).collect()
}

fn matrix(values: &[Vec<String>], columns: usize) -> Result<Vec<Vec<BigRational>>, String> {
    if values.iter().any(|row| row.len() != columns) {
        return Err("matrix column count does not match".into());
    }
    values.iter().map(|row| vector(row)).collect()
}

fn strings(values: &[BigRational]) -> Vec<String> {
    values.iter().map(ToString::to_string).collect()
}

fn evaluate(request: Request) -> Result<Value, String> {
    match request {
        Request::SolvePhi1 { matrix: rows, columns, delta, weights, max_pivots } => {
            let rows = matrix(&rows, columns)?;
            let delta = vector(&delta)?;
            let weights = vector(&weights)?;
            if rows.len() != delta.len() || weights.len() != delta.len() {
                return Err("row, target and weight dimensions must agree".into());
            }
            let (potential, dual, iterations) = if delta.is_empty() {
                (vec![BigRational::zero(); columns], Vec::new(), 0)
            } else {
                let proposed = solve_weighted_l1_projection(&delta, &weights, &rows, max_pivots)
                    .map_err(|e| e.to_string())?;
                (proposed.coefficients, proposed.dual, proposed.iterations)
            };
            let checked = Phi1Functional::evaluate_exact_witness(
                &delta, &rows, &weights, &potential, &dual,
            ).map_err(|e| e.to_string())?;
            Ok(json!({
                "value": checked.value().to_string(),
                "potential": strings(checked.alpha()),
                "residual": strings(checked.primal_residual()),
                "dual": strings(checked.dual_witness()),
                "iterations": iterations,
            }))
        }
        Request::EvaluatePhi1 { matrix: rows, columns, delta, weights, potential, dual } => {
            if potential.len() != columns { return Err("potential column count differs".into()); }
            let checked = Phi1Functional::evaluate_exact_witness(
                &vector(&delta)?, &matrix(&rows, columns)?, &vector(&weights)?, &vector(&potential)?, &vector(&dual)?,
            ).map_err(|e| e.to_string())?;
            Ok(json!({"value": checked.value().to_string()}))
        }
        Request::VerifyPhi1 {
            matrix: rows, columns, delta, weights, potential, residual, dual, value,
        } => {
            if potential.len() != columns {
                return Err("potential column count does not match".into());
            }
            let checked = Phi1Functional::verify_exact_certificate(ExactPhi1Certificate {
                omega: vector(&delta)?,
                d0: matrix(&rows, columns)?,
                weights: vector(&weights)?,
                alpha: vector(&potential)?,
                primal_residual: vector(&residual)?,
                dual_witness: vector(&dual)?,
                reported_value: rational(&value)?,
            }).map_err(|e| e.to_string())?;
            Ok(json!({"value": checked.value().to_string()}))
        }
        Request::PolyhedralGauge { facets, residual } => {
            let residual = vector(&residual)?;
            let value = omega_functional::observer_gauge::polyhedral_gauge(
                &matrix(&facets, residual.len())?, &residual,
            ).ok_or("invalid polyhedral gauge data")?;
            Ok(json!({"value": value.to_string()}))
        }
        Request::DualBound { matrix: rows, columns, delta, weights, dual } => {
            let value = Phi1Functional::verify_exact_dual_bound(
                &matrix(&rows, columns)?, &vector(&delta)?, &vector(&weights)?, &vector(&dual)?,
            ).map_err(|e| e.to_string())?;
            Ok(json!({"value": value.to_string()}))
        }
        Request::SquaredL2 { residual } => {
            let value = omega_functional::observer_gauge::rational_squared_l2(&vector(&residual)?);
            Ok(json!({"value": value.to_string()}))
        }
        Request::RepresentativeMass { residual, weights } => {
            let value = Phi1Functional::weighted_l1_rational(&vector(&weights)?, &vector(&residual)?)
                .ok_or("invalid weights or dimensions")?;
            Ok(json!({"value": value.to_string()}))
        }
        Request::Closure { d0, c0_dim, d1, residual } => {
            let residual = vector(&residual)?;
            let complex = ExactCochainComplexQ::try_new(
                c0_dim, residual.len(), d1.len(), matrix(&d0, c0_dim)?, matrix(&d1, residual.len())?,
            ).map_err(|e| e.to_string())?;
            let input = DegreeOneResidualQ::try_new(&complex, residual).map_err(|e| e.to_string())?;
            let checked = Gamma2Functional::try_compute_exact_quotient(&input)
                .map_err(|e| e.to_string())?;
            Ok(json!({"value": checked.value().to_string(), "coboundary": strings(checked.coboundary())}))
        }
    }
}

fn main() {
    let mut input = String::new();
    let result = io::stdin().read_to_string(&mut input).map_err(|e| e.to_string())
        .and_then(|_| serde_json::from_str(&input).map_err(|e| e.to_string()))
        .and_then(evaluate);
    let response = match result {
        Ok(result) => json!({"schema": "wdp-functionals-v1", "status": "PASS", "authority_effect": "None", "request": serde_json::from_str::<Value>(&input).expect("admitted JSON"), "result": result}),
        Err(reason) => json!({"schema": "wdp-functionals-v1", "status": "REFUSE", "authority_effect": "None", "reason": reason}),
    };
    println!("{response}");
}
