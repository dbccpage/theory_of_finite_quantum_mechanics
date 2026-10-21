use super::{
    characteristic, embedding, eval, polynomial_roots, qstr, rat, reject_float, root_count, sturm,
    validate, Element, Polynomial, Result, Q,
};
use num_bigint::BigInt;
use num_traits::Zero;
use serde_json::{json, Value};
use std::collections::BTreeSet;

#[allow(dead_code)]
#[path = "field_factors.rs"]
mod factors;

const SCHEMA: &str = "spectral_factor_binding_v1";
const SCOPE: &str = "EXACT_EIGENVALUE_FACTORS_AND_REAL_CARRIER_TRANSPORT_NO_DEGREE_OR_DEPENDENCE";

fn exact_keys(value: &Value, expected: &[&str], label: &str) -> Result<()> {
    let object = value
        .as_object()
        .ok_or_else(|| format!("{label}:OBJECT_REQUIRED"))?;
    let actual = object.keys().map(String::as_str).collect::<BTreeSet<_>>();
    if actual != expected.iter().copied().collect() {
        return Err(format!("{label}:EXACT_FIELDS_REQUIRED"));
    }
    Ok(())
}

fn integer(value: &Value, label: &str) -> Result<usize> {
    value
        .as_u64()
        .and_then(|n| usize::try_from(n).ok())
        .ok_or_else(|| format!("{label}:EXACT_NONNEGATIVE_INTEGER_REQUIRED"))
}

fn rational(value: &Value) -> Result<Q> {
    let text = value
        .as_str()
        .ok_or("BINDING_CANONICAL_RATIONAL_REQUIRED")?;
    let (numerator, denominator) = text
        .split_once('/')
        .ok_or("BINDING_CANONICAL_RATIONAL_REQUIRED")?;
    let numerator = numerator
        .parse::<BigInt>()
        .map_err(|_| "BINDING_CANONICAL_RATIONAL_REQUIRED")?;
    let denominator = denominator
        .parse::<BigInt>()
        .map_err(|_| "BINDING_CANONICAL_RATIONAL_REQUIRED")?;
    if denominator <= BigInt::zero() {
        return Err("BINDING_CANONICAL_RATIONAL_REQUIRED".into());
    }
    let q = Q::new(numerator, denominator);
    if qstr(&q) != text {
        return Err("BINDING_CANONICAL_RATIONAL_REQUIRED".into());
    }
    Ok(q)
}

fn field(n: u64) -> Result<(u64, &'static str)> {
    match n {
        1 | 3 | 4 => Ok((0, "Q")),
        8 => Ok((2, "Q(sqrt(2))")),
        5 => Ok((5, "Q(sqrt(5))")),
        _ => Err("BINDING_CONDUCTOR_UNSUPPORTED".into()),
    }
}

fn from_pair(n: u64, a: Q, b: Q) -> Result<Element> {
    let c = match n {
        1 => {
            if !b.is_zero() {
                return Err("BINDING_NONREAL_FIELD_COORDINATE".into());
            }
            vec![a]
        }
        3 | 4 => {
            if !b.is_zero() {
                return Err("BINDING_NONREAL_FIELD_COORDINATE".into());
            }
            vec![a, Q::zero()]
        }
        8 => vec![a, b.clone(), Q::zero(), -b],
        5 => vec![&a - &b, Q::zero(), -rat(2, 1) * &b, -rat(2, 1) * b],
        _ => return Err("BINDING_CONDUCTOR_UNSUPPORTED".into()),
    };
    Element::new(n, c)
}

fn to_pair(value: &Element) -> Result<Value> {
    if value.conjugate() != *value {
        return Err("BINDING_COEFFICIENT_NOT_SELF_CONJUGATE".into());
    }
    let (a, b) = match value.n {
        1 | 3 | 4 => (value.c[0].clone(), Q::zero()),
        8 => (value.c[0].clone(), value.c[1].clone()),
        5 => (
            &value.c[0] - &value.c[2] / rat(2, 1),
            -&value.c[2] / rat(2, 1),
        ),
        _ => return Err("BINDING_CONDUCTOR_UNSUPPORTED".into()),
    };
    if from_pair(value.n, a.clone(), b.clone())? != *value {
        return Err("BINDING_REAL_COORDINATE_ROUND_TRIP".into());
    }
    Ok(json!([qstr(&a), qstr(&b)]))
}

