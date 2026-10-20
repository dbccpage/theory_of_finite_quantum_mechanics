use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde_json::value::RawValue;
use serde_json::{json, Value};
use std::cell::RefCell;
use std::collections::BTreeMap;
use std::io::{self, Read};

#[allow(dead_code)]
#[path = "field_factors.rs"]
mod factors;
#[allow(dead_code)]
#[path = "field_squares.rs"]
mod squares;

type Q = BigRational;
type Result<T> = std::result::Result<T, String>;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
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
    fn integer(value: usize) -> Self {
        Self {
            a: Q::from_integer(value.into()),
            b: Q::zero(),
        }
    }
    fn is_zero(&self) -> bool {
        self.a.is_zero() && self.b.is_zero()
    }
    fn add(&self, other: &Self) -> Self {
        if self.is_zero() {
            return other.clone();
        }
        if other.is_zero() {
            return self.clone();
        }
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
        if other.is_zero() {
            return self.clone();
        }
        self.add(&other.neg())
    }
    fn mul(&self, other: &Self, d: u64) -> Self {
        if self.is_zero() || other.is_zero() {
            return Self::zero();
        }
        if self.b.is_zero() {
            return Self {
                a: &self.a * &other.a,
                b: &self.a * &other.b,
            };
        }
        if other.b.is_zero() {
            return Self {
                a: &self.a * &other.a,
                b: &self.b * &other.a,
            };
        }
        Self {
            a: &self.a * &other.a + Q::from_integer(d.into()) * &self.b * &other.b,
            b: &self.a * &other.b + &self.b * &other.a,
        }
    }
    fn inv(&self, d: u64) -> Result<Self> {
        if self.b.is_zero() {
            if self.a.is_zero() {
                return Err("NONZERO_REAL_FIELD_DIVISOR_REQUIRED".into());
            }
            return Ok(Self {
                a: Q::one() / &self.a,
                b: Q::zero(),
            });
        }
        let norm = &self.a * &self.a - Q::from_integer(d.into()) * &self.b * &self.b;
        if norm.is_zero() {
            return Err("NONZERO_REAL_FIELD_DIVISOR_REQUIRED".into());
        }
        Ok(Self {
            a: &self.a / &norm,
            b: -&self.b / &norm,
        })
    }
    fn wire(&self) -> Value {
        json!([
            format!("{}/{}", self.a.numer(), self.a.denom()),
            format!("{}/{}", self.b.numer(), self.b.denom())
        ])
    }
}

fn field(n: u64) -> Result<(u64, &'static str)> {
    match n {
        1 | 3 | 4 => Ok((0, "Q")),
        5 => Ok((5, "Q(sqrt(5))")),
        8 => Ok((2, "Q(sqrt(2))")),
        _ => Err("UNSUPPORTED_CONDUCTOR".into()),
    }
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
    if format!("{}/{}", q.numer(), q.denom()) != text {
        return Err("REDUCED_RATIONAL_REQUIRED".into());
    }
    Ok(q)
}
fn element(value: &Value, d: u64) -> Result<E> {
    let row = value
        .as_array()
        .filter(|row| row.len() == 2)
        .ok_or("COEFFICIENT_PAIR_REQUIRED")?;
    let result = E {
        a: rational(&row[0])?,
        b: rational(&row[1])?,
    };
    if d == 0 && !result.b.is_zero() {
        return Err("RATIONAL_FIELD_RADICAL_COORDINATE_NONZERO".into());
    }
    Ok(result)
}

type Poly = Vec<E>;
type Exp = Vec<usize>;
type Multi = BTreeMap<Exp, E>;
type Vector = Vec<E>;
type Reduced = Vec<(usize, E)>;

fn ptrim(mut p: Poly) -> Poly {
    while p.len() > 1 && p.last().is_some_and(E::is_zero) {
        p.pop();
    }
    if p.is_empty() {
        p.push(E::zero());
    }
    p
}
fn pzero(p: &[E]) -> bool {
    p.len() == 1 && p[0].is_zero()
}
fn pdiv(a: &[E], b: &[E], d: u64) -> Result<(Poly, Poly)> {
    if pzero(b) {
        return Err("ZERO_POLYNOMIAL_DIVISOR".into());
    }
    let mut remainder = a.to_vec();
    let mut quotient = vec![E::zero(); a.len().saturating_sub(b.len()) + 1];
    let inverse = b.last().unwrap().inv(d)?;
    while !pzero(&remainder) && remainder.len() >= b.len() {
        let shift = remainder.len() - b.len();
        let coefficient = remainder.last().unwrap().mul(&inverse, d);
        quotient[shift] = coefficient.clone();
        for (i, value) in b.iter().enumerate() {
            remainder[i + shift] = remainder[i + shift].sub(&coefficient.mul(value, d));
        }
        remainder = ptrim(remainder);
    }
    Ok((ptrim(quotient), remainder))
}
fn pgcd(mut a: Poly, mut b: Poly, d: u64) -> Result<Poly> {
    while !pzero(&b) {
        let remainder = pdiv(&a, &b, d)?.1;
        a = b;
        b = remainder;
    }
    let inverse = a.last().unwrap().inv(d)?;
    Ok(a.iter().map(|x| x.mul(&inverse, d)).collect())
}
fn derivative(p: &[E], d: u64) -> Poly {
    ptrim(
        p.iter()
            .enumerate()
            .skip(1)
            .map(|(i, x)| x.mul(&E::integer(i), d))
            .collect(),
    )
}
fn peval(p: &[E], x: &E, d: u64) -> E {
    p.iter()
        .rev()
        .fold(E::zero(), |sum, coefficient| sum.mul(x, d).add(coefficient))
}
fn polynomial(value: &Value, d: u64) -> Result<Poly> {
    let entries = value
        .as_array()
        .filter(|x| !x.is_empty())
        .ok_or("NONEMPTY_POLYNOMIAL_REQUIRED")?;
    let mut p: Poly = entries
        .iter()
        .map(|x| element(x, d))
        .collect::<Result<_>>()?;
    if p[0].is_zero() {
        return Err("NONZERO_LEADING_COEFFICIENT_REQUIRED".into());
    }
    p.reverse();
    Ok(p)
}
fn polynomial_wire(p: &[E]) -> Value {
    Value::Array(p.iter().rev().map(E::wire).collect())
}
fn vadd(a: &[E], b: &[E]) -> Vector {
    a.iter().zip(b).map(|(x, y)| x.add(y)).collect()
}
fn vscale(a: &[E], scalar: &E, d: u64) -> Vector {
    a.iter().map(|x| x.mul(scalar, d)).collect()
}
fn vzero(a: &[E]) -> bool {
    a.iter().all(E::is_zero)
}
fn accumulate(out: &mut Multi, exponent: Exp, coefficient: E) {
    if coefficient.is_zero() {
        return;
    }
    let value = out
        .get(&exponent)
        .map_or_else(|| coefficient.clone(), |old| old.add(&coefficient));
    if value.is_zero() {
        out.remove(&exponent);
    } else {
        out.insert(exponent, value);
    }
}
fn mshift(p: &Multi, index: usize) -> Multi {
    p.iter()
        .map(|(powers, coefficient)| {
            let mut powers = powers.clone();
            powers[index] += 1;
            (powers, coefficient.clone())
        })
        .collect()
}
fn madd(a: &Multi, b: &Multi) -> Multi {
    let mut out = a.clone();
    for (powers, coefficient) in b {
        accumulate(&mut out, powers.clone(), coefficient.clone());
    }
    out
}
fn enumerate_basis(bounds: &[usize]) -> Vec<Exp> {
    fn extend(bounds: &[usize], prefix: &mut Exp, out: &mut Vec<Exp>) {
        if prefix.len() == bounds.len() {
            out.push(prefix.clone());
            return;
        }
        for power in 0..bounds[prefix.len()] {
            prefix.push(power);
            extend(bounds, prefix, out);
            prefix.pop();
        }
    }
    let mut out = Vec::new();
    extend(bounds, &mut Vec::new(), &mut out);
    out.sort_by(|a, b| a.iter().sum::<usize>().cmp(&b.iter().sum()).then(a.cmp(b)));
    out
}

