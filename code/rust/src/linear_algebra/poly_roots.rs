// AuthorityEffect: None.
// Exact ordered root identities, not minimal polynomials or splitting degrees.
// Independent Rust arithmetic; shared fixture files supply inputs only.
use super::{
    characteristic, embedding, eval, multiply, qstr, quotient, rat, reject_float, root_count,
    squarefree, sturm, validate, Element, Polynomial, Result, Q,
};
use num_bigint::BigInt;
use num_traits::{One, Zero};
use serde_json::{json, Value};
use std::collections::BTreeSet;

const LIMIT: usize = 4096;
const REPRESENTATION: &str = "ORDERED_REAL_POLYNOMIAL_ROOTS_V1";
const SCOPE: &str = "EXACT_ROOT_IDENTITIES_NO_SPLITTING_DEGREE_OR_DEPENDENCE";

struct AlgebraicData {
    conductor: u64,
    dimension: usize,
    characteristic: Polynomial,
    factors: Vec<(Polynomial, usize)>,
    radical: Polynomial,
}

impl AlgebraicData {
    fn from_input(input: &Value) -> Result<Self> {
        let matrix = validate(input)?;
        let conductor = matrix[0][0].n;
        let characteristic = characteristic(&matrix)?;
        let factors = squarefree(&characteristic)?;
        let radical = factors
            .iter()
            .fold(vec![Element::one(conductor)], |p, (f, _)| multiply(&p, f));
        Ok(Self {
            conductor,
            dimension: matrix.len(),
            characteristic,
            factors,
            radical,
        })
    }

    fn factor_wire(&self) -> Value {
        json!(self
            .factors
            .iter()
            .map(|(p, m)| json!({"polynomial":wire(p),"multiplicity":m}))
            .collect::<Vec<_>>())
    }
}

fn wire(polynomial: &[Element]) -> Value {
    json!(polynomial.iter().map(Element::json).collect::<Vec<_>>())
}

#[derive(Clone)]
struct Root {
    lower: Q,
    upper: Q,
}

// Isolate the radical once, including roots from different Yun factors in the
// same tree. Endpoint roots are removed first and midpoint roots counted once.
// A singleton is rational; an open root identity is not asserted irrational.
fn isolate(radical: &[Element], limit: usize) -> Result<(Vec<Root>, usize)> {
    let n = radical[0].n;
    let mut interior = radical.to_vec();
    let mut roots = Vec::new();
    for endpoint in [Q::zero(), Q::one()] {
        if interior.len() > 1 && eval(&interior, &endpoint).is_zero() {
            interior = quotient(
                &interior,
                &[Element::one(n), Element::rational(n, -&endpoint)],
            )?;
            roots.push(Root {
                lower: endpoint.clone(),
                upper: endpoint,
            });
        }
    }
    let mut used = 0;
    if interior.len() > 1 {
        let sequence = sturm(&interior)?;
        let total = root_count(&sequence, &Q::zero(), &Q::one())?;
        if total != interior.len() - 1 {
            return Err("SPECTRAL_ROOT_REAL_CENSUS_FAILED".into());
        }
        let mut pending = vec![(Q::zero(), Q::one(), total)];
        while let Some((lower, upper, count)) = pending.pop() {
            if count == 0 {
                continue;
            }
            if count == 1 && lower > Q::zero() {
                roots.push(Root { lower, upper });
                continue;
            }
            if used >= limit {
                return Err(format!("REFUSED_IMPLEMENTATION_RESOURCE_LIMIT:spectral_root_sturm_subdivisions:{used}/{limit}"));
            }
            used += 1;
            let midpoint = (&lower + &upper) / rat(2, 1);
            let exact = eval(&interior, &midpoint).is_zero();
            let left = root_count(&sequence, &lower, &midpoint)?;
            let right = root_count(&sequence, &midpoint, &upper)?;
            if left + right + usize::from(exact) != count {
                return Err("SPECTRAL_ROOT_SUBDIVISION_CENSUS_FAILED".into());
            }
            if exact {
                roots.push(Root {
                    lower: midpoint.clone(),
                    upper: midpoint.clone(),
                });
            }
            if right > 0 {
                pending.push((midpoint.clone(), upper, right));
            }
            if left > 0 {
                pending.push((lower, midpoint, left));
            }
        }
    }
    roots.sort_by(|a, b| (&a.lower, &a.upper).cmp(&(&b.lower, &b.upper)));
    if roots.len() != radical.len() - 1 {
        return Err("SPECTRAL_ROOT_DISTINCT_CENSUS_FAILED".into());
    }
    Ok((roots, used))
}