fn element_from_pair_wire(n: u64, pair_val: &Value) -> Result<Element> {
    let pair = pair_val.as_array().ok_or("BINDING_COORDINATE_PAIR_REQUIRED")?;
    if pair.len() != 2 {
        return Err("BINDING_COORDINATE_PAIR_REQUIRED".into());
    }
    let element = from_pair(n, rational(&pair[0])?, rational(&pair[1])?)?;
    if to_pair(&element)? != json!(pair) {
        return Err("BINDING_REAL_COORDINATE_ROUND_TRIP".into());
    }
    Ok(element)
}

fn polynomial_from_wire(n: u64, wire: &Value) -> Result<Polynomial> {
    let arr = wire.as_array().ok_or("BINDING_POLYNOMIAL_ARRAY_REQUIRED")?;
    arr.iter().map(|p| element_from_pair_wire(n, p)).collect()
}

struct InputData {
    n: u64,
    dimension: usize,
    coefficients: Value,
}

impl InputData {
    fn new(input: &Value) -> Result<Self> {
        let matrix = validate(input)?;
        let coefficients = characteristic(&matrix)?
            .iter()
            .map(to_pair)
            .collect::<Result<Vec<_>>>()?;
        Ok(Self {
            n: matrix[0][0].n,
            dimension: matrix.len(),
            coefficients: json!(coefficients),
        })
    }
}

fn transport(n: u64) -> Value {
    json!({
        "rule":"REAL_SPECTRAL_FIELD_BASE_CHANGE_V1",
        "carrier_degree_over_real_field": if n == 1 { 1 } else { 2 },
        "all_roots_real":true,
        "root_field":"E_ALL_CHARACTERISTIC_ROOTS",
        "degree_identity":"[K(all_roots):K]=[E(all_roots):E]"
    })
}

fn find_root_owner(
    lower: &Q,
    upper: &Q,
    polynomials: &[Polynomial],
    sequences: &[Vec<Polynomial>],
) -> Result<usize> {
    let mut owners = Vec::new();
    for (i, p) in polynomials.iter().enumerate() {
        let count = if lower == upper {
            usize::from(eval(p, lower).is_zero())
        } else {
            root_count(&sequences[i], lower, upper)?
        };
        if count > 1 {
            return Err("BINDING_FACTOR_HAS_MULTIPLE_ROOTS_IN_IDENTITY".into());
        }
        if count == 1 {
            owners.push(i);
        }
    }
    if owners.len() != 1 {
        return Err("BINDING_ROOT_OWNER_NOT_UNIQUE".into());
    }
    Ok(owners[0])
}

fn process_root_assignment(
    root: &Value,
    polynomials: &[Polynomial],
    sequences: &[Vec<Polynomial>],
    multiplicities: &[usize],
) -> Result<(usize, usize)> {
    let lower = rational(&root["lower"])?;
    let upper = rational(&root["upper"])?;
    let factor_index = find_root_owner(&lower, &upper, polynomials, sequences)?;
    let multiplicity = integer(&root["multiplicity"], "root_multiplicity")?;
    if multiplicity != multiplicities[factor_index] {
        return Err("BINDING_OWNER_MULTIPLICITY_MISMATCH".into());
    }
    Ok((factor_index, multiplicity))
}

fn verify_census(
    census: &[usize],
    polynomials: &[Polynomial],
    weighted: usize,
    dimension: usize,
) -> Result<()> {
    for (count, p) in census.iter().zip(polynomials) {
        if *count != p.len() - 1 {
            return Err("BINDING_FACTOR_ROOT_CENSUS_MISMATCH".into());
        }
    }
    if weighted != dimension {
        return Err("BINDING_WEIGHTED_CENSUS_MISMATCH".into());
    }
    Ok(())
}