struct Algebra {
    d: u64,
    polynomial: Poly,
    bounds: Vec<usize>,
    basis: Vec<Exp>,
    indices: BTreeMap<Exp, usize>,
    relations: Vec<Multi>,
    roots: Vec<Vector>,
    reductions: RefCell<BTreeMap<Exp, Reduced>>,
}
impl Algebra {
    fn new(p: &[E], d: u64) -> Result<Self> {
        let degree = p.len().saturating_sub(1);
        if !(2..=5).contains(&degree) {
            return Err("SPLITTING_ALGEBRA_DEGREE_TWO_THROUGH_FIVE_REQUIRED".into());
        }
        let inverse = p.last().unwrap().inv(d)?;
        let p: Poly = p.iter().map(|x| x.mul(&inverse, d)).collect();
        if pgcd(p.clone(), derivative(&p, d), d)?.len() != 1 {
            return Err("SEPARABLE_POLYNOMIAL_REQUIRED".into());
        }
        let bounds: Vec<usize> = (2..=degree).rev().collect();
        let basis = enumerate_basis(&bounds);
        let indices = basis
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, e)| (e, i))
            .collect();
        let zero = vec![0; degree - 1];
        let mut residual: Vec<Multi> = p
            .iter()
            .map(|c| {
                let mut terms = Multi::new();
                accumulate(&mut terms, zero.clone(), c.clone());
                terms
            })
            .collect();
        let mut relations = Vec::new();
        for (index, bound) in bounds.iter().copied().enumerate() {
            let mut replacement = Multi::new();
            for (power, coefficient) in residual[..bound].iter().enumerate() {
                for (powers, value) in coefficient {
                    let mut powers = powers.clone();
                    powers[index] += power;
                    accumulate(&mut replacement, powers, value.neg());
                }
            }
            relations.push(replacement);
            let mut quotient = vec![Multi::new(); bound];
            quotient[bound - 1] = residual[bound].clone();
            for j in (1..bound).rev() {
                quotient[j - 1] = madd(&residual[j], &mshift(&quotient[j], index));
            }
            residual = quotient;
        }
        let mut out = Self {
            d,
            polynomial: p,
            bounds,
            basis,
            indices,
            relations,
            roots: Vec::new(),
            reductions: RefCell::new(BTreeMap::new()),
        };
        for index in 0..degree - 1 {
            let mut exponent = zero.clone();
            exponent[index] = 1;
            out.roots.push(out.monomial(&exponent)?);
        }
        let mut last = out.scalar(&out.polynomial[degree - 1].neg());
        for root in &out.roots {
            last = vadd(&last, &vscale(root, &E::one().neg(), d));
        }
        out.roots.push(last);
        for root in &out.roots {
            if !vzero(&out.evaluate(&out.polynomial, root, &out.unit())?) {
                return Err("TRIANGULAR_ROOT_RELATION_FAILED".into());
            }
        }
        Ok(out)
    }
    fn rank(&self) -> usize {
        self.basis.len()
    }
    fn unit(&self) -> Vector {
        self.scalar(&E::one())
    }
    fn scalar(&self, value: &E) -> Vector {
        let mut out = vec![E::zero(); self.rank()];
        out[0] = value.clone();
        out
    }
    fn reduced(&self, powers: &Exp) -> Result<Reduced> {
        if let Some(value) = self.reductions.borrow().get(powers) {
            return Ok(value.clone());
        }
        let result = if let Some(&index) = self.indices.get(powers) {
            vec![(index, E::one())]
        } else {
            let index = (0..self.bounds.len())
                .rev()
                .find(|&i| powers[i] >= self.bounds[i])
                .ok_or("TRIANGULAR_EXPONENT_SHAPE_FAILED")?;
            let mut rest = powers.clone();
            rest[index] -= self.bounds[index];
            let mut out = BTreeMap::<usize, E>::new();
            for (replacement, coefficient) in &self.relations[index] {
                let next: Exp = rest.iter().zip(replacement).map(|(a, b)| a + b).collect();
                for (basis_index, value) in self.reduced(&next)? {
                    let term = coefficient.mul(&value, self.d);
                    let current = out.entry(basis_index).or_insert_with(E::zero);
                    *current = current.add(&term);
                }
            }
            out.into_iter()
                .filter(|(_, value)| !value.is_zero())
                .collect()
        };
        self.reductions
            .borrow_mut()
            .insert(powers.clone(), result.clone());
        Ok(result)
    }
    fn monomial(&self, powers: &Exp) -> Result<Vector> {
        let mut out = vec![E::zero(); self.rank()];
        for (index, value) in self.reduced(powers)? {
            out[index] = value;
        }
        Ok(out)
    }
    fn mul(&self, a: &[E], b: &[E]) -> Result<Vector> {
        if a.len() != self.rank() || b.len() != self.rank() {
            return Err("ALGEBRA_VECTOR_LENGTH_MISMATCH".into());
        }
        let mut out = vec![E::zero(); self.rank()];
        for (i, x) in a.iter().enumerate().filter(|(_, x)| !x.is_zero()) {
            for (j, y) in b.iter().enumerate().filter(|(_, y)| !y.is_zero()) {
                let coefficient = x.mul(y, self.d);
                let powers = self.basis[i]
                    .iter()
                    .zip(&self.basis[j])
                    .map(|(a, b)| a + b)
                    .collect();
                for (index, value) in self.reduced(&powers)? {
                    out[index] = out[index].add(&coefficient.mul(&value, self.d));
                }
            }
        }
        Ok(out)
    }
    fn evaluate(&self, p: &[E], x: &[E], unit: &[E]) -> Result<Vector> {
        let mut out = vec![E::zero(); self.rank()];
        for coefficient in p.iter().rev() {
            out = vadd(&self.mul(&out, x)?, &vscale(unit, coefficient, self.d));
        }
        Ok(out)
    }
    fn action(&self, permutation: &[usize]) -> Result<Vec<Vector>> {
        let degree = self.polynomial.len() - 1;
        let mut sorted = permutation.to_vec();
        sorted.sort_unstable();
        if sorted != (0..degree).collect::<Vec<_>>() {
            return Err("ROOT_PERMUTATION_REQUIRED".into());
        }
        let mut columns = Vec::with_capacity(self.rank());
        columns.push(self.unit());
        for powers in self.basis.iter().skip(1) {
            let index = powers.iter().position(|x| *x > 0).unwrap();
            let mut previous = powers.clone();
            previous[index] -= 1;
            let previous_index = self.indices[&previous];
            columns.push(self.mul(&columns[previous_index], &self.roots[permutation[index]])?);
        }
        Ok(columns)
    }
    fn apply_action(&self, columns: &[Vector], vector: &[E]) -> Vector {
        let mut out = vec![E::zero(); self.rank()];
        for (column, scalar) in columns.iter().zip(vector).filter(|(_, x)| !x.is_zero()) {
            out = vadd(&out, &vscale(column, scalar, self.d));
        }
        out
    }
}

