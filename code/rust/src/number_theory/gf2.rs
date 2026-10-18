
use num_bigint::BigUint;
use num_traits::One;
use std::fmt;

pub const MAX_F2_ENTRIES: usize = 1 << 28;

const WORD_BITS: usize = 64;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum F2Error {
    #[error("a {rows} x {cols} GF(2) matrix exceeds the bound of {limit} entries")]
    TooLarge {
        rows: usize,
        cols: usize,
        limit: usize,
    },
    #[error("row {row} has {actual} entries, expected {expected}")]
    Ragged {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("entry ({row}, {col}) is {value}: GF(2) entries are 0 or 1")]
    NotBinary { row: usize, col: usize, value: i64 },
    #[error("index {index} is outside 0..{len}")]
    IndexOutOfRange { index: usize, len: usize },
    #[error("length mismatch: expected {expected}, got {actual}")]
    LengthMismatch { expected: usize, actual: usize },
    #[error("shape mismatch: expected {expected:?}, got {actual:?}")]
    ShapeMismatch {
        expected: (usize, usize),
        actual: (usize, usize),
    },
    #[error("inverse needs a square matrix, got {rows} x {cols}")]
    NotSquare { rows: usize, cols: usize },
    #[error("listing {count} solutions exceeds the limit of {limit}")]
    EnumerationLimit { count: String, limit: usize },
}

fn words_for(len: usize) -> usize {
    len.div_ceil(WORD_BITS)
}

fn check_entries(rows: usize, cols: usize) -> Result<(), F2Error> {
    match rows.checked_mul(cols) {
        Some(total) if total <= MAX_F2_ENTRIES => Ok(()),
        _ => Err(F2Error::TooLarge {
            rows,
            cols,
            limit: MAX_F2_ENTRIES,
        }),
    }
}

#[derive(Clone, PartialEq, Eq, Hash)]
pub struct F2Vector {
    len: usize,
    words: Vec<u64>,
}

impl fmt::Debug for F2Vector {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "F2Vector[")?;
        for i in 0..self.len {
            write!(f, "{}", u8::from(self.bit(i)))?;
        }
        write!(f, "]")
    }
}

impl F2Vector {
    fn bit(&self, index: usize) -> bool {
        (self.words[index / WORD_BITS] >> (index % WORD_BITS)) & 1 == 1
    }

    fn check(&self, index: usize) -> Result<(), F2Error> {
        if index < self.len {
            Ok(())
        } else {
            Err(F2Error::IndexOutOfRange {
                index,
                len: self.len,
            })
        }
    }

    pub fn zeros(len: usize) -> Result<Self, F2Error> {
        check_entries(1, len)?;
        Ok(Self {
            len,
            words: vec![0; words_for(len)],
        })
    }

    pub fn unit(len: usize, index: usize) -> Result<Self, F2Error> {
        let mut v = Self::zeros(len)?;
        v.set(index, true)?;
        Ok(v)
    }

    pub fn from_bits(bits: &[u8]) -> Result<Self, F2Error> {
        let mut v = Self::zeros(bits.len())?;
        for (index, &bit) in bits.iter().enumerate() {
            match bit {
                0 => {}
                1 => v.words[index / WORD_BITS] |= 1u64 << (index % WORD_BITS),
                other => {
                    return Err(F2Error::NotBinary {
                        row: 0,
                        col: index,
                        value: i64::from(other),
                    })
                }
            }
        }
        Ok(v)
    }

