//! Shared, in-process computation for Rust and Python entrypoints.
use serde_json::{json, Value};

/// Admit every raw numeric token before duplicate object keys are resolved.
/// Exact duplicate keys retain the legacy CLI's last-value semantics.
pub fn parse_exact_json(raw: &str) -> Result<Value, String> {
    if raw.len() > 8 * 1024 * 1024 {
        return Err("INPUT_BUDGET_EXCEEDED".into());
    }
    let (mut quoted, mut escaped, mut number) = (false, false, false);
    for byte in raw.bytes() {
        if quoted {
            if escaped {
                escaped = false;
            } else if byte == b'\\' {
                escaped = true;
            } else if byte == b'"' {
                quoted = false;
            }
        } else if byte == b'"' {
            quoted = true;
            number = false;
        } else if byte.is_ascii_digit() || byte == b'-' {
            number = true;
        } else if number && matches!(byte, b'.' | b'e' | b'E') {
            return Err("FLOAT_INPUT_FORBIDDEN".into());
        } else {
            number = false;
        }
    }
    fn decode(raw: &serde_json::value::RawValue, depth: usize) -> Result<Value, String> {
        if depth > 128 {
            return Err("INPUT_DEPTH_EXCEEDED".into());
        }
        let text = raw.get().trim_start();
        match text.as_bytes().first() {
            Some(b'{') => {
                let fields: std::collections::BTreeMap<String, Box<serde_json::value::RawValue>> =
                    serde_json::from_str(text).map_err(|e| format!("INVALID_JSON:{e}"))?;
                let mut result = serde_json::Map::new();
                for (key, value) in fields {
                    if key == "$serde_json::private::Number" {
                        return Err("RESERVED_JSON_NUMBER_OBJECT".into());
                    }
                    result.insert(key, decode(&value, depth + 1)?);
                }
                Ok(Value::Object(result))
            }
            Some(b'[') => {
                let items: Vec<Box<serde_json::value::RawValue>> =
                    serde_json::from_str(text).map_err(|e| format!("INVALID_JSON:{e}"))?;
                items
                    .iter()
                    .map(|item| decode(item, depth + 1))
                    .collect::<Result<Vec<_>, _>>()
                    .map(Value::Array)
            }
            _ => serde_json::from_str(text).map_err(|e| format!("INVALID_JSON:{e}")),
        }
    }
    let value: Box<serde_json::value::RawValue> =
        serde_json::from_str(raw).map_err(|e| format!("INVALID_JSON:{e}"))?;
    decode(&value, 0)
}

pub fn run_json(name: &str, raw: &str) -> Result<Value, String> {
    run(name, &parse_exact_json(raw)?)
}

pub fn names() -> Vec<String> {
    let mut names = vec![
        "core",
        "targets",
        "c250",
        "c500",
        "c750",
        "c1000",
        "qm122",
        "qm122-carrier",
        "qm122-geometry",
        "qm122-gravity",
        "qm122-spinfoam",
        "entropy",
        "entropy-verdict",
        "entropy-interval",
        "cyclotomic-characteristic",
        "polynomial-roots",
        "rational-polynomial-factors",
        "real-field-squares",
        "real-field-polynomial-factors",
        "real-field-splitting-degrees",
        "real-field-compositum-degrees",
        "quintic-splitting-algebras",
        "spectral-factor-binding",
    ]
    .into_iter()
    .map(str::to_owned)
    .collect::<Vec<_>>();
    names.extend((1..=22).map(|n| format!("target-{n}")));
    names.extend((1..=10).map(|n| format!("c500-b{n:02}")));
    names
}

pub fn reject_floats(value: &Value) -> Result<(), String> {
    match value {
        Value::Number(n) if n.is_f64() || n.to_string().contains(['.', 'e', 'E']) => {
            Err("FLOAT_INPUT_FORBIDDEN".into())
        }
        Value::Array(items) => items.iter().try_for_each(reject_floats),
        Value::Object(items) => items.values().try_for_each(reject_floats),
        _ => Ok(()),
    }
}

