use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde_json::{json, Value};
use std::io::{self, Read};

type Q = BigRational;
type P = Vec<Q>;
type Z = Vec<BigInt>;
type Result<T> = std::result::Result<T, String>;

fn ztrim(mut p: Z) -> Z {
    while p.len() > 1 && p.last().is_some_and(Zero::is_zero) {
        p.pop();
    }
    if p.is_empty() {
        p.push(BigInt::zero());
    }
    p
}
fn qtrim(mut p: P) -> P {
    while p.len() > 1 && p.last().is_some_and(Zero::is_zero) {
        p.pop();
    }
    if p.is_empty() {
        p.push(Q::zero());
    }
    p
}
fn zzero(p: &[BigInt]) -> bool {
    p.len() == 1 && p[0].is_zero()
}
fn qzero(p: &[Q]) -> bool {
    p.len() == 1 && p[0].is_zero()
}
fn qone(p: &[Q]) -> bool {
    p.len() == 1 && p[0].is_one()
}
fn modulo(a: &BigInt, m: &BigInt) -> BigInt {
    ((a % m) + m) % m
}
fn gcd_integer(mut a: BigInt, mut b: BigInt) -> BigInt {
    while !b.is_zero() {
        let r = a % &b;
        a = b;
        b = r;
    }
    a.abs()
}
fn power(mut a: BigInt, mut n: usize) -> BigInt {
    let mut out = BigInt::one();
    while n != 0 {
        if n % 2 == 1 {
            out *= &a;
        }
        n /= 2;
        if n != 0 {
            a = &a * &a;
        }
    }
    out
}
fn ceil_integer_root(value: &BigInt, degree: usize) -> Result<BigInt> {
    if value.is_negative() || degree == 0 {
        return Err("NONNEGATIVE_INTEGER_AND_POSITIVE_ROOT_DEGREE_REQUIRED".into());
    }
    if value <= &BigInt::one() || degree == 1 {
        return Ok(value.clone());
    }
    let bits =
        usize::try_from(value.bits()).map_err(|_| "INTEGER_ROOT_BIT_LENGTH_EXCEEDS_USIZE")?;
    if degree >= bits {
        return Ok(BigInt::from(2));
    }
    let mut root = BigInt::one() << ((bits - 1) / degree + 1);
    let degree_integer = BigInt::from(degree);
    loop {
        let next = (BigInt::from(degree - 1) * &root + value / power(root.clone(), degree - 1))
            / &degree_integer;
        if next >= root {
            break;
        }
        root = next;
    }
    let root_power = power(root.clone(), degree);
    if root_power > *value || power(&root + 1, degree) <= *value {
        return Err("INTEGER_ROOT_BRACKET_FAILED".into());
    }
    Ok(if root_power == *value { root } else { root + 1 })
}
fn verify_root_radius(p: &[BigInt], radius: &BigInt) -> Result<()> {
    if p.len() < 2 || !p.last().unwrap().is_one() || radius.is_negative() {
        return Err("MONIC_POLYNOMIAL_AND_NONNEGATIVE_RADIUS_REQUIRED".into());
    }
    let lower = &p[..p.len() - 1];
    if radius.is_zero() {
        return if lower.iter().all(Zero::is_zero) {
            Ok(())
        } else {
            Err("ROOT_RADIUS_DOMINANCE_FAILED".into())
        };
    }
    let lower_magnitude = lower.iter().rev().fold(BigInt::zero(), |sum, coefficient| {
        sum * radius + coefficient.abs()
    });
    if lower_magnitude >= power(radius.clone(), p.len() - 1) {
        return Err("ROOT_RADIUS_DOMINANCE_FAILED".into());
    }
    Ok(())
}
fn root_radius(p: &[BigInt]) -> Result<BigInt> {
    if p.len() < 2 || !p.last().unwrap().is_one() {
        return Err("MONIC_NONCONSTANT_INTEGER_POLYNOMIAL_REQUIRED".into());
    }
    let degree = p.len() - 1;
    let mut maximum = BigInt::zero();
    let mut root_maximum = BigInt::zero();
    for (i, coefficient) in p[..degree].iter().enumerate() {
        let absolute = coefficient.abs();
        root_maximum = root_maximum.max(ceil_integer_root(&absolute, degree - i)?);
        maximum = maximum.max(absolute);
    }
    let radius = (maximum + BigInt::one()).min(root_maximum * BigInt::from(2));
    verify_root_radius(p, &radius)?;
    Ok(radius)
}
fn coefficient_bound(p: &[BigInt]) -> Result<BigInt> {
    Ok(power(root_radius(p)? + 1, (p.len() - 1) / 2))
}
fn verify_recombination_modulus(bound: &BigInt, modulus: &BigInt) -> Result<()> {
    if bound.is_negative() || modulus <= &(2 * bound) {
        return Err("RECOMBINATION_MODULUS_MUST_EXCEED_TWICE_BOUND".into());
    }
    Ok(())
}
fn zmul(a: &[BigInt], b: &[BigInt]) -> Z {
    let mut out = vec![BigInt::zero(); a.len() + b.len() - 1];
    for (i, x) in a.iter().enumerate() {
        for (j, y) in b.iter().enumerate() {
            out[i + j] += x * y;
        }
    }
    ztrim(out)
}
fn qmul(a: &[Q], b: &[Q]) -> P {
    let mut out = vec![Q::zero(); a.len() + b.len() - 1];
    for (i, x) in a.iter().enumerate() {
        for (j, y) in b.iter().enumerate() {
            out[i + j] += x * y;
        }
    }
    qtrim(out)
}
fn qdiv(a: &[Q], b: &[Q]) -> Result<(P, P)> {
    if qzero(b) {
        return Err("ZERO_POLYNOMIAL_DIVISOR".into());
    }
    let mut r = a.to_vec();
    let mut quotient = vec![Q::zero(); a.len().saturating_sub(b.len()) + 1];
    while !qzero(&r) && r.len() >= b.len() {
        let shift = r.len() - b.len();
        let coefficient = r.last().unwrap() / b.last().unwrap();
        quotient[shift] = coefficient.clone();
        for (j, c) in b.iter().enumerate() {
            r[j + shift] -= &coefficient * c;
        }
        r = qtrim(r);
    }
    Ok((qtrim(quotient), r))
}
fn qquotient(a: &[Q], b: &[Q]) -> Result<P> {
    let (q, r) = qdiv(a, b)?;
    if !qzero(&r) {
        return Err("NONEXACT_RATIONAL_POLYNOMIAL_DIVISION".into());
    }
    Ok(q)
}
fn qmonic(p: &[Q]) -> P {
    let lead = p.last().unwrap();
    p.iter().map(|x| x / lead).collect()
}
fn qgcd(mut a: P, mut b: P) -> Result<P> {
    while !qzero(&b) {
        let r = qdiv(&a, &b)?.1;
        a = b;
        b = r;
    }
    Ok(qmonic(&a))
}
fn derivative(p: &[Q]) -> P {
    qtrim(
        p.iter()
            .enumerate()
            .skip(1)
            .map(|(i, c)| c * Q::from_integer(i.into()))
            .collect(),
    )
}
fn squarefree(p: &[Q]) -> Result<Vec<(P, usize)>> {
    if p.len() == 1 {
        return Ok(Vec::new());
    }
    let p = qmonic(p);
    let mut repeated = qgcd(p.clone(), derivative(&p))?;
    let mut remaining = qquotient(&p, &repeated)?;
    let mut multiplicity = 1;
    let mut out = Vec::new();
    while !qone(&remaining) {
        let common = qgcd(remaining.clone(), repeated.clone())?;
        let factor = qquotient(&remaining, &common)?;
        if !qone(&factor) {
            out.push((factor, multiplicity));
        }
        remaining = common.clone();
        repeated = qquotient(&repeated, &common)?;
        multiplicity += 1;
    }
    if !qone(&repeated) {
        return Err("SQUAREFREE_RECONSTRUCTION_FAILED".into());
    }
    Ok(out)
}

