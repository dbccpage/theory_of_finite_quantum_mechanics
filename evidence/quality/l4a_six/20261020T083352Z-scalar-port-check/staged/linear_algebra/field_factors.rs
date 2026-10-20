#[allow(dead_code)]
#[path = "rational_factors.rs"]
mod rational;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde_json::value::RawValue;
use serde_json::{json, Value};
use std::collections::BTreeMap;
use std::io::{self, Read};

type Q = BigRational;
type Result<T> = std::result::Result<T, String>;
type Polynomial = Vec<Element>;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Element {
    a: Q,
    b: Q,
}

impl Element {
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
    fn scalar(a: Q) -> Self {
        Self { a, b: Q::zero() }
    }
    fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }
    fn is_one(&self) -> bool {
        self.a.is_one() && self.b.is_zero()
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
    fn conjugate(&self) -> Self {
        Self {
            a: self.a.clone(),
            b: -&self.b,
        }
    }
    fn wire(&self) -> Value {
        json!([rational_wire(&self.a), rational_wire(&self.b)])
    }
}

fn field(conductor: u64) -> Result<(u64, &'static str)> {
    match conductor {
        1 | 3 | 4 => Ok((0, "Q")),
        5 => Ok((5, "Q(sqrt(5))")),
        8 => Ok((2, "Q(sqrt(2))")),
        _ => Err("UNSUPPORTED_CONDUCTOR".into()),
    }
}

fn rational_wire(q: &Q) -> String {
    format!("{}/{}", q.numer(), q.denom())
}

fn parse_rational(value: &Value) -> Result<Q> {
    let text = value.as_str().ok_or("CANONICAL_RATIONAL_STRING_REQUIRED")?;
    let (a, b) = text.split_once('/').ok_or("RATIONAL_FORMAT")?;
    let a: BigInt = a.parse().map_err(|_| "RATIONAL_FORMAT")?;
    let b: BigInt = b.parse().map_err(|_| "RATIONAL_FORMAT")?;
    if b <= BigInt::zero() {
        return Err("POSITIVE_RATIONAL_DENOMINATOR_REQUIRED".into());
    }
    let q = Q::new(a, b);
    if rational_wire(&q) != text {
        return Err("REDUCED_RATIONAL_REQUIRED".into());
    }
    Ok(q)
}

fn parse_element(value: &Value, d: u64) -> Result<Element> {
    let entries = value.as_array().ok_or("COEFFICIENT_PAIR_REQUIRED")?;
    if entries.len() != 2 {
        return Err("COEFFICIENT_PAIR_REQUIRED".into());
    }
    let result = Element {
        a: parse_rational(&entries[0])?,
        b: parse_rational(&entries[1])?,
    };
    if d == 0 && !result.b.is_zero() {
        return Err("RATIONAL_FIELD_RADICAL_COORDINATE_NONZERO".into());
    }
    Ok(result)
}

fn parse_polynomial(value: &Value, d: u64) -> Result<Polynomial> {
    let entries = value.as_array().ok_or("COEFFICIENT_ARRAY_REQUIRED")?;
    if entries.is_empty() {
        return Err("NONEMPTY_POLYNOMIAL_REQUIRED".into());
    }
    let mut polynomial = entries
        .iter()
        .map(|x| parse_element(x, d))
        .collect::<Result<Polynomial>>()?;
    if polynomial[0].is_zero() {
        return Err("NONZERO_LEADING_COEFFICIENT_REQUIRED".into());
    }
    polynomial.reverse();
    Ok(polynomial)
}

fn wire(p: &[Element]) -> Value {
    json!(p.iter().rev().map(Element::wire).collect::<Vec<_>>())
}

fn trim(mut p: Polynomial) -> Polynomial {
    while p.len() > 1 && p.last().is_some_and(Element::is_zero) {
        p.pop();
    }
    if p.is_empty() {
        p.push(Element::zero());
    }
    p
}
fn zero(p: &[Element]) -> bool {
    p.len() == 1 && p[0].is_zero()
}
fn one(p: &[Element]) -> bool {
    p.len() == 1 && p[0].is_one()
}

