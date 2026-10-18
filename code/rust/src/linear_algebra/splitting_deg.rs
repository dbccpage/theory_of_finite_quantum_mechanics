// AuthorityEffect: None.
// Exact cubic/quartic splitting degree over E, NOT over a complex carrier K.
// No quintic, compositum, root-assignment, or multiplicative-dependence claim.
#[allow(dead_code)]
#[path = "field_factors.rs"]
mod factors;
#[allow(dead_code)]
#[path = "field_squares.rs"]
mod squares;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde_json::value::RawValue;
use serde_json::{json, Value};
use std::collections::BTreeMap;
use std::io::{self, Read};

type Q = BigRational;
type Result<T> = std::result::Result<T, String>;

#[derive(Clone, Debug, PartialEq, Eq)]
struct E {
    a: Q,
    b: Q,
}
impl E {
    fn zero() -> Self {
        Self {
            a: Q::zero(),
            b: Q::zero(),
        }
    }
    fn one() -> Self {
        Self {
            a: Q::one(),
            b: Q::zero(),
        }
    }
    fn add(&self, other: &Self) -> Self {
        Self {
            a: &self.a + &other.a,
            b: &self.b + &other.b,
        }
    }
    fn neg(&self) -> Self {
        Self {
            a: -&self.a,
            b: -&self.b,
        }
    }
    fn sub(&self, other: &Self) -> Self {
        self.add(&other.neg())
    }
    fn times(&self, integer: i64) -> Self {
        let integer = Q::from_integer(integer.into());
        Self {
            a: &self.a * &integer,
            b: &self.b * integer,
        }
    }
    fn mul(&self, other: &Self, d: u64) -> Self {
        Self {
            a: &self.a * &other.a + Q::from_integer(d.into()) * &self.b * &other.b,
            b: &self.a * &other.b + &self.b * &other.a,
        }
    }
    fn inverse(&self, d: u64) -> Result<Self> {
        let norm = &self.a * &self.a - Q::from_integer(d.into()) * &self.b * &self.b;
        if norm.is_zero() {
            return Err("ZERO_FIELD_DIVISOR".into());
        }
        Ok(Self {
            a: &self.a / &norm,
            b: -&self.b / norm,
        })
    }
    fn square(&self, d: u64) -> Self {
        self.mul(self, d)
    }
    fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }
    fn wire(&self) -> Value {
        json!([qwire(&self.a), qwire(&self.b)])
    }
}
fn qwire(q: &Q) -> String {
    format!("{}/{}", q.numer(), q.denom())
}
fn field(n: u64) -> Result<(u64, &'static str)> {
    match n {
        1 | 3 | 4 => Ok((0, "Q")),
        5 => Ok((5, "Q(sqrt(5))")),
        8 => Ok((2, "Q(sqrt(2))")),
        _ => Err("UNSUPPORTED_CONDUCTOR".into()),
    }
}
fn rational(v: &Value) -> Result<Q> {
    let text = v.as_str().ok_or("CANONICAL_RATIONAL_STRING_REQUIRED")?;
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
fn element(v: &Value, d: u64) -> Result<E> {
    let pair = v.as_array().ok_or("COEFFICIENT_PAIR_REQUIRED")?;
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
fn polynomial(v: &Value, d: u64) -> Result<Vec<E>> {
    let entries = v.as_array().ok_or("COEFFICIENT_ARRAY_REQUIRED")?;
    if entries.is_empty() {
        return Err("NONEMPTY_POLYNOMIAL_REQUIRED".into());
    }
    let p = entries
        .iter()
        .map(|x| element(x, d))
        .collect::<Result<Vec<_>>>()?;
    if p[0].is_zero() {
        return Err("NONZERO_LEADING_COEFFICIENT_REQUIRED".into());
    }
    Ok(p)
}
fn wire(p: &[E]) -> Value {
    json!(p.iter().map(E::wire).collect::<Vec<_>>())
}
fn sum(terms: &[E]) -> E {
    terms.iter().fold(E::zero(), |a, b| a.add(b))
}

struct Input {
    d: u64,
    name: &'static str,
    original: Vec<E>,
    monic: Vec<E>,
}
fn input(n: u64, coefficients: &Value) -> Result<Input> {
    let (d, name) = field(n)?;
    let original = polynomial(coefficients, d)?;
    if original.len() != 4 && original.len() != 5 {
        return Err("DEGREE_THREE_OR_FOUR_REQUIRED".into());
    }
    let inverse = original[0].inverse(d)?;
    let monic = original.iter().map(|x| x.mul(&inverse, d)).collect();
    Ok(Input {
        d,
        name,
        original,
        monic,
    })
}
fn factor(n: u64, p: &[E]) -> Result<Value> {
    factors::evaluate_request(&json!({"operation":"factor","conductor":n,"coefficients":wire(p)}))
}
fn irreducible(certificate: &Value, monic: &[E], d: u64) -> Result<()> {
    let rows = certificate["factors"]
        .as_array()
        .ok_or("FACTOR_ARRAY_REQUIRED")?;
    if rows.len() != 1
        || rows[0]["multiplicity"].as_u64() != Some(1)
        || polynomial(&rows[0]["polynomial"], d)? != monic
    {
        return Err("INPUT_REDUCIBLE_OVER_REAL_FIELD".into());
    }
    Ok(())
}

// Conrad, Cubics and Quartics, Theorems 2.1/3.4 and Corollary 4.3.
// Each signed polynomial expression is an exact stepwise rational fold.
fn cubic_discriminant(a: &E, b: &E, c: &E, d: u64) -> E {
    sum(&[
        a.square(d).mul(&b.square(d), d),
        b.square(d).mul(b, d).times(-4),
        a.square(d).mul(a, d).mul(c, d).times(-4),
        c.square(d).times(-27),
        a.mul(b, d).mul(c, d).times(18),
    ])
}
fn resolvent(p: &[E], d: u64) -> Vec<E> {
    let (a, b, c, e) = (&p[1], &p[2], &p[3], &p[4]);
    vec![
        E::one(),
        b.neg(),
        a.mul(c, d).sub(&e.times(4)),
        sum(&[
            a.square(d).mul(e, d).neg(),
            c.square(d).neg(),
            b.mul(e, d).times(4),
        ]),
    ]
}
fn discriminant(p: &[E], d: u64) -> E {
    if p.len() == 4 {
        cubic_discriminant(&p[1], &p[2], &p[3], d)
    } else {
        let r = resolvent(p, d);
        cubic_discriminant(&r[1], &r[2], &r[3], d)
    }
}
fn pattern(certificate: &Value, d: u64) -> Result<(Vec<u64>, Option<E>)> {
    let rows = certificate["factors"]
        .as_array()
        .ok_or("FACTOR_ARRAY_REQUIRED")?;
    let mut degrees = Vec::new();
    let mut roots = Vec::new();
    for row in rows {
        if row["multiplicity"].as_u64() != Some(1) {
            return Err("RESOLVENT_MULTIPLICITY_NOT_ONE".into());
        }
        let p = polynomial(&row["polynomial"], d)?;
        if p.len() < 2 || p[0] != E::one() {
            return Err("RESOLVENT_MONIC_FACTOR_REQUIRED".into());
        }
        degrees.push(u64::try_from(p.len() - 1).map_err(|_| "REPRESENTATION_SIZE_OVERFLOW")?);
        if p.len() == 2 {
            roots.push(p[1].neg());
        }
    }
    degrees.sort_unstable();
    let root = if degrees == [1, 2] {
        Some(roots[0].clone())
    } else {
        None
    };
    Ok((degrees, root))
}
fn cyclic_values(p: &[E], delta: &E, root: &E, d: u64) -> (E, E) {
    (
        delta.mul(&p[1].square(d).sub(&p[2].sub(root).times(4)), d),
        delta.mul(&root.square(d).sub(&p[4].times(4)), d),
    )
}
fn square_bool(certificate: &Value) -> Result<bool> {
    certificate["is_square"]
        .as_bool()
        .ok_or_else(|| "IS_SQUARE_BOOLEAN_REQUIRED".into())
}
fn classify(
    degree: usize,
    square: bool,
    pattern: &[u64],
    cyclic: Option<(bool, bool)>,
) -> Result<(&'static str, u64)> {
    if degree == 3 {
        return Ok(if square { ("C3", 3) } else { ("S3", 6) });
    }
    match pattern {
        [3] => Ok(if square { ("A4", 12) } else { ("S4", 24) }),
        [1, 1, 1] if square => Ok(("V4", 4)),
        [1, 2] if !square => {
            let (first, second) = cyclic.ok_or("CYCLIC_TESTS_REQUIRED")?;
            Ok(if first && second {
                ("C4", 4)
            } else {
                ("D4", 8)
            })
        }
        [1, 1, 1] | [1, 2] => Err("RESOLVENT_DISCRIMINANT_CONTRADICTION".into()),
        _ => Err("RESOLVENT_FACTOR_PATTERN_INVALID".into()),
    }
}

pub fn irreducible_splitting_degree(n: u64, coefficients: &Value) -> Result<Value> {
    let input = input(n, coefficients)?;
    let p = &input.monic;
    let d = input.d;
    let factorization = factor(n, &input.original)?;
    irreducible(&factorization, p, d)?;
    let delta = discriminant(p, d);
    if delta.is_zero() {
        return Err("ZERO_DISCRIMINANT".into());
    }
    let disc_square = squares::square_certificate(n, &delta.wire())?;
    let mut resolution = Value::Null;
    let mut degrees = Vec::new();
    let mut cyclic = None;
    if p.len() == 5 {
        let r = resolvent(p, d);
        let r_factors = factor(n, &r)?;
        let (pattern, root) = pattern(&r_factors, d)?;
        degrees = pattern;
        let mut tests = Value::Null;
        if let Some(root) = &root {
            let (u, v) = cyclic_values(p, &delta, root, d);
            let first = squares::square_certificate(n, &u.wire())?;
            let second = squares::square_certificate(n, &v.wire())?;
            cyclic = Some((square_bool(&first)?, square_bool(&second)?));
            tests = json!({"first_value":u.wire(),"first_square":first,"second_value":v.wire(),"second_square":second});
        }
        resolution = json!({"coefficients":wire(&r),"factorization":r_factors,"factor_degrees":degrees,
            "root":root.as_ref().map(E::wire),"cyclic_tests":tests});
    }
    let (group, degree) = classify(p.len() - 1, square_bool(&disc_square)?, &degrees, cyclic)?;
    Ok(
        json!({"schema":"real_field_splitting_degree_v1","authority_effect":"None",
        "algorithm":"EXACT_CUBIC_QUARTIC_RESOLVENT_CLASSIFICATION","conductor":n,
        "real_generator_radicand":d,"coefficient_field":input.name,
        "degree_over_real_field":degree,"galois_group":group,"coefficients":wire(&input.original),
        "monic_polynomial":wire(p),"factorization":factorization,"discriminant":delta.wire(),
        "discriminant_square":disc_square,"resolvent":resolution}),
    )
}
fn exact_fields(value: &Value, keys: &[&str]) -> Result<()> {
    let map = value.as_object().ok_or("OBJECT_REQUIRED")?;
    if map.len() != keys.len() || keys.iter().any(|key| !map.contains_key(*key)) {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    Ok(())
}
pub fn evaluate_request(request: &Value) -> Result<Value> {
    exact_fields(request, &["operation", "conductor", "coefficients"])?;
    if request["operation"] != "irreducible_splitting_degree" {
        return Err("SPLITTING_OPERATION_REQUIRED".into());
    }
    let n = request["conductor"]
        .as_u64()
        .ok_or("INTEGER_CONDUCTOR_REQUIRED")?;
    irreducible_splitting_degree(n, &request["coefficients"])
}
pub fn validate_splitting_degree(n: u64, coefficients: &Value, result: &Value) -> Result<()> {
    let input = input(n, coefficients)?;
    let p = &input.monic;
    let d = input.d;
    exact_fields(
        result,
        &[
            "schema",
            "authority_effect",
            "algorithm",
            "conductor",
            "real_generator_radicand",
            "coefficient_field",
            "degree_over_real_field",
            "galois_group",
            "coefficients",
            "monic_polynomial",
            "factorization",
            "discriminant",
            "discriminant_square",
            "resolvent",
        ],
    )?;
    if result["schema"] != "real_field_splitting_degree_v1"
        || result["authority_effect"] != "None"
        || result["algorithm"] != "EXACT_CUBIC_QUARTIC_RESOLVENT_CLASSIFICATION"
        || result["conductor"].as_u64() != Some(n)
        || result["real_generator_radicand"].as_u64() != Some(d)
        || result["coefficient_field"] != input.name
    {
        return Err("SPLITTING_METADATA_MISMATCH".into());
    }
    if polynomial(&result["coefficients"], d)? != input.original {
        return Err("SPLITTING_INPUT_BINDING_MISMATCH".into());
    }
    if polynomial(&result["monic_polynomial"], d)? != *p {
        return Err("MONIC_POLYNOMIAL_MISMATCH".into());
    }
    factors::validate_factorization(n, &wire(&input.original), &result["factorization"])?;
    irreducible(&result["factorization"], p, d)?;
    let delta = discriminant(p, d);
    if delta.is_zero() {
        return Err("ZERO_DISCRIMINANT".into());
    }
    if element(&result["discriminant"], d)? != delta {
        return Err("DISCRIMINANT_MISMATCH".into());
    }
    squares::verify_square_certificate(n, &delta.wire(), &result["discriminant_square"])?;
    let mut degrees = Vec::new();
    let mut cyclic = None;
    if p.len() == 4 {
        if !result["resolvent"].is_null() {
            return Err("CUBIC_RESOLVENT_MUST_BE_NULL".into());
        }
    } else {
        let supplied = &result["resolvent"];
        exact_fields(
            supplied,
            &[
                "coefficients",
                "factorization",
                "factor_degrees",
                "root",
                "cyclic_tests",
            ],
        )?;
        let r = resolvent(p, d);
        if polynomial(&supplied["coefficients"], d)? != r {
            return Err("RESOLVENT_POLYNOMIAL_MISMATCH".into());
        }
        factors::validate_factorization(n, &wire(&r), &supplied["factorization"])?;
        let (pattern, root) = pattern(&supplied["factorization"], d)?;
        degrees = pattern;
        let claimed = supplied["factor_degrees"]
            .as_array()
            .ok_or("RESOLVENT_FACTOR_DEGREES_REQUIRED")?;
        if claimed.len() != degrees.len()
            || claimed
                .iter()
                .zip(&degrees)
                .any(|(a, b)| a.as_u64() != Some(*b))
        {
            return Err("RESOLVENT_FACTOR_DEGREES_MISMATCH".into());
        }
        if let Some(root) = root {
            if element(&supplied["root"], d)? != root {
                return Err("RESOLVENT_ROOT_MISMATCH".into());
            }
            let tests = &supplied["cyclic_tests"];
            exact_fields(
                tests,
                &[
                    "first_value",
                    "first_square",
                    "second_value",
                    "second_square",
                ],
            )?;
            let (u, v) = cyclic_values(p, &delta, &root, d);
            if element(&tests["first_value"], d)? != u {
                return Err("CYCLIC_FIRST_VALUE_MISMATCH".into());
            }
            if element(&tests["second_value"], d)? != v {
                return Err("CYCLIC_SECOND_VALUE_MISMATCH".into());
            }
            squares::verify_square_certificate(n, &u.wire(), &tests["first_square"])?;
            squares::verify_square_certificate(n, &v.wire(), &tests["second_square"])?;
            cyclic = Some((
                square_bool(&tests["first_square"])?,
                square_bool(&tests["second_square"])?,
            ));
        } else if !supplied["root"].is_null() || !supplied["cyclic_tests"].is_null() {
            return Err("UNUSED_RESOLVENT_WITNESSES_MUST_BE_NULL".into());
        }
    }
    let (group, degree) = classify(
        p.len() - 1,
        square_bool(&result["discriminant_square"])?,
        &degrees,
        cyclic,
    )?;
    if result["galois_group"] != group {
        return Err("GALOIS_GROUP_MISMATCH".into());
    }
    if result["degree_over_real_field"].as_u64() != Some(degree) {
        return Err("REAL_SPLITTING_DEGREE_MISMATCH".into());
    }
    Ok(())
}

#[cfg(test)]
pub fn fold_control(terms: &Value, self_join: bool) -> Result<Value> {
    let qs = terms
        .as_array()
        .ok_or("COEFFICIENT_ARRAY_REQUIRED")?
        .iter()
        .map(rational)
        .collect::<Result<Vec<_>>>()?;
    if self_join {
        let mut value = BigInt::zero();
        for (i, a) in qs.iter().enumerate() {
            for (j, b) in qs.iter().enumerate() {
                if i != j {
                    value += a.numer() * b.denom();
                }
            }
        }
        return Ok(json!(qwire(&Q::from_integer(value))));
    }
    let terms = qs
        .into_iter()
        .map(|a| E { a, b: Q::zero() })
        .collect::<Vec<_>>();
    Ok(json!(qwire(&sum(&terms).a)))
}

fn raw_number_admission(input: &str) -> Result<()> {
    let bytes = input.as_bytes();
    let mut i = 0;
    let mut quoted = false;
    let mut escaped = false;
    while i < bytes.len() {
        let byte = bytes[i];
        if quoted {
            if escaped {
                escaped = false;
            } else if byte == b'\\' {
                escaped = true;
            } else if byte == b'"' {
                quoted = false;
            }
            i += 1;
        } else if byte == b'"' {
            quoted = true;
            i += 1;
        } else if matches!(byte, b'-' | b'0'..=b'9') {
            i += 1;
            while i < bytes.len()
                && matches!(bytes[i], b'0'..=b'9' | b'+' | b'-' | b'.' | b'e' | b'E')
            {
                if matches!(bytes[i], b'.' | b'e' | b'E') {
                    return Err("RAW_INEXACT_JSON_NUMBER".into());
                }
                i += 1;
            }
        } else {
            i += 1;
        }
    }
    Ok(())
}
fn run() -> Result<Value> {
    if std::env::args().len() != 1 {
        return Err("USAGE:real_field_splitting_degrees < REQUEST_JSON".into());
    }
    let mut input = String::new();
    io::stdin()
        .read_to_string(&mut input)
        .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
    let exact_numbers = raw_number_admission(&input);
    let fields: BTreeMap<String, Box<RawValue>> =
        serde_json::from_str(&input).map_err(|e| format!("INVALID_JSON:{e}"))?;
    exact_numbers?;
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
        .map_err(|_| "SPLITTING_OPERATION_REQUIRED")?;
    let coefficients: Vec<[String; 2]> = serde_json::from_str(fields["coefficients"].get())
        .map_err(|_| "CANONICAL_RATIONAL_STRING_REQUIRED")?;
    evaluate_request(
        &json!({"operation":operation,"conductor":conductor,"coefficients":coefficients}),
    )
}
fn main() {
    match run() {
        Ok(result) => println!("{}", serde_json::to_string(&result).expect("JSON output")),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}
