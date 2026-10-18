#[allow(dead_code, clippy::duplicate_mod)]
#[path = "field_factors.rs"]
mod factors;
#[allow(dead_code, clippy::duplicate_mod)]
#[path = "splitting_deg.rs"]
mod irreducible;
#[allow(dead_code, clippy::duplicate_mod)]
#[path = "field_squares.rs"]
mod squares;

use num_bigint::BigInt;
use num_rational::BigRational as Q;
use num_traits::Zero;
use serde_json::{json, value::RawValue, Value};
use std::collections::BTreeMap;
use std::io::{self, Read};

type Result<T> = std::result::Result<T, String>;
const SCHEMA: &str = "real_field_compositum_degree_v1";
const ALGORITHM: &str = "EXACT_SMALL_FACTOR_GALOIS_INTERSECTION";
const SCOPE: &str = "E_SPLITTING_DEGREE_NO_IRREDUCIBLE_QUINTIC_NO_CARRIER_TRANSPORT_OR_DEPENDENCE";

#[derive(Clone)]
struct E {
    a: Q,
    b: Q,
}
impl E {
    fn add(&self, other: &Self) -> Self {
        Self {
            a: &self.a + &other.a,
            b: &self.b + &other.b,
        }
    }
    fn scale(&self, n: i64) -> Self {
        let n = Q::from_integer(n.into());
        Self {
            a: &self.a * &n,
            b: &self.b * n,
        }
    }
    fn square(&self, d: u64) -> Self {
        Self {
            a: &self.a * &self.a + Q::from_integer(d.into()) * &self.b * &self.b,
            b: Q::from_integer(2.into()) * &self.a * &self.b,
        }
    }
    fn wire(&self) -> Value {
        json!([qwire(&self.a), qwire(&self.b)])
    }
    fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }
}
fn sum(terms: &[E]) -> E {
    terms.iter().fold(
        E {
            a: Q::zero(),
            b: Q::zero(),
        },
        |a, b| a.add(b),
    )
}
fn qwire(q: &Q) -> String {
    format!("{}/{}", q.numer(), q.denom())
}
fn rational(value: &Value) -> Result<Q> {
    let text = value.as_str().ok_or("CANONICAL_RATIONAL_STRING_REQUIRED")?;
    let (a, b) = text.split_once('/').ok_or("RATIONAL_FORMAT")?;
    let a: BigInt = a.parse().map_err(|_| "RATIONAL_FORMAT")?;
    let b: BigInt = b.parse().map_err(|_| "RATIONAL_FORMAT")?;
    if b <= BigInt::zero() {
        return Err("POSITIVE_RATIONAL_DENOMINATOR_REQUIRED".into());
    }
    let q = Q::new(a, b);
    if qwire(&q) != text {
        return Err("REDUCED_RATIONAL_REQUIRED".into());
    }
    Ok(q)
}
fn field(n: u64) -> Result<(u64, &'static str)> {
    match n {
        1 | 3 | 4 => Ok((0, "Q")),
        8 => Ok((2, "Q(sqrt(2))")),
        5 => Ok((5, "Q(sqrt(5))")),
        _ => Err("UNSUPPORTED_CONDUCTOR".into()),
    }
}
fn element(value: &Value, d: u64) -> Result<E> {
    let pair = value.as_array().ok_or("COEFFICIENT_PAIR_REQUIRED")?;
    if pair.len() != 2 {
        return Err("COEFFICIENT_PAIR_REQUIRED".into());
    }
    let e = E {
        a: rational(&pair[0])?,
        b: rational(&pair[1])?,
    };
    if d == 0 && !e.b.is_zero() {
        return Err("RATIONAL_FIELD_RADICAL_COORDINATE_NONZERO".into());
    }
    Ok(e)
}
fn exact_json(value: &Value) -> Result<()> {
    match value {
        Value::Number(n) if n.is_f64() || n.to_string().contains(['.', 'e', 'E']) => {
            Err("INEXACT_JSON_NUMBER".into())
        }
        Value::Array(rows) => rows.iter().try_for_each(exact_json),
        Value::Object(map) => map.values().try_for_each(exact_json),
        _ => Ok(()),
    }
}
fn keys(value: &Value, names: &[&str]) -> Result<()> {
    let map = value.as_object().ok_or("OBJECT_REQUIRED")?;
    if map.len() != names.len() || names.iter().any(|key| !map.contains_key(*key)) {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    Ok(())
}
fn integer(value: &Value) -> Result<u64> {
    value
        .as_u64()
        .ok_or_else(|| "EXACT_NONNEGATIVE_INTEGER_REQUIRED".into())
}
fn integer_list(value: &Value) -> Result<Vec<u64>> {
    value
        .as_array()
        .ok_or("INTEGER_ARRAY_REQUIRED")?
        .iter()
        .map(integer)
        .collect()
}
fn admitted(n: u64, coefficients: &Value) -> Result<(u64, &'static str)> {
    exact_json(coefficients)?;
    let (d, name) = field(n)?;
    let p = coefficients
        .as_array()
        .ok_or("COEFFICIENT_ARRAY_REQUIRED")?;
    if p.is_empty() {
        return Err("NONEMPTY_POLYNOMIAL_REQUIRED".into());
    }
    if p.len() > 6 {
        return Err("POLYNOMIAL_DEGREE_ABOVE_FIVE".into());
    }
    for coefficient in p {
        element(coefficient, d)?;
    }
    if element(&p[0], d)?.is_zero() {
        return Err("NONZERO_LEADING_COEFFICIENT_REQUIRED".into());
    }
    Ok((d, name))
}

struct Factor {
    index: usize,
    degree: usize,
    polynomial: Value,
}
fn nonlinear(factorization: &Value) -> Result<Vec<Factor>> {
    let mut result = Vec::new();
    for (index, row) in factorization["factors"]
        .as_array()
        .ok_or("FACTOR_ARRAY_REQUIRED")?
        .iter()
        .enumerate()
    {
        let degree = row["polynomial"]
            .as_array()
            .ok_or("COEFFICIENT_ARRAY_REQUIRED")?
            .len()
            .checked_sub(1)
            .ok_or("NONEMPTY_POLYNOMIAL_REQUIRED")?;
        if degree > 1 {
            result.push(Factor {
                index,
                degree,
                polynomial: row["polynomial"].clone(),
            });
        }
    }
    result.sort_by_key(|f| (f.degree, f.index));
    let pattern = result.iter().map(|f| f.degree).collect::<Vec<_>>();
    match pattern.as_slice() {
        [] | [2] | [3] | [4] | [2, 2] | [2, 3] => Ok(result),
        [5] => Err("UNSUPPORTED_IRREDUCIBLE_QUINTIC".into()),
        _ => Err("NONLINEAR_FACTOR_PATTERN_INVALID".into()),
    }
}
fn quadratic_discriminant(p: &Value, d: u64) -> Result<Value> {
    let b = element(&p[1], d)?;
    let c = element(&p[2], d)?;
    Ok(sum(&[b.square(d), c.scale(-4)]).wire())
}
struct Leaf {
    index: usize,
    polynomial_degree: usize,
    degree: u64,
    discriminant: Value,
    group: Option<String>,
}
fn validate_leaf(n: u64, d: u64, factor: &Factor, row: &Value) -> Result<Leaf> {
    keys(
        row,
        &[
            "factor_index",
            "polynomial_degree",
            "degree_over_real_field",
            "certificate",
        ],
    )?;
    if integer(&row["factor_index"])? != factor.index as u64
        || integer(&row["polynomial_degree"])? != factor.degree as u64
    {
        return Err("FACTOR_LEAF_INDEX_OR_DEGREE_MISMATCH".into());
    }
    let certificate = &row["certificate"];
    let (degree, discriminant, group) = if factor.degree == 2 {
        keys(
            certificate,
            &["kind", "discriminant", "discriminant_square"],
        )?;
        let delta = quadratic_discriminant(&factor.polynomial, d)?;
        if certificate["kind"] != "IRREDUCIBLE_QUADRATIC" || certificate["discriminant"] != delta {
            return Err("QUADRATIC_LEAF_DISCRIMINANT_MISMATCH".into());
        }
        squares::verify_square_certificate(n, &delta, &certificate["discriminant_square"])?;
        if certificate["discriminant_square"]["is_square"].as_bool() != Some(false) {
            return Err("QUADRATIC_LEAF_MUST_BE_NONSQUARE".into());
        }
        (2, delta, None)
    } else {
        irreducible::validate_splitting_degree(n, &factor.polynomial, certificate)?;
        (
            integer(&certificate["degree_over_real_field"])?,
            certificate["discriminant"].clone(),
            Some(
                certificate["galois_group"]
                    .as_str()
                    .ok_or("GALOIS_GROUP_STRING_REQUIRED")?
                    .to_string(),
            ),
        )
    };
    if integer(&row["degree_over_real_field"])? != degree {
        return Err("LEAF_SPLITTING_DEGREE_MISMATCH".into());
    }
    Ok(Leaf {
        index: factor.index,
        polynomial_degree: factor.degree,
        degree,
        discriminant,
        group,
    })
}
fn leaf_certificate(n: u64, d: u64, factor: &Factor) -> Result<Value> {
    let certificate = if factor.degree == 2 {
        let delta = quadratic_discriminant(&factor.polynomial, d)?;
        let square = squares::square_certificate(n, &delta)?;
        json!({"kind":"IRREDUCIBLE_QUADRATIC","discriminant":delta,"discriminant_square":square})
    } else {
        irreducible::irreducible_splitting_degree(n, &factor.polynomial)?
    };
    let degree = if factor.degree == 2 {
        2
    } else {
        integer(&certificate["degree_over_real_field"])?
    };
    Ok(
        json!({"factor_index":factor.index,"polynomial_degree":factor.degree,"degree_over_real_field":degree,"certificate":certificate}),
    )
}
fn intersection_rule(leaves: &[Leaf], same: Option<bool>) -> Result<(&'static str, u64)> {
    if leaves.len() != 2 || leaves[0].polynomial_degree != 2 {
        return Err("INTERSECTION_PATTERN_INVALID".into());
    }
    match (
        leaves[1].polynomial_degree,
        leaves[1].group.as_deref(),
        same,
    ) {
        (2, None, Some(true)) => Ok(("QUADRATIC_QUADRATIC_SAME_FIELD", 2)),
        (2, None, Some(false)) => Ok(("QUADRATIC_QUADRATIC_DISJOINT", 1)),
        (3, Some("C3"), None) => Ok(("QUADRATIC_CYCLIC_CUBIC_COPRIME", 1)),
        (3, Some("S3"), Some(true)) => Ok(("QUADRATIC_SYMMETRIC_CUBIC_CONTAINED", 2)),
        (3, Some("S3"), Some(false)) => Ok(("QUADRATIC_SYMMETRIC_CUBIC_DISJOINT", 1)),
        _ => Err("INTERSECTION_BRANCH_INVALID".into()),
    }
}
fn intersection_certificate(n: u64, leaves: &[Leaf]) -> Result<Value> {
    if leaves.len() < 2 {
        return Ok(Value::Null);
    }
    let left = &leaves[0].discriminant;
    let right = &leaves[1].discriminant;
    let certificate = if leaves[1].group.as_deref() == Some("C3") {
        Value::Null
    } else {
        squares::squareclass_certificate(n, left, right)?
    };
    let same = if certificate.is_null() {
        None
    } else {
        Some(
            certificate["same_squareclass"]
                .as_bool()
                .ok_or("SQUARECLASS_BOOLEAN_REQUIRED")?,
        )
    };
    let (rule, degree) = intersection_rule(leaves, same)?;
    Ok(
        json!({"factor_indices":[leaves[0].index,leaves[1].index],"rule":rule,
        "left_discriminant":left,"right_discriminant":right,"squareclass_certificate":certificate,"intersection_degree":degree}),
    )
}
fn validate_intersection(n: u64, leaves: &[Leaf], certificate: &Value) -> Result<u64> {
    if leaves.len() < 2 {
        if !certificate.is_null() {
            return Err("UNUSED_INTERSECTION_MUST_BE_NULL".into());
        }
        return Ok(1);
    }
    keys(
        certificate,
        &[
            "factor_indices",
            "rule",
            "left_discriminant",
            "right_discriminant",
            "squareclass_certificate",
            "intersection_degree",
        ],
    )?;
    if integer_list(&certificate["factor_indices"])?
        != vec![leaves[0].index as u64, leaves[1].index as u64]
    {
        return Err("INTERSECTION_FACTOR_INDICES_MISMATCH".into());
    }
    let (left, right) = (&leaves[0].discriminant, &leaves[1].discriminant);
    if certificate["left_discriminant"] != *left || certificate["right_discriminant"] != *right {
        return Err("INTERSECTION_DISCRIMINANT_BINDING_MISMATCH".into());
    }
    let supplied = &certificate["squareclass_certificate"];
    let same = if leaves[1].group.as_deref() == Some("C3") {
        if !supplied.is_null() {
            return Err("CYCLIC_CUBIC_SQUARECLASS_MUST_BE_NULL".into());
        }
        None
    } else {
        squares::verify_squareclass_certificate(n, left, right, supplied)?;
        Some(
            supplied["same_squareclass"]
                .as_bool()
                .ok_or("SQUARECLASS_BOOLEAN_REQUIRED")?,
        )
    };
    let (rule, degree) = intersection_rule(leaves, same)?;
    if certificate["rule"] != rule {
        return Err("INTERSECTION_RULE_MISMATCH".into());
    }
    if integer(&certificate["intersection_degree"])? != degree {
        return Err("INTERSECTION_DEGREE_MISMATCH".into());
    }
    Ok(degree)
}
fn composite_degree(leaves: &[Leaf], intersection: u64) -> Result<u64> {
    let mut product = 1u64;
    for leaf in leaves {
        product = product
            .checked_mul(leaf.degree)
            .ok_or("SPLITTING_DEGREE_OVERFLOW")?;
    }
    if intersection == 0 || !product.is_multiple_of(intersection) {
        return Err("INTERSECTION_DEGREE_NOT_DIVISOR".into());
    }
    Ok(product / intersection)
}

pub fn compositum_splitting_degree(n: u64, coefficients: &Value) -> Result<Value> {
    let (d, name) = admitted(n, coefficients)?;
    let factorization = factors::evaluate_request(
        &json!({"operation":"factor","conductor":n,"coefficients":coefficients}),
    )?;
    factors::validate_factorization(n, coefficients, &factorization)?;
    let factors = nonlinear(&factorization)?;
    let certificates = factors
        .iter()
        .map(|f| leaf_certificate(n, d, f))
        .collect::<Result<Vec<_>>>()?;
    let leaves = factors
        .iter()
        .zip(&certificates)
        .map(|(f, c)| validate_leaf(n, d, f, c))
        .collect::<Result<Vec<_>>>()?;
    let intersection = intersection_certificate(n, &leaves)?;
    let intersection_degree = validate_intersection(n, &leaves, &intersection)?;
    Ok(
        json!({"schema":SCHEMA,"authority_effect":"None","conductor":n,"real_generator_radicand":d,
        "coefficient_field":name,"coefficients":coefficients,"factorization":factorization,
        "nonlinear_factor_indices":factors.iter().map(|f|f.index).collect::<Vec<_>>(),
        "degree_pattern":factors.iter().map(|f|f.degree).collect::<Vec<_>>(),
        "factor_certificates":certificates,"intersection_certificate":intersection,
        "degree_over_real_field":composite_degree(&leaves,intersection_degree)?,"algorithm":ALGORITHM,"scope":SCOPE}),
    )
}
pub fn validate_compositum_degree(n: u64, coefficients: &Value, certificate: &Value) -> Result<()> {
    let (d, name) = admitted(n, coefficients)?;
    exact_json(certificate)?;
    keys(
        certificate,
        &[
            "schema",
            "authority_effect",
            "conductor",
            "real_generator_radicand",
            "coefficient_field",
            "coefficients",
            "factorization",
            "nonlinear_factor_indices",
            "degree_pattern",
            "factor_certificates",
            "intersection_certificate",
            "degree_over_real_field",
            "algorithm",
            "scope",
        ],
    )?;
    if certificate["schema"] != SCHEMA
        || certificate["authority_effect"] != "None"
        || certificate["algorithm"] != ALGORITHM
        || certificate["scope"] != SCOPE
        || integer(&certificate["conductor"])? != n
        || integer(&certificate["real_generator_radicand"])? != d
        || certificate["coefficient_field"] != name
    {
        return Err("COMPOSITUM_METADATA_MISMATCH".into());
    }
    if certificate["coefficients"] != *coefficients {
        return Err("COMPOSITUM_INPUT_BINDING_MISMATCH".into());
    }
    factors::validate_factorization(n, coefficients, &certificate["factorization"])?;
    let factors = nonlinear(&certificate["factorization"])?;
    if integer_list(&certificate["nonlinear_factor_indices"])?
        != factors.iter().map(|f| f.index as u64).collect::<Vec<_>>()
    {
        return Err("NONLINEAR_FACTOR_INDICES_MISMATCH".into());
    }
    if integer_list(&certificate["degree_pattern"])?
        != factors.iter().map(|f| f.degree as u64).collect::<Vec<_>>()
    {
        return Err("DEGREE_PATTERN_MISMATCH".into());
    }
    let rows = certificate["factor_certificates"]
        .as_array()
        .ok_or("FACTOR_CERTIFICATE_ARRAY_REQUIRED")?;
    if rows.len() != factors.len() {
        return Err("FACTOR_CERTIFICATE_CENSUS_MISMATCH".into());
    }
    let leaves = factors
        .iter()
        .zip(rows)
        .map(|(f, c)| validate_leaf(n, d, f, c))
        .collect::<Result<Vec<_>>>()?;
    let intersection = validate_intersection(n, &leaves, &certificate["intersection_certificate"])?;
    if integer(&certificate["degree_over_real_field"])? != composite_degree(&leaves, intersection)?
    {
        return Err("COMPOSITUM_SPLITTING_DEGREE_MISMATCH".into());
    }
    Ok(())
}
pub fn evaluate_request(request: &Value) -> Result<Value> {
    exact_json(request)?;
    keys(request, &["operation", "conductor", "coefficients"])?;
    if request["operation"] != "compositum_splitting_degree" {
        return Err("COMPOSITUM_OPERATION_REQUIRED".into());
    }
    compositum_splitting_degree(integer(&request["conductor"])?, &request["coefficients"])
}

#[cfg(test)]
pub fn fold_control(terms: &Value, self_join: bool) -> Result<Value> {
    let terms = terms
        .as_array()
        .ok_or("RATIONAL_ARRAY_REQUIRED")?
        .iter()
        .map(rational)
        .collect::<Result<Vec<_>>>()?;
    if self_join {
        let mut numerator = BigInt::zero();
        for (i, a) in terms.iter().enumerate() {
            for (j, b) in terms.iter().enumerate() {
                if i != j {
                    numerator += a.numer() * b.denom();
                }
            }
        }
        return Ok(json!(qwire(&Q::from_integer(numerator))));
    }
    Ok(sum(&terms
        .into_iter()
        .map(|a| E { a, b: Q::zero() })
        .collect::<Vec<_>>())
    .wire()[0]
        .clone())
}

fn raw_number_admission(input: &str) -> Result<()> {
    let bytes = input.as_bytes();
    let (mut index, mut in_string, mut escaped) = (0, false, false);
    while index < bytes.len() {
        let byte = bytes[index];
        if in_string {
            if escaped {
                escaped = false;
            } else if byte == b'\\' {
                escaped = true;
            } else if byte == b'"' {
                in_string = false;
            }
            index += 1;
        } else if byte == b'"' {
            in_string = true;
            index += 1;
        } else if matches!(byte, b'-' | b'0'..=b'9') {
            index += 1;
            while index < bytes.len()
                && matches!(bytes[index], b'0'..=b'9' | b'+' | b'-' | b'.' | b'e' | b'E')
            {
                if matches!(bytes[index], b'.' | b'e' | b'E') {
                    return Err("RAW_INEXACT_JSON_NUMBER".into());
                }
                index += 1;
            }
        } else {
            index += 1;
        }
    }
    Ok(())
}
fn run() -> Result<Value> {
    if std::env::args().len() != 1 {
        return Err("USAGE:real_field_compositum_degrees < REQUEST_JSON".into());
    }
    let mut raw = String::new();
    io::stdin()
        .read_to_string(&mut raw)
        .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
    let number_gate = raw_number_admission(&raw);
    let fields: BTreeMap<String, Box<RawValue>> =
        serde_json::from_str(&raw).map_err(|e| format!("INVALID_JSON:{e}"))?;
    number_gate?;
    if fields.len() != 3
        || ["operation", "conductor", "coefficients"]
            .iter()
            .any(|key| !fields.contains_key(*key))
    {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    let conductor: u64 = serde_json::from_str(fields["conductor"].get())
        .map_err(|_| "INTEGER_CONDUCTOR_REQUIRED")?;
    let operation: String = serde_json::from_str(fields["operation"].get())
        .map_err(|_| "COMPOSITUM_OPERATION_REQUIRED")?;
    let coefficients: Vec<[String; 2]> = serde_json::from_str(fields["coefficients"].get())
        .map_err(|_| "CANONICAL_RATIONAL_STRING_REQUIRED")?;
    evaluate_request(
        &json!({"operation":operation,"conductor":conductor,"coefficients":coefficients}),
    )
}
fn ascii_json(output: &Value) -> String {
    let encoded = serde_json::to_string(output).expect("JSON output");
    let mut result = String::with_capacity(encoded.len());
    for ch in encoded.chars() {
        let n = u32::from(ch);
        if n < 0x7f {
            result.push(ch);
        } else if n <= 0xffff {
            result.push_str(&format!("\\u{n:04x}"));
        } else {
            let x = n - 0x10000;
            result.push_str(&format!(
                "\\u{:04x}\\u{:04x}",
                0xd800 + (x >> 10),
                0xdc00 + (x & 0x3ff)
            ));
        }
    }
    result
}
fn main() {
    match run() {
        Ok(output) => println!("{}", ascii_json(&output)),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}
