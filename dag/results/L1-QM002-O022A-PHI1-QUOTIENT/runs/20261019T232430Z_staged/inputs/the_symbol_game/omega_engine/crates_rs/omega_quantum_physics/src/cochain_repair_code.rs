// AuthorityEffect: None.

//! Repair codes read off a declared cochain complex over GF(2).
//!
//! A complex `C^0 --d0--> C^1 --d1--> C^2` over GF(2) is declared by its two
//! matrices, and `d1 d0 = 0` is replayed at construction with
//! `omega_number_theory::gf2::F2Matrix`. An error is a 1-cochain `e`; its
//! syndrome is the coboundary `d1 e`; the harmless errors are the coboundaries
//! `im d0`; the logical classes are `H^1 = ker d1 / im d0`. Computed exactly:
//!
//! - `dim H^1 = dim C^1 - rank d0 - rank d1`;
//! - the syndrome `d1 e`, and whether `e` lies in `im d0`;
//! - the CSS stabilizer code with one `X` generator per column of `d0` and one
//!   `Z` generator per row of `d1`. Its distance against bit flips (alphabet
//!   `{X}` in [`crate::stabilizer_code_distance`]) is the repair distance
//!   `d = min{|c| : c in ker d1 \ im d0}`: a bit-flip string commutes with the
//!   `Z` checks exactly when it is a cocycle, and it lies in the stabilizer
//!   group exactly when it is a coboundary;
//! - for independent bit flips of rational probability `p` on every 1-cell,
//!   the exact probability that decoding returns the error to its own class,
//!   under the maximum-likelihood rule (for each syndrome, the class of largest
//!   probability) and under the minimum-weight rule (for each syndrome, the
//!   class of its lightest error, ties to the smaller bit mask).
//!
//! The maximum-likelihood probability is never below `1 / |H^1|`: for each
//! syndrome it takes the largest of `|H^1|` class probabilities. At `p = 1/2`
//! every class of every fiber is equally likely, so every rule gets exactly
//! `1 / |H^1|`.
//!
//! [`torus`] declares the periodic `L x L` square lattice and [`repetition`]
//! the length-`n` repetition code (`C^0 = 0`, one check per adjacent pair).
//! Refused: an empty `C^1`, ragged or non-binary matrices, `d1 d0 != 0`,
//! cochains of the wrong length or with entries other than `0, 1`,
//! probabilities outside `[0, 1]`, and enumeration beyond
//! [`MAX_ENUMERATED_CELLS`] cells.

use std::collections::{BTreeMap, BTreeSet};

use crate::pauli::Pauli;
use num_bigint::BigInt;
use num_traits::{One, Signed};
use omega_number_theory::gf2::{F2Error, F2Matrix, F2Vector};
use omega_number_theory::rational::Rational;

use crate::stabilizer_code_distance::{
    CodeDistance, StabilizerCode, StabilizerCodeError, DEFAULT_CANDIDATE_BUDGET,
};

/// The largest `dim C^0` and `dim C^1` for exact enumeration of all errors.
pub const MAX_ENUMERATED_CELLS: usize = 16;

/// Refusals for complexes, cochains and probabilities.
#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum CochainCodeError {
    #[error("C^1 must have at least one cell")]
    EmptyCochains,
    #[error("declared code matrices exceed the finite storage budget")]
    StorageBudget,
    #[error("lattice constructor refused: {0}")]
    Lattice(String),
    #[error("d0 row {row} has length {actual}, expected dim C^0 = {expected}")]
    D0RowLength {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("d1 row {row} has length {actual}, expected dim C^1 = {expected}")]
    D1RowLength {
        row: usize,
        expected: usize,
        actual: usize,
    },
    #[error("{map} entry ({row}, {column}) is not 0 or 1")]
    NonBinary {
        map: &'static str,
        row: usize,
        column: usize,
    },
    #[error("d1 d0 is nonzero over GF(2)")]
    ClosureFails,
    #[error("a cochain has {actual} coordinates, expected {expected}")]
    CochainLength { expected: usize, actual: usize },
    #[error("cochain coordinate {index} is not 0 or 1")]
    NonBinaryCochain { index: usize },
    #[error("probability {0} is outside [0, 1]")]
    ProbabilityOutOfRange(Rational),
    #[error(
        "exact enumeration is limited to {MAX_ENUMERATED_CELLS} cells in C^0 and C^1 and 64 in C^2"
    )]
    TooLargeToEnumerate,
    #[error("the declared family needs size at least {minimum}")]
    FamilyTooSmall { minimum: usize },
    #[error("stabilizer code refused: {0}")]
    Stabilizer(#[from] StabilizerCodeError),
    #[error(transparent)]
    Binary(#[from] F2Error),
}

/// How a decoder picks a class for each syndrome.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DecodingRule {
    MaximumLikelihood,
    MinimumWeight,
}

