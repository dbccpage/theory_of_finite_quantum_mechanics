use serde_json::{json, Value};

fn step_quoted_byte(quoted: &mut bool, escaped: &mut bool, byte: u8) {
    if *escaped {
        *escaped = false;
    } else if byte == b'\\' {
        *escaped = true;
    } else if byte == b'"' {
        *quoted = false;
    }
}

fn step_unquoted_byte(quoted: &mut bool, number: &mut bool, byte: u8) -> Result<(), String> {
    if byte == b'"' {
        *quoted = true;
        *number = false;
    } else if byte.is_ascii_digit() || byte == b'-' {
        *number = true;
    } else if *number && matches!(byte, b'.' | b'e' | b'E') {
        return Err("FLOAT_INPUT_FORBIDDEN".into());
    } else {
        *number = false;
    }
    Ok(())
}

fn scan_raw_float_tokens(raw: &str) -> Result<(), String> {
    let (mut quoted, mut escaped, mut number) = (false, false, false);
    for byte in raw.bytes() {
        if quoted {
            step_quoted_byte(&mut quoted, &mut escaped, byte);
        } else {
            step_unquoted_byte(&mut quoted, &mut number, byte)?;
        }
    }
    Ok(())
}

fn decode_raw_object(text: &str, depth: usize) -> Result<Value, String> {
    let fields: std::collections::BTreeMap<String, Box<serde_json::value::RawValue>> =
        serde_json::from_str(text).map_err(|e| format!("INVALID_JSON:{e}"))?;
    let mut result = serde_json::Map::new();
    for (key, value) in fields {
        if key == "$serde_json::private::Number" {
            return Err("RESERVED_JSON_NUMBER_OBJECT".into());
        }
        result.insert(key, decode_raw_json(&value, depth + 1)?);
    }
    Ok(Value::Object(result))
}

fn decode_raw_array(text: &str, depth: usize) -> Result<Value, String> {
    let items: Vec<Box<serde_json::value::RawValue>> =
        serde_json::from_str(text).map_err(|e| format!("INVALID_JSON:{e}"))?;
    let mut out = Vec::with_capacity(items.len());
    for item in &items {
        out.push(decode_raw_json(item, depth + 1)?);
    }
    Ok(Value::Array(out))
}

fn decode_raw_json(raw: &serde_json::value::RawValue, depth: usize) -> Result<Value, String> {
    if depth > 128 {
        return Err("INPUT_DEPTH_EXCEEDED".into());
    }
    let text = raw.get().trim_start();
    match text.as_bytes().first() {
        Some(b'{') => decode_raw_object(text, depth),
        Some(b'[') => decode_raw_array(text, depth),
        _ => serde_json::from_str(text).map_err(|e| format!("INVALID_JSON:{e}")),
    }
}