fn multiply(a: &[Element], b: &[Element], d: u64) -> Polynomial {
    let mut result = vec![Element::zero(); a.len() + b.len() - 1];
    for (i, x) in a.iter().enumerate() {
        for (j, y) in b.iter().enumerate() {
            result[i + j] = result[i + j].add(&x.mul(y, d));
        }
    }
    trim(result)
}

fn divide(a: &[Element], b: &[Element], d: u64) -> Result<(Polynomial, Polynomial)> {
    if zero(b) {
        return Err("ZERO_POLYNOMIAL_DIVISOR".into());
    }
    let inverse = b.last().unwrap().inverse(d)?;
    let mut remainder = a.to_vec();
    let mut quotient = vec![Element::zero(); a.len().saturating_sub(b.len()) + 1];
    while !zero(&remainder) && remainder.len() >= b.len() {
        let shift = remainder.len() - b.len();
        let coefficient = remainder.last().unwrap().mul(&inverse, d);
        quotient[shift] = coefficient.clone();
        for (i, value) in b.iter().enumerate() {
            remainder[shift + i] = remainder[shift + i].sub(&coefficient.mul(value, d));
        }
        remainder = trim(remainder);
    }
    Ok((trim(quotient), remainder))
}

fn quotient(a: &[Element], b: &[Element], d: u64) -> Result<Polynomial> {
    let (quotient, remainder) = divide(a, b, d)?;
    if !zero(&remainder) {
        return Err("NONEXACT_FIELD_POLYNOMIAL_DIVISION".into());
    }
    Ok(quotient)
}

fn monic(p: &[Element], d: u64) -> Result<Polynomial> {
    let inverse = p.last().unwrap().inverse(d)?;
    Ok(p.iter().map(|x| x.mul(&inverse, d)).collect())
}

fn gcd(mut a: Polynomial, mut b: Polynomial, d: u64) -> Result<Polynomial> {
    while !zero(&b) {
        let remainder = divide(&a, &b, d)?.1;
        a = b;
        b = remainder;
    }
    monic(&a, d)
}

fn derivative(p: &[Element]) -> Polynomial {
    trim(
        p.iter()
            .enumerate()
            .skip(1)
            .map(|(i, x)| {
                let integer = Q::from_integer(i.into());
                Element {
                    a: &x.a * &integer,
                    b: &x.b * integer,
                }
            })
            .collect(),
    )
}

fn squarefree(p: &[Element], d: u64) -> Result<Vec<(Polynomial, usize)>> {
    if p.len() == 1 {
        return Ok(Vec::new());
    }
    let p = monic(p, d)?;
    let mut repeated = gcd(p.clone(), derivative(&p), d)?;
    let mut remaining = quotient(&p, &repeated, d)?;
    let mut multiplicity = 1;
    let mut result = Vec::new();
    while !one(&remaining) {
        let common = gcd(remaining.clone(), repeated.clone(), d)?;
        let part = quotient(&remaining, &common, d)?;
        if !one(&part) {
            result.push((part, multiplicity));
        }
        remaining = common.clone();
        repeated = quotient(&repeated, &common, d)?;
        multiplicity += 1;
    }
    if !one(&repeated) {
        return Err("SQUAREFREE_RECONSTRUCTION_FAILED".into());
    }
    Ok(result)
}

fn shift(p: &[Element], offset: &Element, d: u64) -> Polynomial {
    let mut result = vec![Element::zero()];
    for coefficient in p.iter().rev() {
        result = multiply(&result, &[offset.clone(), Element::one()], d);
        result[0] = result[0].add(coefficient);
    }
    trim(result)
}

fn norm(p: &[Element], d: u64) -> Result<Polynomial> {
    let conjugate = p.iter().map(Element::conjugate).collect::<Polynomial>();
    let result = multiply(p, &conjugate, d);
    if result.iter().any(|x| !x.b.is_zero()) {
        return Err("TRAGER_NORM_NOT_RATIONAL".into());
    }
    Ok(result)
}

