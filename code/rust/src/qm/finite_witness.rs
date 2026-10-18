use num_bigint::BigInt;
use num_traits::Zero;
use omega_number_theory::rational::Rational as Q;
use serde::Serialize;
use serde_json::Value;
use std::str::FromStr;

pub const CLAIMS: &str = include_str!("data/quantum_claims.json");
pub fn qstr(q: &Q) -> String {
    if q.denom() == &BigInt::from(1) {
        q.numer().to_string()
    } else {
        format!("{}/{}", q.numer(), q.denom())
    }
}
pub fn qvec(q: &[Q]) -> Vec<String> {
    q.iter().map(qstr).collect()
}
pub fn parse_q(v: &Value) -> Result<Q, String> {
    let s = if let Some(s) = v.as_str() {
        s.to_owned()
    } else if v.is_i64() || v.is_u64() {
        v.to_string()
    } else {
        return Err("EXACT_RATIONAL_REQUIRED".into());
    };
    if s.len() > 4096 {
        return Err("RESOURCE_LIMIT:rational digits".into());
    }
    let p: Vec<_> = s.split('/').collect();
    if p.len() > 2 {
        return Err("INVALID_RATIONAL".into());
    }
    let n = BigInt::from_str(p[0]).map_err(|_| "INVALID_NUMERATOR")?;
    let d = if p.len() == 2 {
        BigInt::from_str(p[1]).map_err(|_| "INVALID_DENOMINATOR")?
    } else {
        BigInt::from(1)
    };
    if d.is_zero() {
        return Err("ZERO_DENOMINATOR".into());
    }
    Ok(Q::new(n, d))
}
pub fn field_q(v: &Value, k: &str, default: Q) -> Result<Q, String> {
    v.get(k).map(parse_q).unwrap_or(Ok(default))
}
pub fn field_usize(v: &Value, k: &str, default: usize, max: usize) -> Result<usize, String> {
    let n = v
        .get(k)
        .map(|x| x.as_u64().ok_or(format!("INVALID_INTEGER:{k}")))
        .transpose()?
        .unwrap_or(default as u64);
    if n > max as u64 {
        return Err(format!("RESOURCE_LIMIT:{k}"));
    }
    Ok(n as usize)
}

#[derive(Debug, Serialize)]
pub struct Qm122Report {
    pub source_commit: &'static str,
    pub authority_effect: &'static str,
    pub carrier: Value,
    pub geometry: Value,
    pub gravity: Value,
    pub spinfoam: Value,
    pub claim_count: usize,
}
pub fn run(input: &Value) -> Result<Qm122Report, String> {
    Ok(Qm122Report {
        source_commit: "2c28715b0d8b1b79d9a780f2e8b064cae10e0d08",
        authority_effect: "None",
        carrier: crate::qm::report_fiber::run(input.get("carrier").unwrap_or(&Value::Null))?,
        geometry: crate::qm::campaigns::finite_geometry_host::run(
            input.get("geometry").unwrap_or(&Value::Null),
        )?,
        gravity: crate::qm::simplicial_grav::run(input.get("gravity").unwrap_or(&Value::Null))?,
        spinfoam: crate::qm::finite_spinfoam::run(input.get("spinfoam").unwrap_or(&Value::Null))?,
        claim_count: serde_json::from_str::<Value>(CLAIMS).map_err(|e| e.to_string())?["claims"]
            .as_array()
            .ok_or("INVALID_CLAIM_MANIFEST")?
            .len(),
    })
}
