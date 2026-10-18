use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde_json::{json, Value};
use std::cmp::Ordering;
use std::io::{self, Read};

type Q = BigRational;
type Result<T> = std::result::Result<T, String>;

fn qstr(q: &Q) -> String {
    format!("{}/{}", q.numer(), q.denom())
}

fn exact_json(value: &Value, path: &str) -> Result<()> {
    match value {
        Value::Number(n) if n.to_string().contains(['.', 'e', 'E']) => {
            return Err(format!("INEXACT_JSON_NUMBER:{path}"));
        }
        Value::Array(items) => {
            for (i, item) in items.iter().enumerate() {
                exact_json(item, &format!("{path}[{i}]"))?;
            }
        }
        Value::Object(items) => {
            for (key, item) in items {
                exact_json(item, &format!("{path}.{key}"))?;
            }
        }
        _ => {}
    }
    Ok(())
}

fn keys(value: &Value, expected: &[&str], path: &str) -> Result<()> {
    let object = value
        .as_object()
        .ok_or_else(|| format!("OBJECT_REQUIRED:{path}"))?;
    if object.len() != expected.len() || expected.iter().any(|key| !object.contains_key(*key)) {
        return Err(format!("EXACT_FIELDS_REQUIRED:{path}"));
    }
    Ok(())
}

fn rational(value: &Value, path: &str) -> Result<Q> {
    let text = value
        .as_str()
        .ok_or_else(|| format!("RATIONAL_STRING_REQUIRED:{path}"))?;
    let (n, d) = text
        .split_once('/')
        .ok_or_else(|| format!("RATIONAL_FORMAT:{path}"))?;
    let numerator: BigInt = n.parse().map_err(|_| format!("RATIONAL_FORMAT:{path}"))?;
    let denominator: BigInt = d.parse().map_err(|_| format!("RATIONAL_FORMAT:{path}"))?;
    if denominator <= BigInt::zero() {
        return Err(format!("RATIONAL_POSITIVE_DENOMINATOR_REQUIRED:{path}"));
    }
    let q = Q::new(numerator, denominator);
    if qstr(&q) != text {
        return Err(format!("RATIONAL_REDUCED_FORM_REQUIRED:{path}"));
    }
    Ok(q)
}

fn conductor(value: &Value) -> Result<u64> {
    let n = value
        .as_u64()
        .ok_or("CONDUCTOR_UNSIGNED_INTEGER_REQUIRED")?;
    radicand(n)?;
    Ok(n)
}