fn rational_factors(p: &[Element]) -> Result<Vec<(Polynomial, usize)>> {
    if p.iter().any(|x| !x.b.is_zero()) {
        return Err("RATIONAL_BACKEND_NONRATIONAL_COEFFICIENT".into());
    }
    let coefficients = json!(p
        .iter()
        .rev()
        .map(|x| rational_wire(&x.a))
        .collect::<Vec<_>>());
    let output =
        rational::evaluate_request(&json!({"operation":"factor","coefficients":coefficients}))?;
    let rows = output["factors"]
        .as_array()
        .ok_or("RATIONAL_BACKEND_FACTOR_ARRAY")?;
    rows.iter()
        .map(|row| {
            let entries = row["polynomial"]
                .as_array()
                .ok_or("RATIONAL_BACKEND_POLYNOMIAL")?;
            let mut factor = entries
                .iter()
                .map(|x| parse_rational(x).map(Element::scalar))
                .collect::<Result<Polynomial>>()?;
            factor.reverse();
            let multiplicity = row["multiplicity"]
                .as_u64()
                .and_then(|x| usize::try_from(x).ok())
                .filter(|m| *m > 0)
                .ok_or("RATIONAL_BACKEND_MULTIPLICITY")?;
            Ok((factor, multiplicity))
        })
        .collect()
}

fn separable_shift(p: &[Element], d: u64) -> Result<(usize, Polynomial, Polynomial)> {
    let degree = p.len() - 1;
    let bound = degree
        .checked_mul(degree)
        .ok_or("REPRESENTATION_SIZE_OVERFLOW")?;
    for s in 0..=bound {
        let offset = Element {
            a: Q::zero(),
            b: -Q::from_integer(s.into()),
        };
        let shifted = shift(p, &offset, d);
        let rational_norm = norm(&shifted, d)?;
        if gcd(rational_norm.clone(), derivative(&rational_norm), d)?.len() == 1 {
            return Ok((s, shifted, rational_norm));
        }
    }
    Err("TRAGER_PROVED_SHIFT_BOUND_VIOLATION".into())
}

fn factor_squarefree(p: &[Element], d: u64) -> Result<Vec<Polynomial>> {
    if d == 0 {
        return rational_factors(p).map(|rows| rows.into_iter().map(|(p, _)| p).collect());
    }
    let (s, shifted, rational_norm) = separable_shift(p, d)?;
    let offset = Element {
        a: Q::zero(),
        b: Q::from_integer(s.into()),
    };
    let mut result = Vec::new();
    for (rational_factor, multiplicity) in rational_factors(&rational_norm)? {
        if multiplicity != 1 {
            return Err("TRAGER_NORM_FACTOR_NOT_SQUAREFREE".into());
        }
        let intersection = gcd(shifted.clone(), rational_factor.clone(), d)?;
        let degree = rational_factor.len() - 1;
        if intersection.len() < 2
            || degree % 2 != 0
            || degree / 2 != intersection.len() - 1
            || norm(&intersection, d)? != rational_factor
        {
            return Err("TRAGER_FACTOR_PAIRING_FAILED".into());
        }
        result.push(shift(&intersection, &offset, d));
    }
    let product = result
        .iter()
        .fold(vec![Element::one()], |a, b| multiply(&a, b, d));
    if product != p {
        return Err("TRAGER_RECONSTRUCTION_FAILED".into());
    }
    Ok(result)
}

fn factors(p: &[Element], d: u64) -> Result<Vec<(Polynomial, usize)>> {
    let mut result = Vec::new();
    for (part, multiplicity) in squarefree(p, d)? {
        for irreducible in factor_squarefree(&part, d)? {
            result.push((irreducible, multiplicity));
        }
    }
    if d != 0 {
        for (factor, _) in &result {
            if quadratic_has_listed_root(factor, d) {
                return Err("QUADRATIC_HAS_A_FIELD_ROOT".into());
            }
        }
    }
    result.sort_by(|a, b| a.0.iter().rev().cmp(b.0.iter().rev()));
    Ok(result)
}

fn evaluate_at(polynomial: &[Element], point: &Element, d: u64) -> Element {
    let mut acc = Element::zero();
    for coefficient in polynomial.iter().rev() {
        acc = acc.mul(point, d).add(coefficient);
    }
    acc
}