fn multiplicity(root: &Root, factors: &[(Polynomial, usize)]) -> Result<usize> {
    let mut found = None;
    for (factor, m) in factors {
        let count = if root.lower == root.upper {
            usize::from(eval(factor, &root.lower).is_zero())
        } else {
            root_count(&sturm(factor)?, &root.lower, &root.upper)?
        };
        if count > 1 || (count == 1 && found.is_some()) {
            return Err("SPECTRAL_ROOT_FACTOR_ASSIGNMENT_AMBIGUOUS".into());
        }
        if count == 1 {
            found = Some(*m);
        }
    }
    found.ok_or_else(|| "SPECTRAL_ROOT_FACTOR_ASSIGNMENT_MISSING".into())
}

fn output_with_limit(input: &Value, limit: usize) -> Result<Value> {
    let data = AlgebraicData::from_input(input)?;
    let (roots, used) = isolate(&data.radical, limit)?;
    let mut spectrum = Vec::new();
    let mut weighted = 0;
    for root in roots {
        let m = multiplicity(&root, &data.factors)?;
        weighted += m;
        let singleton = root.lower == root.upper;
        spectrum.push(json!({
            "kind":if singleton {"EXACT_RATIONAL_ROOT"} else {"EXACT_REAL_ALGEBRAIC_ROOT"},
            "defining_polynomial":wire(&data.radical),
            "lower":qstr(&root.lower),"upper":qstr(&root.upper),
            "endpoint_convention":if singleton {"SINGLETON"} else {"OPEN"},
            "distinct_root_count":1,"multiplicity":m
        }));
    }
    if weighted != data.dimension {
        return Err("SPECTRAL_ROOT_WEIGHTED_CENSUS_FAILED".into());
    }
    Ok(json!({
        "representation":REPRESENTATION,"carrier_conductor":data.conductor,
        "embedding":embedding(data.conductor)?,"characteristic_polynomial":wire(&data.characteristic),
        "squarefree_factors":data.factor_wire(),"squarefree_radical":wire(&data.radical),
        "spectrum":spectrum,"resource":{"kind":"IMPLEMENTATION_RESOURCE_LIMIT",
        "sturm_subdivisions":used,"sturm_subdivision_limit":LIMIT},"scope":SCOPE
    }))
}

pub fn output(input: &Value) -> Result<Value> {
    output_with_limit(input, LIMIT)
}

fn keys(value: &Value, names: &[&str], path: &str) -> Result<()> {
    let object = value
        .as_object()
        .ok_or_else(|| format!("SPECTRAL_OBJECT_REQUIRED:{path}"))?;
    if object.len() != names.len() || names.iter().any(|name| !object.contains_key(*name)) {
        return Err(format!("SPECTRAL_FIELDS_MISMATCH:{path}"));
    }
    Ok(())
}

fn equal(actual: &Value, expected: &Value, path: &str) -> Result<()> {
    if actual != expected {
        return Err(format!("SPECTRAL_VALUE_MISMATCH:{path}"));
    }
    Ok(())
}

fn count(value: &Value, path: &str) -> Result<usize> {
    value
        .as_u64()
        .and_then(|x| usize::try_from(x).ok())
        .ok_or_else(|| format!("SPECTRAL_UNSIGNED_INTEGER_REQUIRED:{path}"))
}