fn ownership(data: &InputData, factorization: &Value, roots: &Value) -> Result<(Value, Value)> {
    let rows = factorization["factors"]
        .as_array()
        .ok_or("BINDING_FACTORS_ARRAY_REQUIRED")?;
    let polynomials = rows
        .iter()
        .map(|r| polynomial_from_wire(data.n, &r["polynomial"]))
        .collect::<Result<Vec<_>>>()?;
    let sequences = polynomials
        .iter()
        .map(|p| sturm(p))
        .collect::<Result<Vec<_>>>()?;
    let multiplicities = rows
        .iter()
        .map(|r| integer(&r["multiplicity"], "factor_multiplicity"))
        .collect::<Result<Vec<_>>>()?;
    let mut census = vec![0usize; rows.len()];
    let mut assignments = Vec::new();
    let mut weighted = 0usize;
    let spectrum = roots["spectrum"]
        .as_array()
        .ok_or("BINDING_SPECTRUM_ARRAY_REQUIRED")?;
    for (root_index, root) in spectrum.iter().enumerate() {
        let (factor_index, multiplicity) = process_root_assignment(
            root,
            &polynomials,
            &sequences,
            &multiplicities,
        )?;
        census[factor_index] += 1;
        weighted = weighted
            .checked_add(multiplicity)
            .ok_or("BINDING_WEIGHTED_CENSUS_OVERFLOW")?;
        assignments.push(json!({
            "root_index": root_index,
            "factor_index": factor_index,
            "multiplicity": multiplicity,
        }));
    }
    verify_census(&census, &polynomials, weighted, data.dimension)?;
    Ok((json!(assignments), json!(census)))
}

pub fn bind_spectral_factors(input: &Value) -> Result<Value> {
    let data = InputData::new(input)?;
    let (radicand, coefficient_field) = field(data.n)?;
    let factorization = factors::evaluate_request(
        &json!({"operation":"factor","conductor":data.n,"coefficients":data.coefficients}),
    )?;
    factors::validate_factorization(data.n, &data.coefficients, &factorization)?;
    let root_certificate = polynomial_roots::output(input)?;
    polynomial_roots::verify_output(input, &root_certificate)?;
    let (root_assignments, factor_root_counts) =
        ownership(&data, &factorization, &root_certificate)?;
    Ok(json!({
        "schema":SCHEMA,"authority_effect":"None","scope":SCOPE,"input":input,
        "carrier_conductor":data.n,"embedding":embedding(data.n)?,
        "coefficient_field":coefficient_field,"real_generator_radicand":radicand,
        "characteristic_polynomial":data.coefficients,"factorization":factorization,
        "root_certificate":root_certificate,"root_assignments":root_assignments,
        "factor_root_counts":factor_root_counts,"carrier_transport":transport(data.n)
    }))
}

const BINDING_KEYS: [&str; 14] = [
    "schema",
    "authority_effect",
    "scope",
    "input",
    "carrier_conductor",
    "embedding",
    "coefficient_field",
    "real_generator_radicand",
    "characteristic_polynomial",
    "factorization",
    "root_certificate",
    "root_assignments",
    "factor_root_counts",
    "carrier_transport",
];

fn validate_metadata(input: &Value, cert: &Value) -> Result<()> {
    if cert["schema"] != SCHEMA
        || cert["authority_effect"] != "None"
        || cert["scope"] != SCOPE
    {
        return Err("BINDING_SCOPE_OR_SCHEMA_MISMATCH".into());
    }
    if cert["input"] != *input {
        return Err("BINDING_TYPED_INPUT_MISMATCH".into());
    }
    Ok(())
}

fn validate_field_and_poly(data: &InputData, cert: &Value) -> Result<()> {
    let (radicand, coefficient_field) = field(data.n)?;
    if cert["carrier_conductor"].as_u64() != Some(data.n)
        || cert["real_generator_radicand"].as_u64() != Some(radicand)
        || cert["coefficient_field"] != coefficient_field
        || cert["embedding"] != embedding(data.n)?
    {
        return Err("BINDING_FIELD_OR_EMBEDDING_MISMATCH".into());
    }
    if cert["characteristic_polynomial"] != data.coefficients {
        return Err("BINDING_CHARACTERISTIC_COORDINATE_MISMATCH".into());
    }
    Ok(())
}