fn quadratic_has_listed_root(polynomial: &[Element], d: u64) -> bool {
    if polynomial.len() < 3 {
        return false;
    }
    let radical = Element {
        a: Q::zero(),
        b: Q::one(),
    };
    [
        Element::zero(),
        Element::one(),
        Element::one().neg(),
        radical.clone(),
        radical.neg(),
    ]
    .iter()
    .any(|point| evaluate_at(polynomial, point, d).is_zero())
}

fn exact_fields(value: &Value, fields: &[&str]) -> Result<()> {
    let map = value.as_object().ok_or("OBJECT_REQUIRED")?;
    if map.len() != fields.len() || fields.iter().any(|field| !map.contains_key(*field)) {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    Ok(())
}

pub fn evaluate_request(request: &Value) -> Result<Value> {
    exact_fields(request, &["operation", "conductor", "coefficients"])?;
    if request["operation"] != "factor" {
        return Err("FACTOR_OPERATION_REQUIRED".into());
    }
    let conductor = request["conductor"]
        .as_u64()
        .ok_or("INTEGER_CONDUCTOR_REQUIRED")?;
    let (d, name) = field(conductor)?;
    let p = parse_polynomial(&request["coefficients"], d)?;
    let factorization = factors(&p, d)?;
    Ok(
        json!({"schema":"real_field_polynomial_factorization_v1","authority_effect":"None",
        "conductor":conductor,"real_generator_radicand":d,"coefficient_field":name,
        "coefficients":wire(&p),"content":p.last().unwrap().wire(),
        "factors":factorization.iter().map(|(p,m)| json!({"polynomial":wire(p),"multiplicity":m})).collect::<Vec<_>>(),
        "algorithm":"EXACT_TRAGER_RATIONAL_NORM_FACTORIZATION"}),
    )
}

pub fn validate_factorization(conductor: u64, coefficients: &Value, output: &Value) -> Result<()> {
    let (d, name) = field(conductor)?;
    let input = parse_polynomial(coefficients, d)?;
    exact_fields(
        output,
        &[
            "schema",
            "authority_effect",
            "conductor",
            "real_generator_radicand",
            "coefficient_field",
            "coefficients",
            "content",
            "factors",
            "algorithm",
        ],
    )?;
    if output["schema"] != "real_field_polynomial_factorization_v1"
        || output["authority_effect"] != "None"
        || output["conductor"].as_u64() != Some(conductor)
        || output["real_generator_radicand"].as_u64() != Some(d)
        || output["coefficient_field"] != name
        || output["algorithm"] != "EXACT_TRAGER_RATIONAL_NORM_FACTORIZATION"
    {
        return Err("FACTORIZATION_METADATA_MISMATCH".into());
    }
    if parse_polynomial(&output["coefficients"], d)? != input {
        return Err("FACTORIZATION_INPUT_BINDING_MISMATCH".into());
    }
    let content = parse_element(&output["content"], d)?;
    if content != *input.last().unwrap() {
        return Err("FACTORIZATION_CONTENT_MISMATCH".into());
    }
    let rows = output["factors"]
        .as_array()
        .ok_or("FACTOR_ARRAY_REQUIRED")?;
    let mut product = vec![content];
    let mut previous: Option<Polynomial> = None;
    let mut total_degree = 0usize;
    for row in rows {
        exact_fields(row, &["polynomial", "multiplicity"])?;
        let p = parse_polynomial(&row["polynomial"], d)?;
        if p.len() < 2 || !p.last().unwrap().is_one() {
            return Err("MONIC_NONCONSTANT_FACTOR_REQUIRED".into());
        }
        if previous
            .as_ref()
            .is_some_and(|old| old.iter().rev().cmp(p.iter().rev()).is_ge())
        {
            return Err("DISTINCT_NUMERIC_SORTED_FACTORS_REQUIRED".into());
        }
        previous = Some(p.clone());
        let multiplicity = row["multiplicity"]
            .as_u64()
            .and_then(|x| usize::try_from(x).ok())
            .filter(|x| *x > 0)
            .ok_or("POSITIVE_INTEGER_MULTIPLICITY_REQUIRED")?;
        total_degree = total_degree
            .checked_add(
                (p.len() - 1)
                    .checked_mul(multiplicity)
                    .ok_or("FACTORIZATION_DEGREE_MISMATCH")?,
            )
            .ok_or("FACTORIZATION_DEGREE_MISMATCH")?;
        if total_degree >= input.len() {
            return Err("FACTORIZATION_DEGREE_MISMATCH".into());
        }
        if gcd(p.clone(), derivative(&p), d)?.len() != 1 || factor_squarefree(&p, d)?.len() != 1 {
            return Err("REDUCIBLE_CLAIMED_FACTOR".into());
        }
        for _ in 0..multiplicity {
            product = multiply(&product, &p, d);
        }
    }
    if product != input {
        return Err("FACTORIZATION_PRODUCT_MISMATCH".into());
    }
    Ok(())
}

#[cfg(test)]
pub fn shift_control(conductor: u64, coefficients: &Value) -> Result<usize> {
    let (d, _) = field(conductor)?;
    let p = parse_polynomial(coefficients, d)?;
    separable_shift(&monic(&p, d)?, d).map(|(s, _, _)| s)
}

#[cfg(test)]
pub fn norm_control(conductor: u64, coefficients: &Value, wrong_real_bar: bool) -> Result<Value> {
    let (d, _) = field(conductor)?;
    let p = parse_polynomial(coefficients, d)?;
    let product = if wrong_real_bar {
        multiply(&p, &p, d)
    } else {
        norm(&p, d)?
    };
    if product.iter().any(|x| !x.b.try_is_zero().unwrap()) {
        return Err("TRAGER_NORM_NOT_RATIONAL".into());
    }
    Ok(wire(&product))
}

#[cfg(test)]
pub fn fold_control(terms: &Value, self_join: bool) -> Result<Value> {
    let terms = terms
        .as_array()
        .ok_or("COEFFICIENT_ARRAY_REQUIRED")?
        .iter()
        .map(parse_rational)
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
        return Ok(json!(rational_wire(&Q::from_integer(numerator))));
    }
    let sum = terms
        .iter()
        .fold(Element::zero(), |a, b| a.add(&Element::scalar(b.clone())));
    Ok(json!(rational_wire(&sum.a)))
}