// This parses certificate arithmetic, NOT original matrix entries. Derived
// endpoints may exceed the input height limit; canonical rational form remains
// mandatory and floats/booleans are never lifted into the exact domain.
fn rational(value: &Value, path: &str) -> Result<Q> {
    let text = value
        .as_str()
        .ok_or_else(|| format!("SPECTRAL_RATIONAL_STRING_REQUIRED:{path}"))?;
    let (numerator, denominator) = text
        .split_once('/')
        .ok_or_else(|| format!("SPECTRAL_RATIONAL_FORMAT:{path}"))?;
    let n: BigInt = numerator
        .parse()
        .map_err(|_| format!("SPECTRAL_RATIONAL_FORMAT:{path}"))?;
    let d: BigInt = denominator
        .parse()
        .map_err(|_| format!("SPECTRAL_RATIONAL_FORMAT:{path}"))?;
    if d <= BigInt::zero() {
        return Err(format!("SPECTRAL_RATIONAL_DENOMINATOR:{path}"));
    }
    let q = Q::new(n, d);
    if qstr(&q) != text {
        return Err(format!("SPECTRAL_RATIONAL_NOT_REDUCED:{path}"));
    }
    Ok(q)
}

// This validator does not compare the supplied spectrum with output(input).
// It independently checks each proposed identity by exact evaluation/Sturm,
// polynomial binding, factor assignment, disjointness and complete census.
// Only the actual work counter is replayed using the declared deterministic
// producer traversal; arbitrary valid alternative rational isolators can pass.
pub fn verify_output(input: &Value, proposed: &Value) -> Result<()> {
    reject_float(proposed, "spectral_output")?;
    let data = AlgebraicData::from_input(input)?;
    keys(
        proposed,
        &[
            "representation",
            "carrier_conductor",
            "embedding",
            "characteristic_polynomial",
            "squarefree_factors",
            "squarefree_radical",
            "spectrum",
            "resource",
            "scope",
        ],
        "output",
    )?;
    equal(
        &proposed["representation"],
        &json!(REPRESENTATION),
        "representation",
    )?;
    equal(&proposed["scope"], &json!(SCOPE), "scope")?;
    equal(
        &proposed["carrier_conductor"],
        &json!(data.conductor),
        "carrier_conductor",
    )?;
    equal(
        &proposed["embedding"],
        &embedding(data.conductor)?,
        "embedding",
    )?;
    equal(
        &proposed["characteristic_polynomial"],
        &wire(&data.characteristic),
        "characteristic_polynomial",
    )?;
    equal(
        &proposed["squarefree_factors"],
        &data.factor_wire(),
        "squarefree_factors",
    )?;
    equal(
        &proposed["squarefree_radical"],
        &wire(&data.radical),
        "squarefree_radical",
    )?;
    let records = proposed["spectrum"]
        .as_array()
        .ok_or("SPECTRAL_ARRAY_REQUIRED:spectrum")?;
    if records.len() != data.radical.len() - 1 {
        return Err("SPECTRAL_ROOT_DISTINCT_CENSUS_FAILED".into());
    }
    let sequence = sturm(&data.radical)?;
    let mut weighted = 0;
    let mut previous: Option<Root> = None;
    for record in records {
        keys(
            record,
            &[
                "kind",
                "defining_polynomial",
                "lower",
                "upper",
                "endpoint_convention",
                "distinct_root_count",
                "multiplicity",
            ],
            "spectrum_row",
        )?;
        equal(
            &record["defining_polynomial"],
            &wire(&data.radical),
            "defining_polynomial",
        )?;
        if count(&record["distinct_root_count"], "distinct_root_count")? != 1 {
            return Err("SPECTRAL_ROOT_COUNT_MUST_BE_ONE".into());
        }
        let root = Root {
            lower: rational(&record["lower"], "lower")?,
            upper: rational(&record["upper"], "upper")?,
        };
        if root.lower < Q::zero() || root.upper > Q::one() || root.lower > root.upper {
            return Err("SPECTRAL_ROOT_ENDPOINT_DOMAIN".into());
        }
        let singleton = root.lower == root.upper;
        if singleton {
            equal(&record["kind"], &json!("EXACT_RATIONAL_ROOT"), "root_kind")?;
            equal(
                &record["endpoint_convention"],
                &json!("SINGLETON"),
                "endpoint_convention",
            )?;
            if !eval(&data.radical, &root.lower).is_zero() {
                return Err("SPECTRAL_SINGLETON_NOT_ROOT".into());
            }
        } else {
            equal(
                &record["kind"],
                &json!("EXACT_REAL_ALGEBRAIC_ROOT"),
                "root_kind",
            )?;
            equal(
                &record["endpoint_convention"],
                &json!("OPEN"),
                "endpoint_convention",
            )?;
            if root_count(&sequence, &root.lower, &root.upper)? != 1 {
                return Err("SPECTRAL_OPEN_ROOT_COUNT_NOT_ONE".into());
            }
        }
        if let Some(old) = &previous {
            // Shared endpoints are allowed because open intervals exclude
            // boundaries. Duplicate singleton roots are never allowed.
            if old.upper > root.lower
                || (old.lower == old.upper && singleton && old.lower == root.lower)
            {
                return Err("SPECTRAL_ROOTS_OVERLAP_OR_UNORDERED".into());
            }
        }
        let m = count(&record["multiplicity"], "multiplicity")?;
        if m != multiplicity(&root, &data.factors)? {
            return Err("SPECTRAL_ROOT_MULTIPLICITY_MISMATCH".into());
        }
        weighted += m;
        previous = Some(root);
    }
    if weighted != data.dimension {
        return Err("SPECTRAL_ROOT_WEIGHTED_CENSUS_FAILED".into());
    }
    let resource = &proposed["resource"];
    keys(
        resource,
        &["kind", "sturm_subdivisions", "sturm_subdivision_limit"],
        "resource",
    )?;
    equal(
        &resource["kind"],
        &json!("IMPLEMENTATION_RESOURCE_LIMIT"),
        "resource.kind",
    )?;
    if count(
        &resource["sturm_subdivision_limit"],
        "sturm_subdivision_limit",
    )? != LIMIT
    {
        return Err("SPECTRAL_RESOURCE_LIMIT_MISMATCH".into());
    }
    let claimed = count(&resource["sturm_subdivisions"], "sturm_subdivisions")?;
    if claimed > LIMIT || claimed != isolate(&data.radical, LIMIT)?.1 {
        return Err("SPECTRAL_RESOURCE_USAGE_MISMATCH".into());
    }
    Ok(())
}

