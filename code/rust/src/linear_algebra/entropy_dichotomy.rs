// AuthorityEffect: None.
// C750-T565: independent exact arithmetic; no Python output is consumed.
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, ToPrimitive, Zero};
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::io::{self, Read};

#[path = "cyclo_density.rs"]
pub mod cyclotomic_density;

type Q = BigRational;
type Matrix = Vec<Vec<Q>>;
type Result<T> = std::result::Result<T, String>;

fn rat(n: i64, d: i64) -> Q {
    Q::new(n.into(), d.into())
}

fn qstr(q: &Q) -> String {
    format!("{}/{}", q.numer(), q.denom())
}

fn parse_q(v: &Value) -> Result<Q> {
    let s = v.as_str().ok_or("RATIONAL_STRING_REQUIRED")?;
    let (n, d) = s.split_once('/').ok_or("RATIONAL_A_OVER_B_REQUIRED")?;
    let n: BigInt = n.parse().map_err(|_| "RATIONAL_NUMERATOR_INVALID")?;
    let d: BigInt = d.parse().map_err(|_| "RATIONAL_DENOMINATOR_INVALID")?;
    if d <= BigInt::zero() {
        return Err("RATIONAL_DENOMINATOR_NONPOSITIVE".into());
    }
    if n.abs() > BigInt::from(4096) || d > BigInt::from(4096) {
        return Err("REFUSED_AT_BUDGET:rational_input_bound".into());
    }
    let q = Q::new(n, d);
    if qstr(&q) != s {
        return Err("RATIONAL_NOT_REDUCED".into());
    }
    Ok(q)
}

fn reject_float(v: &Value, path: &str) -> Result<()> {
    match v {
        Value::Number(n) if n.is_f64() || n.to_string().contains(['.', 'e', 'E']) => {
            Err(format!("FLOAT_LEAKAGE:{path}"))
        }
        Value::Array(a) => {
            for (i, x) in a.iter().enumerate() {
                reject_float(x, &format!("{path}[{i}]"))?;
            }
            Ok(())
        }
        Value::Object(o) => {
            for (k, x) in o {
                reject_float(x, &format!("{path}.{k}"))?;
            }
            Ok(())
        }
        _ => Ok(()),
    }
}

fn matrix(v: &Value) -> Result<Matrix> {
    let rows = v.as_array().ok_or("MATRIX_ARRAY_REQUIRED")?;
    let d = rows.len();
    if d == 0 || d > 5 {
        return Err("REFUSED_AT_BUDGET:matrix_dimension_max".into());
    }
    let a: Matrix = rows
        .iter()
        .map(|row| {
            let row = row.as_array().ok_or("MATRIX_ROW_ARRAY_REQUIRED")?;
            if row.len() != d {
                return Err("MATRIX_NOT_SQUARE".into());
            }
            row.iter().map(parse_q).collect()
        })
        .collect::<Result<_>>()?;
    for (i, row) in a.iter().enumerate() {
        for (j, entry) in row.iter().enumerate() {
            if entry != &a[j][i] {
                return Err("UNSUPPORTED_NON_REAL_SYMMETRIC_MATRIX".into());
            }
        }
    }
    if (0..d).map(|i| a[i][i].clone()).sum::<Q>() != Q::one() {
        return Err("UNNORMALISED_SPECTRUM:trace_is_not_one".into());
    }
    Ok(a)
}

fn matmul(a: &Matrix, b: &Matrix) -> Matrix {
    let d = a.len();
    (0..d)
        .map(|i| {
            (0..d)
                .map(|j| (0..d).map(|k| &a[i][k] * &b[k][j]).sum())
                .collect()
        })
        .collect()
}

// Congruence by an exact rational block elimination preserves positivity.
// A zero diagonal of a PSD matrix has an identically zero row; otherwise its
// 2x2 principal minor is negative. Positive pivots reduce to their Schur block.
fn validate_psd(a: &Matrix) -> Result<()> {
    let mut block = a.clone();
    while !block.is_empty() {
        let pivot = block[0][0].clone();
        if pivot < Q::zero() {
            return Err("NEGATIVE_EIGENVALUE:negative_schur_pivot".into());
        }
        if pivot.is_zero() {
            if block[0].iter().any(|q| !q.is_zero()) {
                return Err("NEGATIVE_EIGENVALUE:zero_diagonal_nonzero_row".into());
            }
            block = block.iter().skip(1).map(|r| r[1..].to_vec()).collect();
        } else {
            block = (1..block.len())
                .map(|i| {
                    (1..block.len())
                        .map(|j| &block[i][j] - &block[i][0] * &block[0][j] / &pivot)
                        .collect()
                })
                .collect();
        }
    }
    Ok(())
}

fn power_sum_two(a: &Matrix) -> Q {
    // Symmetry was checked at admission, so Tr(A^2)=sum_ij A_ij^2.
    a.iter().flatten().map(|q| q * q).sum()
}

// Faddeev-LeVerrier over Q, returning descending monic coefficients.
fn characteristic(a: &Matrix) -> Vec<Q> {
    let d = a.len();
    let mut b: Matrix = (0..d)
        .map(|i| (0..d).map(|j| rat(i64::from(i == j), 1)).collect())
        .collect();
    let mut coefficients = vec![Q::one()];
    for k in 1..=d {
        let mut ab = matmul(a, &b);
        let c = -(0..d).map(|i| ab[i][i].clone()).sum::<Q>() / rat(k as i64, 1);
        coefficients.push(c.clone());
        for (i, row) in ab.iter_mut().enumerate() {
            row[i] += &c;
        }
        b = ab;
    }
    coefficients
}

fn poly_mul(a: &[Q], b: &[Q]) -> Vec<Q> {
    let mut c = vec![Q::zero(); a.len() + b.len() - 1];
    for (i, x) in a.iter().enumerate() {
        for (j, y) in b.iter().enumerate() {
            c[i + j] += x * y;
        }
    }
    c
}

fn poly_trim(mut p: Vec<Q>) -> Vec<Q> {
    let leading = p
        .iter()
        .position(|x| !x.is_zero())
        .unwrap_or(p.len().saturating_sub(1));
    p.drain(..leading);
    p
}

fn poly_eval(p: &[Q], x: &Q) -> Q {
    p.iter()
        .fold(Q::zero(), |value, coefficient| value * x + coefficient)
}

fn synthetic_divide(p: &[Q], root: &Q) -> Result<Vec<Q>> {
    let mut quotient = vec![p[0].clone()];
    for coefficient in &p[1..p.len() - 1] {
        quotient.push(coefficient + root * quotient.last().expect("nonempty quotient"));
    }
    if p.last().expect("polynomial constant") + root * quotient.last().expect("quotient constant")
        != Q::zero()
    {
        return Err("RATIONAL_ROOT_CERTIFICATE_FAILED".into());
    }
    Ok(quotient)
}

fn primitive_integer_coefficients(p: &[Q]) -> Vec<BigInt> {
    let denominator = p.iter().fold(BigInt::one(), |lcm, q| {
        &lcm / gcd(lcm.clone(), q.denom().clone()) * q.denom()
    });
    let mut coefficients: Vec<BigInt> = p
        .iter()
        .map(|q| q.numer() * (&denominator / q.denom()))
        .collect();
    let content = coefficients
        .iter()
        .fold(BigInt::zero(), |g, n| gcd(g, n.clone()));
    for n in &mut coefficients {
        *n /= &content;
    }
    coefficients
}