fn freduce(p: &[BigInt], prime: &BigInt) -> Z {
    ztrim(p.iter().map(|x| modulo(x, prime)).collect())
}
fn finverse(a: &BigInt, prime: &BigInt) -> Result<BigInt> {
    let (mut r0, mut r1) = (prime.clone(), modulo(a, prime));
    let (mut t0, mut t1) = (BigInt::zero(), BigInt::one());
    while !r1.is_zero() {
        let q = &r0 / &r1;
        (r0, r1) = (r1.clone(), r0 - &q * r1);
        (t0, t1) = (t1.clone(), t0 - &q * t1);
    }
    if !r0.is_one() {
        return Err("FINITE_FIELD_NONINVERTIBLE".into());
    }
    Ok(modulo(&t0, prime))
}
fn fsub(a: &[BigInt], b: &[BigInt], prime: &BigInt) -> Z {
    let mut out = vec![BigInt::zero(); a.len().max(b.len())];
    for (i, x) in a.iter().enumerate() {
        out[i] += x;
    }
    for (i, x) in b.iter().enumerate() {
        out[i] -= x;
    }
    freduce(&out, prime)
}
fn fmul(a: &[BigInt], b: &[BigInt], prime: &BigInt) -> Z {
    freduce(&zmul(a, b), prime)
}
fn fdiv(a: &[BigInt], b: &[BigInt], prime: &BigInt) -> Result<(Z, Z)> {
    if zzero(b) {
        return Err("ZERO_FINITE_FIELD_POLYNOMIAL_DIVISOR".into());
    }
    let mut r = freduce(a, prime);
    let mut quotient = vec![BigInt::zero(); a.len().saturating_sub(b.len()) + 1];
    let inv = finverse(b.last().unwrap(), prime)?;
    while !zzero(&r) && r.len() >= b.len() {
        let shift = r.len() - b.len();
        let coefficient = modulo(&(r.last().unwrap() * &inv), prime);
        quotient[shift] = coefficient.clone();
        for (j, c) in b.iter().enumerate() {
            r[j + shift] -= &coefficient * c;
        }
        r = freduce(&r, prime);
    }
    Ok((ztrim(quotient), r))
}
fn fmonic(p: &[BigInt], prime: &BigInt) -> Result<Z> {
    let inv = finverse(p.last().unwrap(), prime)?;
    Ok(freduce(&p.iter().map(|x| x * &inv).collect::<Z>(), prime))
}
fn fgcd(mut a: Z, mut b: Z, prime: &BigInt) -> Result<Z> {
    while !zzero(&b) {
        let r = fdiv(&a, &b, prime)?.1;
        a = b;
        b = r;
    }
    fmonic(&a, prime)
}
fn fpoly_inverse(a: &[BigInt], modulus: &[BigInt], prime: &BigInt) -> Result<Z> {
    let (mut r0, mut r1) = (modulus.to_vec(), fdiv(a, modulus, prime)?.1);
    let (mut t0, mut t1) = (vec![BigInt::zero()], vec![BigInt::one()]);
    while !zzero(&r1) {
        let (q, r) = fdiv(&r0, &r1, prime)?;
        let t = fsub(&t0, &fmul(&q, &t1, prime), prime);
        (r0, r1) = (r1, r);
        (t0, t1) = (t1, t);
    }
    if r0.len() != 1 {
        return Err("HENSEL_FACTORS_NOT_COPRIME".into());
    }
    let inv = finverse(&r0[0], prime)?;
    fdiv(
        &freduce(&t0.iter().map(|x| x * &inv).collect::<Z>(), prime),
        modulus,
        prime,
    )
    .map(|(_, r)| r)
}
fn fpow(mut base: Z, exponent: &BigInt, modulus: &[BigInt], prime: &BigInt) -> Result<Z> {
    let mut exponent = exponent.clone();
    let mut out = vec![BigInt::one()];
    while exponent > BigInt::zero() {
        if (&exponent % 2_u8).is_one() {
            out = fdiv(&fmul(&out, &base, prime), modulus, prime)?.1;
        }
        exponent /= 2_u8;
        if !exponent.is_zero() {
            base = fdiv(&fmul(&base, &base, prime), modulus, prime)?.1;
        }
    }
    Ok(out)
}
fn is_prime(n: &BigInt) -> bool {
    if n < &BigInt::from(2) {
        return false;
    }
    let mut divisor = BigInt::from(2);
    while &divisor * &divisor <= *n {
        if (n % &divisor).is_zero() {
            return false;
        }
        divisor += 1;
    }
    true
}
fn good_prime(p: &[BigInt], prime: &BigInt) -> Result<bool> {
    if !is_prime(prime) {
        return Ok(false);
    }
    let reduction = freduce(p, prime);
    if reduction.len() != p.len() {
        return Ok(false);
    }
    let derivative = ztrim(
        reduction
            .iter()
            .enumerate()
            .skip(1)
            .map(|(i, c)| modulo(&(c * BigInt::from(i)), prime))
            .collect(),
    );
    Ok(fgcd(reduction, derivative, prime)?.len() == 1)
}
fn choose_prime(p: &[BigInt]) -> Result<BigInt> {
    let mut prime = BigInt::from(2);
    while !good_prime(p, &prime)? {
        prime += 1;
    }
    Ok(prime)
}
fn nullspace(mut matrix: Vec<Z>, prime: &BigInt) -> Result<Vec<Z>> {
    let n = matrix.len();
    let mut pivot_columns = Vec::new();
    let mut row = 0;
    for col in 0..n {
        let Some(pivot) = (row..n).find(|&r| !matrix[r][col].is_zero()) else {
            continue;
        };
        matrix.swap(row, pivot);
        let inv = finverse(&matrix[row][col], prime)?;
        for value in &mut matrix[row] {
            *value = modulo(&(&*value * &inv), prime);
        }
        let normalized = matrix[row].clone();
        for (r, entries) in matrix.iter_mut().enumerate() {
            if r == row {
                continue;
            }
            let multiplier = entries[col].clone();
            for (value, pivot_value) in entries.iter_mut().zip(&normalized) {
                *value = modulo(&(&*value - &multiplier * pivot_value), prime);
            }
        }
        pivot_columns.push(col);
        row += 1;
    }
    let mut basis = Vec::new();
    for free in (0..n).filter(|c| !pivot_columns.contains(c)) {
        let mut vector = vec![BigInt::zero(); n];
        vector[free] = BigInt::one();
        for (r, &pivot) in pivot_columns.iter().enumerate() {
            vector[pivot] = modulo(&(-&matrix[r][free]), prime);
        }
        basis.push(ztrim(vector));
    }
    Ok(basis)
}
fn berlekamp(p: &[BigInt], prime: &BigInt) -> Result<Vec<Z>> {
    if !good_prime(p, prime)? {
        return Err("BAD_REDUCTION_PRIME".into());
    }
    let p = freduce(p, prime);
    let n = p.len() - 1;
    let xp = fpow(vec![BigInt::zero(), BigInt::one()], prime, &p, prime)?;
    let mut matrix = vec![vec![BigInt::zero(); n]; n];
    let mut column = vec![BigInt::one()];
    for col in 0..n {
        for (row, entries) in matrix.iter_mut().enumerate() {
            entries[col] = column.get(row).cloned().unwrap_or_default();
            if row == col {
                entries[col] = modulo(&(&entries[col] - 1), prime);
            }
        }
        column = fdiv(&fmul(&column, &xp, prime), &p, prime)?.1;
    }
    let basis = nullspace(matrix, prime)?;
    let expected = basis.len();
    let mut factors = vec![p.clone()];
    for vector in basis {
        let mut scalar = BigInt::zero();
        while &scalar < prime && factors.len() < expected {
            let mut shifted = vector.clone();
            shifted[0] = modulo(&(&shifted[0] - &scalar), prime);
            let mut next = Vec::new();
            for factor in factors {
                let divisor = fgcd(factor.clone(), shifted.clone(), prime)?;
                if divisor.len() > 1 && divisor.len() < factor.len() {
                    let (other, remainder) = fdiv(&factor, &divisor, prime)?;
                    if !zzero(&remainder) {
                        return Err("BERLEKAMP_DIVISION_FAILED".into());
                    }
                    next.push(divisor);
                    next.push(other);
                } else {
                    next.push(factor);
                }
            }
            factors = next;
            scalar += 1;
        }
        if factors.len() == expected {
            break;
        }
    }
    if factors.len() != expected {
        return Err("BERLEKAMP_FACTOR_CENSUS_FAILED".into());
    }
    let product = factors
        .iter()
        .fold(vec![BigInt::one()], |a, b| fmul(&a, b, prime));
    if product != freduce(p.as_slice(), prime) {
        return Err("BERLEKAMP_PRODUCT_FAILED".into());
    }
    Ok(factors)
}