fn fixtures(interface: &Value) -> Result<&Vec<Value>> {
    reject_float(interface, "interface")?;
    let fixtures = interface["fixtures"]
        .as_array()
        .ok_or("FIXTURES_REQUIRED")?;
    if fixtures.is_empty() || fixtures.len() > 64 {
        return Err("REFUSED_AT_BUDGET:fixture_cases_max".into());
    }
    let mut ids = BTreeSet::new();
    for input in fixtures {
        let id = input["fixture_id"].as_str().ok_or("FIXTURE_ID_REQUIRED")?;
        if !ids.insert(id) {
            return Err(format!("DUPLICATE_FIXTURE_ID:{id}"));
        }
    }
    Ok(fixtures)
}

pub fn report(interface: &Value) -> Result<Value> {
    let mut cases = Vec::new();
    for input in fixtures(interface)? {
        cases.push(json!({"input":input,"output":output(input)?}));
    }
    Ok(json!({"authority_effect":"None","schema":"ordered_real_polynomial_roots_v1","cases":cases}))
}

pub fn verify_report(interface: &Value, proposed: &Value) -> Result<()> {
    reject_float(proposed, "spectral_report")?;
    let inputs = fixtures(interface)?;
    keys(proposed, &["authority_effect", "schema", "cases"], "report")?;
    equal(
        &proposed["authority_effect"],
        &json!("None"),
        "authority_effect",
    )?;
    equal(
        &proposed["schema"],
        &json!("ordered_real_polynomial_roots_v1"),
        "schema",
    )?;
    let cases = proposed["cases"]
        .as_array()
        .ok_or("SPECTRAL_ARRAY_REQUIRED:cases")?;
    if cases.len() != inputs.len() {
        return Err("SPECTRAL_REPORT_CENSUS_MISMATCH".into());
    }
    for (input, case) in inputs.iter().zip(cases) {
        keys(case, &["input", "output"], "case")?;
        equal(&case["input"], input, "typed_input")?;
        verify_output(input, &case["output"])?;
    }
    Ok(())
}

#[cfg(test)]
pub fn test_lowered_limit(input: &Value, limit: usize) -> Result<Value> {
    if limit >= LIMIT {
        return Err("TEST_LIMIT_MUST_BE_STRICTLY_LOWER_THAN_PRODUCTION".into());
    }
    output_with_limit(input, limit)
}