struct RrtWorkBudget {
    used: usize,
    limit: usize,
}

impl Default for RrtWorkBudget {
    fn default() -> Self {
        Self {
            used: 0,
            limit: 100000,
        }
    }
}

impl RrtWorkBudget {
    // One shared limit for trial divisors, generated positive divisors
    // (including 1), and divisor pairs, across this entire spectral extraction.
    fn charge(&mut self) -> Result<()> {
        if self.used >= self.limit {
            return Err(format!(
                "REFUSED_IMPLEMENTATION_RESOURCE_LIMIT:rational_root_work_items:{}/{}",
                self.used, self.limit
            ));
        }
        self.used += 1;
        Ok(())
    }
}

fn positive_divisors(n: &BigInt, budget: &mut RrtWorkBudget) -> Result<Vec<BigInt>> {
    budget.charge()?;
    let mut divisors = vec![BigInt::one()];
    for (prime, exponent) in factor_with_budget(&n.abs(), Some(budget))? {
        let previous = divisors.clone();
        let mut power = BigInt::one();
        for _ in 0..exponent {
            power *= prime;
            for divisor in &previous {
                budget.charge()?;
                divisors.push(divisor * &power);
            }
        }
    }
    divisors.sort();
    Ok(divisors)
}

fn find_rational_root(p: &[Q], budget: &mut RrtWorkBudget) -> Result<Option<Q>> {
    // PSD and trace-one admission already puts every root in [0,1]. Zero and
    // one are peeled separately. The rational-root theorem makes this finite
    // candidate census exhaustive when its explicit budget has not refused.
    let integers = primitive_integer_coefficients(p);
    let numerators = positive_divisors(integers.last().expect("nonzero constant"), budget)?;
    let denominators = positive_divisors(&integers[0], budget)?;
    let mut seen = BTreeSet::new();
    for numerator in numerators {
        for denominator in &denominators {
            // Count every attempted divisor pair, including non-reduced or
            // out-of-domain pairs, across every residual of this extraction.
            budget.charge()?;
            if &numerator >= denominator {
                continue;
            }
            let root = Q::new(numerator.clone(), denominator.clone());
            if !seen.insert(root.clone()) {
                continue;
            }
            if poly_eval(p, &root).is_zero() {
                return Ok(Some(root));
            }
        }
    }
    Ok(None)
}

fn squared_quadratic(p: &[Q]) -> Option<Vec<Q>> {
    if p.len() != 5 || p[0] != Q::one() {
        return None;
    }
    let b = &p[1] / rat(2, 1);
    let c = (&p[2] - &b * &b) / rat(2, 1);
    let quadratic = vec![Q::one(), b, c];
    (poly_mul(&quadratic, &quadratic) == p).then_some(quadratic)
}

// Bounded integer factorization for squareclass and valuation certificates.
// Each trial division is counted; budget exhaustion is a refusal.
fn factors(n: &BigInt) -> Result<BTreeMap<u64, i64>> {
    factor_with_budget(n, None)
}

fn factor_with_budget(
    n: &BigInt,
    mut budget: Option<&mut RrtWorkBudget>,
) -> Result<BTreeMap<u64, i64>> {
    let mut n = n.clone();
    if n <= BigInt::zero() {
        return Err("ZERO_HAS_NO_PRIME_FACTORIZATION".into());
    }
    let mut out = BTreeMap::new();
    let mut p = 2_u64;
    let mut candidates = 0;
    while BigInt::from(p) * p <= n {
        if let Some(work) = budget.as_deref_mut() {
            work.charge()?;
        }
        if candidates == 100000 {
            return Err(
                "REFUSED_IMPLEMENTATION_RESOURCE_LIMIT:trial_divisor_candidates:100000/100000"
                    .into(),
            );
        }
        candidates += 1;
        while (&n % p).is_zero() {
            *out.entry(p).or_default() += 1;
            n /= p;
        }
        p = if p == 2 { 3 } else { p + 2 };
    }
    if n > BigInt::one() {
        // At normal exit n < p^2 and p <= 200001 by the candidate budget.
        // The conversion is proved bounded here, not an input-width ceiling.
        let residual = n
            .to_u64()
            .expect("trial-factor residual below 200001 squared");
        *out.entry(residual).or_default() += 1;
    }
    Ok(out)
}

fn valuation(q: &Q) -> Result<BTreeMap<u64, i64>> {
    if q <= &Q::zero() {
        return Err("LOG_ARGUMENT_NONPOSITIVE".into());
    }
    let mut f = factors(q.numer())?;
    for (p, k) in factors(q.denom())? {
        *f.entry(p).or_default() -= k;
    }
    f.retain(|_, k| *k != 0);
    Ok(f)
}