/// A declared GF(2) cochain complex read as a repair code.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CochainRepairCode {
    c0: usize,
    d0: Vec<Vec<u8>>,
    d1: Vec<Vec<u8>>,
    d0_matrix: F2Matrix,
    d1_matrix: F2Matrix,
    ranks: [usize; 2],
}

/// Bit `i` of the mask is entry `i`.
fn bit_mask(bits: impl Iterator<Item = u8>) -> u32 {
    bits.enumerate()
        .fold(0, |acc, (i, b)| acc | (u32::from(b) << i))
}

impl CochainRepairCode {
    /// `d0` is `dim C^1 x c0`, `d1` is `dim C^2 x dim C^1`.
    pub fn new(c0: usize, d0: Vec<Vec<u8>>, d1: Vec<Vec<u8>>) -> Result<Self, CochainCodeError> {
        let c1 = d0.len();
        if c0 > 4096 || c1 > 4096 || d1.len() > 4096 {
            return Err(CochainCodeError::StorageBudget);
        }
        if c0
            .checked_mul(c1)
            .and_then(|n| d1.len().checked_mul(c1).and_then(|m| n.checked_add(m)))
            .is_none_or(|n| n > 1 << 20)
        {
            return Err(CochainCodeError::StorageBudget);
        }
        if c1 == 0 {
            return Err(CochainCodeError::EmptyCochains);
        }
        if let Some(row) = d0.iter().position(|r| r.len() != c0) {
            return Err(CochainCodeError::D0RowLength {
                row,
                expected: c0,
                actual: d0[row].len(),
            });
        }
        if let Some(row) = d1.iter().position(|r| r.len() != c1) {
            return Err(CochainCodeError::D1RowLength {
                row,
                expected: c1,
                actual: d1[row].len(),
            });
        }
        for (map, matrix) in [("d0", &d0), ("d1", &d1)] {
            for (row, values) in matrix.iter().enumerate() {
                if let Some(column) = values.iter().position(|&v| v > 1) {
                    return Err(CochainCodeError::NonBinary { map, row, column });
                }
            }
        }
        let d0_matrix = F2Matrix::from_rows(&d0)?;
        let d1_matrix = if d1.is_empty() {
            F2Matrix::zeros(0, c1)?
        } else {
            F2Matrix::from_rows(&d1)?
        };
        if !d1_matrix.mul(&d0_matrix)?.is_zero() {
            return Err(CochainCodeError::ClosureFails);
        }
        let ranks = [d0_matrix.rank(), d1_matrix.rank()];
        Ok(Self {
            c0,
            d0,
            d1,
            d0_matrix,
            d1_matrix,
            ranks,
        })
    }

    /// `[dim C^0, dim C^1, dim C^2]`.
    pub fn cells(&self) -> [usize; 3] {
        [self.c0, self.d0.len(), self.d1.len()]
    }

    /// `dim H^1 = dim C^1 - rank d0 - rank d1`.
    pub fn cohomology_dimension(&self) -> usize {
        self.d0.len() - self.ranks[0] - self.ranks[1]
    }

    fn check_cochain(&self, e: &[u8]) -> Result<(), CochainCodeError> {
        if e.len() != self.d0.len() {
            return Err(CochainCodeError::CochainLength {
                expected: self.d0.len(),
                actual: e.len(),
            });
        }
        if let Some(index) = e.iter().position(|&v| v > 1) {
            return Err(CochainCodeError::NonBinaryCochain { index });
        }
        Ok(())
    }