    pub fn from_indices(len: usize, indices: &[usize]) -> Result<Self, F2Error> {
        let mut v = Self::zeros(len)?;
        for &index in indices {
            v.flip(index)?;
        }
        Ok(v)
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn get(&self, index: usize) -> Result<bool, F2Error> {
        self.check(index)?;
        Ok(self.bit(index))
    }

    pub fn set(&mut self, index: usize, value: bool) -> Result<(), F2Error> {
        self.check(index)?;
        let mask = 1u64 << (index % WORD_BITS);
        if value {
            self.words[index / WORD_BITS] |= mask;
        } else {
            self.words[index / WORD_BITS] &= !mask;
        }
        Ok(())
    }

    pub fn flip(&mut self, index: usize) -> Result<(), F2Error> {
        self.check(index)?;
        self.words[index / WORD_BITS] ^= 1u64 << (index % WORD_BITS);
        Ok(())
    }

    pub fn weight(&self) -> usize {
        self.words.iter().map(|w| w.count_ones() as usize).sum()
    }

    pub fn is_zero(&self) -> bool {
        self.words.iter().all(|&w| w == 0)
    }

    pub fn support(&self) -> Vec<usize> {
        let mut out = Vec::new();
        for (word_index, &word) in self.words.iter().enumerate() {
            let mut w = word;
            while w != 0 {
                out.push(word_index * WORD_BITS + w.trailing_zeros() as usize);
                w &= w - 1;
            }
        }
        out
    }

    pub fn to_bits(&self) -> Vec<u8> {
        (0..self.len).map(|i| u8::from(self.bit(i))).collect()
    }

    fn check_same_length(&self, other: &Self) -> Result<(), F2Error> {
        if self.len == other.len {
            Ok(())
        } else {
            Err(F2Error::LengthMismatch {
                expected: self.len,
                actual: other.len,
            })
        }
    }

    pub fn add(&self, other: &Self) -> Result<Self, F2Error> {
        let mut out = self.clone();
        out.add_assign(other)?;
        Ok(out)
    }

    pub fn add_assign(&mut self, other: &Self) -> Result<(), F2Error> {
        self.check_same_length(other)?;
        for (a, b) in self.words.iter_mut().zip(&other.words) {
            *a ^= *b;
        }
        Ok(())
    }

    pub fn dot(&self, other: &Self) -> Result<bool, F2Error> {
        self.check_same_length(other)?;
        let ones: u32 = self
            .words
            .iter()
            .zip(&other.words)
            .map(|(a, b)| (a & b).count_ones())
            .sum();
        Ok(ones % 2 == 1)
    }
}

#[derive(Clone, PartialEq, Eq, Hash)]
pub struct F2Matrix {
    rows: usize,
    cols: usize,
    words_per_row: usize,
    data: Vec<u64>,
}

impl fmt::Debug for F2Matrix {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "F2Matrix {}x{}", self.rows, self.cols)?;
        for r in 0..self.rows {
            for c in 0..self.cols {
                write!(f, "{}", u8::from(self.bit(r, c)))?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct F2Rref {
    pub matrix: F2Matrix,
    pub pivot_columns: Vec<usize>,
}

impl F2Rref {
    pub fn rank(&self) -> usize {
        self.pivot_columns.len()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct F2AffineSpace {
    particular: F2Vector,
    direction: Vec<F2Vector>,
}

impl F2AffineSpace {
    pub fn particular(&self) -> &F2Vector {
        &self.particular
    }

    pub fn direction(&self) -> &[F2Vector] {
        &self.direction
    }

    pub fn dimension(&self) -> usize {
        self.direction.len()
    }

    pub fn count(&self) -> BigUint {
        BigUint::one() << self.direction.len()
    }

    pub fn contains(&self, x: &F2Vector) -> Result<bool, F2Error> {
        let difference = x.add(&self.particular)?;
        if self.direction.is_empty() {
            return Ok(difference.is_zero());
        }
        let basis = F2Matrix::from_columns(self.particular.len(), &self.direction)?;
        Ok(basis.solve(&difference)?.is_some())
    }

    pub fn enumerate(&self, limit: usize) -> Result<Vec<F2Vector>, F2Error> {
        if self.direction.len() >= usize::BITS as usize || (1usize << self.direction.len()) > limit
        {
            return Err(F2Error::EnumerationLimit {
                count: self.count().to_string(),
                limit,
            });
        }
        let total = 1usize << self.direction.len();
        let mut out = Vec::with_capacity(total);
        for mask in 0..total {
            let mut x = self.particular.clone();
            for (i, d) in self.direction.iter().enumerate() {
                if (mask >> i) & 1 == 1 {
                    x.add_assign(d)?;
                }
            }
            out.push(x);
        }
        Ok(out)
    }
}

impl F2Matrix {
    fn bit(&self, r: usize, c: usize) -> bool {
        (self.data[r * self.words_per_row + c / WORD_BITS] >> (c % WORD_BITS)) & 1 == 1
    }

    fn row_slice(&self, r: usize) -> &[u64] {
        &self.data[r * self.words_per_row..(r + 1) * self.words_per_row]
    }

    fn check_row(&self, r: usize) -> Result<(), F2Error> {
        if r < self.rows {
            Ok(())
        } else {
            Err(F2Error::IndexOutOfRange {
                index: r,
                len: self.rows,
            })
        }
    }

    fn check_col(&self, c: usize) -> Result<(), F2Error> {
        if c < self.cols {
            Ok(())
        } else {
            Err(F2Error::IndexOutOfRange {
                index: c,
                len: self.cols,
            })
        }
    }

    pub fn zeros(rows: usize, cols: usize) -> Result<Self, F2Error> {
        check_entries(rows, cols)?;
        let words_per_row = words_for(cols);
        Ok(Self {
            rows,
            cols,
            words_per_row,
            data: vec![0; rows * words_per_row],
        })
    }

    pub fn identity(n: usize) -> Result<Self, F2Error> {
        let mut m = Self::zeros(n, n)?;
        for i in 0..n {
            m.set(i, i, true)?;
        }
        Ok(m)
    }

    pub fn from_rows(rows: &[Vec<u8>]) -> Result<Self, F2Error> {
        let cols = rows.first().map_or(0, Vec::len);
        let mut m = Self::zeros(rows.len(), cols)?;
        for (r, row) in rows.iter().enumerate() {
            if row.len() != cols {
                return Err(F2Error::Ragged {
                    row: r,
                    expected: cols,
                    actual: row.len(),
                });
            }
            for (c, &entry) in row.iter().enumerate() {
                match entry {
                    0 => {}
                    1 => m.set(r, c, true)?,
                    other => {
                        return Err(F2Error::NotBinary {
                            row: r,
                            col: c,
                            value: i64::from(other),
                        })
                    }
                }
            }
        }
        Ok(m)
    }

    pub fn from_integer_rows(rows: &[Vec<i64>]) -> Result<Self, F2Error> {
        let cols = rows.first().map_or(0, Vec::len);
        let mut m = Self::zeros(rows.len(), cols)?;
        for (r, row) in rows.iter().enumerate() {
            if row.len() != cols {
                return Err(F2Error::Ragged {
                    row: r,
                    expected: cols,
                    actual: row.len(),
                });
            }
            for (c, &entry) in row.iter().enumerate() {
                if entry.rem_euclid(2) == 1 {
                    m.set(r, c, true)?;
                }
            }
        }
        Ok(m)
    }

    pub fn from_columns(rows: usize, columns: &[F2Vector]) -> Result<Self, F2Error> {
        let mut m = Self::zeros(rows, columns.len())?;
        for (c, column) in columns.iter().enumerate() {
            if column.len() != rows {
                return Err(F2Error::LengthMismatch {
                    expected: rows,
                    actual: column.len(),
                });
            }
            for r in column.support() {
                m.set(r, c, true)?;
            }
        }
        Ok(m)
    }

    pub fn from_row_vectors(cols: usize, rows: &[F2Vector]) -> Result<Self, F2Error> {
        let mut m = Self::zeros(rows.len(), cols)?;
        for (r, row) in rows.iter().enumerate() {
            if row.len() != cols {
                return Err(F2Error::LengthMismatch {
                    expected: cols,
                    actual: row.len(),
                });
            }
            for c in row.support() {
                m.set(r, c, true)?;
            }
        }
        Ok(m)
    }

    pub fn rows(&self) -> usize {
        self.rows
    }

    pub fn cols(&self) -> usize {
        self.cols
    }

    pub fn get(&self, r: usize, c: usize) -> Result<bool, F2Error> {
        self.check_row(r)?;
        self.check_col(c)?;
        Ok(self.bit(r, c))
    }

    pub fn set(&mut self, r: usize, c: usize, value: bool) -> Result<(), F2Error> {
        self.check_row(r)?;
        self.check_col(c)?;
        let index = r * self.words_per_row + c / WORD_BITS;
        let mask = 1u64 << (c % WORD_BITS);
        if value {
            self.data[index] |= mask;
        } else {
            self.data[index] &= !mask;
        }
        Ok(())
    }

    pub fn row(&self, r: usize) -> Result<F2Vector, F2Error> {
        self.check_row(r)?;
        Ok(F2Vector {
            len: self.cols,
            words: self.row_slice(r).to_vec(),
        })
    }

    pub fn column(&self, c: usize) -> Result<F2Vector, F2Error> {
        self.check_col(c)?;
        let mut v = F2Vector::zeros(self.rows)?;
        for r in 0..self.rows {
            if self.bit(r, c) {
                v.set(r, true)?;
            }
        }
        Ok(v)
    }

    pub fn to_rows(&self) -> Vec<Vec<u8>> {
        (0..self.rows)
            .map(|r| (0..self.cols).map(|c| u8::from(self.bit(r, c))).collect())
            .collect()
    }

    pub fn is_zero(&self) -> bool {
        self.data.iter().all(|&w| w == 0)
    }

    pub fn transpose(&self) -> Self {
        let mut t = Self {
            rows: self.cols,
            cols: self.rows,
            words_per_row: words_for(self.rows),
            data: vec![0; self.cols * words_for(self.rows)],
        };
        for r in 0..self.rows {
            for c in 0..self.cols {
                if self.bit(r, c) {
                    t.data[c * t.words_per_row + r / WORD_BITS] |= 1u64 << (r % WORD_BITS);
                }
            }
        }
        t
    }

    pub fn add(&self, other: &Self) -> Result<Self, F2Error> {
        if (self.rows, self.cols) != (other.rows, other.cols) {
            return Err(F2Error::ShapeMismatch {
                expected: (self.rows, self.cols),
                actual: (other.rows, other.cols),
            });
        }
        let mut out = self.clone();
        for (a, b) in out.data.iter_mut().zip(&other.data) {
            *a ^= *b;
        }
        Ok(out)
    }

    pub fn mul(&self, other: &Self) -> Result<Self, F2Error> {
        if self.cols != other.rows {
            return Err(F2Error::ShapeMismatch {
                expected: (self.cols, other.cols),
                actual: (other.rows, other.cols),
            });
        }
        let mut out = Self::zeros(self.rows, other.cols)?;
        for r in 0..self.rows {
            for k in 0..self.cols {
                if self.bit(r, k) {
                    for w in 0..out.words_per_row {
                        out.data[r * out.words_per_row + w] ^=
                            other.data[k * other.words_per_row + w];
                    }
                }
            }
        }
        Ok(out)
    }

    pub fn mul_vec(&self, v: &F2Vector) -> Result<F2Vector, F2Error> {
        if v.len != self.cols {
            return Err(F2Error::LengthMismatch {
                expected: self.cols,
                actual: v.len,
            });
        }
        let mut out = F2Vector::zeros(self.rows)?;
        for r in 0..self.rows {
            let ones: u32 = self
                .row_slice(r)
                .iter()
                .zip(&v.words)
                .map(|(a, b)| (a & b).count_ones())
                .sum();
            if ones % 2 == 1 {
                out.set(r, true)?;
            }
        }
        Ok(out)
    }

    pub fn vec_mul(&self, v: &F2Vector) -> Result<F2Vector, F2Error> {
        if v.len != self.rows {
            return Err(F2Error::LengthMismatch {
                expected: self.rows,
                actual: v.len,
            });
        }
        let mut out = F2Vector::zeros(self.cols)?;
        for r in v.support() {
            for (a, b) in out.words.iter_mut().zip(self.row_slice(r)) {
                *a ^= *b;
            }
        }
        Ok(out)
    }

    fn swap_rows(&mut self, a: usize, b: usize) {
        if a == b {
            return;
        }
        let w = self.words_per_row;
        for k in 0..w {
            self.data.swap(a * w + k, b * w + k);
        }
    }

    fn xor_row_into(&mut self, dst: usize, src: usize) {
        let w = self.words_per_row;
        if dst == src || w == 0 {
            return;
        }
        if src < dst {
            let (low, high) = self.data.split_at_mut(dst * w);
            for (d, s) in high[..w].iter_mut().zip(&low[src * w..src * w + w]) {
                *d ^= *s;
            }
        } else {
            let (low, high) = self.data.split_at_mut(src * w);
            for (d, s) in low[dst * w..dst * w + w].iter_mut().zip(&high[..w]) {
                *d ^= *s;
            }
        }
    }

    pub fn rref(&self) -> F2Rref {
        let mut m = self.clone();
        let mut pivot_columns = Vec::new();
        let mut next_row = 0;
        for c in 0..m.cols {
            if next_row == m.rows {
                break;
            }
            let Some(pivot) = (next_row..m.rows).find(|&r| m.bit(r, c)) else {
                continue;
            };
            m.swap_rows(next_row, pivot);
            for r in 0..m.rows {
                if r != next_row && m.bit(r, c) {
                    m.xor_row_into(r, next_row);
                }
            }
            pivot_columns.push(c);
            next_row += 1;
        }
        F2Rref {
            matrix: m,
            pivot_columns,
        }
    }

    pub fn rank(&self) -> usize {
        self.rref().rank()
    }

    pub fn inverse(&self) -> Result<Option<Self>, F2Error> {
        if self.rows != self.cols {
            return Err(F2Error::NotSquare {
                rows: self.rows,
                cols: self.cols,
            });
        }
        let width = self.cols.checked_mul(2).ok_or(F2Error::TooLarge {
            rows: self.rows,
            cols: self.cols,
            limit: MAX_F2_ENTRIES,
        })?;
        let mut augmented = Self::zeros(self.rows, width)?;
        for row in 0..self.rows {
            for col in 0..self.cols {
                if self.bit(row, col) {
                    augmented.set(row, col, true)?;
                }
            }
            augmented.set(row, self.cols + row, true)?;
        }
        let reduced = augmented.rref();
        if reduced
            .pivot_columns
            .iter()
            .take_while(|&&col| col < self.cols)
            .count()
            != self.cols
        {
            return Ok(None);
        }
        let mut inverse = Self::zeros(self.rows, self.cols)?;
        for row in 0..self.rows {
            for col in 0..self.cols {
                if reduced.matrix.bit(row, self.cols + col) {
                    inverse.set(row, col, true)?;
                }
            }
        }
        Ok(Some(inverse))
    }

    pub fn nullspace(&self) -> Vec<F2Vector> {
        let reduced = self.rref();
        let mut is_pivot = vec![false; self.cols];
        for &c in &reduced.pivot_columns {
            is_pivot[c] = true;
        }
        let mut basis = Vec::new();
        for free in (0..self.cols).filter(|&c| !is_pivot[c]) {
            let mut x = F2Vector {
                len: self.cols,
                words: vec![0; words_for(self.cols)],
            };
            x.words[free / WORD_BITS] |= 1u64 << (free % WORD_BITS);
            for (row, &pivot) in reduced.pivot_columns.iter().enumerate() {
                if reduced.matrix.bit(row, free) {
                    x.words[pivot / WORD_BITS] |= 1u64 << (pivot % WORD_BITS);
                }
            }
            basis.push(x);
        }
        basis
    }

    pub fn left_nullspace(&self) -> Vec<F2Vector> {
        self.transpose().nullspace()
    }

    pub fn column_space_basis(&self) -> Vec<F2Vector> {
        self.rref()
            .pivot_columns
            .iter()
            .filter_map(|&c| self.column(c).ok())
            .collect()
    }

    pub fn row_space_basis(&self) -> Vec<F2Vector> {
        let reduced = self.rref();
        (0..reduced.rank())
            .filter_map(|r| reduced.matrix.row(r).ok())
            .collect()
    }

    pub fn solve(&self, b: &F2Vector) -> Result<Option<F2AffineSpace>, F2Error> {
        if b.len != self.rows {
            return Err(F2Error::LengthMismatch {
                expected: self.rows,
                actual: b.len,
            });
        }
        let mut augmented = Self::zeros(self.rows, self.cols + 1)?;
        for r in 0..self.rows {
            for c in 0..self.cols {
                if self.bit(r, c) {
                    augmented.set(r, c, true)?;
                }
            }
            if b.bit(r) {
                augmented.set(r, self.cols, true)?;
            }
        }
        let reduced = augmented.rref();
        if reduced.pivot_columns.last() == Some(&self.cols) {
            return Ok(None);
        }
        let mut particular = F2Vector::zeros(self.cols)?;
        for (row, &pivot) in reduced.pivot_columns.iter().enumerate() {
            if reduced.matrix.bit(row, self.cols) {
                particular.set(pivot, true)?;
            }
        }
        Ok(Some(F2AffineSpace {
            particular,
            direction: self.nullspace(),
        }))
    }

    pub fn in_column_space(&self, b: &F2Vector) -> Result<bool, F2Error> {
        Ok(self.solve(b)?.is_some())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct F2Span {
    len: usize,
    echelon: Vec<(usize, F2Vector)>,
}

impl F2Span {
    pub fn new(len: usize) -> Self {
        Self {
            len,
            echelon: Vec::new(),
        }
    }

    pub fn dimension(&self) -> usize {
        self.echelon.len()
    }

    pub fn reduce(&self, v: &F2Vector) -> Result<F2Vector, F2Error> {
        if v.len != self.len {
            return Err(F2Error::LengthMismatch {
                expected: self.len,
                actual: v.len,
            });
        }
        let mut reduced = v.clone();
        for (pivot, basis) in &self.echelon {
            if reduced.bit(*pivot) {
                reduced.add_assign(basis)?;
            }
        }
        Ok(reduced)
    }

    pub fn contains(&self, v: &F2Vector) -> Result<bool, F2Error> {
        Ok(self.reduce(v)?.is_zero())
    }

    pub fn insert(&mut self, v: &F2Vector) -> Result<bool, F2Error> {
        let reduced = self.reduce(v)?;
        let Some(&pivot) = reduced.support().first() else {
            return Ok(false);
        };
        for (_, basis) in &mut self.echelon {
            if basis.bit(pivot) {
                basis.add_assign(&reduced)?;
            }
        }
        self.echelon.push((pivot, reduced));
        Ok(true)
    }
}

#[cfg(test)]
mod inverse_tests {
    use super::*;

    #[test]
    fn inverse_replays_both_products_and_crosses_word_boundaries() {
        let mut matrix = F2Matrix::identity(65).unwrap();
        matrix.set(0, 64, true).unwrap();
        matrix.set(1, 0, true).unwrap();
        let inverse = matrix.inverse().unwrap().unwrap();
        let identity = F2Matrix::identity(65).unwrap();
        assert_eq!(matrix.mul(&inverse).unwrap(), identity);
        assert_eq!(inverse.mul(&matrix).unwrap(), identity);
        assert_ne!(inverse, matrix);
    }

    #[test]
    fn inverse_distinguishes_singular_nonsquare_and_empty() {
        let singular = F2Matrix::from_rows(&[vec![1, 1], vec![1, 1]]).unwrap();
        assert_eq!(singular.inverse().unwrap(), None);
        assert!(matches!(
            F2Matrix::zeros(2, 3).unwrap().inverse(),
            Err(F2Error::NotSquare { rows: 2, cols: 3 })
        ));
        let empty = F2Matrix::zeros(0, 0).unwrap();
        assert_eq!(empty.inverse().unwrap(), Some(empty));
    }

    #[test]
    fn inverse_refuses_oversized_augmentation_before_allocating() {
        let n = 1 << 14;
        let matrix = F2Matrix::zeros(n, n).unwrap();
        assert!(matches!(matrix.inverse(), Err(F2Error::TooLarge { .. })));
    }
}