// sqrt(q) = coefficient * sqrt(squarefree positive radicand).
fn squarefree_root(q: &Q) -> Result<(Q, BigInt)> {
    if q < &Q::zero() {
        return Err("NEGATIVE_QUADRATIC_DISCRIMINANT".into());
    }
    if q.is_zero() {
        return Ok((Q::zero(), BigInt::one()));
    }
    let n = q.numer() * q.denom();
    let mut square = BigInt::one();
    let mut radicand = BigInt::one();
    for (p, k) in factors(&n)? {
        square *= BigInt::from(p).pow((k / 2) as u32);
        if k % 2 != 0 {
            radicand *= p;
        }
    }
    Ok((Q::new(square, q.denom().clone()), radicand))
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct Eigenvalue {
    center: Q,
    coefficient: Q,
    radicand: BigInt,
}

impl Eigenvalue {
    fn rational(value: Q) -> Self {
        Self {
            center: value,
            coefficient: Q::zero(),
            radicand: BigInt::one(),
        }
    }

    // Exact sign of a + b sqrt(d), using rational squared comparisons.
    fn sign(&self) -> std::cmp::Ordering {
        use std::cmp::Ordering;
        if self.coefficient.is_zero() {
            return self.center.cmp(&Q::zero());
        }
        let a = &self.center;
        let b = &self.coefficient;
        if a.is_zero() || a.signum() == b.signum() {
            return b.cmp(&Q::zero());
        }
        let magnitude = (a * a).cmp(&(b * b * Q::from_integer(self.radicand.clone())));
        match (a.is_positive(), magnitude) {
            (true, Ordering::Greater) | (false, Ordering::Less) => Ordering::Greater,
            (_, Ordering::Equal) => Ordering::Equal,
            _ => Ordering::Less,
        }
    }

    fn norm(&self) -> Q {
        &self.center * &self.center
            - &self.coefficient * &self.coefficient * Q::from_integer(self.radicand.clone())
    }

    fn json(&self) -> Value {
        if self.coefficient.is_zero() {
            json!({"kind":"rational", "value": qstr(&self.center)})
        } else {
            let radicand: Value = serde_json::from_str(&self.radicand.to_string())
                .expect("arbitrary-precision positive JSON integer");
            json!({"kind":"quadratic", "center":qstr(&self.center),
                "coefficient":qstr(&self.coefficient), "radicand":radicand})
        }
    }
}

fn spectrum(a: &Matrix) -> Result<Vec<Eigenvalue>> {
    spectrum_with_budget(a, &mut RrtWorkBudget::default())
}

fn spectrum_with_budget(a: &Matrix, candidates: &mut RrtWorkBudget) -> Result<Vec<Eigenvalue>> {
    let polynomial = characteristic(a);
    let mut residual = polynomial.clone();
    let mut values = Vec::new();
    let mut product = vec![Q::one()];
    while residual.len() > 1 {
        let boundary = if residual.last().expect("constant").is_zero() {
            Some(Q::zero())
        } else if poly_eval(&residual, &Q::one()).is_zero() {
            Some(Q::one())
        } else {
            None
        };
        if let Some(root) = boundary {
            residual = synthetic_divide(&residual, &root)?;
            product = poly_mul(&product, &[Q::one(), -&root]);
            values.push(Eigenvalue::rational(root));
            continue;
        }
        if residual.len() == 2 {
            let root = -&residual[1] / &residual[0];
            product = poly_mul(&product, &residual);
            values.push(Eigenvalue::rational(root));
            break;
        }
        let square = squared_quadratic(&residual);
        if residual.len() == 3 || square.is_some() {
            let multiplicity = if square.is_some() { 2 } else { 1 };
            let quadratic = square.unwrap_or_else(|| residual.clone());
            let center = -&quadratic[1] / rat(2, 1);
            let delta = &center * &center - &quadratic[2];
            let (coefficient, radicand) = squarefree_root(&delta)?;
            for _ in 0..multiplicity {
                if radicand.is_one() {
                    values.push(Eigenvalue::rational(&center - &coefficient));
                    values.push(Eigenvalue::rational(&center + &coefficient));
                } else {
                    values.push(Eigenvalue {
                        center: center.clone(),
                        coefficient: -&coefficient,
                        radicand: radicand.clone(),
                    });
                    values.push(Eigenvalue {
                        center: center.clone(),
                        coefficient: coefficient.clone(),
                        radicand: radicand.clone(),
                    });
                }
                product = poly_mul(&product, &quadratic);
            }
            break;
        }
        if let Some(root) = find_rational_root(&residual, candidates)? {
            residual = synthetic_divide(&residual, &root)?;
            product = poly_mul(&product, &[Q::one(), -&root]);
            values.push(Eigenvalue::rational(root));
        } else {
            // For degree 3, lack of a rational root establishes irreducibility. At
            // degrees 4/5 this is only an unsupported residual, not a claim
            // that no factorization or splitting field exists.
            return Err(if residual.len() == 4 {
                "REFUSED_UNSUPPORTED:irreducible_cubic_spectrum".into()
            } else {
                format!(
                    "REFUSED_UNSUPPORTED:residual_spectrum_degree_{}",
                    residual.len() - 1
                )
            });
        }
    }
    if product != polynomial {
        return Err("SPECTRUM_CHARACTERISTIC_PRODUCT_MISMATCH".into());
    }
    for value in &values {
        if value.sign().is_lt() {
            return Err("NEGATIVE_EIGENVALUE".into());
        }
        let mut complement = value.clone();
        complement.center = Q::one() - &complement.center;
        complement.coefficient = -complement.coefficient;
        if complement.sign().is_lt() {
            return Err("EIGENVALUE_EXCEEDS_ONE".into());
        }
    }
    let quadratic_pairs: BTreeSet<_> = values
        .iter()
        .filter(|v| !v.coefficient.is_zero())
        .map(|v| (v.center.clone(), v.radicand.clone(), v.coefficient.abs()))
        .collect();
    if quadratic_pairs.len() > 1 {
        return Err("REFUSED_UNSUPPORTED:multiple_distinct_quadratic_pairs".into());
    }
    values.sort_by(|a, b| {
        (
            !a.coefficient.is_zero(),
            &a.center,
            &a.radicand,
            &a.coefficient,
        )
            .cmp(&(
                !b.coefficient.is_zero(),
                &b.center,
                &b.radicand,
                &b.coefficient,
            ))
    });
    Ok(values)
}

type EchelonRow = (usize, Vec<Q>, Vec<Q>);

// Track elementary row operations against the greedily selected ORIGINAL rows.
// This emits a checkable coordinate certificate, never an integer-relation guess.
fn row_basis(rows: &[Vec<Q>]) -> (Vec<usize>, Vec<Vec<Q>>) {
    let mut basis = Vec::new();
    let mut echelon: Vec<EchelonRow> = Vec::new();
    for (index, row) in rows.iter().enumerate() {
        let mut residue = row.clone();
        let mut combination = vec![Q::zero(); basis.len() + 1];
        combination[basis.len()] = Q::one();
        for (pivot, reduced, transform) in &echelon {
            let factor = residue[*pivot].clone();
            for (x, y) in residue.iter_mut().zip(reduced) {
                *x -= &factor * y;
            }
            for (x, y) in combination.iter_mut().zip(transform) {
                *x -= &factor * y;
            }
        }
        if let Some(pivot) = residue.iter().position(|x| !x.is_zero()) {
            let scale = residue[pivot].clone();
            for x in &mut residue {
                *x /= &scale;
            }
            for x in &mut combination {
                *x /= &scale;
            }
            for (_, _, transform) in &mut echelon {
                transform.push(Q::zero());
            }
            basis.push(index);
            echelon.push((pivot, residue, combination));
        }
    }
    let coordinates = rows
        .iter()
        .map(|row| {
            let mut residue = row.clone();
            let mut coefficients = vec![Q::zero(); basis.len()];
            for (pivot, reduced, transform) in &echelon {
                let factor = residue[*pivot].clone();
                for (x, y) in residue.iter_mut().zip(reduced) {
                    *x -= &factor * y;
                }
                for (x, y) in coefficients.iter_mut().zip(transform) {
                    *x += &factor * y;
                }
            }
            assert!(
                residue.iter().all(Zero::is_zero),
                "exact row-basis reconstruction"
            );
            coefficients
        })
        .collect();
    (basis, coordinates)
}

fn rational_rows(rows: &[Vec<Q>]) -> Vec<Vec<String>> {
    rows.iter().map(|r| r.iter().map(qstr).collect()).collect()
}

fn gcd(mut a: BigInt, mut b: BigInt) -> BigInt {
    while !b.is_zero() {
        let r = &a % &b;
        a = b;
        b = r;
    }
    a.abs()
}

fn relation_within_bound(coordinates: &[Q]) -> bool {
    let denominator = coordinates.iter().fold(BigInt::one(), |lcm, q| {
        (&lcm / gcd(lcm.clone(), q.denom().clone())) * q.denom()
    });
    let mut relation = vec![denominator.clone()];
    relation.extend(
        coordinates
            .iter()
            .map(|q| -q.numer() * (&denominator / q.denom())),
    );
    let divisor = relation
        .iter()
        .fold(BigInt::zero(), |g, x| gcd(g, x.clone()));
    relation
        .iter()
        .all(|x| (x / &divisor).abs() <= BigInt::from(64))
}

fn dependence(values: &[Eigenvalue]) -> Result<Value> {
    let mut arguments: Vec<Eigenvalue> = Vec::new();
    for value in values {
        if value.sign().is_eq() || arguments.last() == Some(value) {
            continue;
        }
        arguments.push(value.clone());
    }
    let pair = arguments.iter().find(|v| !v.coefficient.is_zero());
    let mut primes = BTreeSet::new();
    let mut valuations = Vec::new();
    for value in &arguments {
        let q = if value.coefficient.is_zero() {
            value.center.clone()
        } else {
            value.norm()
        };
        let row = valuation(&q)?;
        primes.extend(row.keys().copied());
        valuations.push(row);
    }
    let primes: Vec<_> = primes.into_iter().collect();
    let mut generators: Vec<Value> = primes
        .iter()
        .map(|p| json!({"kind":"prime", "value":p}))
        .collect();
    if let Some(member) = pair {
        let mut plus = member.clone();
        plus.coefficient = plus.coefficient.abs();
        let mut minus = plus.clone();
        minus.coefficient = -minus.coefficient;
        // q+/q- > 1 and conjugation takes it to its inverse; hence its log
        // is Q-independent of rational-prime logs by applying conjugation.
        // The actual eigenvalue-log basis is then obtained by Q row operations.
        generators.push(
            json!({"kind":"quadratic_ratio", "numerator":plus.json(), "denominator":minus.json()}),
        );
    }
    let rows: Vec<Vec<Q>> = arguments
        .iter()
        .zip(valuations)
        .map(|(value, valuations)| {
            let denominator = if value.coefficient.is_zero() { 1 } else { 2 };
            let mut row: Vec<Q> = primes
                .iter()
                .map(|p| rat(*valuations.get(p).unwrap_or(&0), denominator))
                .collect();
            if pair.is_some() {
                row.push(if value.coefficient.is_zero() {
                    Q::zero()
                } else if value.coefficient.is_positive() {
                    rat(1, 2)
                } else {
                    rat(-1, 2)
                });
            }
            row
        })
        .collect();
    let (basis, coordinates) = row_basis(&rows);
    if coordinates.iter().any(|row| !relation_within_bound(row)) {
        return Err("REFUSED_AT_BUDGET:dependence_integer_coefficient_abs_max".into());
    }
    Ok(json!({
        "status":"EXACT",
        "method":if pair.is_some() { "PRIME_AND_CONJUGATE_RATIO_Q_ROW_BASIS" } else { "PRIME_EXPONENT_Q_ROW_BASIS" },
        "arguments":arguments.iter().map(Eigenvalue::json).collect::<Vec<_>>(),
        "generators":generators,
        "exponent_rows":rational_rows(&rows),
        "basis_argument_indices":basis,
        "coordinates":rational_rows(&coordinates)
    }))
}

fn splitting_field(values: &[Eigenvalue], conductor: u64) -> Result<Value> {
    let phi = match conductor {
        1 => 1,
        3 | 4 => 2,
        5 | 8 => 4,
        _ => return Err("CONDUCTOR_OUTSIDE_FROZEN_CLASS".into()),
    };
    let radicand = values
        .iter()
        .find(|v| !v.coefficient.is_zero())
        .map_or_else(BigInt::one, |v| v.radicand.clone());
    let contained = radicand.is_one()
        || (radicand == BigInt::from(2) && conductor == 8)
        || (radicand == BigInt::from(5) && conductor == 5);
    let relative_degree = if contained { 1 } else { 2 };
    Ok(json!({
        "spectrum_splitting_field":if radicand.is_one() { "Q".to_string() } else { format!("Q(sqrt({radicand}))") },
        "spectrum_degree_over_q":if radicand.is_one() { 1 } else { 2 },
        "carrier_conductor":conductor,
        "extension_degree_over_carrier":relative_degree,
        "compositum_degree_over_q":phi*relative_degree
    }))
}

// Classification uses exact positivity and purity plus the named theorem.
// It never numerically decides algebraicity or transcendence.
fn entropy_verdict(pure: bool) -> Value {
    if pure {
        json!({"verdict":"CARRIED", "reason":"PURE_STATE_ZERO",
            "anchor":"ZERO_LOG_ZERO_CONVENTION_AND_REAL_LOG_ONE", "quantity_type":"CARRIER_ZERO"})
    } else {
        json!({"verdict":"REFUSED_TRANSCENDENTAL", "reason":"MIXED_STATE_POSITIVITY_AND_BAKER_REDUCTION",
            "anchor":"A1", "quantity_type":"TRANSCENDENTAL_VALUE"})
    }
}

fn validated_input(input: &Value) -> Result<(Matrix, u64)> {
    reject_float(input, "input")?;
    let object = input.as_object().ok_or("INPUT_OBJECT_REQUIRED")?;
    let fields: BTreeSet<_> = object.keys().map(String::as_str).collect();
    if fields != BTreeSet::from(["fixture_id", "system_id", "conductor", "matrix", "scope"]) {
        return Err("INPUT_FIELDS_DIFFER_FROM_DECLARED_SCHEMA".into());
    }
    if input["fixture_id"].as_str().is_none_or(str::is_empty) {
        return Err("FIXTURE_ID_REQUIRED".into());
    }
    let conductor = input["conductor"]
        .as_u64()
        .ok_or("CONDUCTOR_INTEGER_REQUIRED")?;
    let system = input["system_id"].as_str().ok_or("SYSTEM_ID_REQUIRED")?;
    let (dimension, expected_conductor) = match system {
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
    if conductor != expected_conductor {
        return Err("SYSTEM_CONDUCTOR_MISMATCH".into());
    }
    let expected_scope = if system == "S8" {
        "S8_DIMENSION_ONLY_PROXY"
    } else {
        "DECLARED_SYSTEM_STATE"
    };
    if input["scope"] != expected_scope {
        return Err("SYSTEM_SCOPE_MISMATCH".into());
    }
    let a = matrix(&input["matrix"])?;
    if a.len() != dimension {
        return Err("SYSTEM_DIMENSION_MISMATCH".into());
    }
    if system == "S6" || system == "S7" {
        for (i, row) in a.iter().enumerate() {
            if row.iter().enumerate().any(|(j, q)| i != j && !q.is_zero()) {
                return Err("LADDER_SYSTEM_REQUIRES_DIAGONAL_STATE".into());
            }
        }
    }
    if system == "S6" {
        if a[0][0] <= Q::zero() {
            return Err("S6_GEOMETRIC_LADDER_REQUIRED".into());
        }
        let ratio = &a[1][1] / &a[0][0];
        if ratio <= Q::zero()
            || ratio >= Q::one()
            || (1..dimension).any(|i| a[i][i] != &ratio * &a[i - 1][i - 1])
        {
            return Err("S6_GEOMETRIC_LADDER_REQUIRED".into());
        }
    }
    validate_psd(&a)?;
    Ok((a, conductor))
}

// This classification has no factorization or splitting-field dependency.
// A rational symmetric matrix has algebraic spectrum via its characteristic
// polynomial; positivity, trace one and Tr(A^2) decide the purity hypothesis.
pub fn general_verdict(input: &Value) -> Result<Value> {
    if cyclotomic_density::has_coefficient_objects(input) {
        return cyclotomic_density::general_verdict(input);
    }
    let (a, _) = validated_input(input)?;
    Ok(entropy_verdict(power_sum_two(&a) == Q::one()))
}

pub fn evaluate(input: &Value) -> Result<Value> {
    let (a, conductor) = validated_input(input)?;
    let values = spectrum(&a)?;
    let mut grouped: Vec<Value> = Vec::new();
    for value in &values {
        let root = value.json();
        if grouped.last().is_some_and(|x| x["root"] == root) {
            let item = grouped.last_mut().expect("existing group");
            item["multiplicity"] =
                json!(item["multiplicity"].as_u64().expect("integer multiplicity") + 1);
        } else {
            grouped.push(json!({"root":root,"multiplicity":1}));
        }
    }
    let power_sum = power_sum_two(&a);
    let pure = power_sum == Q::one();
    Ok(json!({
        "characteristic_polynomial":characteristic(&a).iter().map(qstr).collect::<Vec<_>>(),
        "spectrum":grouped,
        "splitting_field":splitting_field(&values,conductor)?,
        "dependence":dependence(&values)?,
        "purity":if pure { "PURE" } else { "MIXED" },
        "renyi2_power_sum":qstr(&power_sum),
        "entropy":entropy_verdict(pure)
    }))
}

pub fn report(interface: &Value) -> Result<Value> {
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
        let fixture_id = input["fixture_id"].as_str().ok_or("FIXTURE_ID_REQUIRED")?;
        if !ids.insert(fixture_id) {
            return Err(format!("DUPLICATE_FIXTURE_ID:{fixture_id}"));
        }
        cases.push(json!({"input":input,"output":evaluate(input)?}));
    }
    Ok(json!({"authority_effect":"None", "schema":"c750_b01_exact_v1", "cases":cases}))
}

pub fn verdict_report(interface: &Value) -> Result<Value> {
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
        cases.push(json!({"input":input,"entropy":general_verdict(input)?}));
    }
    Ok(json!({"authority_effect":"None","schema":"c750_b01_verdict_v1","cases":cases}))
}