fn rref(mut rows: Vec<Vector>, width: usize, d: u64) -> Result<(Vec<Vector>, Vec<usize>)> {
    if rows.iter().any(|row| row.len() < width) {
        return Err("MATRIX_SHAPE_MISMATCH".into());
    }
    let mut pivots = Vec::new();
    let mut next = 0;
    for column in 0..width {
        let Some(pivot) = (next..rows.len()).find(|&i| !rows[i][column].is_zero()) else {
            continue;
        };
        rows.swap(next, pivot);
        let inverse = rows[next][column].inv(d)?;
        rows[next] = vscale(&rows[next], &inverse, d);
        let normalized = rows[next].clone();
        for (index, row) in rows.iter_mut().enumerate() {
            if index == next || row[column].is_zero() {
                continue;
            }
            let multiplier = row[column].clone();
            for (value, pivot_value) in row.iter_mut().zip(&normalized) {
                if !pivot_value.is_zero() {
                    *value = value.sub(&multiplier.mul(pivot_value, d));
                }
            }
        }
        pivots.push(column);
        next += 1;
        if next == rows.len() {
            break;
        }
    }
    Ok((rows, pivots))
}
fn nullspace(rows: Vec<Vector>, width: usize, d: u64) -> Result<Vec<Vector>> {
    let (rows, pivots) = rref(rows, width, d)?;
    let mut basis = Vec::new();
    for free in (0..width).filter(|column| !pivots.contains(column)) {
        let mut vector = vec![E::zero(); width];
        vector[free] = E::one();
        for (row, &pivot) in pivots.iter().enumerate() {
            vector[pivot] = rows[row][free].neg();
        }
        basis.push(vector);
    }
    Ok(basis)
}
fn rank(columns: &[Vector], d: u64) -> Result<usize> {
    let width = columns.first().map_or(0, Vec::len);
    Ok(rref(columns.to_vec(), width, d)?.1.len())
}
fn linear_combination(basis: &[Vector], coefficients: &[E], width: usize, d: u64) -> Vector {
    let mut out = vec![E::zero(); width];
    for (column, coefficient) in basis.iter().zip(coefficients).filter(|(_, c)| !c.is_zero()) {
        out = vadd(&out, &vscale(column, coefficient, d));
    }
    out
}
struct Coordinates {
    basis: Vec<Vector>,
    rows: Vec<usize>,
    inverse: Vec<Vector>,
    d: u64,
}
impl Coordinates {
    fn new(basis: &[Vector], d: u64) -> Result<Self> {
        if basis.is_empty() {
            return Err("NONEMPTY_INDEPENDENT_BASIS_REQUIRED".into());
        }
        let (_, rows) = rref(basis.to_vec(), basis[0].len(), d)?;
        let m = basis.len();
        if rows.len() != m {
            return Err("LINEARLY_DEPENDENT_BASIS".into());
        }
        let mut augmented = Vec::with_capacity(m);
        for (i, &row) in rows.iter().enumerate() {
            let mut entries: Vector = basis.iter().map(|column| column[row].clone()).collect();
            entries.extend((0..m).map(|j| if i == j { E::one() } else { E::zero() }));
            augmented.push(entries);
        }
        let (reduced, pivots) = rref(augmented, m, d)?;
        if pivots.len() != m {
            return Err("COORDINATE_MINOR_SINGULAR".into());
        }
        Ok(Self {
            basis: basis.to_vec(),
            rows,
            inverse: reduced.iter().map(|row| row[m..].to_vec()).collect(),
            d,
        })
    }
    fn get(&self, target: &[E]) -> Result<Vector> {
        if target.len() != self.basis[0].len() {
            return Err("COORDINATE_VECTOR_LENGTH_MISMATCH".into());
        }
        let selected: Vector = self.rows.iter().map(|&i| target[i].clone()).collect();
        let coefficients: Vector = self
            .inverse
            .iter()
            .map(|row| {
                row.iter()
                    .zip(&selected)
                    .fold(E::zero(), |sum, (a, b)| sum.add(&a.mul(b, self.d)))
            })
            .collect();
        if linear_combination(&self.basis, &coefficients, target.len(), self.d) != target {
            return Err("VECTOR_OUTSIDE_CERTIFIED_SPAN".into());
        }
        Ok(coefficients)
    }
}
fn fixed_basis(algebra: &Algebra, actions: &[Vec<Vector>]) -> Result<Vec<Vector>> {
    let n = algebra.rank();
    let mut equations = Vec::new();
    for action in actions {
        for row in 0..n {
            equations.push(
                (0..n)
                    .map(|column| {
                        action[column][row].sub(&if row == column { E::one() } else { E::zero() })
                    })
                    .collect(),
            );
        }
    }
    nullspace(equations, n, algebra.d)
}
fn ideal_basis(algebra: &Algebra, idempotent: &[E]) -> Result<Vec<Vector>> {
    let mut original = Vec::new();
    let mut echelon: BTreeMap<usize, Vector> = BTreeMap::new();
    let mut all_columns = Vec::with_capacity(algebra.rank());
    for index in 0..algebra.rank() {
        let mut monomial = vec![E::zero(); algebra.rank()];
        monomial[index] = E::one();
        let column = algebra.mul(idempotent, &monomial)?;
        let mut remainder = column.clone();
        for (&pivot, row) in &echelon {
            if remainder[pivot].is_zero() {
                continue;
            }
            let coefficient = remainder[pivot].clone();
            remainder = vadd(&remainder, &vscale(row, &coefficient.neg(), algebra.d));
        }
        if let Some(pivot) = remainder.iter().position(|x| !x.is_zero()) {
            let normalized = vscale(&remainder, &remainder[pivot].inv(algebra.d)?, algebra.d);
            echelon.insert(pivot, normalized);
            original.push(column.clone());
        }
        all_columns.push(column);
    }
    if original.len() != 20 {
        return Err("LOCAL_IDEAL_DIMENSION_MISMATCH".into());
    }
    let coordinates = Coordinates::new(&original, algebra.d)?;
    for column in &all_columns {
        coordinates.get(column)?;
    }
    Ok(original)
}
fn restricted_fixed_basis(
    algebra: &Algebra,
    basis: &[Vector],
    action: &[Vector],
) -> Result<Vec<Vector>> {
    let coordinates = Coordinates::new(basis, algebra.d)?;
    let columns: Vec<Vector> = basis
        .iter()
        .map(|column| coordinates.get(&algebra.apply_action(action, column)))
        .collect::<Result<_>>()?;
    let m = basis.len();
    let equations: Vec<Vector> = (0..m)
        .map(|row| {
            (0..m)
                .map(|column| {
                    columns[column][row].sub(&if row == column { E::one() } else { E::zero() })
                })
                .collect()
        })
        .collect();
    Ok(nullspace(equations, m, algebra.d)?
        .iter()
        .map(|coefficients| linear_combination(basis, coefficients, algebra.rank(), algebra.d))
        .collect())
}