fn radicand(n: u64) -> Result<u64> {
    match n {
        1 | 3 | 4 => Ok(0),
        8 => Ok(2),
        5 => Ok(5),
        _ => Err("CONDUCTOR_OUTSIDE_REAL_FIELD_CLASS".into()),
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct Element {
    a: Q,
    b: Q,
}

impl Element {
    fn parse(value: &Value, d: u64, path: &str) -> Result<Self> {
        let pair = value
            .as_array()
            .ok_or_else(|| format!("COORDINATE_PAIR_REQUIRED:{path}"))?;
        if pair.len() != 2 {
            return Err(format!("COORDINATE_PAIR_REQUIRED:{path}"));
        }
        let element = Self {
            a: rational(&pair[0], &format!("{path}[0]"))?,
            b: rational(&pair[1], &format!("{path}[1]"))?,
        };
        if d == 0 && !element.b.is_zero() {
            return Err(format!("RATIONAL_FIELD_NONZERO_RADICAL_COORDINATE:{path}"));
        }
        Ok(element)
    }
    fn wire(&self) -> Value {
        json!([qstr(&self.a), qstr(&self.b)])
    }
    fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }
    fn neg(&self) -> Self {
        Self {
            a: -&self.a,
            b: -&self.b,
        }
    }
    fn mul(&self, other: &Self, d: u64) -> Self {
        Self {
            a: &self.a * &other.a + Q::from_integer(d.into()) * &self.b * &other.b,
            b: &self.a * &other.b + &self.b * &other.a,
        }
    }
    fn norm(&self, d: u64) -> Q {
        &self.a * &self.a - Q::from_integer(d.into()) * &self.b * &self.b
    }
    fn divide(&self, other: &Self, d: u64) -> Result<Self> {
        if other.is_zero() {
            return Err("SQUARECLASS_ZERO_ARGUMENT".into());
        }
        let norm = other.norm(d);
        if norm.is_zero() {
            return Err("NONZERO_FIELD_ELEMENT_HAS_ZERO_NORM".into());
        }
        Ok(self.mul(
            &Self {
                a: &other.a / &norm,
                b: -&other.b / &norm,
            },
            d,
        ))
    }
    fn sign(&self, d: u64) -> Ordering {
        if self.b.is_zero() {
            return self.a.cmp(&Q::zero());
        }
        if self.a.is_zero() || self.a.is_positive() == self.b.is_positive() {
            return self.b.cmp(&Q::zero());
        }
        let order = (&self.a * &self.a).cmp(&(Q::from_integer(d.into()) * &self.b * &self.b));
        if self.a.is_positive() {
            order
        } else {
            order.reverse()
        }
    }
}

fn integer_sqrt(n: &BigInt) -> Option<BigInt> {
    if n.is_negative() {
        return None;
    }
    if n < &BigInt::from(2) {
        return Some(n.clone());
    }
    let mut x = BigInt::one() << n.bits().div_ceil(2);
    loop {
        let next = (&x + n / &x) >> 1;
        if next >= x {
            return Some(x);
        }
        x = next;
    }
}

fn rational_sqrt(q: &Q) -> Option<Q> {
    let numerator = integer_sqrt(q.numer())?;
    let denominator = integer_sqrt(q.denom())?;
    if &numerator * &numerator != *q.numer() || &denominator * &denominator != *q.denom() {
        return None;
    }
    Some(Q::new(numerator, denominator))
}

enum Decision {
    Square(Element),
    Nonsquare(&'static str),
}

fn decide(input: &Element, d: u64) -> Result<Decision> {
    if d == 0 {
        return Ok(match rational_sqrt(&input.a) {
            Some(x) => Decision::Square(Element { a: x, b: Q::zero() }),
            None => Decision::Nonsquare("RATIONAL_NONSQUARE"),
        });
    }
    if input.b.is_zero() {
        if let Some(x) = rational_sqrt(&input.a) {
            return Ok(Decision::Square(Element { a: x, b: Q::zero() }));
        }
        if let Some(y) = rational_sqrt(&(&input.a / Q::from_integer(d.into()))) {
            return Ok(Decision::Square(Element { a: Q::zero(), b: y }));
        }
        return Ok(Decision::Nonsquare("RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D"));
    }
    let Some(r) = rational_sqrt(&input.norm(d)) else {
        return Ok(Decision::Nonsquare("NORM_NOT_RATIONAL_SQUARE"));
    };
    for half_trace in [
        (&input.a + &r) / Q::from_integer(2.into()),
        (&input.a - &r) / Q::from_integer(2.into()),
    ] {
        if let Some(x) = rational_sqrt(&half_trace) {
            if x.is_zero() {
                continue;
            }
            let y = &input.b / (Q::from_integer(2.into()) * &x);
            let mut root = Element { a: x, b: y };
            if root.mul(&root, d) != *input {
                return Err("SQUARE_WITNESS_RECONSTRUCTION_FAILED".into());
            }
            if root.sign(d) == Ordering::Less {
                root = root.neg();
            }
            return Ok(Decision::Square(root));
        }
    }
    Ok(Decision::Nonsquare("NO_RATIONAL_HALF_TRACE_SQUARE"))
}

fn square_from_element(n: u64, input: &Element) -> Result<Value> {
    let d = radicand(n)?;
    let (is_square, root, obstruction) = match decide(input, d)? {
        Decision::Square(root) => (true, root.wire(), Value::Null),
        Decision::Nonsquare(reason) => (false, Value::Null, json!(reason)),
    };
    Ok(
        json!({"schema":"real_field_square_v1","authority_effect":"None","conductor":n,
        "real_generator_radicand":d,"coefficients":input.wire(),"is_square":is_square,
        "root":root,"obstruction":obstruction}),
    )
}

pub fn square_certificate(n: u64, coefficients: &Value) -> Result<Value> {
    exact_json(coefficients, "coefficients")?;
    let d = radicand(n)?;
    square_from_element(n, &Element::parse(coefficients, d, "coefficients")?)
}

pub fn squareclass_certificate(n: u64, left: &Value, right: &Value) -> Result<Value> {
    exact_json(left, "left")?;
    exact_json(right, "right")?;
    let d = radicand(n)?;
    let left = Element::parse(left, d, "left")?;
    let right = Element::parse(right, d, "right")?;
    if left.is_zero() || right.is_zero() {
        return Err("SQUARECLASS_ZERO_ARGUMENT".into());
    }
    let quotient = left.divide(&right, d)?;
    let square = square_from_element(n, &quotient)?;
    Ok(
        json!({"schema":"real_field_squareclass_v1","authority_effect":"None","conductor":n,
        "left":left.wire(),"right":right.wire(),"quotient":quotient.wire(),
        "same_squareclass":square["is_square"],"square_certificate":square}),
    )
}

fn equal(actual: &Value, expected: &Value, path: &str) -> Result<()> {
    if actual != expected {
        return Err(format!("CERTIFICATE_BINDING_MISMATCH:{path}"));
    }
    Ok(())
}

fn negative_obstruction(input: &Element, d: u64) -> Option<&'static str> {
    if d == 0 {
        return rational_sqrt(&input.a)
            .is_none()
            .then_some("RATIONAL_NONSQUARE");
    }
    if input.b.is_zero() {
        return (rational_sqrt(&input.a).is_none()
            && rational_sqrt(&(&input.a / Q::from_integer(d.into()))).is_none())
        .then_some("RATIONAL_SQUARECLASS_OUTSIDE_1_OR_D");
    }
    let Some(r) = rational_sqrt(&input.norm(d)) else {
        return Some("NORM_NOT_RATIONAL_SQUARE");
    };
    for sign in [1, -1] {
        let candidate = (&input.a + Q::from_integer(sign.into()) * &r) / Q::from_integer(2.into());
        if rational_sqrt(&candidate).is_some_and(|x| !x.is_zero()) {
            return None;
        }
    }
    Some("NO_RATIONAL_HALF_TRACE_SQUARE")
}

pub fn verify_square_certificate(n: u64, coefficients: &Value, certificate: &Value) -> Result<()> {
    exact_json(coefficients, "coefficients")?;
    exact_json(certificate, "certificate")?;
    let d = radicand(n)?;
    let input = Element::parse(coefficients, d, "coefficients")?;
    keys(
        certificate,
        &[
            "schema",
            "authority_effect",
            "conductor",
            "real_generator_radicand",
            "coefficients",
            "is_square",
            "root",
            "obstruction",
        ],
        "square_certificate",
    )?;
    equal(
        &certificate["schema"],
        &json!("real_field_square_v1"),
        "schema",
    )?;
    equal(
        &certificate["authority_effect"],
        &json!("None"),
        "authority_effect",
    )?;
    if conductor(&certificate["conductor"])? != n {
        return Err("CERTIFICATE_BINDING_MISMATCH:conductor".into());
    }
    let claimed_d = certificate["real_generator_radicand"]
        .as_u64()
        .ok_or("RADICAND_UNSIGNED_INTEGER_REQUIRED")?;
    if claimed_d != d {
        return Err("CERTIFICATE_BINDING_MISMATCH:real_generator_radicand".into());
    }
    let certified_input =
        Element::parse(&certificate["coefficients"], d, "certificate.coefficients")?;
    if certified_input != input {
        return Err("CERTIFICATE_BINDING_MISMATCH:coefficients".into());
    }
    let square = certificate["is_square"]
        .as_bool()
        .ok_or("IS_SQUARE_BOOLEAN_REQUIRED")?;
    if square {
        if !certificate["obstruction"].is_null() {
            return Err("SQUARE_OBSTRUCTION_MUST_BE_NULL".into());
        }
        let root = Element::parse(&certificate["root"], d, "certificate.root")?;
        if root.mul(&root, d) != input {
            return Err("SQUARE_WITNESS_PRODUCT_MISMATCH".into());
        }
        if root.sign(d) == Ordering::Less {
            return Err("SQUARE_WITNESS_NEGATIVE_SIGN".into());
        }
    } else {
        if !certificate["root"].is_null() {
            return Err("NONSQUARE_ROOT_MUST_BE_NULL".into());
        }
        let obstruction = negative_obstruction(&input, d).ok_or("FALSE_NONSQUARE_CERTIFICATE")?;
        equal(
            &certificate["obstruction"],
            &json!(obstruction),
            "obstruction",
        )?;
    }
    Ok(())
}

pub fn verify_squareclass_certificate(
    n: u64,
    left: &Value,
    right: &Value,
    certificate: &Value,
) -> Result<()> {
    exact_json(left, "left")?;
    exact_json(right, "right")?;
    exact_json(certificate, "certificate")?;
    let d = radicand(n)?;
    let left = Element::parse(left, d, "left")?;
    let right = Element::parse(right, d, "right")?;
    if left.is_zero() || right.is_zero() {
        return Err("SQUARECLASS_ZERO_ARGUMENT".into());
    }
    keys(
        certificate,
        &[
            "schema",
            "authority_effect",
            "conductor",
            "left",
            "right",
            "quotient",
            "same_squareclass",
            "square_certificate",
        ],
        "squareclass_certificate",
    )?;
    equal(
        &certificate["schema"],
        &json!("real_field_squareclass_v1"),
        "schema",
    )?;
    equal(
        &certificate["authority_effect"],
        &json!("None"),
        "authority_effect",
    )?;
    if conductor(&certificate["conductor"])? != n {
        return Err("CERTIFICATE_BINDING_MISMATCH:conductor".into());
    }
    if Element::parse(&certificate["left"], d, "certificate.left")? != left {
        return Err("CERTIFICATE_BINDING_MISMATCH:left".into());
    }
    if Element::parse(&certificate["right"], d, "certificate.right")? != right {
        return Err("CERTIFICATE_BINDING_MISMATCH:right".into());
    }
    let quotient = Element::parse(&certificate["quotient"], d, "certificate.quotient")?;
    if quotient.mul(&right, d) != left {
        return Err("SQUARECLASS_QUOTIENT_PRODUCT_MISMATCH".into());
    }
    verify_square_certificate(n, &quotient.wire(), &certificate["square_certificate"])?;
    let same = certificate["same_squareclass"]
        .as_bool()
        .ok_or("SAME_SQUARECLASS_BOOLEAN_REQUIRED")?;
    if Some(same) != certificate["square_certificate"]["is_square"].as_bool() {
        return Err("SQUARECLASS_BOOLEAN_DISAGREEMENT".into());
    }
    Ok(())
}

fn request_operation(request: &Value) -> Result<(&str, u64)> {
    exact_json(request, "request")?;
    let operation = request["operation"]
        .as_str()
        .ok_or("OPERATION_STRING_REQUIRED")?;
    match operation {
        "square" => keys(
            request,
            &["operation", "conductor", "coefficients"],
            "request",
        )?,
        "squareclass" => keys(
            request,
            &["operation", "conductor", "left", "right"],
            "request",
        )?,
        _ => return Err("UNKNOWN_REAL_FIELD_OPERATION".into()),
    }
    Ok((operation, conductor(&request["conductor"])?))
}

pub fn handle_request(request: &Value) -> Result<Value> {
    let (operation, n) = request_operation(request)?;
    match operation {
        "square" => square_certificate(n, &request["coefficients"]),
        _ => squareclass_certificate(n, &request["left"], &request["right"]),
    }
}

pub fn verify_certificate(request: &Value, certificate: &Value) -> Result<()> {
    let (operation, n) = request_operation(request)?;
    match operation {
        "square" => verify_square_certificate(n, &request["coefficients"], certificate),
        _ => verify_squareclass_certificate(n, &request["left"], &request["right"], certificate),
    }
}

fn cli() -> Result<Value> {
    if std::env::args().len() != 1 {
        return Err("USAGE:real_field_squares < REQUEST_JSON".into());
    }
    let mut text = String::new();
    io::stdin()
        .read_to_string(&mut text)
        .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
    let request = serde_json::from_str(&text).map_err(|e| format!("INVALID_JSON:{e}"))?;
    crate::linear_algebra::json_admission::admit_exact_json(&text)?;
    handle_request(&request)
}

fn main() {
    match cli() {
        Ok(value) => println!(
            "{}",
            serde_json::to_string(&value).expect("JSON serialization")
        ),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}