pub fn verify_output(input: &Value, output: &Value) -> Result<()> {
    reject_float(output, "output")?;
    let expected = evaluate(input)?;
    if output != &expected {
        let fields = expected.as_object().expect("output object");
        for (key, value) in fields {
            if output.get(key) != Some(value) {
                return Err(format!("OUTPUT_MISMATCH:{key}"));
            }
        }
        return Err("OUTPUT_FIELDS_DIFFER_FROM_DECLARED_SCHEMA".into());
    }
    Ok(())
}

// For x in [1,2], z=(x-1)/(x+1) is in [0,1/3]. The first m positive
// terms of 2*atanh(z) give a lower bound; the geometric tail majorant
// 2*z^(2m+1)/((2m+1)*(1-z^2)) gives a proved upper bound.
fn log_series_interval(x: &Q, tolerance: &Q) -> Result<(Q, Q, usize)> {
    if x < &Q::one() || x > &rat(2, 1) || tolerance <= &Q::zero() {
        return Err("LOG_SERIES_DOMAIN_ERROR".into());
    }
    let z = (x - Q::one()) / (x + Q::one());
    if z.is_zero() {
        return Ok((Q::zero(), Q::zero(), 0));
    }
    let z_squared = &z * &z;
    let mut power = z;
    let mut lower = Q::zero();
    for m in 1..=4096 {
        lower += rat(2, (2 * m - 1) as i64) * &power;
        power *= &z_squared;
        let tail = rat(2, (2 * m + 1) as i64) * &power / (Q::one() - &z_squared);
        if tail <= *tolerance {
            return Ok((lower.clone(), lower + tail, m));
        }
    }
    Err("REFUSED_AT_BUDGET:approximation_series_terms_max".into())
}