fn validate_root_assignments(cert: &Value, expected: &Value) -> Result<()> {
    let supplied = cert["root_assignments"]
        .as_array()
        .ok_or("BINDING_ASSIGNMENTS_ARRAY_REQUIRED")?;
    let actual = expected.as_array().expect("constructed array");
    if supplied.len() != actual.len() {
        return Err("BINDING_ASSIGNMENT_CENSUS_MISMATCH".into());
    }
    for (row, exp) in supplied.iter().zip(actual) {
        exact_keys(
            row,
            &["root_index", "factor_index", "multiplicity"],
            "assignment",
        )?;
        for key in ["root_index", "factor_index", "multiplicity"] {
            if integer(&row[key], key)? != integer(&exp[key], key)? {
                return Err(format!("BINDING_ASSIGNMENT_MISMATCH:{key}"));
            }
        }
    }
    Ok(())
}

fn validate_factor_root_counts(cert: &Value, expected: &Value) -> Result<()> {
    let supplied = cert["factor_root_counts"]
        .as_array()
        .ok_or("BINDING_FACTOR_COUNTS_ARRAY_REQUIRED")?;
    let exp_arr = expected.as_array().expect("constructed array");
    if supplied.len() != exp_arr.len() {
        return Err("BINDING_FACTOR_COUNT_LENGTH_MISMATCH".into());
    }
    for (count, correct) in supplied.iter().zip(exp_arr) {
        if integer(count, "factor_root_count")? != integer(correct, "factor_root_count")? {
            return Err("BINDING_FACTOR_ROOT_CENSUS_MISMATCH".into());
        }
    }
    Ok(())
}

fn validate_carrier_transport(n: u64, cert: &Value) -> Result<()> {
    exact_keys(
        &cert["carrier_transport"],
        &[
            "rule",
            "carrier_degree_over_real_field",
            "all_roots_real",
            "root_field",
            "degree_identity",
        ],
        "carrier_transport",
    )?;
    if cert["carrier_transport"] != transport(n) {
        return Err("BINDING_CARRIER_TRANSPORT_MISMATCH".into());
    }
    Ok(())
}

fn validate_post_ownership(
    certificate: &Value,
    assignments: &Value,
    census: &Value,
    conductor: u64,
) -> Result<()> {
    validate_root_assignments(certificate, assignments)?;
    validate_factor_root_counts(certificate, census)?;
    validate_carrier_transport(conductor, certificate)
}

pub fn validate_spectral_factor_binding(input: &Value, certificate: &Value) -> Result<()> {
    let data = InputData::new(input)?;
    reject_float(certificate, "spectral_factor_binding")?;
    exact_keys(certificate, &BINDING_KEYS, "binding")?;
    validate_metadata(input, certificate)?;
    validate_field_and_poly(&data, certificate)?;
    factors::validate_factorization(data.n, &data.coefficients, &certificate["factorization"])?;
    polynomial_roots::verify_output(input, &certificate["root_certificate"])?;
    let (assignments, census) = ownership(
        &data,
        &certificate["factorization"],
        &certificate["root_certificate"],
    )?;
    validate_post_ownership(certificate, &assignments, &census, data.n)
}

pub fn evaluate_request(request: &Value) -> Result<Value> {
    reject_float(request, "binding_request")?;
    exact_keys(request, &["operation", "input"], "request")?;
    if request["operation"] != "bind_spectral_factors" {
        return Err("BINDING_OPERATION_REQUIRED".into());
    }
    bind_spectral_factors(&request["input"])
}

#[cfg(test)]
pub fn coordinate_control(n: u64, coefficients: Vec<Q>) -> Result<Value> {
    to_pair(&Element::new(n, coefficients)?)
}

#[cfg(test)]
pub fn closed_right_control(
    input: &Value,
    certificate: &Value,
    root_index: usize,
) -> Result<Vec<usize>> {
    let data = InputData::new(input)?;
    let row = &certificate["root_certificate"]["spectrum"][root_index];
    let lower = rational(&row["lower"])?;
    let upper = rational(&row["upper"])?;
    certificate["factorization"]["factors"]
        .as_array()
        .ok_or("BINDING_FACTORS_ARRAY_REQUIRED")?
        .iter()
        .map(|factor| {
            let p = polynomial_from_wire(data.n, &factor["polynomial"])?;
            Ok(root_count(&sturm(&p)?, &lower, &upper)? + usize::from(eval(&p, &upper).is_zero()))
        })
        .collect()
}
