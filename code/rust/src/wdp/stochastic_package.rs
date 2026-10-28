
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::{
    solve_in_image, ExactLinearAlgebraError, ImageMembership,
};
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use tfqm_finite_probability::stochastic_map::StochasticMap;
use serde::Serialize;

use crate::error::WdpError;
use crate::types::AuthorityEffect;

pub type Matrix = Vec<Vec<BigRational>>;

pub type FunctionMixture = Vec<(Vec<usize>, BigRational)>;

pub const MAX_ENUMERATION: usize = 1_000_000;

pub const MAX_MATRIX_ENTRIES: usize = 1_000_000;

fn invalid(detail: String) -> WdpError {
    WdpError::InvalidInput { detail }
}

pub fn mass(p: &[BigRational]) -> BigRational {
    p.iter().fold(BigRational::zero(), |acc, x| acc + x)
}

pub(crate) fn matrix_shape(m: &[Vec<BigRational>], what: &str) -> Result<(usize, usize), WdpError> {
    let rows = m.len();
    if rows == 0 {
        return Err(invalid(format!("{what} needs at least one row")));
    }
    let cols = m[0].len();
    if cols == 0 {
        return Err(invalid(format!("{what} needs at least one column")));
    }
    for (i, row) in m.iter().enumerate() {
        if row.len() != cols {
            return Err(invalid(format!(
                "{what} row {i} has {} entries, expected {cols}",
                row.len()
            )));
        }
    }
    Ok((rows, cols))
}

pub(crate) fn matrix_apply(m: &[Vec<BigRational>], x: &[BigRational]) -> Vec<BigRational> {
    m.iter()
        .map(|row| {
            row.iter()
                .zip(x)
                .fold(BigRational::zero(), |acc, (a, b)| acc + a * b)
        })
        .collect()
}

fn column_defect(m: &[Vec<BigRational>], cols: usize) -> Option<(usize, BigRational)> {
    (0..cols).find_map(|j| {
        let sum = m.iter().fold(BigRational::zero(), |acc, row| acc + &row[j]);
        (!sum.is_one()).then_some((j, sum))
    })
}

pub(crate) fn bounded_power(base: usize, exponent: usize, limit: usize) -> Option<usize> {
    base.checked_pow(u32::try_from(exponent).ok()?)
        .filter(|&power| power <= limit)
}

fn sum_updates(updates: &[Matrix], n_out: usize, n_in: usize) -> Matrix {
    let mut total = vec![vec![BigRational::zero(); n_in]; n_out];
    for update in updates {
        for (total_row, row) in total.iter_mut().zip(update) {
            for (t, x) in total_row.iter_mut().zip(row) {
                *t += x;
            }
        }
    }
    total
}

fn check_nonnegative(m: &[Vec<BigRational>], what: &str) -> Result<(), WdpError> {
    for (i, row) in m.iter().enumerate() {
        for (j, entry) in row.iter().enumerate() {
            if entry.is_negative() {
                return Err(invalid(format!("{what} entry ({i}, {j}) is negative")));
            }
        }
    }
    Ok(())
}

pub fn preserves_basis_mass(m: &[Vec<BigRational>]) -> bool {
    matrix_shape(m, "matrix").is_ok_and(|(_, cols)| column_defect(m, cols).is_none())
}

pub fn is_permutation_matrix(m: &[Vec<BigRational>]) -> bool {
    let n = m.len();
    if n == 0 || m.iter().any(|row| row.len() != n) {
        return false;
    }
    let is_bit = |x: &BigRational| x.is_zero() || x.is_one();
    if !m.iter().flatten().all(is_bit) {
        return false;
    }
    let rows_ok = m
        .iter()
        .all(|row| row.iter().filter(|x| x.is_one()).count() == 1);
    let cols_ok = (0..n).all(|j| m.iter().filter(|row| row[j].is_one()).count() == 1);
    rows_ok && cols_ok
}