fn rational_log_interval(q: &Q, tolerance: &Q) -> Result<(Q, Q, usize)> {
    if q <= &Q::zero() || q > &Q::one() {
        return Err("ENTROPY_LOG_DOMAIN_ERROR".into());
    }
    let mut x = q.clone();
    let mut shift = 0;
    while x < Q::one() {
        x *= rat(2, 1);
        shift += 1;
    }
    let local_tolerance = tolerance / rat(shift + 1, 1);
    let (xlo, xhi, xt) = log_series_interval(&x, &local_tolerance)?;
    let (twolo, twohi, tt) = log_series_interval(&rat(2, 1), &local_tolerance)?;
    Ok((
        xlo - rat(shift, 1) * twohi,
        (xhi - rat(shift, 1) * twolo).min(Q::zero()),
        xt.max(tt),
    ))
}

fn polynomial_division(a: &[Q], b: &[Q]) -> Result<(Vec<Q>, Vec<Q>)> {
    if b.iter().all(Zero::is_zero) {
        return Err("POLYNOMIAL_DIVISION_BY_ZERO".into());
    }
    let mut remainder = poly_trim(a.to_vec());
    if remainder.len() < b.len() {
        return Ok((vec![Q::zero()], remainder));
    }
    let quotient_degree = remainder.len() - b.len();
    let mut quotient = vec![Q::zero(); quotient_degree + 1];
    while remainder.len() >= b.len() && remainder.iter().any(|q| !q.is_zero()) {
        let degree = remainder.len() - b.len();
        let coefficient = &remainder[0] / &b[0];
        quotient[quotient_degree - degree] += &coefficient;
        for (target, source) in remainder.iter_mut().zip(b) {
            *target -= &coefficient * source;
        }
        remainder = poly_trim(remainder);
    }
    Ok((poly_trim(quotient), remainder))
}

fn polynomial_quotient(a: &[Q], b: &[Q]) -> Result<Vec<Q>> {
    let (quotient, remainder) = polynomial_division(a, b)?;
    if remainder.iter().any(|q| !q.is_zero()) {
        return Err("POLYNOMIAL_DIVISIBILITY_CERTIFICATE_FAILED".into());
    }
    Ok(quotient)
}

fn derivative(p: &[Q]) -> Vec<Q> {
    if p.len() == 1 {
        return vec![Q::zero()];
    }
    p.iter()
        .take(p.len() - 1)
        .enumerate()
        .map(|(i, q)| q * rat((p.len() - 1 - i) as i64, 1))
        .collect()
}

fn polynomial_gcd(a: &[Q], b: &[Q]) -> Result<Vec<Q>> {
    let mut left = poly_trim(a.to_vec());
    let mut right = poly_trim(b.to_vec());
    while right.iter().any(|q| !q.is_zero()) {
        let (_, remainder) = polynomial_division(&left, &right)?;
        left = right;
        right = remainder;
    }
    let scale = left[0].clone();
    if scale.is_zero() {
        return Err("ZERO_POLYNOMIAL_GCD".into());
    }
    for q in &mut left {
        *q /= &scale;
    }
    Ok(left)
}

fn squarefree_factors(p: &[Q]) -> Result<Vec<(Vec<Q>, usize)>> {
    let mut repeated = polynomial_gcd(p, &derivative(p))?;
    let mut remaining = polynomial_quotient(p, &repeated)?;
    let mut multiplicity = 1;
    let mut factors = Vec::new();
    while remaining.len() > 1 {
        let common = polynomial_gcd(&remaining, &repeated)?;
        let factor = polynomial_quotient(&remaining, &common)?;
        if factor.len() > 1 {
            factors.push((factor, multiplicity));
        }
        remaining = common;
        repeated = polynomial_quotient(&repeated, &remaining)?;
        multiplicity += 1;
        if multiplicity > p.len() {
            return Err("SQUAREFREE_MULTIPLICITY_LOOP_FAILED".into());
        }
    }
    let mut product = vec![Q::one()];
    for (factor, count) in &factors {
        for _ in 0..*count {
            product = poly_mul(&product, factor);
        }
    }
    if product != p {
        return Err("SQUAREFREE_MULTIPLICITY_PRODUCT_MISMATCH".into());
    }
    Ok(factors)
}