pub fn parse_exact_json(raw: &str) -> Result<Value, String> {
    if raw.len() > 8 * 1024 * 1024 {
        return Err("INPUT_BUDGET_EXCEEDED".into());
    }
    scan_raw_float_tokens(raw)?;
    let value: Box<serde_json::value::RawValue> =
        serde_json::from_str(raw).map_err(|e| format!("INVALID_JSON:{e}"))?;
    decode_raw_json(&value, 0)
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
        "textbook-atlas",
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

fn run_c1000_suite() -> Result<Value, String> {
    let price_list = crate::qm::causal_prices::build_full_price_list();
    let totality = crate::qm::causal_prices::verify_price_list_totality(&price_list);
    Ok(json!({
        "authority_effect": "None",
        "scope": "declared C1000 finite witnesses",
        "no_signalling": omega_quantum_physics::no_signalling::verify_no_signalling_on_bell_states(),
        "rotation_groups": crate::qm::campaigns::rotation_groups::build_rotation_groups_receipt().map_err(|error| error.to_string())?,
        "boost_powers": crate::qm::campaigns::lorentz_boost::power_sequence(10).map_err(|e| e.to_string())?,
        "contextuality": crate::qm::campaigns::context_barrier::evaluate_campaign_block_07()?,
        "correlation": crate::qm::campaigns::quantum_correlation::q2_optimal_witness(),
        "parameters": crate::qm::group_param::build_frozen_inventory().map_err(|e| e.to_string())?,
        "price_list": price_list,
        "totality": totality,
        "declared_adjudications": crate::qm::causal_prices::adjudicate_fqmr1_clauses()
    }))
}

fn run_entropy_interval(input: &Value, value: &Value) -> Result<Value, String> {
    let k = match input.get("terms") {
        Some(x) => x.as_u64().ok_or("INVALID_TERMS".to_string())?,
        None => 32,
    };
    if value.get("fixtures").is_some() {
        crate::linear_algebra::entropy_dichotomy::external_report(value, k)
    } else {
        crate::linear_algebra::entropy_dichotomy::evaluate_external(value, k)
    }
}

fn dispatch_campaign_suites(name: &str, value: &Value) -> Option<Result<Value, String>> {
    match name {
        "core" => Some(
            serde_json::to_value(crate::run_finite_qm_verification_suite())
                .map_err(|e| e.to_string()),
        ),
        "targets" => Some(crate::legacy_suites::run_legacy_target("--all")),
        "c250" => Some(crate::legacy_suites::run_legacy_target("--c250-all")),
        "c500" => Some(crate::legacy_suites::run_legacy_target("--c500-all")),
        "c750" => Some(crate::qm::entropy_bounds::run(value)),
        "c1000" => Some(run_c1000_suite()),
        "textbook-atlas" => Some(crate::qm::textbook_problems::run_textbook_atlas()),
        _ => None,
    }
}

fn dispatch_qm122_and_entropy_suites(
    name: &str,
    input: &Value,
    value: &Value,
) -> Option<Result<Value, String>> {
    match name {
        "qm122" => Some(
            crate::qm::finite_witness::run(value)
                .and_then(|v| serde_json::to_value(v).map_err(|e| e.to_string())),
        ),
        "qm122-carrier" => Some(crate::qm::report_fiber::run(value)),
        "qm122-geometry" => Some(crate::qm::campaigns::finite_geometry_host::run(value)),
        "qm122-gravity" => Some(crate::qm::simplicial_grav::run(value)),
        "qm122-spinfoam" => Some(crate::qm::finite_spinfoam::run(value)),
        "entropy" => Some(if value.get("fixtures").is_some() {
            crate::linear_algebra::entropy_dichotomy::report(value)
        } else {
            crate::linear_algebra::entropy_dichotomy::evaluate(value)
        }),
        "entropy-verdict" => Some(crate::linear_algebra::entropy_dichotomy::verdict_report(value)),
        "entropy-interval" => Some(run_entropy_interval(input, value)),
        _ => None,
    }
}

fn dispatch_real_field_suites(name: &str, value: &Value) -> Option<Result<Value, String>> {
    match name {
        "real-field-squares" => Some(crate::linear_algebra::real_field_squares::handle_request(value)),
        "real-field-polynomial-factors" => Some(
            crate::linear_algebra::real_field_polynomial_factors::evaluate_request(value),
        ),
        "real-field-splitting-degrees" => Some(
            crate::linear_algebra::real_field_splitting_degrees::evaluate_request(value),
        ),
        "real-field-compositum-degrees" => Some(
            crate::linear_algebra::real_field_compositum_degrees::evaluate_request(value),
        ),
        _ => None,
    }
}

fn dispatch_algebra_suites(
    name: &str,
    input: &Value,
    value: &Value,
) -> Option<Result<Value, String>> {
    if let Some(res) = dispatch_real_field_suites(name, value) {
        return Some(res);
    }
    match name {
        "cyclotomic-characteristic" => Some(
            crate::linear_algebra::entropy_dichotomy::cyclotomic_density::characteristic_report(value),
        ),
        "polynomial-roots" => Some(if value.get("fixtures").is_some() {
            crate::linear_algebra::entropy_dichotomy::cyclotomic_density::polynomial_roots::report(value)
        } else {
            crate::linear_algebra::entropy_dichotomy::cyclotomic_density::polynomial_roots::output(value)
        }),
        "rational-polynomial-factors" => Some(
            crate::linear_algebra::rational_polynomial_factors::evaluate_request(value),
        ),
        "quintic-splitting-algebras" => Some(crate::linear_algebra::quintic_split::evaluate_request(value)),
        "spectral-factor-binding" => Some(
            crate::linear_algebra::entropy_dichotomy::cyclotomic_density::spectral_factor_binding::evaluate_request(input),
        ),
        _ => None,
    }
}

pub fn run(name: &str, input: &Value) -> Result<Value, String> {
    reject_floats(input)?;
    let value = input.get("input").unwrap_or(input);
    if let Some(res) = dispatch_campaign_suites(name, value) {
        return res;
    }
    if let Some(res) = dispatch_qm122_and_entropy_suites(name, input, value) {
        return res;
    }
    if let Some(res) = dispatch_algebra_suites(name, input, value) {
        return res;
    }
    if name.starts_with("target-") || name.starts_with("c500-b") {
        return crate::legacy_suites::run_legacy_target(&format!("--{name}"));
    }
    Err(format!("UNKNOWN_SUITE:{name}"))
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