    /// The coboundary `d1 e`.
    pub fn syndrome(&self, e: &[u8]) -> Result<Vec<u8>, CochainCodeError> {
        self.check_cochain(e)?;
        Ok(self.d1_matrix.mul_vec(&F2Vector::from_bits(e)?)?.to_bits())
    }

    /// Whether `e = d0 f` for some `f`.
    pub fn is_coboundary(&self, e: &[u8]) -> Result<bool, CochainCodeError> {
        Ok(self.coboundary_preimage(e)?.is_some())
    }

    /// A replayable primitive repair, using the shared bit-packed solver.
    /// This scales with matrix size instead of enumerating all 0-cochains.
    pub fn coboundary_preimage(&self, e: &[u8]) -> Result<Option<Vec<u8>>, CochainCodeError> {
        self.check_cochain(e)?;
        Ok(self
            .d0_matrix
            .solve(&F2Vector::from_bits(e)?)?
            .map(|space| space.particular().to_bits()))
    }

    /// One `X` generator per column of `d0`, one `Z` generator per row of `d1`.
    pub fn stabilizer_code(&self) -> Result<StabilizerCode, CochainCodeError> {
        let letter = |bit: u8, p: Pauli| if bit == 1 { p } else { Pauli::I };
        let mut generators: Vec<Vec<Pauli>> = (0..self.c0)
            .map(|v| self.d0.iter().map(|row| letter(row[v], Pauli::X)).collect())
            .collect();
        generators.extend(
            self.d1
                .iter()
                .map(|row| row.iter().map(|&b| letter(b, Pauli::Z)).collect()),
        );
        Ok(StabilizerCode::try_new_with_length(self.d0.len(), generators)?)
    }

    /// `d = min{|c| : c in ker d1 \ im d0}`, with a minimal cocycle as witness.
    pub fn repair_distance(&self) -> Result<CodeDistance, CochainCodeError> {
        Ok(self
            .stabilizer_code()?
            .distance_over(&[Pauli::X], DEFAULT_CANDIDATE_BUDGET)?)
    }

    /// The exact probability that `rule` returns an error of independent bit
    /// flips (probability `p` per cell) to its own class.
    pub fn logical_success_probability(
        &self,
        p: &Rational,
        rule: DecodingRule,
    ) -> Result<Rational, CochainCodeError> {
        if p.is_negative() || p > &Rational::one() {
            return Err(CochainCodeError::ProbabilityOutOfRange(p.clone()));
        }
        let c1 = self.d0.len();
        if c1 > MAX_ENUMERATED_CELLS || self.c0 > MAX_ENUMERATED_CELLS || self.d1.len() > 64 {
            return Err(CochainCodeError::TooLargeToEnumerate);
        }
        let columns: Vec<u32> = (0..self.c0)
            .map(|v| bit_mask(self.d0.iter().map(|row| row[v])))
            .collect();
        let faces: Vec<u32> = self
            .d1
            .iter()
            .map(|row| bit_mask(row.iter().copied()))
            .collect();
        let coboundaries: BTreeSet<u32> = (0u32..1 << self.c0)
            .map(|f| {
                (0..self.c0)
                    .filter(|v| f >> v & 1 == 1)
                    .fold(0, |acc, v| acc ^ columns[v])
            })
            .collect();

        let total_candidates = 1usize
            .checked_shl(c1 as u32)
            .ok_or(CochainCodeError::TooLargeToEnumerate)?;
        let work_budget = total_candidates
            .checked_mul(coboundaries.len().max(1))
            .ok_or(CochainCodeError::TooLargeToEnumerate)?;
        if work_budget > (1 << 24) {
            return Err(CochainCodeError::TooLargeToEnumerate);
        }

        struct Fiber {
            class_map: BTreeMap<u32, usize>,
            classes: Vec<(u32, Vec<u64>)>,
            lightest: (u32, usize),
        }
        let mut fibers: BTreeMap<u64, Fiber> = BTreeMap::new();
        for e in 0u32..1 << c1 {
            let syndrome = faces.iter().enumerate().fold(0u64, |acc, (f, face)| {
                acc | (u64::from((e & face).count_ones() & 1) << f)
            });
            let weight = e.count_ones();
            let fiber = fibers.entry(syndrome).or_insert_with(|| Fiber {
                class_map: BTreeMap::new(),
                classes: Vec::new(),
                lightest: (u32::MAX, 0),
            });
            let canonical_rep = coboundaries.iter().map(|&b| e ^ b).min().unwrap_or(e);
            let class = match fiber.class_map.get(&canonical_rep) {
                Some(&idx) => idx,
                None => {
                    let idx = fiber.classes.len();
                    fiber.class_map.insert(canonical_rep, idx);
                    fiber.classes.push((canonical_rep, vec![0; c1 + 1]));
                    idx
                }
            };
            fiber.classes[class].1[weight as usize] += 1;
            if weight < fiber.lightest.0 {
                fiber.lightest = (weight, class);
            }
        }

        let q = Rational::one() - p;
        let powers: Vec<Rational> = (0..=c1)
            .map(|w| num_traits::pow(p.clone(), w) * num_traits::pow(q.clone(), c1 - w))
            .collect();
        let probability = |counts: &[u64]| -> Rational {
            counts
                .iter()
                .zip(&powers)
                .map(|(&count, power)| power * Rational::from_integer(BigInt::from(count)))
                .sum()
        };
        Ok(fibers
            .values()
            .map(|fiber| match rule {
                DecodingRule::MaximumLikelihood => fiber
                    .classes
                    .iter()
                    .map(|(_, counts)| probability(counts))
                    .max()
                    .expect("every fiber holds at least one error"),
                DecodingRule::MinimumWeight => probability(&fiber.classes[fiber.lightest.1].1),
            })
            .sum())
    }
}

