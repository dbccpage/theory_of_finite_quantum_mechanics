
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::elimination::{self, LinearSolution};
use linear_algebra::exact_field::{matrix as mx, ExactFieldError};
use linear_algebra::scalars::{ExactRing, Field, Ring, Semiring};

pub const MAX_COMPLEX_DIMENSION: usize = 8;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum LieAlgebraError {
    #[error("a structure-constant table for dimension {dimension} needs {expected} entries, got {actual}")]
    TableLength {
        dimension: usize,
        expected: usize,
        actual: usize,
    },
    #[error("the matrices are not square of one common size (or there are none)")]
    Shape,
    #[error("the basis matrices are linearly dependent")]
    DependentBasis,
    #[error("the commutator of basis elements {a} and {b} is not in their span")]
    NotClosed { a: usize, b: usize },
    #[error("the dimension {dimension} exceeds the complex bound {MAX_COMPLEX_DIMENSION}")]
    DimensionTooLarge { dimension: usize },
    #[error("cochain degree {degree} exceeds the dimension {dimension}")]
    DegreeTooLarge { degree: usize, dimension: usize },
    #[error("index {index} is out of range for dimension {dimension}")]
    IndexOutOfRange { index: usize, dimension: usize },
    #[error(transparent)]
    Matrix(#[from] ExactFieldError),
}

pub trait LieAlgebra {
    type Scalar: Field + ExactRing;

    fn dimension(&self) -> usize;

    fn structure_constant(&self, a: usize, b: usize, e: usize) -> Self::Scalar;
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StructureConstants<F> {
    dimension: usize,
    table: Vec<F>,
}

impl<F: Field + ExactRing> StructureConstants<F> {
    pub fn new(dimension: usize, table: Vec<F>) -> Result<Self, LieAlgebraError> {
        let expected = dimension * dimension * dimension;
        if table.len() != expected {
            return Err(LieAlgebraError::TableLength {
                dimension,
                expected,
                actual: table.len(),
            });
        }
        Ok(Self { dimension, table })
    }

    pub fn from_fn(dimension: usize, mut f: impl FnMut(usize, usize, usize) -> F) -> Self {
        let mut table = Vec::with_capacity(dimension * dimension * dimension);
        for a in 0..dimension {
            for b in 0..dimension {
                for e in 0..dimension {
                    table.push(f(a, b, e));
                }
            }
        }
        Self { dimension, table }
    }

    pub fn abelian(n: usize) -> Self {
        Self::from_fn(n, |_, _, _| F::zero())
    }
}

impl<F: Field + ExactRing> LieAlgebra for StructureConstants<F> {
    type Scalar = F;

    fn dimension(&self) -> usize {
        self.dimension
    }

    fn structure_constant(&self, a: usize, b: usize, e: usize) -> F {
        self.table[(a * self.dimension + b) * self.dimension + e].clone()
    }
}

fn check_index<L: LieAlgebra + ?Sized>(algebra: &L, index: usize) -> Result<(), LieAlgebraError> {
    if index >= algebra.dimension() {
        return Err(LieAlgebraError::IndexOutOfRange {
            index,
            dimension: algebra.dimension(),
        });
    }
    Ok(())
}

pub fn verify_antisymmetry<L: LieAlgebra>(algebra: &L) -> bool {
    let n = algebra.dimension();
    (0..n).all(|a| {
        (0..n).all(|b| {
            (0..n).all(|e| {
                algebra
                    .structure_constant(a, b, e)
                    .add(&algebra.structure_constant(b, a, e))
                    .is_zero()
            })
        })
    })
}

pub fn verify_jacobi<L: LieAlgebra>(algebra: &L) -> bool {
    let n = algebra.dimension();
    let c = |a: usize, b: usize, e: usize| algebra.structure_constant(a, b, e);
    for a in 0..n {
        for b in 0..n {
            for cc in 0..n {
                for e in 0..n {
                    let mut sum = L::Scalar::zero();
                    for d in 0..n {
                        sum = sum
                            .add(&c(a, b, d).mul(&c(d, cc, e)))
                            .add(&c(b, cc, d).mul(&c(d, a, e)))
                            .add(&c(cc, a, d).mul(&c(d, b, e)));
                    }
                    if !sum.is_zero() {
                        return false;
                    }
                }
            }
        }
    }
    true
}

pub fn bracket<L: LieAlgebra>(
    algebra: &L,
    x: &[L::Scalar],
    y: &[L::Scalar],
) -> Result<Vec<L::Scalar>, LieAlgebraError> {
    let n = algebra.dimension();
    if x.len() != n || y.len() != n {
        return Err(LieAlgebraError::Shape);
    }
    let mut out = vec![L::Scalar::zero(); n];
    for a in 0..n {
        for b in 0..n {
            let coefficient = x[a].mul(&y[b]);
            if coefficient.is_zero() {
                continue;
            }
            for (e, slot) in out.iter_mut().enumerate() {
                *slot = slot.add(&coefficient.mul(&algebra.structure_constant(a, b, e)));
            }
        }
    }
    Ok(out)
}

pub fn adjoint_matrix<L: LieAlgebra>(
    algebra: &L,
    a: usize,
) -> Result<BasicMatrix<L::Scalar>, LieAlgebraError> {
    check_index(algebra, a)?;
    let n = algebra.dimension();
    Ok(mx::from_fn(n, n, |e, b| {
        algebra.structure_constant(a, b, e)
    })?)
}

pub fn adjoint_is_representation<L: LieAlgebra>(algebra: &L) -> Result<bool, LieAlgebraError> {
    let n = algebra.dimension();
    let ad: Vec<BasicMatrix<L::Scalar>> = (0..n)
        .map(|a| adjoint_matrix(algebra, a))
        .collect::<Result<_, _>>()?;
    for a in 0..n {
        for b in 0..n {
            let commutator = mx::commutator(&ad[a], &ad[b])?;
            let mut expected = mx::zeros::<L::Scalar>(n, n)?;
            for (e, ad_e) in ad.iter().enumerate() {
                expected = mx::add(
                    &expected,
                    &mx::scale(ad_e, &algebra.structure_constant(a, b, e))?,
                )?;
            }
            if commutator != expected {
                return Ok(false);
            }
        }
    }
    Ok(true)
}

pub fn killing_form<L: LieAlgebra>(algebra: &L) -> Result<BasicMatrix<L::Scalar>, LieAlgebraError> {
    let n = algebra.dimension();
    let ad: Vec<BasicMatrix<L::Scalar>> = (0..n)
        .map(|a| adjoint_matrix(algebra, a))
        .collect::<Result<_, _>>()?;
    let mut entries = Vec::with_capacity(n * n);
    for a in 0..n {
        for b in 0..n {
            entries.push(mx::trace(&mx::multiply(&ad[a], &ad[b])?)?);
        }
    }
    Ok(BasicMatrix::from_row_major(n, n, entries).map_err(ExactFieldError::from)?)
}

pub fn structure_constants_from_matrices<F: Field + ExactRing>(
    basis: &[BasicMatrix<F>],
) -> Result<StructureConstants<F>, LieAlgebraError> {
    let n = basis.len();
    let size = basis.first().ok_or(LieAlgebraError::Shape)?.rows();
    if basis.iter().any(|m| m.rows() != size || m.cols() != size) {
        return Err(LieAlgebraError::Shape);
    }
    let columns: Vec<F> = (0..size * size)
        .flat_map(|row| basis.iter().map(move |m| m.as_slice()[row].clone()))
        .collect();
    let system =
        BasicMatrix::from_row_major(size * size, n, columns).map_err(ExactFieldError::from)?;
    if elimination::rank(&system)? < n {
        return Err(LieAlgebraError::DependentBasis);
    }
    let mut table = Vec::with_capacity(n * n * n);
    for a in 0..n {
        for b in 0..n {
            let commutator = mx::commutator(&basis[a], &basis[b])?;
            match elimination::solve(&system, commutator.as_slice())? {
                LinearSolution::Consistent { particular, .. } => table.extend(particular),
                LinearSolution::Inconsistent { .. } => {
                    return Err(LieAlgebraError::NotClosed { a, b })
                }
            }
        }
    }
    StructureConstants::new(n, table)
}


fn subsets(n: usize, k: usize) -> Vec<Vec<usize>> {
    fn grow(n: usize, k: usize, start: usize, current: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
        if current.len() == k {
            out.push(current.clone());
            return;
        }
        for i in start..n {
            current.push(i);
            grow(n, k, i + 1, current, out);
            current.pop();
        }
    }
    let mut out = Vec::new();
    grow(n, k, 0, &mut Vec::new(), &mut out);
    out
}

fn sort_word(mut word: Vec<usize>) -> Option<(i8, Vec<usize>)> {
    let mut sign = 1i8;
    for i in 1..word.len() {
        let mut j = i;
        while j > 0 && word[j - 1] > word[j] {
            word.swap(j - 1, j);
            sign = -sign;
            j -= 1;
        }
    }
    word.windows(2)
        .all(|w| w[0] != w[1])
        .then_some((sign, word))
}

fn check_complex_size<L: LieAlgebra>(algebra: &L) -> Result<usize, LieAlgebraError> {
    let n = algebra.dimension();
    if n > MAX_COMPLEX_DIMENSION {
        return Err(LieAlgebraError::DimensionTooLarge { dimension: n });
    }
    Ok(n)
}

pub fn chevalley_eilenberg_differential<L: LieAlgebra>(
    algebra: &L,
    k: usize,
) -> Result<BasicMatrix<L::Scalar>, LieAlgebraError> {
    let n = check_complex_size(algebra)?;
    if k > n {
        return Err(LieAlgebraError::DegreeTooLarge {
            degree: k,
            dimension: n,
        });
    }
    let columns = subsets(n, k);
    let rows = subsets(n, k + 1);
    let mut entries = vec![L::Scalar::zero(); rows.len() * columns.len()];
    for (col, subset) in columns.iter().enumerate() {
        for position in 0..k {
            let leibniz_sign = if position % 2 == 0 { 1i8 } else { -1i8 };
            let c = subset[position];
            for a in 0..n {
                for b in (a + 1)..n {
                    let coefficient = algebra.structure_constant(a, b, c).neg();
                    if coefficient.is_zero() {
                        continue;
                    }
                    let mut word: Vec<usize> = subset[..position].to_vec();
                    word.push(a);
                    word.push(b);
                    word.extend_from_slice(&subset[position + 1..]);
                    if let Some((sign, sorted)) = sort_word(word) {
                        let row = rows
                            .binary_search(&sorted)
                            .expect("a sorted (k+1)-subset is a basis index");
                        let total_sign = sign * leibniz_sign;
                        let term = if total_sign > 0 {
                            coefficient.clone()
                        } else {
                            coefficient.neg()
                        };
                        let slot = &mut entries[row * columns.len() + col];
                        *slot = slot.add(&term);
                    }
                }
            }
        }
    }
    Ok(
        BasicMatrix::from_row_major(rows.len(), columns.len(), entries)
            .map_err(ExactFieldError::from)?,
    )
}

pub fn chevalley_eilenberg_squares_to_zero<L: LieAlgebra>(
    algebra: &L,
) -> Result<bool, LieAlgebraError> {
    let n = check_complex_size(algebra)?;
    for k in 0..n.saturating_sub(1) {
        let d_k = chevalley_eilenberg_differential(algebra, k)?;
        let d_next = chevalley_eilenberg_differential(algebra, k + 1)?;
        if !mx::is_zero_matrix(&mx::multiply(&d_next, &d_k)?) {
            return Ok(false);
        }
    }
    Ok(true)
}

pub fn cohomology_betti_numbers<L: LieAlgebra>(algebra: &L) -> Result<Vec<usize>, LieAlgebraError> {
    let n = check_complex_size(algebra)?;
    let mut ranks = Vec::with_capacity(n + 1);
    for k in 0..n {
        ranks.push(elimination::rank(&chevalley_eilenberg_differential(
            algebra, k,
        )?)?);
    }
    ranks.push(0);
    let dims: Vec<usize> = (0..=n).map(|k| subsets(n, k).len()).collect();
    Ok((0..=n)
        .map(|k| {
            let previous = if k == 0 { 0 } else { ranks[k - 1] };
            dims[k] - ranks[k] - previous
        })
        .collect())
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_rational::BigRational;
    use omega_number_theory::rational::ri;

    #[test]
    fn subsets_are_the_lexicographic_basis_of_the_exterior_powers() {
        assert_eq!(
            subsets(4, 2),
            vec![
                vec![0, 1],
                vec![0, 2],
                vec![0, 3],
                vec![1, 2],
                vec![1, 3],
                vec![2, 3]
            ]
        );
        assert_eq!(subsets(3, 0), vec![Vec::<usize>::new()]);
        assert_eq!(subsets(3, 3), vec![vec![0, 1, 2]]);
    }

    #[test]
    fn sorting_a_word_tracks_the_sign_and_detects_repeats() {
        assert_eq!(sort_word(vec![2, 0, 1]), Some((1, vec![0, 1, 2])));
        assert_eq!(sort_word(vec![1, 0]), Some((-1, vec![0, 1])));
        assert_eq!(sort_word(vec![0, 1, 0]), None);
    }

    #[test]
    fn a_table_of_the_wrong_length_is_refused() {
        let result = StructureConstants::<BigRational>::new(2, vec![ri(0); 7]);
        assert_eq!(
            result,
            Err(LieAlgebraError::TableLength {
                dimension: 2,
                expected: 8,
                actual: 7
            })
        );
        assert!(StructureConstants::<BigRational>::new(2, vec![ri(0); 8]).is_ok());
    }
}