fn verify_lift(p: &[BigInt], factors: &[Z], modulus: &BigInt) -> Result<()> {
    if factors
        .iter()
        .any(|f| f.len() < 2 || !f.last().unwrap().is_one())
    {
        return Err("HENSEL_MONIC_FACTOR_FAILED".into());
    }
    let product = factors
        .iter()
        .fold(vec![BigInt::one()], |a, b| fmul(&a, b, modulus));
    if product != freduce(p, modulus) {
        return Err("HENSEL_PRODUCT_CONGRUENCE_FAILED".into());
    }
    Ok(())
}
fn lift(p: &[BigInt], initial: &[Z], prime: &BigInt, bound: &BigInt) -> Result<(Vec<Z>, BigInt)> {
    let mut factors = initial.to_vec();
    let mut modulus = prime.clone();
    verify_lift(p, &factors, &modulus)?;
    let mut inverses = Vec::new();
    for (i, factor) in initial.iter().enumerate() {
        let complement = initial
            .iter()
            .enumerate()
            .filter(|(j, _)| *j != i)
            .fold(vec![BigInt::one()], |a, (_, b)| fmul(&a, b, prime));
        inverses.push(fpoly_inverse(&complement, factor, prime)?);
    }
    while modulus <= 2 * bound {
        let next_modulus = &modulus * prime;
        let product = factors
            .iter()
            .fold(vec![BigInt::one()], |a, b| fmul(&a, b, &next_modulus));
        let mut error = vec![BigInt::zero(); p.len().max(product.len())];
        for (i, c) in p.iter().enumerate() {
            error[i] += c;
        }
        for (i, c) in product.iter().enumerate() {
            error[i] -= c;
        }
        for c in &mut error {
            if !(&*c % &modulus).is_zero() {
                return Err("HENSEL_NONEXACT_CORRECTION".into());
            }
            *c = modulo(&(&*c / &modulus), prime);
        }
        let error = ztrim(error);
        for i in 0..factors.len() {
            let correction = fdiv(&fmul(&error, &inverses[i], prime), &initial[i], prime)?.1;
            for (j, c) in correction.iter().enumerate() {
                factors[i][j] += &modulus * c;
            }
        }
        modulus = next_modulus;
        verify_lift(p, &factors, &modulus)?;
    }
    Ok((factors, modulus))
}
fn centered(p: &[BigInt], modulus: &BigInt) -> Z {
    ztrim(
        p.iter()
            .map(|x| {
                let r = modulo(x, modulus);
                if 2 * &r > *modulus {
                    r - modulus
                } else {
                    r
                }
            })
            .collect(),
    )
}
fn zquotient(p: &[BigInt], factor: &[BigInt]) -> Option<Z> {
    if factor.len() < 2 || !factor.last()?.is_one() {
        return None;
    }
    let mut remainder = p.to_vec();
    let mut q = vec![BigInt::zero(); p.len().saturating_sub(factor.len()) + 1];
    while !zzero(&remainder) && remainder.len() >= factor.len() {
        let shift = remainder.len() - factor.len();
        let coefficient = remainder.last()?.clone();
        q[shift] = coefficient.clone();
        for (i, c) in factor.iter().enumerate() {
            remainder[shift + i] -= &coefficient * c;
        }
        remainder = ztrim(remainder);
    }
    zzero(&remainder).then(|| ztrim(q))
}
struct Recombination<'a> {
    polynomial: &'a Z,
    factors: &'a [Z],
    modulus: &'a BigInt,
}
impl Recombination<'_> {
    fn subset(
        &self,
        start: usize,
        target: usize,
        product: Z,
        chosen: &mut Vec<usize>,
    ) -> Option<(Z, Z, Vec<usize>)> {
        if target == 0 {
            let candidate = centered(&product, self.modulus);
            return zquotient(self.polynomial, &candidate).map(|q| (candidate, q, chosen.clone()));
        }
        for i in start..self.factors.len() {
            let degree = self.factors[i].len() - 1;
            if degree > target {
                continue;
            }
            chosen.push(i);
            let next = freduce(&zmul(&product, &self.factors[i]), self.modulus);
            if let Some(found) = self.subset(i + 1, target - degree, next, chosen) {
                return Some(found);
            }
            chosen.pop();
        }
        None
    }
}
fn recombine(mut p: Z, mut factors: Vec<Z>, modulus: &BigInt) -> Vec<Z> {
    let mut result = Vec::new();
    loop {
        let search = Recombination {
            polynomial: &p,
            factors: &factors,
            modulus,
        };
        let found = (1..=(p.len() - 1) / 2)
            .find_map(|degree| search.subset(0, degree, vec![BigInt::one()], &mut Vec::new()));
        match found {
            Some((factor, quotient, indices)) => {
                result.push(factor);
                p = quotient;
                factors = factors
                    .into_iter()
                    .enumerate()
                    .filter_map(|(i, f)| (!indices.contains(&i)).then_some(f))
                    .collect();
            }
            None => {
                if p.len() > 1 {
                    result.push(p);
                }
                return result;
            }
        }
    }
}
fn factor_monic_integer(p: Z) -> Result<Vec<Z>> {
    if p.len() <= 2 {
        return Ok(vec![p]);
    }
    let prime = choose_prime(&p)?;
    let modular = berlekamp(&p, &prime)?;
    if modular.len() == 1 {
        return Ok(vec![p]);
    }
    let bound = coefficient_bound(&p)?;
    let (lifted, modulus) = lift(&p, &modular, &prime, &bound)?;
    verify_recombination_modulus(&bound, &modulus)?;
    let factors = recombine(p.clone(), lifted, &modulus);
    if factors.iter().fold(vec![BigInt::one()], |a, b| zmul(&a, b)) != p {
        return Err("RECOMBINATION_PRODUCT_FAILED".into());
    }
    Ok(factors)
}
fn factor_squarefree_rational(p: &[Q]) -> Result<Vec<P>> {
    if p.len() <= 2 {
        return Ok(vec![p.to_vec()]);
    }
    let denominator = p.iter().fold(BigInt::one(), |a, q| {
        let g = gcd_integer(a.clone(), q.denom().clone());
        a / g * q.denom()
    });
    let integers: Z = p
        .iter()
        .map(|q| q.numer() * (&denominator / q.denom()))
        .collect();
    let divisor = integers
        .iter()
        .fold(BigInt::zero(), |a, c| gcd_integer(a, c.clone()));
    let primitive: Z = integers.iter().map(|c| c / &divisor).collect();
    let leading = primitive.last().unwrap();
    let n = primitive.len() - 1;
    let transformed: Z = primitive
        .iter()
        .enumerate()
        .map(|(j, c)| {
            if j == n {
                BigInt::one()
            } else {
                c * power(leading.clone(), n - 1 - j)
            }
        })
        .collect();
    let factors = factor_monic_integer(transformed)?;
    Ok(factors
        .into_iter()
        .map(|h| {
            let degree = h.len() - 1;
            let denominator = power(leading.clone(), degree);
            h.into_iter()
                .enumerate()
                .map(|(j, c)| Q::new(c * power(leading.clone(), j), denominator.clone()))
                .collect()
        })
        .collect())
}
fn factor(p: &[Q]) -> Result<Vec<(P, usize)>> {
    let mut out = Vec::new();
    for (part, multiplicity) in squarefree(p)? {
        for irreducible in factor_squarefree_rational(&part)? {
            out.push((irreducible, multiplicity));
        }
    }
    out.sort_by(|a, b| a.0.iter().rev().cmp(b.0.iter().rev()));
    Ok(out)
}
fn parse_coefficients(value: &Value) -> Result<P> {
    let entries = value.as_array().ok_or("COEFFICIENT_ARRAY_REQUIRED")?;
    if entries.is_empty() {
        return Err("NONEMPTY_POLYNOMIAL_REQUIRED".into());
    }
    let mut p = Vec::new();
    for entry in entries {
        let text = entry.as_str().ok_or("CANONICAL_RATIONAL_STRING_REQUIRED")?;
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
        p.push(q);
    }
    if p[0].is_zero() {
        return Err("NONZERO_LEADING_COEFFICIENT_REQUIRED".into());
    }
    p.reverse();
    Ok(p)
}
fn wire(p: &[Q]) -> Value {
    json!(p
        .iter()
        .rev()
        .map(|q| format!("{}/{}", q.numer(), q.denom()))
        .collect::<Vec<_>>())
}
fn exact_fields(value: &Value, fields: &[&str]) -> Result<()> {
    let map = value.as_object().ok_or("OBJECT_REQUIRED")?;
    if map.len() != fields.len() || fields.iter().any(|field| !map.contains_key(*field)) {
        return Err("EXACT_FIELDS_REQUIRED".into());
    }
    Ok(())
}
pub fn evaluate_request(request: &Value) -> Result<Value> {
    exact_fields(request, &["operation", "coefficients"])?;
    if request["operation"] != "factor" {
        return Err("FACTOR_OPERATION_REQUIRED".into());
    }
    let p = parse_coefficients(&request["coefficients"])?;
    let factors = factor(&p)?;
    let leading = p.last().unwrap();
    Ok(
        json!({"schema":"rational_polynomial_factorization_v1","authority_effect":"None",
        "coefficient_field":"Q","coefficients":wire(&p),"content":format!("{}/{}",leading.numer(),leading.denom()),
        "factors":factors.iter().map(|(p,m)|json!({"polynomial":wire(p),"multiplicity":m})).collect::<Vec<_>>(),
        "algorithm":"EXACT_BERLEKAMP_HENSEL_RECOMBINATION"}),
    )
}
pub fn validate_factorization(coefficients: &Value, output: &Value) -> Result<()> {
    let input = parse_coefficients(coefficients)?;
    exact_fields(
        output,
        &[
            "schema",
            "authority_effect",
            "coefficient_field",
            "coefficients",
            "content",
            "factors",
            "algorithm",
        ],
    )?;
    if output["schema"] != "rational_polynomial_factorization_v1"
        || output["authority_effect"] != "None"
        || output["coefficient_field"] != "Q"
        || output["algorithm"] != "EXACT_BERLEKAMP_HENSEL_RECOMBINATION"
    {
        return Err("FACTORIZATION_METADATA_MISMATCH".into());
    }
    if parse_coefficients(&output["coefficients"])? != input {
        return Err("FACTORIZATION_INPUT_BINDING_MISMATCH".into());
    }
    let content = parse_coefficients(&json!([output["content"].clone()]))?;
    if content[0] != *input.last().unwrap() {
        return Err("FACTORIZATION_CONTENT_MISMATCH".into());
    }
    let rows = output["factors"]
        .as_array()
        .ok_or("FACTOR_ARRAY_REQUIRED")?;
    let mut product = content;
    let mut previous: Option<P> = None;
    let mut total_degree = 0usize;
    for row in rows {
        exact_fields(row, &["polynomial", "multiplicity"])?;
        let polynomial = parse_coefficients(&row["polynomial"])?;
        if polynomial.len() < 2 || !polynomial.last().unwrap().is_one() {
            return Err("MONIC_NONCONSTANT_FACTOR_REQUIRED".into());
        }
        if previous
            .as_ref()
            .is_some_and(|old| old.iter().rev().cmp(polynomial.iter().rev()).is_ge())
        {
            return Err("DISTINCT_NUMERIC_SORTED_FACTORS_REQUIRED".into());
        }
        previous = Some(polynomial.clone());
        let multiplicity = row["multiplicity"]
            .as_u64()
            .and_then(|x| usize::try_from(x).ok())
            .filter(|x| *x > 0)
            .ok_or("POSITIVE_INTEGER_MULTIPLICITY_REQUIRED")?;
        total_degree = total_degree
            .checked_add(
                (polynomial.len() - 1)
                    .checked_mul(multiplicity)
                    .ok_or("FACTORIZATION_DEGREE_MISMATCH")?,
            )
            .ok_or("FACTORIZATION_DEGREE_MISMATCH")?;
        if total_degree >= input.len() {
            return Err("FACTORIZATION_DEGREE_MISMATCH".into());
        }
        if qgcd(polynomial.clone(), derivative(&polynomial))?.len() != 1
            || factor_squarefree_rational(&polynomial)?.len() != 1
        {
            return Err("REDUCIBLE_CLAIMED_FACTOR".into());
        }
        for _ in 0..multiplicity {
            product = qmul(&product, &polynomial);
        }
    }
    if product != input {
        return Err("FACTORIZATION_PRODUCT_MISMATCH".into());
    }
    Ok(())
}
#[cfg(test)]
pub fn bad_prime_control() -> Result<()> {
    berlekamp(&[1.into(), 0.into(), 1.into()], &2.into()).map(|_| ())
}
#[cfg(test)]
pub fn hensel_mutation_control() -> Result<()> {
    let p = vec![1.into(), 0.into(), 0.into(), 0.into(), 1.into()];
    let prime = BigInt::from(3);
    let initial = berlekamp(&p, &prime)?;
    let (mut factors, modulus) = lift(&p, &initial, &prime, &9.into())?;
    factors[0][0] += 1;
    verify_lift(&p, &factors, &modulus)
}
#[cfg(test)]
pub fn recombination_mutation_control() -> Result<()> {
    zquotient(&[(-1).into(), 0.into(), 1.into()], &[2.into(), 1.into()])
        .map(|_| ())
        .ok_or_else(|| "RECOMBINATION_EXACT_DIVISION_FAILED".into())
}
#[cfg(test)]
pub fn integer_root_control(value: &BigInt, degree: usize) -> Result<BigInt> {
    ceil_integer_root(value, degree)
}
#[cfg(test)]
pub fn radius_bound_control(descending: &[BigInt]) -> Result<(BigInt, BigInt)> {
    let p: Z = descending.iter().rev().cloned().collect();
    Ok((root_radius(&p)?, coefficient_bound(&p)?))
}
#[cfg(test)]
pub fn radius_mutation_control(descending: &[BigInt], radius: &BigInt) -> Result<()> {
    let p: Z = descending.iter().rev().cloned().collect();
    verify_root_radius(&p, radius)
}
#[cfg(test)]
pub fn recombination_modulus_control(modulus: &BigInt) -> Result<()> {
    let p = vec![BigInt::from(-10000), BigInt::zero(), BigInt::one()];
    verify_recombination_modulus(&coefficient_bound(&p)?, modulus)
}
#[cfg(test)]
pub fn hensel_carry_control(wrong_modulus: bool) -> Result<()> {
    let p: Z = vec![(-2).into(), 0.into(), 1.into()];
    let prime = BigInt::from(7);
    let next_modulus = &prime * &prime;
    let initial = berlekamp(&p, &prime)?;
    let product_modulus = if wrong_modulus { &prime } else { &next_modulus };
    let product = initial
        .iter()
        .fold(vec![BigInt::one()], |a, b| fmul(&a, b, product_modulus));
    let error: Z = p
        .iter()
        .enumerate()
        .map(|(i, coefficient)| {
            let difference = coefficient - product.get(i).cloned().unwrap_or_default();
            assert!((&difference % &prime).is_zero());
            modulo(&(difference / &prime), &prime)
        })
        .collect();
    let mut factors = initial.clone();
    for (i, factor) in initial.iter().enumerate() {
        let complement = initial
            .iter()
            .enumerate()
            .filter(|(j, _)| *j != i)
            .fold(vec![BigInt::one()], |a, (_, b)| fmul(&a, b, &prime));
        let inverse = fpoly_inverse(&complement, factor, &prime)?;
        let correction = fdiv(&fmul(&error, &inverse, &prime), factor, &prime)?.1;
        for (j, coefficient) in correction.iter().enumerate() {
            factors[i][j] += &prime * coefficient;
        }
    }
    verify_lift(&p, &factors, &next_modulus)
}
#[cfg(test)]
pub fn hensel_verification_modulus_control(mutate: bool) -> Result<()> {
    let p: Z = vec![(-2).into(), 0.into(), 1.into()];
    let prime = BigInt::from(7);
    let initial = berlekamp(&p, &prime)?;
    let (mut factors, modulus) = lift(&p, &initial, &prime, &BigInt::from(9))?;
    if mutate {
        factors[0][0] += &prime;
        verify_lift(&p, &factors, &prime)?;
    }
    verify_lift(&p, &factors, &modulus)
}
fn run() -> Result<Value> {
    if std::env::args().len() != 1 {
        return Err("USAGE:rational_polynomial_factors < REQUEST_JSON".into());
    }
    let mut input = String::new();
    io::stdin()
        .read_to_string(&mut input)
        .map_err(|e| format!("INPUT_READ_ERROR:{e}"))?;
    let request = serde_json::from_str(&input).map_err(|e| format!("INVALID_JSON:{e}"))?;
    evaluate_request(&request)
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