struct Primitive {
    parameter: BigInt,
    element: Vector,
    polynomial: Poly,
}
fn primitive_element(algebra: &Algebra, basis: &[Vector], parameter: &BigInt) -> Vector {
    let value = E {
        a: Q::from_integer(parameter.clone()),
        b: Q::zero(),
    };
    let mut power = E::one();
    let coefficients: Vector = basis
        .iter()
        .map(|_| {
            let current = power.clone();
            power = power.mul(&value, algebra.d);
            current
        })
        .collect();
    linear_combination(basis, &coefficients, algebra.rank(), algebra.d)
}
fn primitive_polynomial(
    algebra: &Algebra,
    theta: &[E],
    unit: &[E],
    dimension: usize,
) -> Result<Poly> {
    let mut powers = vec![unit.to_vec()];
    for _ in 1..dimension {
        powers.push(algebra.mul(powers.last().unwrap(), theta)?);
    }
    let coordinates =
        Coordinates::new(&powers, algebra.d).map_err(|_| "PRIMITIVE_KRYLOV_RANK_FAILED")?;
    let next = algebra.mul(powers.last().unwrap(), theta)?;
    let coefficients = coordinates.get(&next)?;
    let mut polynomial: Poly = coefficients.iter().map(E::neg).collect();
    polynomial.push(E::one());
    if pgcd(
        polynomial.clone(),
        derivative(&polynomial, algebra.d),
        algebra.d,
    )?
    .len()
        != 1
    {
        return Err("PRIMITIVE_POLYNOMIAL_NOT_SQUAREFREE".into());
    }
    if !vzero(&algebra.evaluate(&polynomial, theta, unit)?) {
        return Err("PRIMITIVE_POLYNOMIAL_RELATION_FAILED".into());
    }
    Ok(polynomial)
}
fn find_primitive(
    algebra: &Algebra,
    basis: &[Vector],
    unit: &[E],
    maximum: usize,
) -> Result<Primitive> {
    Coordinates::new(basis, algebra.d)?.get(unit)?;
    for parameter in 0..=maximum {
        let parameter = BigInt::from(parameter);
        let theta = primitive_element(algebra, basis, &parameter);
        match primitive_polynomial(algebra, &theta, unit, basis.len()) {
            Ok(polynomial) => {
                return Ok(Primitive {
                    parameter,
                    element: theta,
                    polynomial,
                })
            }
            Err(error) if error == "PRIMITIVE_KRYLOV_RANK_FAILED" => {}
            Err(error) => return Err(error),
        }
    }
    Err("PROVED_PRIMITIVE_FAMILY_EXHAUSTED_INVARIANT_FAILURE".into())
}
fn determinant(mut rows: Vec<Vector>, d: u64) -> Result<E> {
    let n = rows.len();
    if rows.iter().any(|row| row.len() != n) {
        return Err("SQUARE_MATRIX_REQUIRED".into());
    }
    let mut result = E::one();
    for column in 0..n {
        let Some(pivot) = (column..n).find(|&row| !rows[row][column].is_zero()) else {
            return Ok(E::zero());
        };
        if pivot != column {
            rows.swap(pivot, column);
            result = result.neg();
        }
        let diagonal = rows[column][column].clone();
        result = result.mul(&diagonal, d);
        let inverse = diagonal.inv(d)?;
        let normalized: Vector = rows[column].iter().map(|x| x.mul(&inverse, d)).collect();
        for row in rows.iter_mut().skip(column + 1) {
            let multiplier = row[column].clone();
            if multiplier.is_zero() {
                continue;
            }
            for index in column..n {
                row[index] = row[index].sub(&multiplier.mul(&normalized[index], d));
            }
        }
    }
    Ok(result)
}
fn discriminant(p: &[E], d: u64) -> Result<E> {
    let derivative = derivative(p, d);
    let n = p.len() - 1;
    let m = derivative.len() - 1;
    let mut rows = vec![vec![E::zero(); n + m]; n + m];
    for shift in 0..m {
        for (index, coefficient) in p.iter().rev().enumerate() {
            rows[shift][shift + index] = coefficient.clone();
        }
    }
    for shift in 0..n {
        for (index, coefficient) in derivative.iter().rev().enumerate() {
            rows[m + shift][shift + index] = coefficient.clone();
        }
    }
    let result = determinant(rows, d)?.mul(&p.last().unwrap().inv(d)?, d);
    Ok(if (n * (n - 1) / 2).is_multiple_of(2) {
        result
    } else {
        result.neg()
    })
}

const T: [usize; 5] = [1, 2, 3, 4, 0];
const U: [usize; 5] = [0, 2, 4, 1, 3];
const SCHEMA: &str = "quintic_splitting_degree_v1";
const ALGORITHM: &str = "EXACT_LOCALIZED_QUINTIC_FIXED_ALGEBRAS";
const SCOPE: &str = "E_QUINTIC_SPLITTING_DEGREE_NO_CARRIER_TRANSPORT_OR_DEPENDENCE";