/// The periodic `side x side` square lattice: vertex `(i, j)` is cell
/// `i side + j`; edge `(i, j) -> (i, j + 1)` is cell `i side + j` and edge
/// `(i, j) -> (i + 1, j)` is cell `side^2 + i side + j`; face `(i, j)` is bounded
/// by those two edges and the ones leaving `(i, j + 1)` and `(i + 1, j)`.
pub fn torus(side: usize) -> Result<CochainRepairCode, CochainCodeError> {
    rectangular_torus(side, side)
}
/// Rectangular periodic lattice using the canonical homology cell numbering.
pub fn rectangular_torus(
    rows: usize,
    columns: usize,
) -> Result<CochainRepairCode, CochainCodeError> {
    if rows.checked_mul(columns).is_none_or(|n| n > 256) {
        return Err(CochainCodeError::StorageBudget);
    }
    let complex = omega_homology::square_lattice::periodic_square_complex(rows, columns)
        .map_err(|e| CochainCodeError::Lattice(e.to_string()))?
        .f2_complex()
        .map_err(|e| CochainCodeError::Lattice(e.to_string()))?;
    let d0 = complex
        .coboundary(0)
        .map_err(|e| CochainCodeError::Lattice(e.to_string()))?;
    let d1 = complex
        .coboundary(1)
        .map_err(|e| CochainCodeError::Lattice(e.to_string()))?;
    CochainRepairCode::new(complex.cell_count(0), d0.to_rows(), d1.to_rows())
}

/// The repetition code of length `length`: no 0-cells, `length` bits, and a
/// check on each adjacent pair.
pub fn repetition(length: usize) -> Result<CochainRepairCode, CochainCodeError> {
    if length < 2 {
        return Err(CochainCodeError::FamilyTooSmall { minimum: 2 });
    }
    if length > 1024 {
        return Err(CochainCodeError::StorageBudget);
    }
    let d1 = (0..length - 1)
        .map(|i| {
            (0..length)
                .map(|e| u8::from(e == i || e == i + 1))
                .collect()
        })
        .collect();
    CochainRepairCode::new(0, vec![Vec::new(); length], d1)
}
#[cfg(test)]
mod lattice_budget_tests {
    use super::*;
    #[test]
    fn cochain_lattice_constructors_refuse_unbounded_allocation() {
        assert!(matches!(
            torus(usize::MAX),
            Err(CochainCodeError::StorageBudget)
        ));
        assert!(matches!(
            repetition(usize::MAX),
            Err(CochainCodeError::StorageBudget)
        ));
        let t = rectangular_torus(2, 3).unwrap();
        assert_eq!(t.cells(), [6, 12, 6]);
        assert_eq!(t.cohomology_dimension(), 2);
    }
}