pub fn run(name: &str, input: &Value) -> Result<Value, String> {
    reject_floats(input)?;
    let value = input.get("input").unwrap_or(input);
    match name {
        "core" => serde_json::to_value(crate::run_finite_qm_verification_suite())
            .map_err(|e| e.to_string()),
        "targets" => crate::legacy_suites::run_legacy_target("--all"),
        "c250" => crate::legacy_suites::run_legacy_target("--c250-all"),
        "c500" => crate::legacy_suites::run_legacy_target("--c500-all"),
        "c750" => crate::qm::entropy_bounds::run(value),
        "c1000" => Ok(
            json!({"authority_effect":"None", "scope":"declared C1000 finite witnesses",
            "no_signalling":omega_quantum_physics::no_signalling::verify_no_signalling_on_bell_states(),
            "rotation_groups":crate::qm::campaigns::rotation_groups::build_rotation_groups_receipt().map_err(|error|error.to_string())?,
            "boost_powers":crate::qm::campaigns::lorentz_boost::power_sequence(10).map_err(|e| e.to_string())?,
            "contextuality":crate::qm::campaigns::context_barrier::evaluate_campaign_block_07()?,
            "correlation":crate::qm::campaigns::quantum_correlation::q2_optimal_witness(),
            "parameters":crate::qm::group_param::build_frozen_inventory().map_err(|e| e.to_string())?,
            "price_list":crate::qm::causal_prices::build_full_price_list(),
            "totality":crate::qm::causal_prices::verify_price_list_totality(&crate::qm::causal_prices::build_full_price_list()),
            "declared_adjudications":crate::qm::causal_prices::adjudicate_fqmr1_clauses()}),
        ),
        "qm122" => serde_json::to_value(crate::qm::finite_witness::run(value)?).map_err(|e| e.to_string()),
        "qm122-carrier" => crate::qm::report_fiber::run(value),
        "qm122-geometry" => crate::qm::campaigns::finite_geometry_host::run(value),
        "qm122-gravity" => crate::qm::simplicial_grav::run(value),
        "qm122-spinfoam" => crate::qm::finite_spinfoam::run(value),
        "entropy" if value.get("fixtures").is_some() => crate::linear_algebra::entropy_dichotomy::report(value),
        "entropy" => crate::linear_algebra::entropy_dichotomy::evaluate(value),
        "entropy-verdict" => crate::linear_algebra::entropy_dichotomy::verdict_report(value),
        "entropy-interval" => {
            let k = input
                .get("terms")
                .map(|x| x.as_u64().ok_or("INVALID_TERMS".to_string()))
                .transpose()?
                .unwrap_or(32);
            if value.get("fixtures").is_some() {
                crate::linear_algebra::entropy_dichotomy::external_report(value, k)
            } else {
                crate::linear_algebra::entropy_dichotomy::evaluate_external(value, k)
            }
        }
        "cyclotomic-characteristic" => {
            crate::linear_algebra::entropy_dichotomy::cyclotomic_density::characteristic_report(value)
        }
        "polynomial-roots" if value.get("fixtures").is_some() => {
            crate::linear_algebra::entropy_dichotomy::cyclotomic_density::polynomial_roots::report(value)
        }
        "polynomial-roots" => crate::linear_algebra::entropy_dichotomy::cyclotomic_density::polynomial_roots::output(value),
        "rational-polynomial-factors" => {
            crate::linear_algebra::rational_polynomial_factors::evaluate_request(value)
        }
        "real-field-squares" => crate::linear_algebra::real_field_squares::handle_request(value),
        "real-field-polynomial-factors" => {
            crate::linear_algebra::real_field_polynomial_factors::evaluate_request(value)
        }
        "real-field-splitting-degrees" => {
            crate::linear_algebra::real_field_splitting_degrees::evaluate_request(value)
        }
        "real-field-compositum-degrees" => {
            crate::linear_algebra::real_field_compositum_degrees::evaluate_request(value)
        }
        "quintic-splitting-algebras" => crate::linear_algebra::quintic_split::evaluate_request(value),
        "spectral-factor-binding" => crate::linear_algebra::entropy_dichotomy::cyclotomic_density::spectral_factor_binding::evaluate_request(input),
        _ if name.starts_with("target-") || name.starts_with("c500-b") => {
            crate::legacy_suites::run_legacy_target(&format!("--{name}"))
        }
        _ => Err(format!("UNKNOWN_SUITE:{name}")),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn raw_admission_keeps_overwritten_inexact_tokens_visible() {
        for raw in [
            r#"{"x":1.0,"x":1}"#,
            r#"{"x":1e0,"x":1}"#,
            r#"{"x":{"nested":1.0},"x":1}"#,
        ] {
            assert_eq!(parse_exact_json(raw).unwrap_err(), "FLOAT_INPUT_FORBIDDEN");
        }
        for raw in [
            r#"{"x":{"$serde_json::private::Number":"1"}}"#,
            r#"{"x":{"\u0024serde_json::private::Number":"1"}}"#,
        ] {
            assert_eq!(
                parse_exact_json(raw).unwrap_err(),
                "RESERVED_JSON_NUMBER_OBJECT"
            );
        }
        assert!(parse_exact_json("{broken").is_err());
    }

    #[test]
    fn exact_duplicate_semantics_and_arbitrary_precision_are_preserved() {
        for previous in [
            "2".to_string(),
            format!("1{}", "0".repeat(5000)),
            r#""quoted\"1e0\\""#.to_string(),
        ] {
            let raw = format!(r#"{{"x":{previous},"x":1}}"#);
            assert_eq!(parse_exact_json(&raw).unwrap(), json!({"x":1}));
        }
        let huge = format!("1{}", "0".repeat(5000));
        assert_eq!(parse_exact_json(&huge).unwrap().to_string(), huge);
        assert_eq!(
            parse_exact_json(r#"["1.0", "1e0", "3/5"]"#).unwrap(),
            json!(["1.0", "1e0", "3/5"])
        );
    }
}