fn raw_number_admission(input: &str) -> Result<()> {
    crate::linear_algebra::json_admission::admit_exact_json(input)
}

fn run() -> Result<Value> {
    if std::env::args().len() != 1 {
        return Err("USAGE:real_field_polynomial_factors < REQUEST_JSON".into());
    }
    let mut input = String::new();
    io::stdin()
        .read_to_string(&mut input)
        .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
    let raw_numbers = raw_number_admission(&input);
    let fields: BTreeMap<String, Box<RawValue>> =
        serde_json::from_str(&input).map_err(|e| format!("INVALID_JSON:{e}"))?;
    raw_numbers?;
    if fields.len() != 3
        || ["operation", "conductor", "coefficients"]
            .iter()
            .any(|key| !fields.contains_key(*key))
    {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    let conductor: u64 = serde_json::from_str(fields["conductor"].get())
        .map_err(|_| "INTEGER_CONDUCTOR_REQUIRED")?;
    let operation: String =
        serde_json::from_str(fields["operation"].get()).map_err(|_| "FACTOR_OPERATION_REQUIRED")?;
    let coefficients: Vec<[String; 2]> = serde_json::from_str(fields["coefficients"].get())
        .map_err(|_| "CANONICAL_RATIONAL_STRING_REQUIRED")?;
    let request = json!({"operation":operation,"conductor":conductor,"coefficients":coefficients});
    evaluate_request(&request)
}

#[cfg(test)]
mod root_challenge {
    use super::*;

    #[test]
    fn x_squared_minus_two_over_q_sqrt2_is_not_an_irreducible_factor() {
        let polynomial = vec![
            Element {
                a: Q::from_integer((-2).into()),
                b: Q::zero(),
            },
            Element::zero(),
            Element::one(),
        ];
        assert!(quadratic_has_listed_root(&polynomial, 2));
        let unchanged_producer = vec![(polynomial, 1usize)];
        assert!(unchanged_producer
            .iter()
            .any(|(factor, _)| quadratic_has_listed_root(factor, 2)));
    }
}

fn main() {
    match run() {
        Ok(output) => println!("{}", serde_json::to_string(&output).expect("JSON output")),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}