fn sturm_sequence(p: &[Q]) -> Result<Vec<Vec<Q>>> {
    let mut sequence = vec![p.to_vec(), derivative(p)];
    while sequence.last().expect("Sturm derivative").len() > 1 {
        let end = sequence.len();
        let (_, remainder) = polynomial_division(&sequence[end - 2], &sequence[end - 1])?;
        if remainder.iter().all(Zero::is_zero) {
            return Err("STURM_FACTOR_NOT_SQUAREFREE".into());
        }
        // Positive scaling ONLY: multiplying a negative-leading remainder by
        // -1 to make it monic would invalidate the variation counts.
        let scale = remainder[0].abs();
        sequence.push(remainder.into_iter().map(|q| -q / &scale).collect());
    }
    Ok(sequence)
}

fn sturm_variations(sequence: &[Vec<Q>], endpoint: &Q) -> usize {
    let mut previous = None;
    let mut changes = 0;
    for polynomial in sequence {
        let sign = poly_eval(polynomial, endpoint).cmp(&Q::zero());
        if sign.is_eq() {
            continue;
        }
        if previous.is_some_and(|s| s != sign) {
            changes += 1;
        }
        previous = Some(sign);
    }
    changes
}

// V(a)-V(b) counts (a,b]. Subtract the exact root at b, when present,
// to obtain a strict-open count. Midpoint roots are recorded separately once.
fn sturm_open_count(sequence: &[Vec<Q>], lo: &Q, hi: &Q) -> Result<usize> {
    let count = sturm_variations(sequence, lo) as isize
        - sturm_variations(sequence, hi) as isize
        - isize::from(poly_eval(&sequence[0], hi).is_zero());
    usize::try_from(count).map_err(|_| "STURM_NEGATIVE_ROOT_COUNT".into())
}

// The uniform continuity modulus avoids any root-separation assumption.
// B=k+12, delta=2^-B: |h(x)-h(q)| <= delta*(B+2) for |x-q|<=delta.
// These are proved upper bounds, not changes to either production ceiling.
struct ClusterBounds {
    bits: u64,
    delta: Q,
    radius: Q,
    log_tolerance: Q,
    subdivision_bound: usize,
}

impl ClusterBounds {
    fn new(k: u64, dimension: usize) -> Result<Self> {
        if k > 32 || !(1..=5).contains(&dimension) {
            return Err("CLUSTER_PROOF_DOMAIN_ERROR".into());
        }
        let bits = k + 12;
        let delta = Q::new(BigInt::one(), BigInt::one() << bits);
        Ok(Self {
            bits,
            radius: &delta * rat((bits + 2) as i64, 1),
            delta,
            log_tolerance: Q::new(BigInt::one(), BigInt::one() << k)
                / rat((8 * dimension) as i64, 1),
            subdivision_bound: dimension * bits as usize,
        })
    }
}

fn cluster_entropy_interval(lo: &Q, hi: &Q, bounds: &ClusterBounds) -> Result<(Q, Q, usize)> {
    if lo == hi && (lo.is_zero() || lo.is_one()) {
        return Ok((Q::zero(), Q::zero(), 0));
    }
    if lo < &Q::zero() || lo > hi || hi > &Q::one() || hi - lo > bounds.delta {
        return Err("CLUSTER_ENTROPY_INTERVAL_DOMAIN_ERROR".into());
    }
    let midpoint = (lo + hi) / rat(2, 1);
    if midpoint < &bounds.delta / rat(2, 1) {
        return Err("CLUSTER_LOG_SHIFT_PROOF_BOUND_FAILED".into());
    }
    let (log_lo, log_hi, terms) = rational_log_interval(&midpoint, &bounds.log_tolerance)?;
    if terms > 64 {
        return Err("CLUSTER_SERIES_PROOF_BOUND_FAILED".into());
    }
    let radius = if lo == hi {
        Q::zero()
    } else {
        bounds.radius.clone()
    };
    Ok((
        (-&midpoint * log_hi - &radius).max(Q::zero()),
        -midpoint * log_lo + radius,
        terms,
    ))
}

struct RootEnclosure {
    polynomial: Vec<Q>,
    multiplicity: usize,
    distinct_root_count: usize,
    lo: Q,
    hi: Q,
    entropy_lo: Q,
    entropy_hi: Q,
}

impl RootEnclosure {
    fn json(&self) -> Value {
        json!({"squarefree_polynomial":self.polynomial.iter().map(qstr).collect::<Vec<_>>(),
            "multiplicity":self.multiplicity,"lower":qstr(&self.lo),"upper":qstr(&self.hi),
            "kind":if self.lo == self.hi { "EXACT_RATIONAL_ROOT" } else { "STURM_OPEN_SPECTRAL_CLUSTER" },
            "distinct_root_count":self.distinct_root_count,"entropy_lower":qstr(&self.entropy_lo),"entropy_upper":qstr(&self.entropy_hi)})
    }
}

fn sturm_entropy_enclosures(
    p: &[Q],
    bounds: &ClusterBounds,
) -> Result<(Vec<RootEnclosure>, usize, usize)> {
    sturm_entropy_enclosures_with_limit(p, bounds, 4096)
}

