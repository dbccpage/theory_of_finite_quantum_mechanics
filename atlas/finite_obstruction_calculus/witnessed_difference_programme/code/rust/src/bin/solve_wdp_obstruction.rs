// Executable finite evidence; AuthorityEffect: None.
use num_rational::BigRational;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::io::{self, Read};
use std::str::FromStr;
use wdp_finite_witness::cochains::{Cochain1, FiniteComplex};
use wdp_finite_witness::obstruction::solve_exact_potential;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Request {
    vertices: Vec<String>,
    edges: Vec<(String, String)>,
    cochain: BTreeMap<String, String>,
}

#[derive(Serialize, Default)]
struct Response {
    status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    reason: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    phi1: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    is_exact: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    potential: Option<BTreeMap<String, String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    residual: Option<BTreeMap<String, String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    dual_witness: Option<BTreeMap<String, String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    authority_effect: Option<String>,
}

fn parse_rational(s: &str) -> Result<BigRational, String> {
    if let Ok(r) = BigRational::from_str(s) {
        return Ok(r);
    }
    if let Some((num_s, den_s)) = s.split_once('/') {
        let num = num_s.trim().parse::<num_bigint::BigInt>().map_err(|e| e.to_string())?;
        let den = den_s.trim().parse::<num_bigint::BigInt>().map_err(|e| e.to_string())?;
        if den == num_bigint::BigInt::from(0) {
            return Err("Division by zero in rational input".to_string());
        }
        return Ok(BigRational::new(num, den));
    }
    let int_val = s.trim().parse::<num_bigint::BigInt>().map_err(|e| e.to_string())?;
    Ok(BigRational::from(int_val))
}

fn main() {
    let mut buffer = String::new();
    if let Err(e) = io::stdin().read_to_string(&mut buffer) {
        let resp = Response {
            status: "REFUSE".into(),
            reason: Some(format!("Failed to read stdin: {}", e)),
            phi1: None,
            is_exact: None,
            potential: None,
            residual: None,
            dual_witness: None,
            authority_effect: None,
        };
        println!("{}", serde_json::to_string(&resp).unwrap());
        return;
    }

    let req: Request = match serde_json::from_str(&buffer) {
        Ok(r) => r,
        Err(e) => {
            let resp = Response {
                status: "REFUSE".into(),
                reason: Some(format!("JSON parse error: {}", e)),
                phi1: None,
                is_exact: None,
                potential: None,
                residual: None,
                dual_witness: None,
                authority_effect: None,
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
            return;
        }
    };

    if req.vertices.iter().any(|vertex| vertex.contains(',')) {
        println!("{}", serde_json::json!({"status": "REFUSE", "reason": "vertex labels containing commas are not supported by this graph wire format"}));
        return;
    }
    let complex = match FiniteComplex::new(req.vertices, req.edges) {
        Ok(c) => c,
        Err(e) => {
            let resp = Response {
                status: "REFUSE".into(),
                reason: Some(format!("Complex error: {}", e)),
                phi1: None,
                is_exact: None,
                potential: None,
                residual: None,
                dual_witness: None,
                authority_effect: None,
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
            return;
        }
    };

    let mut cochain_values = BTreeMap::new();
    for (k, v) in req.cochain {
        let parts: Vec<&str> = k.split(',').collect();
        if parts.len() != 2 {
            let resp = Response {
                status: "REFUSE".into(),
                reason: Some(format!("Invalid edge key: {}", k)),
                phi1: None,
                is_exact: None,
                potential: None,
                residual: None,
                dual_witness: None,
                authority_effect: None,
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
            return;
        }
        let rat = match parse_rational(&v) {
            Ok(r) => r,
            Err(e) => {
                let resp = Response {
                    status: "REFUSE".into(),
                    reason: Some(format!("Invalid rational string '{}': {}", v, e)),
                    phi1: None,
                    is_exact: None,
                    potential: None,
                    residual: None,
                    dual_witness: None,
                    authority_effect: None,
                };
                println!("{}", serde_json::to_string(&resp).unwrap());
                return;
            }
        };
        cochain_values.insert((parts[0].to_string(), parts[1].to_string()), rat);
    }

    let h = Cochain1 { values: cochain_values };
    let cert = match solve_exact_potential(&complex, &h) {
        Ok(c) => c,
        Err(e) => {
            let resp = Response {
                status: "REFUSE".into(),
                reason: Some(format!("Solver error: {}", e)),
                phi1: None,
                is_exact: None,
                potential: None,
                residual: None,
                dual_witness: None,
                authority_effect: None,
            };
            println!("{}", serde_json::to_string(&resp).unwrap());
            return;
        }
    };

    let mut pot_map = BTreeMap::new();
    for (k, v) in cert.potential_c0.values {
        pot_map.insert(k, v.to_string());
    }
    let mut res_map = BTreeMap::new();
    for ((u, v), val) in cert.residual_c1.values {
        res_map.insert(format!("{},{}", u, v), val.to_string());
    }
    let mut dual_map = BTreeMap::new();
    for ((u, v), val) in cert.dual_witness_c1.values {
        dual_map.insert(format!("{},{}", u, v), val.to_string());
    }

    let resp = Response {
        status: "PASS".into(),
        reason: None,
        phi1: Some(cert.phi1_value.to_string()),
        is_exact: Some(cert.is_exact),
        potential: Some(pot_map),
        residual: Some(res_map),
        dual_witness: Some(dual_map),
        authority_effect: Some(cert.authority_effect),
    };
    println!("{}", serde_json::to_string(&resp).unwrap());
}
