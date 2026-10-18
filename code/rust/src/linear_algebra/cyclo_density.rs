use super::{
    cluster_entropy_interval, entropy_verdict, parse_q, qstr, rat, reject_float, ClusterBounds,
    Result, Q,
};
use num_traits::{One, Signed, Zero};
use serde_json::{json, Value};
use std::cmp::Ordering;
use std::collections::BTreeSet;

#[path = "poly_roots.rs"]
pub mod polynomial_roots;
#[path = "spectral_factors.rs"]
pub mod spectral_factor_binding;

fn modulus(n: u64) -> Result<Vec<Q>> {
    let integers = match n {
        1 => vec![-1, 1],
        3 => vec![1, 1, 1],
        4 => vec![1, 0, 1],
        5 => vec![1, 1, 1, 1, 1],
        8 => vec![1, 0, 0, 0, 1],
        _ => return Err("CYCLOTOMIC_CONDUCTOR_UNSUPPORTED".into()),
    };
    Ok(integers.into_iter().map(|x| rat(x, 1)).collect())
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct Element {
    n: u64,
    c: Vec<Q>,
}

impl Element {
    pub(crate) fn new(n: u64, c: Vec<Q>) -> Result<Self> {
        if c.len() + 1 != modulus(n)?.len() {
            return Err("CYCLOTOMIC_COEFFICIENT_LENGTH".into());
        }
        Ok(Self { n, c })
    }

    fn rational(n: u64, value: Q) -> Self {
        let mut c = vec![Q::zero(); modulus(n).expect("validated conductor").len() - 1];
        c[0] = value;
        Self { n, c }
    }

    fn zero(n: u64) -> Self {
        Self::rational(n, Q::zero())
    }
    fn one(n: u64) -> Self {
        Self::rational(n, Q::one())
    }
    pub(crate) fn is_zero(&self) -> bool {
        self.c.iter().all(Zero::is_zero)
    }
    pub(crate) fn json(&self) -> Value {
        json!({"cyclotomic_coefficients":self.c.iter().map(qstr).collect::<Vec<_>>()})
    }
    pub(crate) fn add(&self, rhs: &Self) -> Self {
        assert_eq!(self.n, rhs.n, "internal field conductor invariant");
        Self {
            n: self.n,
            c: self.c.iter().zip(&rhs.c).map(|(a, b)| a + b).collect(),
        }
    }
    pub(crate) fn neg(&self) -> Self {
        Self {
            n: self.n,
            c: self.c.iter().map(|q| -q).collect(),
        }
    }
    pub(crate) fn sub(&self, rhs: &Self) -> Self {
        self.add(&rhs.neg())
    }
    fn scale(&self, q: &Q) -> Self {
        Self {
            n: self.n,
            c: self.c.iter().map(|x| x * q).collect(),
        }
    }
    pub(crate) fn mul(&self, rhs: &Self) -> Self {
        assert_eq!(self.n, rhs.n, "internal field conductor invariant");
        let d = self.c.len();
        let phi = modulus(self.n).expect("validated conductor");
        let mut product = vec![Q::zero(); 2 * d - 1];
        for (i, a) in self.c.iter().enumerate() {
            for (j, b) in rhs.c.iter().enumerate() {
                product[i + j] += a * b;
            }
        }
        for k in (d..product.len()).rev() {
            let leading = product[k].clone();
            for j in 0..d {
                product[k - d + j] -= &leading * &phi[j];
            }
        }
        product.truncate(d);
        Self {
            n: self.n,
            c: product,
        }
    }
    pub(crate) fn pow(&self, power: u64) -> Self {
        let mut result = Self::one(self.n);
        let mut base = self.clone();
        let mut remaining = power;
        while remaining != 0 {
            if remaining % 2 == 1 {
                result = result.mul(&base);
            }
            remaining /= 2;
            if remaining != 0 {
                base = base.mul(&base);
            }
        }
        result
    }
    pub(crate) fn conjugate(&self) -> Self {
        if self.n == 1 {
            return self.clone();
        }
        let mut c = vec![Q::zero(); self.c.len()];
        c[1] = Q::one();
        let inverse_zeta = Self { n: self.n, c }.pow(self.n - 1);
        self.c.iter().rev().fold(Self::zero(self.n), |a, q| {
            a.mul(&inverse_zeta).add(&Self::rational(self.n, q.clone()))
        })
    }
    #[allow(clippy::needless_range_loop)]
    pub(crate) fn inverse(&self) -> Result<Self> {
        if self.is_zero() {
            return Err("CYCLOTOMIC_DIVISION_BY_ZERO".into());
        }
        let d = self.c.len();
        let mut rows = vec![vec![Q::zero(); d + 1]; d];
        for col in 0..d {
            let mut basis = Self::zero(self.n);
            basis.c[col] = Q::one();
            let image = self.mul(&basis);
            for row in 0..d {
                rows[row][col] = image.c[row].clone();
            }
        }
        rows[0][d] = Q::one();
        for col in 0..d {
            let pivot = (col..d)
                .find(|&row| !rows[row][col].is_zero())
                .ok_or("CYCLOTOMIC_INVERSE_SINGULAR")?;
            rows.swap(col, pivot);
            let divisor = rows[col][col].clone();
            for entry in &mut rows[col][col..=d] {
                *entry /= &divisor;
            }
            let pivot_row = rows[col].clone();
            for row in 0..d {
                if row == col {
                    continue;
                }
                let scale = rows[row][col].clone();
                for j in col..=d {
                    rows[row][j] -= &scale * &pivot_row[j];
                }
            }
        }
        let inverse = Self {
            n: self.n,
            c: rows.into_iter().map(|row| row[d].clone()).collect(),
        };
        if self.mul(&inverse) != Self::one(self.n) {
            return Err("CYCLOTOMIC_INVERSE_PRODUCT_FAILED".into());
        }
        Ok(inverse)
    }
    fn div(&self, rhs: &Self) -> Result<Self> {
        Ok(self.mul(&rhs.inverse()?))
    }
    pub(crate) fn sign(&self) -> Result<Ordering> {
        if self.conjugate() != *self {
            return Err("REAL_FIELD_ELEMENT_REQUIRED".into());
        }
        let (a, b, d) = match self.n {
            8 => (self.c[0].clone(), self.c[1].clone(), 2),
            5 => (
                &self.c[0] - &self.c[2] / rat(2, 1),
                -&self.c[2] / rat(2, 1),
                5,
            ),
            _ => (self.c[0].clone(), Q::zero(), 0),
        };
        if b.is_zero() {
            return Ok(a.cmp(&Q::zero()));
        }
        if a.is_zero() || a.is_positive() == b.is_positive() {
            return Ok(b.cmp(&Q::zero()));
        }
        let comparison = (&a * &a).cmp(&(rat(d, 1) * &b * &b));
        Ok(if a.is_positive() {
            comparison
        } else {
            comparison.reverse()
        })
    }
}

fn parse_element(n: u64, value: &Value) -> Result<Element> {
    if value.is_string() {
        return Ok(Element::rational(n, parse_q(value)?));
    }
    let object = value
        .as_object()
        .ok_or("CYCLOTOMIC_ENTRY_OBJECT_OR_RATIONAL_REQUIRED")?;
    if object.len() != 1 || !object.contains_key("cyclotomic_coefficients") {
        return Err("CYCLOTOMIC_ENTRY_FIELDS".into());
    }
    let coefficients = object["cyclotomic_coefficients"]
        .as_array()
        .ok_or("CYCLOTOMIC_COEFFICIENT_ARRAY_REQUIRED")?;
    if coefficients.len() + 1 != modulus(n)?.len() {
        return Err("CYCLOTOMIC_COEFFICIENT_LENGTH".into());
    }
    Element::new(n, coefficients.iter().map(parse_q).collect::<Result<_>>()?)
}

type Matrix = Vec<Vec<Element>>;
type Polynomial = Vec<Element>;

pub fn has_coefficient_objects(input: &Value) -> bool {
    input["matrix"].as_array().is_some_and(|rows| {
        rows.iter().any(|row| {
            row.as_array()
                .is_some_and(|entries| entries.iter().any(Value::is_object))
        })
    })
}

fn validate(input: &Value) -> Result<Matrix> {
    reject_float(input, "input")?;
    let fields: BTreeSet<_> = input
        .as_object()
        .ok_or("INPUT_OBJECT_REQUIRED")?
        .keys()
        .map(String::as_str)
        .collect();
    if fields != BTreeSet::from(["fixture_id", "system_id", "conductor", "matrix", "scope"]) {
        return Err("INPUT_FIELDS_DIFFER_FROM_DECLARED_SCHEMA".into());
    }
    if input["fixture_id"].as_str().is_none_or(str::is_empty) {
        return Err("FIXTURE_ID_REQUIRED".into());
    }
    let n = input["conductor"]
        .as_u64()
        .ok_or("CONDUCTOR_INTEGER_REQUIRED")?;
    let system = input["system_id"].as_str().ok_or("SYSTEM_ID_REQUIRED")?;
    let (d, expected_n) = match system {
        "S1" => (2, 4),
        "S2" => (3, 3),
        "S3" => (2, 8),
        "S4" => (4, 8),
        "S5" => (5, 5),
        "S6" => (4, 1),
        "S7" => (3, 1),
        "S8" => (4, 4),
        _ => return Err("SYSTEM_OUTSIDE_FROZEN_CLASS".into()),
    };
    if n != expected_n {
        return Err("SYSTEM_CONDUCTOR_MISMATCH".into());
    }
    let scope = if system == "S8" {
        "S8_DIMENSION_ONLY_PROXY"
    } else {
        "DECLARED_SYSTEM_STATE"
    };
    if input["scope"] != scope {
        return Err("SYSTEM_SCOPE_MISMATCH".into());
    }
    let rows = input["matrix"].as_array().ok_or("MATRIX_ARRAY_REQUIRED")?;
    if rows.is_empty() || rows.len() > 5 {
        return Err("REFUSED_AT_BUDGET:matrix_dimension_max".into());
    }
    if rows.len() != d {
        return Err("SYSTEM_DIMENSION_MISMATCH".into());
    }
    let matrix: Matrix = rows
        .iter()
        .map(|row| {
            let entries = row.as_array().ok_or("MATRIX_ROW_ARRAY_REQUIRED")?;
            if entries.len() != d {
                return Err("MATRIX_NOT_SQUARE".into());
            }
            entries.iter().map(|x| parse_element(n, x)).collect()
        })
        .collect::<Result<_>>()?;
    for (i, row) in matrix.iter().enumerate() {
        for (j, entry) in row.iter().enumerate() {
            if entry != &matrix[j][i].conjugate() {
                return Err("NON_HERMITIAN_MATRIX".into());
            }
        }
    }
    if trace(&matrix) != Element::one(n) {
        return Err("UNNORMALISED_SPECTRUM:trace_is_not_one".into());
    }
    if system == "S6" || system == "S7" {
        for (i, row) in matrix.iter().enumerate() {
            if row.iter().enumerate().any(|(j, x)| i != j && !x.is_zero()) {
                return Err("LADDER_SYSTEM_REQUIRES_DIAGONAL_STATE".into());
            }
        }
    }
    if system == "S6" {
        if matrix[0][0].sign()? != Ordering::Greater {
            return Err("S6_GEOMETRIC_LADDER_REQUIRED".into());
        }
        let ratio = matrix[1][1].div(&matrix[0][0])?;
        if ratio.sign()? != Ordering::Greater
            || ratio.sub(&Element::one(n)).sign()? != Ordering::Less
            || (1..d).any(|i| matrix[i][i] != matrix[i - 1][i - 1].mul(&ratio))
        {
            return Err("S6_GEOMETRIC_LADDER_REQUIRED".into());
        }
    }
    psd(&matrix)?;
    Ok(matrix)
}

fn trace(matrix: &Matrix) -> Element {
    matrix
        .iter()
        .enumerate()
        .fold(Element::zero(matrix[0][0].n), |sum, (i, row)| {
            sum.add(&row[i])
        })
}
fn matmul(a: &Matrix, b: &Matrix) -> Matrix {
    let d = a.len();
    (0..d)
        .map(|i| {
            (0..d)
                .map(|j| {
                    (0..d).fold(Element::zero(a[0][0].n), |sum, k| {
                        sum.add(&a[i][k].mul(&b[k][j]))
                    })
                })
                .collect()
        })
        .collect()
}
fn psd(matrix: &Matrix) -> Result<()> {
    let mut remaining = matrix.clone();
    while !remaining.is_empty() {
        let pivot = &remaining[0][0];
        match pivot.sign()? {
            Ordering::Less => return Err("NEGATIVE_EIGENVALUE:negative_schur_pivot".into()),
            Ordering::Equal => {
                if remaining[0].iter().any(|x| !x.is_zero()) {
                    return Err("NEGATIVE_EIGENVALUE:zero_diagonal_nonzero_row".into());
                }
                remaining = remaining
                    .into_iter()
                    .skip(1)
                    .map(|row| row.into_iter().skip(1).collect())
                    .collect();
            }
            Ordering::Greater => {
                let inverse = pivot.inverse()?;
                remaining = (1..remaining.len())
                    .map(|i| {
                        (1..remaining.len())
                            .map(|j| {
                                remaining[i][j]
                                    .sub(&remaining[i][0].mul(&inverse).mul(&remaining[0][j]))
                            })
                            .collect()
                    })
                    .collect();
            }
        }
    }
    Ok(())
}
fn characteristic(matrix: &Matrix) -> Result<Polynomial> {
    let d = matrix.len();
    let n = matrix[0][0].n;
    let mut b: Matrix = (0..d)
        .map(|i| {
            (0..d)
                .map(|j| Element::rational(n, rat(i64::from(i == j), 1)))
                .collect()
        })
        .collect();
    let mut coefficients = vec![Element::one(n)];
    for k in 1..=d {
        b = matmul(matrix, &b);
        let coefficient = trace(&b).scale(&rat(-1, k as i64));
        if coefficient.conjugate() != coefficient {
            return Err("CHARACTERISTIC_NOT_REAL".into());
        }
        for (i, row) in b.iter_mut().enumerate() {
            row[i] = row[i].add(&coefficient);
        }
        coefficients.push(coefficient);
    }
    if b.iter().flatten().any(|x| !x.is_zero()) {
        return Err("CAYLEY_HAMILTON_REMAINDER_NONZERO".into());
    }
    Ok(coefficients)
}

pub fn embedding(n: u64) -> Result<Value> {
    modulus(n)?;
    let (radicand, interval) = match n {
        8 => (2, vec!["7/5", "3/2"]),
        5 => (5, vec!["11/5", "12/5"]),
        _ => (0, vec!["1/1", "1/1"]),
    };
    Ok(
        json!({"real_generator_radicand":radicand,"real_generator_interval":interval,
        "complex_conjugation":"zeta_to_zeta_inverse"}),
    )
}
pub fn general_verdict(input: &Value) -> Result<Value> {
    let matrix = validate(input)?;
    Ok(entropy_verdict(
        trace(&matmul(&matrix, &matrix)) == Element::one(matrix[0][0].n),
    ))
}
pub fn characteristic_output(input: &Value) -> Result<Value> {
    let matrix = validate(input)?;
    let n = matrix[0][0].n;
    let power_sum = trace(&matmul(&matrix, &matrix));
    let pure = power_sum == Element::one(n);
    Ok(
        json!({"characteristic_polynomial":characteristic(&matrix)?.iter().map(Element::json).collect::<Vec<_>>(),
        "renyi2_power_sum":power_sum.json(),"purity":if pure {"PURE"} else {"MIXED"},
        "entropy":entropy_verdict(pure),"embedding":embedding(n)?,
        "spectrum_scope":"CHARACTERISTIC_ONLY_NO_SPLITTING_OR_DEPENDENCE"}),
    )
}
pub fn characteristic_report(interface: &Value) -> Result<Value> {
    reject_float(interface, "interface")?;
    let fixtures = interface["fixtures"]
        .as_array()
        .ok_or("FIXTURES_REQUIRED")?;
    if fixtures.is_empty() || fixtures.len() > 64 {
        return Err("REFUSED_AT_BUDGET:fixture_cases_max".into());
    }
    let mut ids = BTreeSet::new();
    let mut cases = Vec::new();
    for input in fixtures {
        let id = input["fixture_id"].as_str().ok_or("FIXTURE_ID_REQUIRED")?;
        if !ids.insert(id) {
            return Err(format!("DUPLICATE_FIXTURE_ID:{id}"));
        }
        cases.push(json!({"input":input,"output":characteristic_output(input)?}));
    }
    Ok(json!({"schema":"cyclotomic_density_v1","authority_effect":"None","cases":cases}))
}

fn trim(mut p: Polynomial) -> Polynomial {
    let leading = p.iter().position(|x| !x.is_zero()).unwrap_or(p.len() - 1);
    p.drain(..leading);
    p
}
fn eval(p: &[Element], x: &Q) -> Element {
    p.iter().fold(Element::zero(p[0].n), |value, coefficient| {
        value.scale(x).add(coefficient)
    })
}
fn multiply(a: &[Element], b: &[Element]) -> Polynomial {
    let mut result = vec![Element::zero(a[0].n); a.len() + b.len() - 1];
    for (i, x) in a.iter().enumerate() {
        for (j, y) in b.iter().enumerate() {
            result[i + j] = result[i + j].add(&x.mul(y));
        }
    }
    result
}
fn divide(a: &[Element], b: &[Element]) -> Result<(Polynomial, Polynomial)> {
    if b.iter().all(Element::is_zero) {
        return Err("POLYNOMIAL_DIVISION_BY_ZERO".into());
    }
    let mut remainder = trim(a.to_vec());
    if remainder.len() < b.len() {
        return Ok((vec![Element::zero(a[0].n)], remainder));
    }
    let degree = remainder.len() - b.len();
    let mut quotient = vec![Element::zero(a[0].n); degree + 1];
    let inverse = b[0].inverse()?;
    while remainder.len() >= b.len() && remainder.iter().any(|x| !x.is_zero()) {
        let offset = degree - (remainder.len() - b.len());
        let coefficient = remainder[0].mul(&inverse);
        quotient[offset] = quotient[offset].add(&coefficient);
        for (target, source) in remainder.iter_mut().zip(b) {
            *target = target.sub(&coefficient.mul(source));
        }
        remainder = trim(remainder);
    }
    Ok((trim(quotient), remainder))
}
fn quotient(a: &[Element], b: &[Element]) -> Result<Polynomial> {
    let (q, r) = divide(a, b)?;
    if r.iter().any(|x| !x.is_zero()) {
        return Err("POLYNOMIAL_DIVISIBILITY_CERTIFICATE_FAILED".into());
    }
    Ok(q)
}
fn derivative(p: &[Element]) -> Polynomial {
    if p.len() == 1 {
        return vec![Element::zero(p[0].n)];
    }
    p.iter()
        .take(p.len() - 1)
        .enumerate()
        .map(|(i, x)| x.scale(&rat((p.len() - i - 1) as i64, 1)))
        .collect()
}
fn polynomial_gcd(a: &[Element], b: &[Element]) -> Result<Polynomial> {
    let (mut left, mut right) = (trim(a.to_vec()), trim(b.to_vec()));
    while right.iter().any(|x| !x.is_zero()) {
        let (_, remainder) = divide(&left, &right)?;
        left = right;
        right = remainder;
    }
    let inverse = left[0].inverse()?;
    Ok(left.iter().map(|x| x.mul(&inverse)).collect())
}
fn squarefree(p: &[Element]) -> Result<Vec<(Polynomial, usize)>> {
    let mut repeated = polynomial_gcd(p, &derivative(p))?;
    let mut remaining = quotient(p, &repeated)?;
    let mut multiplicity = 1;
    let mut factors = Vec::new();
    while remaining.len() > 1 {
        let common = polynomial_gcd(&remaining, &repeated)?;
        let factor = quotient(&remaining, &common)?;
        if factor.len() > 1 {
            factors.push((factor, multiplicity));
        }
        remaining = common;
        repeated = quotient(&repeated, &remaining)?;
        multiplicity += 1;
        if multiplicity > p.len() {
            return Err("SQUAREFREE_MULTIPLICITY_LOOP_FAILED".into());
        }
    }
    let mut product = vec![Element::one(p[0].n)];
    for (factor, count) in &factors {
        for _ in 0..*count {
            product = multiply(&product, factor);
        }
    }
    if product != p {
        return Err("SQUAREFREE_MULTIPLICITY_PRODUCT_MISMATCH".into());
    }
    Ok(factors)
}
fn sturm(p: &[Element]) -> Result<Vec<Polynomial>> {
    let mut sequence = vec![p.to_vec(), derivative(p)];
    while sequence.last().expect("derivative").len() > 1 {
        let end = sequence.len();
        let (_, remainder) = divide(&sequence[end - 2], &sequence[end - 1])?;
        if remainder.iter().all(Element::is_zero) {
            return Err("STURM_FACTOR_NOT_SQUAREFREE".into());
        }
        let leading_sign = remainder[0].sign()?;
        let absolute = if leading_sign == Ordering::Less {
            remainder[0].neg()
        } else {
            remainder[0].clone()
        };
        let inverse = absolute.inverse()?;
        sequence.push(remainder.iter().map(|x| x.neg().mul(&inverse)).collect());
    }
    Ok(sequence)
}
fn variations(sequence: &[Polynomial], x: &Q) -> Result<usize> {
    let mut previous = None;
    let mut changes = 0;
    for p in sequence {
        let sign = eval(p, x).sign()?;
        if sign == Ordering::Equal {
            continue;
        }
        if previous.is_some_and(|old| old != sign) {
            changes += 1;
        }
        previous = Some(sign);
    }
    Ok(changes)
}
fn root_count(sequence: &[Polynomial], lo: &Q, hi: &Q) -> Result<usize> {
    let count = variations(sequence, lo)? as isize
        - variations(sequence, hi)? as isize
        - isize::from(eval(&sequence[0], hi).is_zero());
    usize::try_from(count).map_err(|_| "STURM_NEGATIVE_ROOT_COUNT".into())
}

struct Root {
    polynomial: Polynomial,
    multiplicity: usize,
    distinct_root_count: usize,
    lo: Q,
    hi: Q,
    entropy_lo: Q,
    entropy_hi: Q,
}
impl Root {
    fn json(&self) -> Value {
        json!({"squarefree_polynomial":self.polynomial.iter().map(Element::json).collect::<Vec<_>>(),
            "multiplicity":self.multiplicity,"lower":qstr(&self.lo),"upper":qstr(&self.hi),
            "kind":if self.lo==self.hi {"EXACT_RATIONAL_ROOT"} else {"STURM_OPEN_SPECTRAL_CLUSTER"},
            "distinct_root_count":self.distinct_root_count,"entropy_lower":qstr(&self.entropy_lo),"entropy_upper":qstr(&self.entropy_hi)})
    }
}
fn isolate(
    p: &[Element],
    bounds: &ClusterBounds,
    limit: usize,
) -> Result<(Vec<Root>, usize, usize)> {
    let n = p[0].n;
    let mut roots = Vec::new();
    let mut used = 0;
    let mut max_terms = 0;
    for (factor, multiplicity) in squarefree(p)? {
        let mut interior = factor.clone();
        for endpoint in [Q::zero(), Q::one()] {
            if interior.len() > 1 && eval(&interior, &endpoint).is_zero() {
                interior = quotient(
                    &interior,
                    &[Element::one(n), Element::rational(n, -&endpoint)],
                )?;
                roots.push(Root {
                    polynomial: factor.clone(),
                    multiplicity,
                    distinct_root_count: 1,
                    lo: endpoint.clone(),
                    hi: endpoint,
                    entropy_lo: Q::zero(),
                    entropy_hi: Q::zero(),
                });
            }
        }
        if interior.len() == 1 {
            continue;
        }
        let sequence = sturm(&interior)?;
        let total = root_count(&sequence, &Q::zero(), &Q::one())?;
        if total != interior.len() - 1 {
            return Err("PSD_SPECTRUM_ROOT_CENSUS_FAILED".into());
        }
        let mut queue = vec![(Q::zero(), Q::one(), total)];
        while let Some((lo, hi, count)) = queue.pop() {
            if count == 0 {
                continue;
            }
            if &hi - &lo <= bounds.delta {
                let (entropy_lo, entropy_hi, terms) = cluster_entropy_interval(&lo, &hi, bounds)?;
                max_terms = max_terms.max(terms);
                roots.push(Root {
                    polynomial: interior.clone(),
                    multiplicity,
                    distinct_root_count: count,
                    lo,
                    hi,
                    entropy_lo,
                    entropy_hi,
                });
                continue;
            }
            if used >= limit {
                return Err(format!(
                    "REFUSED_IMPLEMENTATION_RESOURCE_LIMIT:sturm_subdivisions:{used}/{limit}"
                ));
            }
            if used >= bounds.subdivision_bound {
                return Err("CLUSTER_SUBDIVISION_PROOF_BOUND_FAILED".into());
            }
            used += 1;
            let midpoint = (&lo + &hi) / rat(2, 1);
            let exact = eval(&interior, &midpoint).is_zero();
            let left = root_count(&sequence, &lo, &midpoint)?;
            let right = root_count(&sequence, &midpoint, &hi)?;
            if left + right + usize::from(exact) != count {
                return Err("STURM_SUBDIVISION_ROOT_CENSUS_FAILED".into());
            }
            if exact {
                let (entropy_lo, entropy_hi, terms) =
                    cluster_entropy_interval(&midpoint, &midpoint, bounds)?;
                max_terms = max_terms.max(terms);
                roots.push(Root {
                    polynomial: interior.clone(),
                    multiplicity,
                    distinct_root_count: 1,
                    lo: midpoint.clone(),
                    hi: midpoint.clone(),
                    entropy_lo,
                    entropy_hi,
                });
            }
            if right != 0 {
                queue.push((midpoint.clone(), hi, right));
            }
            if left != 0 {
                queue.push((lo, midpoint, left));
            }
        }
    }
    if roots
        .iter()
        .map(|r| r.multiplicity * r.distinct_root_count)
        .sum::<usize>()
        != p.len() - 1
    {
        return Err("STURM_WEIGHTED_MULTIPLICITY_CENSUS_FAILED".into());
    }
    roots.sort_by(|a, b| (&a.lo, &a.hi).cmp(&(&b.lo, &b.hi)));
    Ok((roots, used, max_terms))
}

pub fn evaluate_external(input: &Value, k: u64) -> Result<Value> {
    if k > 32 {
        return Err("REFUSED_AT_BUDGET:approximation_k_max".into());
    }
    let matrix = validate(input)?;
    if trace(&matmul(&matrix, &matrix)) == Element::one(matrix[0][0].n) {
        return Ok(json!({"entropy":entropy_verdict(true),"approximation":null}));
    }
    let bound = Q::new(1.into(), num_bigint::BigInt::one() << k);
    let bounds = ClusterBounds::new(k, matrix.len())?;
    let (roots, used, max_terms) = isolate(&characteristic(&matrix)?, &bounds, 4096)?;
    let lower = roots.iter().fold(Q::zero(), |sum, r| {
        sum + rat((r.multiplicity * r.distinct_root_count) as i64, 1) * &r.entropy_lo
    });
    let upper = roots.iter().fold(Q::zero(), |sum, r| {
        sum + rat((r.multiplicity * r.distinct_root_count) as i64, 1) * &r.entropy_hi
    });
    let width = &upper - &lower;
    if width < Q::zero() || width > bound {
        return Err("INTERVAL_BOUND_NOT_ESTABLISHED".into());
    }
    Ok(
        json!({"entropy":{"verdict":"EXTERNALLY_INTERFACED","reason":"MIXED_STATE_WITH_RATIONAL_INTERVAL_INTERFACE",
        "anchor":"A1","quantity_type":"APPROXIMATION_NOT_MEMBERSHIP"},"approximation":{
        "authority_effect":"None","quantity_type":"APPROXIMATION_NOT_MEMBERSHIP",
        "metric":"ABSOLUTE_ERROR_IN_REAL_NATURAL_LOG_ENTROPY",
        "method":"CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS_AND_RATIONAL_ATANH_GEOMETRIC_TAIL",
        "root_isolation":"EXACT_CYCLOTOMIC_REAL_STURM_SPECTRAL_CLUSTERS",
        "approximation_algorithm":"DYADIC_STURM_CLUSTERS_WITH_UNIFORM_ENTROPY_MODULUS",
        "spectral_count_convention":"OPEN_BINS_PLUS_EXACT_SINGLETONS",
        "cluster_precision_bits":bounds.bits,"uniform_entropy_radius":qstr(&bounds.radius),
        "sturm_subdivision_proved_bound":bounds.subdivision_bound,
        "log_shift_proved_bound":bounds.bits+1,"series_terms_proved_bound":64,
        "psd_validation":"EXACT_CYCLOTOMIC_HERMITIAN_SCHUR_COMPLEMENT",
        "requested_k":k,"requested_bound":qstr(&bound),"lower":qstr(&lower),"upper":qstr(&upper),
        "interval_width":qstr(&width),"rational_estimate":qstr(&((&lower+&upper)/rat(2,1))),
        "absolute_error_bound":qstr(&(&width/rat(2,1))),"max_series_terms":max_terms,
        "root_isolation_subdivisions":used,
        "root_isolation_resource_limit":{"kind":"IMPLEMENTATION_RESOURCE_LIMIT","unit":"SUBDIVISION","limit":4096},
        "eigenvalue_intervals":roots.iter().map(Root::json).collect::<Vec<_>>()}}),
    )
}

pub fn verify_characteristic(input: &Value, output: &Value) -> Result<()> {
    reject_float(output, "output")?;
    if let Some(path) = super::first_mismatch(&characteristic_output(input)?, output, "output") {
        return Err(format!("CYCLOTOMIC_OUTPUT_MISMATCH:{path}"));
    }
    Ok(())
}

#[cfg(test)]
pub fn test_sturm_limit(input: &Value, k: u64, limit: usize) -> Result<()> {
    if limit >= 4096 {
        return Err("TEST_LIMIT_MUST_BE_STRICTLY_LOWER_THAN_PRODUCTION".into());
    }
    if k > 32 {
        return Err("REFUSED_AT_BUDGET:approximation_k_max".into());
    }
    let matrix = validate(input)?;
    let bounds = ClusterBounds::new(k, matrix.len())?;
    isolate(&characteristic(&matrix)?, &bounds, limit).map(|_| ())
}

#[cfg(test)]
pub fn test_cluster_proof_bound(input: &Value, k: u64) -> Result<()> {
    let matrix = validate(input)?;
    let mut bounds = ClusterBounds::new(k, matrix.len())?;
    bounds.subdivision_bound = 1;
    isolate(&characteristic(&matrix)?, &bounds, 4096).map(|_| ())
}

#[cfg(test)]
pub fn test_negative_remainder_rescaling() -> Result<(usize, usize)> {
    let p = vec![
        Element::one(8),
        Element::rational(8, rat(-1, 1)),
        Element::rational(8, rat(1, 8)),
    ];
    let (_, remainder) = divide(&p, &derivative(&p))?;
    if remainder[0].sign()? != Ordering::Less {
        return Err("NEGATIVE_REMAINDER_CONTROL_FAILED".into());
    }
    let mut sequence = sturm(&p)?;
    let correct = root_count(&sequence, &Q::zero(), &Q::one())?;
    for coefficient in sequence.last_mut().expect("nonempty sequence") {
        *coefficient = coefficient.neg();
    }
    let mutated = root_count(&sequence, &Q::zero(), &Q::one())?;
    Ok((correct, mutated))
}

#[cfg(test)]
mod literal_characteristic {
    use super::*;

    #[test]
    fn a_zero_one_by_one_matrix_has_the_monic_linear_characteristic_polynomial() {
        let matrix = vec![vec![Element::rational(1, rat(0, 1))]];
        assert_eq!(
            characteristic(&matrix).unwrap(),
            vec![Element::one(1), Element::zero(1)]
        );
    }
}