fn sturm_entropy_enclosures_with_limit(
    p: &[Q],
    bounds: &ClusterBounds,
    subdivision_limit: usize,
) -> Result<(Vec<RootEnclosure>, usize, usize)> {
    let mut enclosures = Vec::new();
    let mut bisections = 0;
    let mut max_terms = 0;
    for (factor, multiplicity) in squarefree_factors(p)? {
        let mut interior = factor.clone();
        for endpoint in [Q::zero(), Q::one()] {
            if interior.len() > 1 && poly_eval(&interior, &endpoint).is_zero() {
                interior = synthetic_divide(&interior, &endpoint)?;
                enclosures.push(RootEnclosure {
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
        let sequence = sturm_sequence(&interior)?;
        let total = sturm_open_count(&sequence, &Q::zero(), &Q::one())?;
        if total != interior.len() - 1 {
            return Err("PSD_SPECTRUM_ROOT_CENSUS_FAILED".into());
        }
        let mut queue = vec![(Q::zero(), Q::one(), total)];
        while let Some((lo, hi, count)) = queue.pop() {
            if count == 0 {
                continue;
            }
            // A bin may retain multiple distinct roots. Endpoints are excluded
            // from its count and handled separately, even when they are roots.
            if &hi - &lo <= bounds.delta {
                let (entropy_lo, entropy_hi, terms) = cluster_entropy_interval(&lo, &hi, bounds)?;
                max_terms = max_terms.max(terms);
                enclosures.push(RootEnclosure {
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
            // This is an added operational subdivision limit, not the frozen
            // logarithm-series term budget. It is shared by all factors and
            // all subsequent refinements, and exhaustion is an honest refusal.
            if bisections >= subdivision_limit {
                return Err(format!(
                    "REFUSED_IMPLEMENTATION_RESOURCE_LIMIT:sturm_subdivisions:{bisections}/{subdivision_limit}"
                ));
            }
            if bisections >= bounds.subdivision_bound {
                return Err("CLUSTER_SUBDIVISION_PROOF_BOUND_FAILED".into());
            }
            bisections += 1;
            let midpoint = (&lo + &hi) / rat(2, 1);
            let exact_root = poly_eval(&interior, &midpoint).is_zero();
            let left = sturm_open_count(&sequence, &lo, &midpoint)?;
            let right = sturm_open_count(&sequence, &midpoint, &hi)?;
            if left + right + usize::from(exact_root) != count {
                return Err("STURM_SUBDIVISION_ROOT_CENSUS_FAILED".into());
            }
            if exact_root {
                let (entropy_lo, entropy_hi, terms) =
                    cluster_entropy_interval(&midpoint, &midpoint, bounds)?;
                max_terms = max_terms.max(terms);
                enclosures.push(RootEnclosure {
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
    if enclosures
        .iter()
        .map(|root| root.multiplicity * root.distinct_root_count)
        .sum::<usize>()
        != p.len() - 1
    {
        return Err("STURM_WEIGHTED_MULTIPLICITY_CENSUS_FAILED".into());
    }
    enclosures.sort_by(|a, b| (&a.lo, &a.hi).cmp(&(&b.lo, &b.hi)));
    Ok((enclosures, bisections, max_terms))
}

// The external verdict requires an interval whose exact width meets its error
// obligation. Admission/characteristic/Sturm calculations cover rational real-
// symmetric PSD inputs independently of any splitting or dependence routine.
pub fn evaluate_external(input: &Value, k: u64) -> Result<Value> {
    if cyclotomic_density::has_coefficient_objects(input) {
        return cyclotomic_density::evaluate_external(input, k);
    }
    if k > 32 {
        return Err("REFUSED_AT_BUDGET:approximation_k_max".into());
    }
    let (a, _) = validated_input(input)?;
    if power_sum_two(&a) == Q::one() {
        return Ok(json!({"entropy":entropy_verdict(true),"approximation":null}));
    }
    let bound = Q::new(BigInt::one(), BigInt::one() << k);
    let bounds = ClusterBounds::new(k, a.len())?;
    let (roots, bisections, max_terms) = sturm_entropy_enclosures(&characteristic(&a), &bounds)?;
    let mut lower = Q::zero();
    let mut upper = Q::zero();
    for root in &roots {
        lower += rat((root.multiplicity * root.distinct_root_count) as i64, 1) * &root.entropy_lo;
        upper += rat((root.multiplicity * root.distinct_root_count) as i64, 1) * &root.entropy_hi;
    }
    let width = &upper - &lower;
    if width < Q::zero() || width > bound {
        return Err("INTERVAL_BOUND_NOT_ESTABLISHED".into());
    }
    let midpoint = (&lower + &upper) / rat(2, 1);
    Ok(json!({
        "entropy":{"verdict":"EXTERNALLY_INTERFACED", "reason":"MIXED_STATE_WITH_RATIONAL_INTERVAL_INTERFACE",
            "anchor":"A1", "quantity_type":"APPROXIMATION_NOT_MEMBERSHIP"},
        "approximation":{
            "authority_effect":"None", "quantity_type":"APPROXIMATION_NOT_MEMBERSHIP",
            "metric":"ABSOLUTE_ERROR_IN_REAL_NATURAL_LOG_ENTROPY",
            "method":"RATIONAL_STURM_SPECTRAL_CLUSTERS_AND_ATANH_GEOMETRIC_TAIL",
            "root_isolation":"EXACT_RATIONAL_STURM_SPECTRAL_CLUSTERS",
            "approximation_algorithm":"DYADIC_STURM_CLUSTERS_WITH_UNIFORM_ENTROPY_MODULUS",
            "spectral_count_convention":"OPEN_BINS_PLUS_EXACT_SINGLETONS",
            "cluster_precision_bits":bounds.bits,"uniform_entropy_radius":qstr(&bounds.radius),
            "sturm_subdivision_proved_bound":bounds.subdivision_bound,
            "log_shift_proved_bound":bounds.bits+1,"series_terms_proved_bound":64,
            "psd_validation":"EXACT_RATIONAL_SCHUR_COMPLEMENT",
            "requested_k":k, "requested_bound":qstr(&bound),
            "lower":qstr(&lower), "upper":qstr(&upper), "interval_width":qstr(&width),
            "rational_estimate":qstr(&midpoint), "absolute_error_bound":qstr(&(width/rat(2,1))),
            "max_series_terms":max_terms,
            "root_isolation_subdivisions":bisections,
            "root_isolation_resource_limit":{"kind":"IMPLEMENTATION_RESOURCE_LIMIT","unit":"SUBDIVISION","limit":4096},
            "eigenvalue_intervals":roots.iter().map(RootEnclosure::json).collect::<Vec<_>>()
        }
    }))
}

pub fn external_report(interface: &Value, k: u64) -> Result<Value> {
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
        cases.push(json!({"input":input,"output":evaluate_external(input,k)?}));
    }
    Ok(json!({"authority_effect":"None","schema":"c750_b01_external_v1","cases":cases}))
}

fn first_mismatch(expected: &Value, actual: &Value, path: &str) -> Option<String> {
    match (expected, actual) {
        (Value::Object(a), Value::Object(b)) => {
            let keys: BTreeSet<_> = a.keys().chain(b.keys()).collect();
            for key in keys {
                let child = format!("{path}.{key}");
                match (a.get(key), b.get(key)) {
                    (Some(x), Some(y)) => {
                        if let Some(mismatch) = first_mismatch(x, y, &child) {
                            return Some(mismatch);
                        }
                    }
                    _ => return Some(child),
                }
            }
            None
        }
        (Value::Array(a), Value::Array(b)) => {
            if a.len() != b.len() {
                return Some(format!("{path}.length"));
            }
            for (i, (x, y)) in a.iter().zip(b).enumerate() {
                if let Some(mismatch) = first_mismatch(x, y, &format!("{path}[{i}]")) {
                    return Some(mismatch);
                }
            }
            None
        }
        _ => (expected != actual).then(|| path.to_string()),
    }
}

pub fn verify_external_output(input: &Value, k: u64, output: &Value) -> Result<()> {
    reject_float(output, "output")?;
    let expected = evaluate_external(input, k)?;
    if let Some(path) = first_mismatch(&expected, output, "output") {
        return Err(format!("EXTERNAL_OUTPUT_MISMATCH:{path}"));
    }
    Ok(())
}

// Test-only dependency injection lowers an operational resource limit without
// mutating global state or exposing a production CLI/API budget override.
#[cfg(test)]
pub fn test_spectrum_with_rrt_limit(input: &Value, limit: usize) -> Result<()> {
    if limit >= 100000 {
        return Err("TEST_LIMIT_MUST_BE_STRICTLY_LOWER_THAN_PRODUCTION".into());
    }
    let (matrix, _) = validated_input(input)?;
    spectrum_with_budget(&matrix, &mut RrtWorkBudget { used: 0, limit }).map(|_| ())
}

#[cfg(test)]
pub fn test_external_with_sturm_limit(input: &Value, k: u64, limit: usize) -> Result<()> {
    if limit >= 4096 {
        return Err("TEST_LIMIT_MUST_BE_STRICTLY_LOWER_THAN_PRODUCTION".into());
    }
    if k > 32 {
        return Err("REFUSED_AT_BUDGET:approximation_k_max".into());
    }
    let (matrix, _) = validated_input(input)?;
    let bounds = ClusterBounds::new(k, matrix.len())?;
    sturm_entropy_enclosures_with_limit(&characteristic(&matrix), &bounds, limit).map(|_| ())
}

// Explicitly scoped local faults exercise the analytic and proof-bound gates;
// no production override, shared mutable state, or receipt-writing path exists.
#[cfg(test)]
pub fn test_cluster_modulus(k: u64, omit_radius: bool) -> Result<Value> {
    let mut bounds = ClusterBounds::new(k, 5)?;
    if omit_radius {
        bounds.radius = Q::zero();
    }
    let (lower, upper, terms) = cluster_entropy_interval(&Q::zero(), &bounds.delta, &bounds)?;
    Ok(json!({"lower":qstr(&lower),"upper":qstr(&upper),"terms":terms}))
}

#[cfg(test)]
pub fn test_cluster_proof_bound(input: &Value, k: u64) -> Result<()> {
    let (matrix, _) = validated_input(input)?;
    let mut bounds = ClusterBounds::new(k, matrix.len())?;
    bounds.subdivision_bound = 1;
    sturm_entropy_enclosures(&characteristic(&matrix), &bounds).map(|_| ())
}

#[cfg(test)]
pub fn test_cluster_zero_log_fault() -> Result<()> {
    rational_log_interval(&Q::zero(), &rat(1, 100)).map(|_| ())
}

pub fn inject(interface: &Value, mutation: &str) -> Result<()> {
    let baseline = report(interface)?;
    let fixture_id = match mutation {
        "float_leakage"
        | "planted_algebraic_entropy"
        | "false_interval_width"
        | "false_root_multiplicity" => "s1_mixed_half",
        "zero_log_zero" | "unnormalised_spectrum" | "non_psd_state" => "s1_pure",
        "false_splitting_degree" => "s1_sqrt2",
        _ => return Err(format!("UNKNOWN_MUTATION:{mutation}")),
    };
    let case = baseline["cases"]
        .as_array()
        .expect("cases")
        .iter()
        .find(|c| c["input"]["fixture_id"] == fixture_id)
        .ok_or_else(|| format!("MUTATION_FIXTURE_ABSENT:{fixture_id}"))?;
    let mut input = case["input"].clone();
    let mut output = case["output"].clone();
    if mutation == "false_interval_width" || mutation == "false_root_multiplicity" {
        let mut external = evaluate_external(&input, 8)?;
        if mutation == "false_interval_width" {
            external["approximation"]["interval_width"] = json!("0/1");
        } else {
            external["approximation"]["eigenvalue_intervals"][0]["multiplicity"] = json!(1);
        }
        return verify_external_output(&input, 8, &external)
            .map_err(|error| format!("INJECTED_OBJECT:{mutation}:{fixture_id}:{error}"));
    }
    match mutation {
        "float_leakage" => {
            output["entropy"]["value"] = serde_json::from_str("0.5").expect("injected JSON decimal")
        }
        "zero_log_zero" => output["entropy"]["quantity_type"] = json!("UNDEFINED_LOG_ZERO"),
        "unnormalised_spectrum" => input["matrix"][0][0] = json!("2/1"),
        "false_splitting_degree" => output["splitting_field"]["spectrum_degree_over_q"] = json!(1),
        "planted_algebraic_entropy" => output["entropy"]["verdict"] = json!("CARRIED"),
        "non_psd_state" => input["matrix"] = json!([["0/1", "1/1"], ["1/1", "1/1"]]),
        _ => unreachable!("mutation validated above"),
    }
    verify_output(&input, &output)
        .map_err(|error| format!("INJECTED_OBJECT:{mutation}:{fixture_id}:{error}"))
}

fn cli() -> Result<Value> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let mut input = String::new();
    let mut mutation = None;
    let mut external_k = None;
    let mut verdict_only = false;
    let mut cyclotomic_characteristic = false;
    let mut spectral_roots = false;
    match args.as_slice() {
        [] => {
            io::stdin()
                .read_to_string(&mut input)
                .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
        }
        [option, path] if option == "--interface" => {
            input =
                std::fs::read_to_string(path).map_err(|e| format!("INTERFACE_READ_ERROR:{e}"))?;
        }
        [option,path,verdict] if option == "--interface" && verdict == "--verdict-only" => {
            input = std::fs::read_to_string(path).map_err(|e| format!("INTERFACE_READ_ERROR:{e}"))?;
            verdict_only = true;
        }
        [verdict] if verdict == "--verdict-only" => {
            io::stdin().read_to_string(&mut input).map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
            verdict_only = true;
        }
        [option,path,characteristic] if option == "--interface" && characteristic == "--cyclotomic-characteristic" => {
            input = std::fs::read_to_string(path).map_err(|e|format!("INTERFACE_READ_ERROR:{e}"))?;
            cyclotomic_characteristic = true;
        }
        [characteristic] if characteristic == "--cyclotomic-characteristic" => {
            io::stdin().read_to_string(&mut input).map_err(|e|format!("INPUT_READ_ERROR:{e}"))?;
            cyclotomic_characteristic = true;
        }
        [option,path,roots] if option == "--interface" && roots == "--spectral-roots" => {
            input = std::fs::read_to_string(path).map_err(|e|format!("INTERFACE_READ_ERROR:{e}"))?;
            spectral_roots = true;
        }
        [roots] if roots == "--spectral-roots" => {
            io::stdin().read_to_string(&mut input).map_err(|e|format!("INPUT_READ_ERROR:{e}"))?;
            spectral_roots = true;
        }
        [option, path, inject, name] if option == "--interface" && inject == "--inject" => {
            input =
                std::fs::read_to_string(path).map_err(|e| format!("INTERFACE_READ_ERROR:{e}"))?;
            mutation = Some(name.as_str());
        }
        [option, path, external, k] if option == "--interface" && external == "--external-k" => {
            input =
                std::fs::read_to_string(path).map_err(|e| format!("INTERFACE_READ_ERROR:{e}"))?;
            external_k = Some(k.parse().map_err(|_| "APPROXIMATION_K_INTEGER_REQUIRED")?);
        }
        [external, k] if external == "--external-k" => {
            io::stdin()
                .read_to_string(&mut input)
                .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
            external_k = Some(k.parse().map_err(|_| "APPROXIMATION_K_INTEGER_REQUIRED")?);
        }
        _ => return Err(
            "USAGE:entropy_dichotomy [--interface INPUT_JSON] [--inject MUTATION | --external-k K | --verdict-only | --cyclotomic-characteristic | --spectral-roots]"
                .into(),
        ),
    }
    let input: Value = serde_json::from_str(&input).map_err(|e| format!("INVALID_JSON:{e}"))?;
    if spectral_roots {
        return if input.get("fixtures").is_some() {
            cyclotomic_density::polynomial_roots::report(&input)
        } else {
            cyclotomic_density::polynomial_roots::output(&input)
        };
    }
    if cyclotomic_characteristic {
        return cyclotomic_density::characteristic_report(&input);
    }
    if let Some(mutation) = mutation {
        inject(&input, mutation)?;
        return Err(format!("MUTATION_SURVIVED:{mutation}"));
    }
    if let Some(k) = external_k {
        return if input.get("fixtures").is_some() {
            external_report(&input, k)
        } else {
            evaluate_external(&input, k)
        };
    }
    if verdict_only {
        return verdict_report(&input);
    }
    if input.get("fixtures").is_some() {
        report(&input)
    } else {
        evaluate(&input)
    }
}

fn main() {
    let output = cli();
    match output {
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