fn exact_json(value: &Value) -> Result<()> {
    match value {
        Value::Number(number)
            if number.is_f64() || number.to_string().contains(['.', 'e', 'E']) =>
        {
            Err("INEXACT_JSON_NUMBER".into())
        }
        Value::Array(values) => {
            for value in values {
                exact_json(value)?;
            }
            Ok(())
        }
        Value::Object(values) => {
            for value in values.values() {
                exact_json(value)?;
            }
            Ok(())
        }
        _ => Ok(()),
    }
}
fn keys(value: &Value, names: &[&str]) -> Result<()> {
    let entries = value.as_object().ok_or("OBJECT_REQUIRED")?;
    if entries.len() != names.len() || names.iter().any(|name| !entries.contains_key(*name)) {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    Ok(())
}
fn small_integer(value: &Value) -> Result<u64> {
    value
        .as_u64()
        .ok_or_else(|| "EXACT_NONNEGATIVE_INTEGER_REQUIRED".into())
}
fn big_integer(value: &Value) -> Result<BigInt> {
    let number = value
        .as_number()
        .ok_or("EXACT_NONNEGATIVE_INTEGER_REQUIRED")?;
    let text = number.to_string();
    if text.is_empty() || text.contains(['.', 'e', 'E']) {
        return Err("EXACT_NONNEGATIVE_INTEGER_REQUIRED".into());
    }
    let parsed: BigInt = text
        .parse()
        .map_err(|_| "EXACT_NONNEGATIVE_INTEGER_REQUIRED")?;
    if parsed < BigInt::zero() {
        return Err("EXACT_NONNEGATIVE_INTEGER_REQUIRED".into());
    }
    Ok(parsed)
}
fn sparse_wire(vector: &[E]) -> Value {
    Value::Array(
        vector
            .iter()
            .enumerate()
            .filter(|(_, x)| !x.is_zero())
            .map(|(i, x)| json!([i, x.wire()]))
            .collect(),
    )
}
fn sparse(value: &Value, algebra: &Algebra) -> Result<Vector> {
    let rows = value.as_array().ok_or("SPARSE_ALGEBRA_ARRAY_REQUIRED")?;
    let mut out = vec![E::zero(); algebra.rank()];
    let mut previous = None;
    for row in rows {
        let row = row
            .as_array()
            .filter(|x| x.len() == 2)
            .ok_or("SPARSE_ALGEBRA_ROW_REQUIRED")?;
        let index =
            usize::try_from(small_integer(&row[0])?).map_err(|_| "SPARSE_ALGEBRA_INDEX_RANGE")?;
        if index >= algebra.rank() || previous.is_some_and(|old| index <= old) {
            return Err("STRICTLY_INCREASING_ALGEBRA_INDICES_REQUIRED".into());
        }
        let coefficient = element(&row[1], algebra.d)?;
        if coefficient.is_zero() {
            return Err("NONZERO_SPARSE_COEFFICIENT_REQUIRED".into());
        }
        out[index] = coefficient;
        previous = Some(index);
    }
    Ok(out)
}
fn basis_wire(basis: &[Vector]) -> Value {
    Value::Array(basis.iter().map(|v| sparse_wire(v)).collect())
}
fn parse_basis(value: &Value, dimension: usize, algebra: &Algebra) -> Result<Vec<Vector>> {
    let rows = value
        .as_array()
        .filter(|x| x.len() == dimension)
        .ok_or("ALGEBRA_BASIS_CENSUS_MISMATCH")?;
    rows.iter().map(|x| sparse(x, algebra)).collect()
}
fn factor_polynomial(n: u64, p: &[E]) -> Result<Value> {
    let coefficients = polynomial_wire(p);
    let certificate = factors::evaluate_request(
        &json!({"operation":"factor","conductor":n,"coefficients":coefficients}),
    )?;
    factors::validate_factorization(n, &coefficients, &certificate)?;
    Ok(certificate)
}
fn factor_pattern(n: u64, p: &[E], certificate: &Value, d: u64) -> Result<Vec<usize>> {
    factors::validate_factorization(n, &polynomial_wire(p), certificate)?;
    let rows = certificate["factors"]
        .as_array()
        .ok_or("FACTOR_ARRAY_REQUIRED")?;
    let mut pattern = Vec::new();
    for row in rows {
        if small_integer(&row["multiplicity"])? != 1 {
            return Err("RESOLVENT_REPEATED_FACTOR".into());
        }
        pattern.push(polynomial(&row["polynomial"], d)?.len() - 1);
    }
    pattern.sort_unstable();
    Ok(pattern)
}
fn irreducible_input(n: u64, p: &[E], certificate: &Value, d: u64) -> Result<()> {
    let pattern = factor_pattern(n, p, certificate, d)?;
    if p.len() != 6 || pattern != [5] {
        return Err("IRREDUCIBLE_QUINTIC_REQUIRED".into());
    }
    Ok(())
}
fn full_root(p: &[E], certificate: &Value, d: u64, pattern: &[usize]) -> Result<Option<E>> {
    if pattern == [6] {
        return Ok(None);
    }
    if pattern != [1, 5] {
        return Err("FULL_FIXED_FACTOR_PATTERN_INVARIANT_FAILURE".into());
    }
    let mut roots = Vec::new();
    for row in certificate["factors"].as_array().unwrap() {
        let factor = polynomial(&row["polynomial"], d)?;
        if factor.len() == 2 {
            let root = factor[0].neg().mul(&factor[1].inv(d)?, d);
            if !peval(p, &root, d).is_zero() {
                return Err("FULL_FIXED_LINEAR_ROOT_FAILED".into());
            }
            roots.push(root);
        }
    }
    if roots.len() != 1 {
        return Err("UNIQUE_FULL_FIXED_ROOT_REQUIRED".into());
    }
    Ok(roots.pop())
}
fn fixed_record(
    algebra: &Algebra,
    n: u64,
    generators: &[Vec<usize>],
    basis: &[Vector],
    unit: &[E],
    maximum: usize,
) -> Result<Value> {
    let primitive = find_primitive(algebra, basis, unit, maximum)?;
    let factorization = factor_polynomial(n, &primitive.polynomial)?;
    let parameter: Value = serde_json::from_str(&primitive.parameter.to_string())
        .map_err(|_| "INTEGER_PARAMETER_ENCODING_FAILED")?;
    Ok(
        json!({"generators":generators,"dimension":basis.len(),"basis":basis_wire(basis),
        "primitive_parameter":parameter,"primitive_element":sparse_wire(&primitive.element),
        "polynomial":polynomial_wire(&primitive.polynomial),"factorization":factorization}),
    )
}
fn projector(algebra: &Algebra, theta: &[E], p: &[E], root: &E) -> Result<Vector> {
    let (quotient, remainder) = pdiv(p, &[root.neg(), E::one()], algebra.d)?;
    if !pzero(&remainder) {
        return Err("LOCAL_ROOT_POLYNOMIAL_MISMATCH".into());
    }
    let denominator = peval(&quotient, root, algebra.d);
    let inverse = denominator
        .inv(algebra.d)
        .map_err(|_| "LOCAL_PROJECTOR_DENOMINATOR_ZERO")?;
    Ok(vscale(
        &algebra.evaluate(&quotient, theta, &algebra.unit())?,
        &inverse,
        algebra.d,
    ))
}
fn verify_projector(
    algebra: &Algebra,
    e: &[E],
    theta: &[E],
    root: &E,
    actions: &[Vec<Vector>],
) -> Result<()> {
    if algebra.mul(e, e)? != e {
        return Err("LOCAL_IDEMPOTENT_SQUARE_MISMATCH".into());
    }
    if algebra.mul(theta, e)? != vscale(e, root, algebra.d) {
        return Err("LOCAL_IDEMPOTENT_EIGENVALUE_MISMATCH".into());
    }
    for action in actions {
        if algebra.apply_action(action, e) != e {
            return Err("LOCAL_IDEMPOTENT_INVARIANCE_FAILED".into());
        }
    }
    Ok(())
}
fn classified(pattern: Option<&[usize]>, square: bool) -> Result<(&'static str, u64)> {
    match pattern {
        None => Ok(if square { ("A5", 60) } else { ("S5", 120) }),
        Some([1, 1, 1, 1]) if square => Ok(("C5", 5)),
        Some([2, 2]) if square => Ok(("D5", 10)),
        Some([4]) if !square => Ok(("F20", 20)),
        Some([1, 1, 1, 1] | [2, 2] | [4]) => Err("QUINTIC_DISCRIMINANT_PARITY_MISMATCH".into()),
        _ => Err("LOCAL_FIXED_FACTOR_PATTERN_INVARIANT_FAILURE".into()),
    }
}

pub fn quintic_splitting_degree(conductor: &Value, coefficients: &Value) -> Result<Value> {
    exact_json(conductor)?;
    exact_json(coefficients)?;
    let n = small_integer(conductor)?;
    let (d, coefficient_field) = field(n)?;
    let input = polynomial(coefficients, d)?;
    if input.len() != 6 {
        return Err("IRREDUCIBLE_QUINTIC_REQUIRED".into());
    }
    let factorization = factor_polynomial(n, &input)?;
    irreducible_input(n, &input, &factorization, d)?;
    let algebra = Algebra::new(&input, d)?;
    let disc = discriminant(&algebra.polynomial, d)?;
    if disc.is_zero() {
        return Err("QUINTIC_DISCRIMINANT_ZERO".into());
    }
    let square_certificate = squares::square_certificate(n, &disc.wire())?;
    squares::verify_square_certificate(n, &disc.wire(), &square_certificate)?;
    let square = square_certificate["is_square"]
        .as_bool()
        .ok_or("SQUARE_BOOLEAN_REQUIRED")?;
    let actions = vec![algebra.action(&T)?, algebra.action(&U)?];
    let basis = fixed_basis(&algebra, &actions)?;
    if basis.len() != 6 || rank(&basis, d)? != 6 {
        return Err("FULL_FIXED_DIMENSION_MISMATCH".into());
    }
    let full = fixed_record(
        &algebra,
        n,
        &[T.to_vec(), U.to_vec()],
        &basis,
        &algebra.unit(),
        75,
    )?;
    let full_polynomial = polynomial(&full["polynomial"], d)?;
    let pattern = factor_pattern(n, &full_polynomial, &full["factorization"], d)?;
    let root = full_root(&full_polynomial, &full["factorization"], d, &pattern)?;
    let (localized, group, degree) = if let Some(root) = root {
        let theta = sparse(&full["primitive_element"], &algebra)?;
        let e = projector(&algebra, &theta, &full_polynomial, &root)?;
        verify_projector(&algebra, &e, &theta, &root, &actions)?;
        let ideal = ideal_basis(&algebra, &e)?;
        let cyclic_basis = restricted_fixed_basis(&algebra, &ideal, &actions[0])?;
        if cyclic_basis.len() != 4 {
            return Err("LOCAL_FIXED_DIMENSION_MISMATCH".into());
        }
        let cyclic = fixed_record(&algebra, n, &[T.to_vec()], &cyclic_basis, &e, 18)?;
        let local_polynomial = polynomial(&cyclic["polynomial"], d)?;
        let local_pattern = factor_pattern(n, &local_polynomial, &cyclic["factorization"], d)?;
        let (group, degree) = classified(Some(&local_pattern), square)?;
        (
            json!({"root":root.wire(),"idempotent":sparse_wire(&e),"ideal_dimension":20,
            "ideal_basis":basis_wire(&ideal),"cyclic_fixed_algebra":cyclic}),
            group,
            degree,
        )
    } else {
        let (group, degree) = classified(None, square)?;
        (Value::Null, group, degree)
    };
    Ok(
        json!({"schema":SCHEMA,"authority_effect":"None","algorithm":ALGORITHM,"scope":SCOPE,
        "conductor":n,"real_generator_radicand":d,"coefficient_field":coefficient_field,
        "algebra_rank":120,"coefficients":coefficients,"monic_polynomial":polynomial_wire(&algebra.polynomial),
        "factorization":factorization,"discriminant":disc.wire(),"discriminant_square":square_certificate,
        "full_fixed_algebra":full,"localized_fixed_algebra":localized,"galois_group":group,
        "degree_over_real_field":degree}),
    )
}

struct ValidatedFixed {
    theta: Vector,
    polynomial: Poly,
    pattern: Vec<usize>,
}
fn validate_fixed(
    algebra: &Algebra,
    n: u64,
    record: &Value,
    generators: &[Vec<usize>],
    actions: &[Vec<Vector>],
    actual_basis: &[Vector],
    unit: &[E],
) -> Result<ValidatedFixed> {
    keys(
        record,
        &[
            "generators",
            "dimension",
            "basis",
            "primitive_parameter",
            "primitive_element",
            "polynomial",
            "factorization",
        ],
    )?;
    let supplied_generators: Vec<Vec<usize>> = record["generators"]
        .as_array()
        .ok_or("GENERATOR_ARRAY_REQUIRED")?
        .iter()
        .map(|row| {
            row.as_array()
                .ok_or_else(|| "GENERATOR_PERMUTATION_REQUIRED".to_string())?
                .iter()
                .map(|index| {
                    usize::try_from(small_integer(index)?)
                        .map_err(|_| "GENERATOR_INDEX_RANGE".into())
                })
                .collect()
        })
        .collect::<Result<_>>()?;
    if supplied_generators != generators {
        return Err("FIXED_ALGEBRA_GENERATORS_MISMATCH".into());
    }
    let dimension = actual_basis.len();
    if small_integer(&record["dimension"])? != dimension as u64 {
        return Err("FIXED_ALGEBRA_DIMENSION_MISMATCH".into());
    }
    let supplied = parse_basis(&record["basis"], dimension, algebra)?;
    let actual_coordinates = Coordinates::new(actual_basis, algebra.d)?;
    for vector in &supplied {
        for action in actions {
            if algebra.apply_action(action, vector) != *vector {
                return Err("FIXED_BASIS_INVARIANCE_FAILED".into());
            }
        }
        actual_coordinates.get(vector)?;
    }
    let supplied_coordinates = Coordinates::new(&supplied, algebra.d)?;
    for vector in actual_basis {
        supplied_coordinates.get(vector)?;
    }
    supplied_coordinates.get(unit)?;
    let parameter = big_integer(&record["primitive_parameter"])?;
    let theta = sparse(&record["primitive_element"], algebra)?;
    if theta != primitive_element(algebra, &supplied, &parameter) {
        return Err("PRIMITIVE_PARAMETER_ELEMENT_MISMATCH".into());
    }
    let expected_polynomial = primitive_polynomial(algebra, &theta, unit, dimension)?;
    let supplied_polynomial = polynomial(&record["polynomial"], algebra.d)?;
    if supplied_polynomial != expected_polynomial {
        return Err("FIXED_PRIMITIVE_POLYNOMIAL_MISMATCH".into());
    }
    let pattern = factor_pattern(n, &expected_polynomial, &record["factorization"], algebra.d)?;
    Ok(ValidatedFixed {
        theta,
        polynomial: expected_polynomial,
        pattern,
    })
}
fn validate_ideal(algebra: &Algebra, e: &[E], value: &Value) -> Result<Vec<Vector>> {
    let supplied = parse_basis(value, 20, algebra)?;
    let coordinates = Coordinates::new(&supplied, algebra.d)?;
    for vector in &supplied {
        if algebra.mul(e, vector)? != *vector {
            return Err("LOCAL_IDEAL_BASIS_MEMBERSHIP_FAILED".into());
        }
    }
    for index in 0..algebra.rank() {
        let mut monomial = vec![E::zero(); algebra.rank()];
        monomial[index] = E::one();
        coordinates.get(&algebra.mul(e, &monomial)?)?;
    }
    coordinates.get(e)?;
    Ok(supplied)
}
fn admit_quintic_inputs(
    conductor: &Value,
    coefficients: &Value,
    certificate: &Value,
) -> Result<(u64, u64, Poly, &'static str)> {
    exact_json(conductor)?;
    exact_json(coefficients)?;
    exact_json(certificate)?;
    let n = small_integer(conductor)?;
    let (d, coefficient_field) = field(n)?;
    let input = polynomial(coefficients, d)?;
    if input.len() != 6 {
        return Err("IRREDUCIBLE_QUINTIC_REQUIRED".into());
    }
    Ok((n, d, input, coefficient_field))
}
fn validate_quintic_tags(certificate: &Value) -> Result<()> {
    keys(
        certificate,
        &[
            "schema",
            "authority_effect",
            "algorithm",
            "scope",
            "conductor",
            "real_generator_radicand",
            "coefficient_field",
            "algebra_rank",
            "coefficients",
            "monic_polynomial",
            "factorization",
            "discriminant",
            "discriminant_square",
            "full_fixed_algebra",
            "localized_fixed_algebra",
            "galois_group",
            "degree_over_real_field",
        ],
    )?;

    if certificate["schema"] != SCHEMA
        || certificate["authority_effect"] != "None"
        || certificate["algorithm"] != ALGORITHM
        || certificate["scope"] != SCOPE
    {
        return Err("QUINTIC_METADATA_MISMATCH".into());
    }
    Ok(())
}
fn validate_quintic_field_binding(
    certificate: &Value,
    n: u64,
    d: u64,
    coefficient_field: &str,
) -> Result<()> {
    if small_integer(&certificate["conductor"])? != n
        || small_integer(&certificate["real_generator_radicand"])? != d
        || certificate["coefficient_field"] != coefficient_field
        || small_integer(&certificate["algebra_rank"])? != 120
    {
        return Err("QUINTIC_METADATA_MISMATCH".into());
    }
    Ok(())
}
fn admit_quintic_algebra(n: u64, d: u64, input: &[E], certificate: &Value) -> Result<Algebra> {
    if polynomial(&certificate["coefficients"], d)? != input {
        return Err("QUINTIC_INPUT_BINDING_MISMATCH".into());
    }
    irreducible_input(n, input, &certificate["factorization"], d)?;
    let algebra = Algebra::new(input, d)?;
    if polynomial(&certificate["monic_polynomial"], d)? != algebra.polynomial {
        return Err("MONIC_QUINTIC_BINDING_MISMATCH".into());
    }
    Ok(algebra)
}
fn validate_quintic_discriminant(n: u64, algebra: &Algebra, certificate: &Value) -> Result<bool> {
    let disc = discriminant(&algebra.polynomial, algebra.d)?;
    if disc.is_zero() {
        return Err("QUINTIC_DISCRIMINANT_ZERO".into());
    }
    if element(&certificate["discriminant"], algebra.d)? != disc {
        return Err("QUINTIC_DISCRIMINANT_MISMATCH".into());
    }
    squares::verify_square_certificate(n, &disc.wire(), &certificate["discriminant_square"])?;
    certificate["discriminant_square"]["is_square"]
        .as_bool()
        .ok_or("SQUARE_BOOLEAN_REQUIRED".into())
}
struct ValidatedQuinticFixed {
    full: ValidatedFixed,
    actions: Vec<Vec<Vector>>,
    root: Option<E>,
}
fn validate_quintic_fixed(
    algebra: &Algebra,
    n: u64,
    certificate: &Value,
) -> Result<ValidatedQuinticFixed> {
    let actions = vec![algebra.action(&T)?, algebra.action(&U)?];
    let basis = fixed_basis(algebra, &actions)?;
    if basis.len() != 6 || rank(&basis, algebra.d)? != 6 {
        return Err("FULL_FIXED_DIMENSION_MISMATCH".into());
    }
    let record = &certificate["full_fixed_algebra"];
    let full = validate_fixed(
        algebra,
        n,
        record,
        &[T.to_vec(), U.to_vec()],
        &actions,
        &basis,
        &algebra.unit(),
    )?;
    let root = full_root(
        &full.polynomial,
        &record["factorization"],
        algebra.d,
        &full.pattern,
    )?;
    Ok(ValidatedQuinticFixed {
        full,
        actions,
        root,
    })
}
fn validate_local_projector(
    algebra: &Algebra,
    fixed: &ValidatedQuinticFixed,
    root: &E,
    local: &Value,
) -> Result<Vector> {
    keys(
        local,
        &[
            "root",
            "idempotent",
            "ideal_dimension",
            "ideal_basis",
            "cyclic_fixed_algebra",
        ],
    )?;
    if element(&local["root"], algebra.d)? != *root {
        return Err("LOCAL_ROOT_BINDING_MISMATCH".into());
    }
    let e = sparse(&local["idempotent"], algebra)?;
    if projector(algebra, &fixed.full.theta, &fixed.full.polynomial, root)? != e {
        return Err("LOCAL_PROJECTOR_FORMULA_MISMATCH".into());
    }
    verify_projector(algebra, &e, &fixed.full.theta, root, &fixed.actions)?;
    Ok(e)
}
fn validate_local_cyclic(
    algebra: &Algebra,
    n: u64,
    local: &Value,
    e: &[E],
    actions: &[Vec<Vector>],
) -> Result<ValidatedFixed> {
    if small_integer(&local["ideal_dimension"])? != 20 {
        return Err("LOCAL_IDEAL_DIMENSION_MISMATCH".into());
    }
    let ideal = validate_ideal(algebra, e, &local["ideal_basis"])?;
    let basis = restricted_fixed_basis(algebra, &ideal, &actions[0])?;
    if basis.len() != 4 {
        return Err("LOCAL_FIXED_DIMENSION_MISMATCH".into());
    }
    validate_fixed(
        algebra,
        n,
        &local["cyclic_fixed_algebra"],
        &[T.to_vec()],
        &actions[..1],
        &basis,
        e,
    )
}
fn validate_quintic_classification(
    algebra: &Algebra,
    n: u64,
    certificate: &Value,
    fixed: &ValidatedQuinticFixed,
    square: bool,
) -> Result<(&'static str, u64)> {
    let Some(root) = &fixed.root else {
        if !certificate["localized_fixed_algebra"].is_null() {
            return Err("UNUSED_LOCALIZED_ALGEBRA_MUST_BE_NULL".into());
        }
        return classified(None, square);
    };
    let local = &certificate["localized_fixed_algebra"];
    let e = validate_local_projector(algebra, fixed, root, local)?;
    let cyclic = validate_local_cyclic(algebra, n, local, &e, &fixed.actions)?;
    classified(Some(&cyclic.pattern), square)
}
fn validate_quintic_result(certificate: &Value, group: &str, degree: u64) -> Result<()> {
    if certificate["galois_group"] != group {
        return Err("QUINTIC_GALOIS_GROUP_MISMATCH".into());
    }
    if small_integer(&certificate["degree_over_real_field"])? != degree {
        return Err("QUINTIC_SPLITTING_DEGREE_MISMATCH".into());
    }
    Ok(())
}
pub fn validate_quintic_degree(
    conductor: &Value,
    coefficients: &Value,
    certificate: &Value,
) -> Result<()> {
    let (n, d, input, coefficient_field) =
        admit_quintic_inputs(conductor, coefficients, certificate)?;
    validate_quintic_tags(certificate)?;
    validate_quintic_field_binding(certificate, n, d, coefficient_field)?;
    let algebra = admit_quintic_algebra(n, d, &input, certificate)?;
    let square = validate_quintic_discriminant(n, &algebra, certificate)?;
    let fixed = validate_quintic_fixed(&algebra, n, certificate)?;
    let (group, degree) =
        validate_quintic_classification(&algebra, n, certificate, &fixed, square)?;
    validate_quintic_result(certificate, group, degree)
}

pub fn evaluate_request(request: &Value) -> Result<Value> {
    exact_json(request)?;
    keys(request, &["operation", "conductor", "coefficients"])?;
    if request["operation"] != "quintic_splitting_degree" {
        return Err("QUINTIC_OPERATION_REQUIRED".into());
    }
    quintic_splitting_degree(&request["conductor"], &request["coefficients"])
}
fn raw_number_admission(input: &str) -> Result<()> {
    let mut quoted = false;
    let mut escaped = false;
    let mut number = false;
    for byte in input.bytes() {
        if quoted {
            if escaped {
                escaped = false;
            } else if byte == b'\\' {
                escaped = true;
            } else if byte == b'"' {
                quoted = false;
            }
            continue;
        }
        if byte == b'"' {
            quoted = true;
            number = false;
            continue;
        }
        if byte.is_ascii_digit() || byte == b'-' {
            number = true;
        } else if number && matches!(byte, b'.' | b'e' | b'E') {
            return Err("RAW_INEXACT_JSON_NUMBER".into());
        } else {
            number = false;
        }
    }
    Ok(())
}
fn ascii_json(value: &Value) -> Result<String> {
    let encoded = serde_json::to_string(value).map_err(|e| format!("JSON_OUTPUT_ERROR:{e}"))?;
    let mut output = String::new();
    for character in encoded.chars() {
        if character as u32 >= 0x7f {
            for unit in character.encode_utf16(&mut [0; 2]) {
                output.push_str(&format!("\\u{unit:04x}"));
            }
        } else {
            output.push(character);
        }
    }
    Ok(output)
}
fn run() -> Result<Value> {
    if std::env::args().len() != 1 {
        return Err("USAGE:quintic_splitting_algebras < REQUEST_JSON".into());
    }
    let mut input = String::new();
    io::stdin()
        .read_to_string(&mut input)
        .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
    raw_number_admission(&input)?;
    let fields: BTreeMap<String, Box<RawValue>> =
        serde_json::from_str(&input).map_err(|e| format!("INVALID_JSON:{e}"))?;
    if fields.len() != 3
        || ["operation", "conductor", "coefficients"]
            .iter()
            .any(|key| !fields.contains_key(*key))
    {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    let operation: String = serde_json::from_str(fields["operation"].get())
        .map_err(|_| "QUINTIC_OPERATION_REQUIRED")?;
    let conductor: u64 = serde_json::from_str(fields["conductor"].get())
        .map_err(|_| "INTEGER_CONDUCTOR_REQUIRED")?;
    let coefficients: Vec<[String; 2]> = serde_json::from_str(fields["coefficients"].get())
        .map_err(|_| "CANONICAL_RATIONAL_STRING_REQUIRED")?;
    evaluate_request(
        &json!({"operation":operation,"conductor":conductor,"coefficients":coefficients}),
    )
}
fn main() {
    match run().and_then(|value| ascii_json(&value)) {
        Ok(output) => println!("{output}"),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}

#[cfg(test)]
pub struct AlgebraControl(Algebra);
#[cfg(test)]
impl AlgebraControl {
    pub fn new(conductor: u64, coefficients: &Value) -> Result<Self> {
        let (d, _) = field(conductor)?;
        Ok(Self(Algebra::new(&polynomial(coefficients, d)?, d)?))
    }
    pub fn dimension(&self) -> usize {
        self.0.rank()
    }
    pub fn basis(&self) -> Vec<Vec<usize>> {
        self.0.basis.clone()
    }
    pub fn roots(&self) -> Vec<Value> {
        self.0.roots.iter().map(|x| sparse_wire(x)).collect()
    }
    pub fn unit(&self) -> Value {
        sparse_wire(&self.0.unit())
    }
    pub fn mul(&self, a: &Value, b: &Value) -> Result<Value> {
        Ok(sparse_wire(
            &self.0.try_mul(&sparse(a, &self.0)?, &sparse(b, &self.0)?).unwrap()?,
        ))
    }
    pub fn add(&self, a: &Value, b: &Value) -> Result<Value> {
        Ok(sparse_wire(&vadd(
            &sparse(a, &self.0)?,
            &sparse(b, &self.0)?,
        )))
    }
    pub fn scale(&self, a: &Value, c: &Value) -> Result<Value> {
        Ok(sparse_wire(&vscale(
            &sparse(a, &self.0)?,
            &element(c, self.0.d)?,
            self.0.d,
        )))
    }
    pub fn action(&self, permutation: &[usize], value: &Value) -> Result<Value> {
        let matrix = self.0.action(permutation)?;
        Ok(sparse_wire(
            &self.0.apply_action(&matrix, &sparse(value, &self.0)?),
        ))
    }
    pub fn fixed_primitive(&self, generators: &[Vec<usize>]) -> Result<Value> {
        let matrices = generators
            .iter()
            .map(|g| self.0.action(g))
            .collect::<Result<Vec<_>>>()?;
        let basis = fixed_basis(&self.0, &matrices)?;
        let m = basis.len();
        let primitive = find_primitive(&self.0, &basis, &self.0.unit(), (m - 1) * m * (m - 1) / 2)?;
        Ok(
            json!({"dimension":m,"basis":basis_wire(&basis),"primitive_element":sparse_wire(&primitive.element),
            "polynomial":polynomial_wire(&primitive.polynomial)}),
        )
    }
    pub fn local_projector(&self, theta: &Value, p: &Value, r: &Value) -> Result<Value> {
        let theta = sparse(theta, &self.0)?;
        let p = polynomial(p, self.0.d)?;
        let r = element(r, self.0.d)?;
        let e = projector(&self.0, &theta, &p, &r)?;
        let ideal = ideal_basis(&self.0, &e)?;
        let t = self.0.action(&T)?;
        let cyclic = restricted_fixed_basis(&self.0, &ideal, &t)?;
        Ok(
            json!({"idempotent":sparse_wire(&e),"ideal_dimension":ideal.len(),"cyclic_dimension":cyclic.len()}),
        )
    }
}
#[cfg(test)]
pub fn fold_control(values: &Value, self_join: bool) -> Result<Value> {
    let entries = values.as_array().ok_or("ARRAY_REQUIRED")?;
    let values: Vec<Q> = entries.iter().map(rational).collect::<Result<_>>()?;
    let sum = if self_join {
        let mut sum = BigInt::zero();
        for (i, a) in values.iter().enumerate() {
            for (j, b) in values.iter().enumerate() {
                if i != j {
                    sum += a.numer() * b.denom();
                }
            }
        }
        Q::from_integer(sum)
    } else {
        values.iter().fold(Q::zero(), |a, b| a + b)
    };
    Ok(json!(format!("{}/{}", sum.numer(), sum.denom())))
}
#[cfg(test)]
pub fn localized_unit_control(
    conductor: u64,
    coefficients: &Value,
    certificate: &Value,
    wrong_unit: bool,
) -> Result<()> {
    let (d, _) = field(conductor)?;
    let algebra = Algebra::new(&polynomial(coefficients, d)?, d)?;
    let local = &certificate["localized_fixed_algebra"];
    let theta = sparse(
        &local["cyclic_fixed_algebra"]["primitive_element"],
        &algebra,
    )?;
    let unit = if wrong_unit {
        algebra.unit()
    } else {
        sparse(&local["idempotent"], &algebra)?
    };
    primitive_polynomial(&algebra, &theta, &unit, 4).map(|_| ())
}

#[cfg(test)]
mod quintic_validation_challenges {
    use super::*;
    fn challenge_case(values: [i64; 6], group: &str, degree: u64) -> (Value, Value) {
        let coefficients = Value::Array(
            values
                .into_iter()
                .map(|n| json!([format!("{n}/1"), "0/1"]))
                .collect(),
        );
        let certificate = quintic_splitting_degree(&json!(1), &coefficients)
            .expect("classical irreducible fixture");
        assert_eq!(certificate["galois_group"], group);
        assert_eq!(certificate["degree_over_real_field"], degree);
        assert_eq!(
            validate_quintic_degree(&json!(1), &coefficients, &certificate),
            Ok(())
        );
        for key in [
            "schema",
            "authority_effect",
            "algorithm",
            "scope",
            "conductor",
            "real_generator_radicand",
            "coefficient_field",
            "algebra_rank",
        ] {
            let mut invalid = certificate.clone();
            invalid[key] = Value::Null;
            assert!(
                validate_quintic_degree(&json!(1), &coefficients, &invalid).is_err(),
                "{key}"
            );
        }
        (coefficients, certificate)
    }
    #[test]
    fn localized_frobenius_certificate_and_deep_bindings() {
        let (coefficients, certificate) = challenge_case([1, 0, 0, 0, 0, -2], "F20", 20);
        let mut invalid = certificate.clone();
        invalid["galois_group"] = json!("S5");
        assert_eq!(
            validate_quintic_degree(&json!(1), &coefficients, &invalid),
            Err("QUINTIC_GALOIS_GROUP_MISMATCH".into())
        );
        let mut invalid = certificate.clone();
        invalid["degree_over_real_field"] = json!(120);
        assert_eq!(
            validate_quintic_degree(&json!(1), &coefficients, &invalid),
            Err("QUINTIC_SPLITTING_DEGREE_MISMATCH".into())
        );
        let mut invalid = certificate;
        invalid["localized_fixed_algebra"]["ideal_dimension"] = json!(21);
        assert_eq!(
            validate_quintic_degree(&json!(1), &coefficients, &invalid),
            Err("LOCAL_IDEAL_DIMENSION_MISMATCH".into())
        );
    }
    #[test]
    fn nonlocalized_symmetric_certificate_is_verified() {
        challenge_case([1, 0, 0, 0, -1, -1], "S5", 120);
    }
    #[test]
    fn square_discriminant_alternating_certificate_is_verified() {
        challenge_case([1, 0, 0, 0, 20, 16], "A5", 60);
    }
}