fn matrix_product(a: &[Vec<BigRational>], b: &[Vec<BigRational>]) -> Matrix {
    let cols = b.first().map_or(0, Vec::len);
    a.iter()
        .map(|row| {
            (0..cols)
                .map(|j| {
                    row.iter()
                        .zip(b)
                        .fold(BigRational::zero(), |acc, (x, b_row)| acc + x * &b_row[j])
                })
                .collect()
        })
        .collect()
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LeftInverse {
    NoLeftInverse,
    SignedOnly(Matrix),
    Stochastic(StochasticUpdate),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct StochasticUpdate {
    n_out: usize,
    n_in: usize,
    entries: Matrix,
}

impl StochasticUpdate {
    pub fn new(entries: Matrix) -> Result<Self, WdpError> {
        let (n_out, n_in) = matrix_shape(&entries, "stochastic update")?;
        check_nonnegative(&entries, "stochastic update")?;
        if let Some((j, sum)) = column_defect(&entries, n_in) {
            return Err(invalid(format!(
                "stochastic update column {j} sums to {sum}, not 1"
            )));
        }
        Ok(Self {
            n_out,
            n_in,
            entries,
        })
    }

    pub fn identity(n: usize) -> Result<Self, WdpError> {
        if n.checked_mul(n)
            .is_none_or(|entries| entries > MAX_MATRIX_ENTRIES)
        {
            return Err(invalid(format!(
                "a {n} x {n} update exceeds {MAX_MATRIX_ENTRIES} entries"
            )));
        }
        let f: Vec<usize> = (0..n).collect();
        Self::from_function(&f, n)
    }

    pub fn from_function(f: &[usize], n_out: usize) -> Result<Self, WdpError> {
        if n_out
            .checked_mul(f.len())
            .is_none_or(|n| n > MAX_MATRIX_ENTRIES)
        {
            return Err(invalid(format!(
                "a {n_out} x {} update exceeds {MAX_MATRIX_ENTRIES} entries",
                f.len()
            )));
        }
        if n_out > MAX_MATRIX_ENTRIES {
            return Err(invalid(format!(
                "{n_out} outputs exceed the cap {MAX_MATRIX_ENTRIES}"
            )));
        }
        if let Some((j, target)) = f.iter().enumerate().find(|(_, t)| **t >= n_out) {
            return Err(invalid(format!(
                "function value f({j}) = {target} lies outside 0..{n_out}"
            )));
        }
        let entries = (0..n_out)
            .map(|i| {
                f.iter()
                    .map(|&t| {
                        if t == i {
                            BigRational::one()
                        } else {
                            BigRational::zero()
                        }
                    })
                    .collect()
            })
            .collect();
        Self::new(entries)
    }

    pub fn n_out(&self) -> usize {
        self.n_out
    }

    pub fn n_in(&self) -> usize {
        self.n_in
    }

    pub fn entries(&self) -> &[Vec<BigRational>] {
        &self.entries
    }

    pub fn get(&self, i: usize, j: usize) -> Option<&BigRational> {
        self.entries.get(i).and_then(|row| row.get(j))
    }

    pub fn apply(&self, p: &[BigRational]) -> Result<Vec<BigRational>, WdpError> {
        if p.len() != self.n_in {
            return Err(invalid(format!(
                "vector has {} entries, the update has {} inputs",
                p.len(),
                self.n_in
            )));
        }
        Ok(matrix_apply(&self.entries, p))
    }

    pub fn compose(&self, next: &StochasticUpdate) -> Result<StochasticUpdate, WdpError> {
        if self.n_out != next.n_in {
            return Err(invalid(format!(
                "cannot compose: first update has {} outputs, second has {} inputs",
                self.n_out, next.n_in
            )));
        }
        Self::new(matrix_product(&next.entries, &self.entries))
    }

    pub fn is_deterministic(&self) -> bool {
        self.entries
            .iter()
            .flatten()
            .all(|x| x.is_zero() || x.is_one())
    }

    pub fn as_function(&self) -> Option<Vec<usize>> {
        if !self.is_deterministic() {
            return None;
        }
        (0..self.n_in)
            .map(|j| (0..self.n_out).find(|&i| self.entries[i][j].is_one()))
            .collect()
    }

    pub fn is_permutation(&self) -> bool {
        is_permutation_matrix(&self.entries)
    }

    pub fn mixture_of_functions(&self) -> Result<FunctionMixture, WdpError> {
        self.mixture_of_functions_with_limit(MAX_ENUMERATION)
    }

    pub fn mixture_of_functions_with_limit(
        &self,
        limit: usize,
    ) -> Result<FunctionMixture, WdpError> {
        let supports: Vec<Vec<usize>> = (0..self.n_in)
            .map(|j| {
                (0..self.n_out)
                    .filter(|&i| !self.entries[i][j].is_zero())
                    .collect()
            })
            .collect();
        let mut count: usize = 1;
        for support in &supports {
            count = count
                .checked_mul(support.len())
                .filter(|&c| c <= limit)
                .ok_or_else(|| {
                    invalid(format!(
                        "more than {limit} supported functions; enumeration refused"
                    ))
                })?;
        }
        let mut mixture = Vec::with_capacity(count);
        let mut choice = vec![0usize; self.n_in];
        loop {
            let f: Vec<usize> = choice
                .iter()
                .zip(&supports)
                .map(|(&c, support)| support[c])
                .collect();
            let weight = f
                .iter()
                .enumerate()
                .fold(BigRational::one(), |acc, (j, &i)| acc * &self.entries[i][j]);
            mixture.push((f, weight));
            let mut position = self.n_in;
            loop {
                if position == 0 {
                    return Ok(mixture);
                }
                position -= 1;
                choice[position] += 1;
                if choice[position] < supports[position].len() {
                    break;
                }
                choice[position] = 0;
            }
        }
    }

    pub fn recompose(
        mixture: &[(Vec<usize>, BigRational)],
        n_out: usize,
        n_in: usize,
    ) -> Result<Matrix, WdpError> {
        if n_out == 0 || n_in == 0 {
            return Err(invalid(
                "recomposition needs positive dimensions".to_string(),
            ));
        }
        if n_out
            .checked_mul(n_in)
            .is_none_or(|n| n > MAX_MATRIX_ENTRIES)
        {
            return Err(invalid(format!(
                "a {n_out} x {n_in} matrix exceeds {MAX_MATRIX_ENTRIES} entries"
            )));
        }
        let mut matrix = vec![vec![BigRational::zero(); n_in]; n_out];
        for (f, weight) in mixture {
            if f.len() != n_in {
                return Err(invalid(format!(
                    "function has {} values, expected {n_in}",
                    f.len()
                )));
            }
            for (j, &i) in f.iter().enumerate() {
                if i >= n_out {
                    return Err(invalid(format!(
                        "function value f({j}) = {i} lies outside 0..{n_out}"
                    )));
                }
                matrix[i][j] += weight;
            }
        }
        Ok(matrix)
    }

    pub fn stochastic_left_inverse(&self) -> Result<LeftInverse, WdpError> {
        if self.n_out != self.n_in {
            return Err(invalid(format!(
                "left-inverse search is exact on square carriers, found {} x {}",
                self.n_out, self.n_in
            )));
        }
        let n = self.n_in;
        let transposed: Vec<BigRational> = (0..n)
            .flat_map(|r| (0..n).map(move |c| (r, c)))
            .map(|(r, c)| self.entries[c][r].clone())
            .collect();
        let system =
            BasicMatrix::from_row_major(n, n, transposed).map_err(ExactLinearAlgebraError::from)?;
        let mut inverse_rows = Vec::with_capacity(n);
        for k in 0..n {
            let target: Vec<BigRational> = (0..n)
                .map(|i| {
                    if i == k {
                        BigRational::one()
                    } else {
                        BigRational::zero()
                    }
                })
                .collect();
            match solve_in_image(&system, &target)? {
                ImageMembership::InImage(witness) => inverse_rows.push(witness.potential),
                ImageMembership::NotInImage { .. } => return Ok(LeftInverse::NoLeftInverse),
            }
        }
        match Self::new(inverse_rows.clone()) {
            Ok(update) => Ok(LeftInverse::Stochastic(update)),
            Err(_) => Ok(LeftInverse::SignedOnly(inverse_rows)),
        }
    }

    pub fn to_stochastic_map(&self, label: &str) -> Result<StochasticMap, WdpError> {
        let rows: Matrix = (0..self.n_in)
            .map(|j| {
                (0..self.n_out)
                    .map(|i| self.entries[i][j].clone())
                    .collect()
            })
            .collect();
        Ok(StochasticMap::try_from_rows(
            self.n_in, self.n_out, rows, label,
        )?)
    }

    pub fn from_stochastic_map(map: &StochasticMap) -> Result<Self, WdpError> {
        let rows = map.rows();
        let entries: Matrix = (0..map.target_n())
            .map(|i| rows.iter().map(|row| row[i].clone()).collect())
            .collect();
        Self::new(entries)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ClassicalInstrument {
    n_out: usize,
    n_in: usize,
    updates: Vec<Matrix>,
}

impl ClassicalInstrument {
    pub fn new(updates: Vec<Matrix>) -> Result<Self, WdpError> {
        let first = updates
            .first()
            .ok_or_else(|| invalid("an instrument needs at least one outcome".to_string()))?;
        let (n_out, n_in) = matrix_shape(first, "instrument update 0")?;
        for (o, update) in updates.iter().enumerate() {
            let shape = matrix_shape(update, &format!("instrument update {o}"))?;
            if shape != (n_out, n_in) {
                return Err(invalid(format!(
                    "instrument update {o} is {} x {}, expected {n_out} x {n_in}",
                    shape.0, shape.1
                )));
            }
            check_nonnegative(update, &format!("instrument update {o}"))?;
        }
        if let Some((j, sum)) = column_defect(&sum_updates(&updates, n_out, n_in), n_in) {
            return Err(invalid(format!(
                "instrument sum column {j} sums to {sum}, not 1"
            )));
        }
        Ok(Self {
            n_out,
            n_in,
            updates,
        })
    }

    pub fn outcomes(&self) -> usize {
        self.updates.len()
    }

    pub fn n_out(&self) -> usize {
        self.n_out
    }

    pub fn n_in(&self) -> usize {
        self.n_in
    }

    pub fn updates(&self) -> &[Matrix] {
        &self.updates
    }

    pub fn total_update(&self) -> Result<StochasticUpdate, WdpError> {
        StochasticUpdate::new(sum_updates(&self.updates, self.n_out, self.n_in))
    }

    fn check_input(&self, p: &[BigRational]) -> Result<(), WdpError> {
        if let Some(i) = p.iter().position(Signed::is_negative) {
            return Err(invalid(format!("input vector entry {i} is negative")));
        }
        if p.len() != self.n_in {
            return Err(invalid(format!(
                "vector has {} entries, the instrument has {} inputs",
                p.len(),
                self.n_in
            )));
        }
        Ok(())
    }

    fn step(&self, outcome: usize, current: &[BigRational]) -> Result<Vec<BigRational>, WdpError> {
        let update = self.updates.get(outcome).ok_or_else(|| {
            invalid(format!(
                "outcome {outcome} outside 0..{}",
                self.updates.len()
            ))
        })?;
        if current.len() != self.n_in {
            return Err(invalid(format!(
                "vector has {} entries, the instrument has {} inputs",
                current.len(),
                self.n_in
            )));
        }
        Ok(matrix_apply(update, current))
    }

    pub fn run(&self, word: &[usize], p: &[BigRational]) -> Result<Vec<BigRational>, WdpError> {
        self.check_input(p)?;
        let mut current = p.to_vec();
        for &o in word {
            current = self.step(o, &current)?;
        }
        Ok(current)
    }

    pub fn law(&self, word: &[usize], p: &[BigRational]) -> Result<BigRational, WdpError> {
        Ok(mass(&self.run(word, p)?))
    }

    pub fn law_total(&self, n: usize, p: &[BigRational]) -> Result<BigRational, WdpError> {
        self.law_total_with_limit(n, p, MAX_ENUMERATION)
    }

    pub fn law_total_with_limit(
        &self,
        n: usize,
        p: &[BigRational],
        limit: usize,
    ) -> Result<BigRational, WdpError> {
        self.check_input(p)?;
        let outcomes = self.updates.len();
        if n > limit {
            return Err(invalid(format!(
                "word length {n} exceeds the enumeration cap {limit}"
            )));
        }
        bounded_power(outcomes, n, limit).ok_or_else(|| {
            invalid(format!(
                "more than {limit} words of length {n}; enumeration refused"
            ))
        })?;
        let mut total = BigRational::zero();
        let mut vectors: Vec<Vec<BigRational>> = vec![p.to_vec()];
        let mut word: Vec<usize> = Vec::new();
        loop {
            while word.len() < n {
                let next = self.step(0, &vectors[word.len()])?;
                vectors.push(next);
                word.push(0);
            }
            total += mass(&vectors[n]);
            loop {
                let Some(last) = word.pop() else {
                    return Ok(total);
                };
                vectors.pop();
                if last + 1 < outcomes {
                    let next = self.step(last + 1, &vectors[word.len()])?;
                    vectors.push(next);
                    word.push(last + 1);
                    break;
                }
            }
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SignedShearReport {
    pub t: Matrix,
    pub t_inverse: Matrix,
    pub t_preserves_basis_mass: bool,
    pub t_inverse_preserves_basis_mass: bool,
    pub inverse_times_t_is_identity: bool,
    pub t_is_permutation_matrix: bool,
    pub t_is_column_stochastic: bool,
    pub t_image_of_first_basis_vector: Vec<BigRational>,
    pub refusal: WdpError,
    pub authority_effect: AuthorityEffect,
}

fn integer_matrix(rows: &[&[i64]]) -> Matrix {
    rows.iter()
        .map(|row| {
            row.iter()
                .map(|&x| BigRational::from_integer(x.into()))
                .collect()
        })
        .collect()
}

pub fn signed_shear_counterexample() -> Result<SignedShearReport, WdpError> {
    let t = integer_matrix(&[&[2, 1], &[-1, 0]]);
    let t_inverse = integer_matrix(&[&[0, -1], &[1, 2]]);
    let identity = integer_matrix(&[&[1, 0], &[0, 1]]);
    let refusal = match StochasticUpdate::new(t.clone()) {
        Err(e) => e,
        Ok(_) => {
            return Err(invalid(
                "the signed shear was accepted as a stochastic update".to_string(),
            ))
        }
    };
    let first_basis: Vec<BigRational> = vec![BigRational::one(), BigRational::zero()];
    Ok(SignedShearReport {
        t_preserves_basis_mass: preserves_basis_mass(&t),
        t_inverse_preserves_basis_mass: preserves_basis_mass(&t_inverse),
        inverse_times_t_is_identity: matrix_product(&t_inverse, &t) == identity,
        t_is_permutation_matrix: is_permutation_matrix(&t),
        t_is_column_stochastic: StochasticUpdate::new(t.clone()).is_ok(),
        t_image_of_first_basis_vector: matrix_apply(&t, &first_basis),
        refusal,
        authority_effect: AuthorityEffect::None,
        t,
        t_inverse,
    })
}
