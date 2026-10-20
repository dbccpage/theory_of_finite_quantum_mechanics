use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_bigint::{BigInt, BigUint};
use num_traits::{One, ToPrimitive, Zero};
use thiserror::Error;

use crate::error::FusionError;
use crate::scalar::FusionScalar;
use linear_algebra::exact_field::{characteristic_polynomial, matrix};
use omega_number_theory::algebraic_real::{largest_real_root, RealAlgebraic};

pub const MAX_RANK: usize = 32;

pub const MAX_FUSION_WORD: usize = 1 << 14;

fn admit_rank(rank: usize) -> Result<(), FusionError> {
    if rank == 0 || rank > MAX_RANK {
        return Err(FusionError::RankOutOfRange {
            rank,
            max: MAX_RANK,
        });
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum RingDefect {
    #[error("unit law fails on label {label}")]
    Unit { label: usize },
    #[error("labels {left} and {right} do not commute")]
    Commutativity { left: usize, right: usize },
    #[error(
        "associativity fails on {labels:?}: outcome {outcome} occurs {left} times in the \
         left bracketing and {right} in the right"
    )]
    Associativity {
        labels: (usize, usize, usize),
        outcome: usize,
        left: u128,
        right: u128,
    },
    #[error("label {label} has no dual (unit occurs once in label x dual, involutively)")]
    Duality { label: usize },
    #[error("Frobenius reciprocity fails on {labels:?}")]
    Reciprocity { labels: (usize, usize, usize) },
    #[error("a multiplicity sum overflows 128 bits on {labels:?}")]
    Overflow { labels: (usize, usize, usize) },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AbelianGroup {
    moduli: Vec<usize>,
    order: usize,
}

impl AbelianGroup {
    pub fn new(moduli: &[usize]) -> Result<Self, FusionError> {
        let mut order: usize = 1;
        for &m in moduli {
            if m < 2 {
                return Err(FusionError::RankOutOfRange {
                    rank: m,
                    max: MAX_RANK,
                });
            }
            order = order.checked_mul(m).ok_or(FusionError::Overflow {
                context: "sizing an abelian group",
            })?;
            if order > MAX_RANK {
                return Err(FusionError::RankOutOfRange {
                    rank: order,
                    max: MAX_RANK,
                });
            }
        }
        Ok(Self {
            moduli: moduli.to_vec(),
            order,
        })
    }

    pub fn moduli(&self) -> &[usize] {
        &self.moduli
    }

    pub fn order(&self) -> usize {
        self.order
    }

    pub fn digits(&self, label: usize) -> Result<Vec<usize>, FusionError> {
        if label >= self.order {
            return Err(FusionError::Label {
                label,
                rank: self.order,
            });
        }
        let mut rest = label;
        Ok(self
            .moduli
            .iter()
            .map(|&m| {
                let digit = rest % m;
                rest /= m;
                digit
            })
            .collect())
    }

    pub fn label(&self, digits: &[usize]) -> Result<usize, FusionError> {
        if digits.len() != self.moduli.len() {
            return Err(FusionError::ListLength {
                what: "digits",
                expected: self.moduli.len(),
                got: digits.len(),
            });
        }
        let mut label = 0usize;
        let mut stride = 1usize;
        for (&digit, &m) in digits.iter().zip(&self.moduli) {
            if digit >= m {
                return Err(FusionError::Label {
                    label: digit,
                    rank: m,
                });
            }
            label += digit * stride;
            stride *= m;
        }
        Ok(label)
    }

    pub fn add(&self, a: usize, b: usize) -> Result<usize, FusionError> {
        let (da, db) = (self.digits(a)?, self.digits(b)?);
        let sum: Vec<usize> = da
            .iter()
            .zip(&db)
            .zip(&self.moduli)
            .map(|((x, y), m)| (x + y) % m)
            .collect();
        self.label(&sum)
    }

    pub fn negate(&self, a: usize) -> Result<usize, FusionError> {
        let da = self.digits(a)?;
        let negated: Vec<usize> = da
            .iter()
            .zip(&self.moduli)
            .map(|(x, m)| (m - x) % m)
            .collect();
        self.label(&negated)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FusionTable {
    rank: usize,
    names: Vec<String>,
    n: Vec<u64>,
}

impl FusionTable {
    pub fn new(rank: usize, multiplicities: Vec<u64>) -> Result<Self, FusionError> {
        admit_rank(rank)?;
        let names = (0..rank).map(|label| label.to_string()).collect();
        Self::with_names(rank, names, multiplicities)
    }

    pub fn with_names(
        rank: usize,
        names: Vec<String>,
        multiplicities: Vec<u64>,
    ) -> Result<Self, FusionError> {
        admit_rank(rank)?;
        let expected = rank * rank * rank;
        if multiplicities.len() != expected {
            return Err(FusionError::TableShape {
                rank,
                expected,
                got: multiplicities.len(),
            });
        }
        if names.len() != rank {
            return Err(FusionError::ListLength {
                what: "label names",
                expected: rank,
                got: names.len(),
            });
        }
        Ok(Self {
            rank,
            names,
            n: multiplicities,
        })
    }

    pub fn from_array<const R: usize>(n: [[[u64; R]; R]; R]) -> Result<Self, FusionError> {
        admit_rank(R)?;
        let flat = n
            .iter()
            .flat_map(|plane| plane.iter().flat_map(|row| row.iter().copied()))
            .collect();
        Self::new(R, flat)
    }

    pub fn rank(&self) -> usize {
        self.rank
    }

    pub fn names(&self) -> &[String] {
        &self.names
    }

    fn check(&self, label: usize) -> Result<usize, FusionError> {
        if label < self.rank {
            Ok(label)
        } else {
            Err(FusionError::Label {
                label,
                rank: self.rank,
            })
        }
    }

    fn at(&self, a: usize, b: usize, c: usize) -> u64 {
        self.n
            .get((a * self.rank + b) * self.rank + c)
            .copied()
            .unwrap_or(0)
    }

    pub fn multiplicity(&self, a: usize, b: usize, c: usize) -> Result<u64, FusionError> {
        Ok(self.at(self.check(a)?, self.check(b)?, self.check(c)?))
    }

    fn associativity_sum(&self, first: impl Fn(usize) -> (u64, u64)) -> Option<u128> {
        (0..self.rank).try_fold(0u128, |acc, e| {
            let (x, y) = first(e);
            acc.checked_add(u128::from(x).checked_mul(u128::from(y))?)
        })
    }

    fn unique_dual(&self, a: usize) -> Result<usize, usize> {
        let mut found = None;
        for b in 0..self.rank {
            let multiplicity = self.at(a, b, 0);
            if multiplicity > 0 {
                if found.is_some() || multiplicity != 1 {
                    return Err(a);
                }
                found = Some(b);
            }
        }
        found.ok_or(a)
    }

    fn dual_labels(&self) -> Result<Vec<usize>, usize> {
        let mut dual = Vec::with_capacity(self.rank);
        for a in 0..self.rank {
            dual.push(self.unique_dual(a)?);
        }
        for a in 0..self.rank {
            let back = dual.get(dual.get(a).copied().unwrap_or(a)).copied();
            if back != Some(a) {
                return Err(a);
            }
        }
        Ok(dual)
    }

    fn first_unit_defect(&self) -> Option<RingDefect> {
        (0..self.rank)
            .find(|&label| {
                (0..self.rank).any(|c| {
                    let expected = u64::from(c == label);
                    self.at(0, label, c) != expected || self.at(label, 0, c) != expected
                })
            })
            .map(|label| RingDefect::Unit { label })
    }

    fn first_commutativity_defect(&self) -> Option<RingDefect> {
        (0..self.rank)
            .flat_map(|left| (left + 1..self.rank).map(move |right| (left, right)))
            .find(|&(left, right)| {
                (0..self.rank).any(|c| self.at(left, right, c) != self.at(right, left, c))
            })
            .map(|(left, right)| RingDefect::Commutativity { left, right })
    }

    fn associativity_defect_at(
        &self,
        a: usize,
        b: usize,
        c: usize,
        d: usize,
    ) -> Option<RingDefect> {
        let left = self.associativity_sum(|e| (self.at(a, b, e), self.at(e, c, d)));
        let right = self.associativity_sum(|f| (self.at(b, c, f), self.at(a, f, d)));
        match (left, right) {
            (Some(left), Some(right)) if left != right => Some(RingDefect::Associativity {
                labels: (a, b, c),
                outcome: d,
                left,
                right,
            }),
            (Some(_), Some(_)) => None,
            _ => Some(RingDefect::Overflow { labels: (a, b, c) }),
        }
    }

    fn associativity_defect_for_pair(&self, a: usize, b: usize) -> Option<RingDefect> {
        for c in 0..self.rank {
            for d in 0..self.rank {
                if let Some(defect) = self.associativity_defect_at(a, b, c, d) {
                    return Some(defect);
                }
            }
        }
        None
    }

    fn first_associativity_defect(&self) -> Option<RingDefect> {
        for a in 0..self.rank {
            for b in 0..self.rank {
                if let Some(defect) = self.associativity_defect_for_pair(a, b) {
                    return Some(defect);
                }
            }
        }
        None
    }

    fn first_duality_defect(&self) -> Option<RingDefect> {
        self.dual_labels()
            .err()
            .map(|label| RingDefect::Duality { label })
    }

    fn reciprocity_defect_for_pair(&self, dual: &[usize], a: usize, b: usize) -> Option<usize> {
        let a_star = dual.get(a).copied().unwrap_or(a);
        let b_star = dual.get(b).copied().unwrap_or(b);
        (0..self.rank).find(|&c| {
            let here = self.at(a, b, c);
            here != self.at(a_star, c, b) || here != self.at(c, b_star, a)
        })
    }

    fn first_reciprocity_defect(&self, dual: &[usize]) -> Option<RingDefect> {
        for a in 0..self.rank {
            for b in 0..self.rank {
                if let Some(c) = self.reciprocity_defect_for_pair(dual, a, b) {
                    return Some(RingDefect::Reciprocity { labels: (a, b, c) });
                }
            }
        }
        None
    }

    pub fn first_defect(&self) -> Option<RingDefect> {
        self.first_unit_defect()
            .or_else(|| self.first_commutativity_defect())
            .or_else(|| self.first_noncommutative_remainder())
    }

    pub fn first_defect_allowing_noncommutative(&self) -> Option<RingDefect> {
        self.first_unit_defect()
            .or_else(|| self.first_noncommutative_remainder())
    }

    fn first_noncommutative_remainder(&self) -> Option<RingDefect> {
        self.first_associativity_defect()
            .or_else(|| self.first_duality_defect())
            .or_else(|| {
                let dual = self.dual_labels().ok()?;
                self.first_reciprocity_defect(&dual)
            })
    }

    pub fn validate(&self) -> Result<FusionRing, FusionError> {
        FusionRing::try_new(self.clone())
    }

    pub fn charge_counts(&self, label: usize, copies: usize) -> Result<Vec<BigUint>, FusionError> {
        let label = self.check(label)?;
        if copies > MAX_FUSION_WORD {
            return Err(FusionError::Budget {
                what: "fusion word length",
                requested: copies as u128,
                limit: MAX_FUSION_WORD as u128,
            });
        }
        let mut counts = self.unit_counts();
        for _ in 0..copies {
            counts = self.step(&counts, label);
        }
        Ok(counts)
    }

    pub fn charge_counts_u64(&self, label: usize, copies: usize) -> Result<Vec<u64>, FusionError> {
        self.charge_counts(label, copies)?
            .iter()
            .map(|count| {
                count.to_u64().ok_or(FusionError::Overflow {
                    context: "narrowing a fusion-path count to u64",
                })
            })
            .collect()
    }

    fn unit_counts(&self) -> Vec<BigUint> {
        (0..self.rank)
            .map(|c| {
                if c == 0 {
                    BigUint::one()
                } else {
                    BigUint::zero()
                }
            })
            .collect()
    }

    fn step(&self, counts: &[BigUint], w: usize) -> Vec<BigUint> {
        (0..self.rank)
            .map(|c| {
                (0..self.rank)
                    .map(|a| {
                        counts.get(a).map_or_else(BigUint::zero, |count| {
                            count * BigUint::from(self.at(a, w, c))
                        })
                    })
                    .fold(BigUint::zero(), |acc, term| acc + term)
            })
            .collect()
    }

    pub fn ising() -> Self {
        let n = [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
            [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
        ];
        let flat = n
            .iter()
            .flat_map(|plane| plane.iter().flat_map(|row| row.iter().copied()))
            .collect();
        Self {
            rank: 3,
            names: ["1", "sigma", "psi"].map(String::from).to_vec(),
            n: flat,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FusionRing {
    table: FusionTable,
    dual: Vec<usize>,
}

impl FusionRing {
    pub fn try_new(table: FusionTable) -> Result<Self, FusionError> {
        if let Some(defect) = table.first_defect_allowing_noncommutative() {
            return Err(FusionError::Ring(defect));
        }
        let dual = table
            .dual_labels()
            .map_err(|label| FusionError::Ring(RingDefect::Duality { label }))?;
        Ok(Self { table, dual })
    }

    pub fn rank(&self) -> usize {
        self.table.rank
    }

    pub fn names(&self) -> &[String] {
        &self.table.names
    }

    pub fn unit(&self) -> usize {
        0
    }

    pub fn table(&self) -> &FusionTable {
        &self.table
    }

    pub fn dual(&self, a: usize) -> Result<usize, FusionError> {
        self.table.check(a)?;
        self.dual.get(a).copied().ok_or(FusionError::Label {
            label: a,
            rank: self.table.rank,
        })
    }

    pub fn multiplicity(&self, a: usize, b: usize, c: usize) -> Result<u64, FusionError> {
        self.table.multiplicity(a, b, c)
    }

    pub(crate) fn n(&self, a: usize, b: usize, c: usize) -> u64 {
        self.table.at(a, b, c)
    }

    pub fn fuse(&self, a: usize, b: usize) -> Result<Vec<usize>, FusionError> {
        self.table.check(a)?;
        self.table.check(b)?;
        Ok((0..self.table.rank)
            .filter(|&c| self.table.at(a, b, c) > 0)
            .collect())
    }

    pub fn is_commutative(&self) -> bool {
        self.table.first_commutativity_defect().is_none()
    }

    pub fn is_multiplicity_free(&self) -> bool {
        self.table.n.iter().all(|&m| m <= 1)
    }

    pub fn is_pointed(&self) -> bool {
        (0..self.rank()).all(|a| {
            (0..self.rank()).all(|b| {
                (0..self.rank()).try_fold(0u64, |acc, c| acc.checked_add(self.table.at(a, b, c)))
                    == Some(1)
            })
        })
    }

    pub fn fusion_paths(&self, word: &[usize], target: usize) -> Result<BigUint, FusionError> {
        let counts = self.fusion_path_counts(word)?;
        self.table.check(target)?;
        Ok(counts.get(target).cloned().unwrap_or_else(BigUint::zero))
    }

    pub fn fusion_path_counts(&self, word: &[usize]) -> Result<Vec<BigUint>, FusionError> {
        if word.len() > MAX_FUSION_WORD {
            return Err(FusionError::Budget {
                what: "fusion word length",
                requested: word.len() as u128,
                limit: MAX_FUSION_WORD as u128,
            });
        }
        let mut counts = self.table.unit_counts();
        for &w in word {
            self.table.check(w)?;
            counts = self.table.step(&counts, w);
        }
        Ok(counts)
    }

    pub fn fusion_matrix(&self, a: usize) -> Result<Vec<Vec<BigInt>>, FusionError> {
        self.table.check(a)?;
        Ok((0..self.rank())
            .map(|b| {
                (0..self.rank())
                    .map(|c| BigInt::from(self.table.at(a, b, c)))
                    .collect()
            })
            .collect())
    }

    fn rational_fusion_matrix(
        &self,
        a: usize,
    ) -> Result<BasicMatrix<omega_number_theory::rational::Rational>, FusionError> {
        matrix::from_rows(
            self.fusion_matrix(a)?
                .into_iter()
                .map(|row| {
                    row.into_iter()
                        .map(omega_number_theory::rational::Rational::from_integer)
                        .collect()
                })
                .collect(),
        )
        .map_err(FusionError::from)
    }

    pub fn characteristic_polynomial(&self, a: usize) -> Result<Vec<BigInt>, FusionError> {
        Ok(
            characteristic_polynomial::characteristic_polynomial(&self.rational_fusion_matrix(a)?)?
                .into_iter()
                .map(|q| q.to_integer())
                .collect(),
        )
    }

    pub fn frobenius_perron_dimension(&self, a: usize) -> Result<RealAlgebraic, FusionError> {
        largest_real_root(&self.characteristic_polynomial(a)?).map_err(FusionError::from)
    }

    pub fn global_dimension_squared(&self) -> Result<RealAlgebraic, FusionError> {
        let r = self.rank();
        let mut total = matrix::zeros::<omega_number_theory::rational::Rational>(r, r)?;
        for a in 0..r {
            let a_star = self.dual(a)?;
            let left = self.rational_fusion_matrix(a)?;
            let right = self.rational_fusion_matrix(a_star)?;
            total = matrix::add(&total, &matrix::multiply(&left, &right)?)?;
        }
        largest_real_root(
            &characteristic_polynomial::characteristic_polynomial(&total)?
                .into_iter()
                .map(|q| q.to_integer())
                .collect::<Vec<_>>(),
        )
        .map_err(FusionError::from)
    }

    pub fn verlinde_defects<K: FusionScalar>(
        &self,
        s_tilde: &BasicMatrix<K>,
        d_squared: &K,
    ) -> Result<Vec<[usize; 3]>, FusionError> {
        let r = self.rank();
        if s_tilde.shape() != (r, r) {
            return Err(FusionError::Shape {
                operation: "Verlinde check",
                left: s_tilde.shape(),
                right: (r, r),
            });
        }
        let d_inverse =
            omega_number_theory::scalar::inverse(d_squared).map_err(FusionError::from)?;
        let mut first_row_inverse = Vec::with_capacity(r);
        for x in 0..r {
            first_row_inverse.push(
                omega_number_theory::scalar::inverse(s_tilde.get_ref(0, x)?)
                    .map_err(FusionError::from)?,
            );
        }
        let mut defects = Vec::new();
        for a in 0..r {
            for b in 0..r {
                self.collect_verlinde_pair(
                    s_tilde,
                    &first_row_inverse,
                    &d_inverse,
                    a,
                    b,
                    &mut defects,
                )?;
            }
        }
        Ok(defects)
    }

    fn verlinde_value<K: FusionScalar>(
        &self,
        s_tilde: &BasicMatrix<K>,
        weights: &[K],
        d_inverse: &K,
        a: usize,
        b: usize,
        c: usize,
    ) -> Result<K, FusionError> {
        let mut total = K::zero();
        for (x, weight) in weights.iter().enumerate() {
            let term = s_tilde
                .get_ref(a, x)?
                .mul(s_tilde.get_ref(b, x)?)
                .mul(&s_tilde.get_ref(c, x)?.conjugate())
                .mul(weight);
            total = total.add(&term);
        }
        Ok(total.mul(d_inverse))
    }

    fn collect_verlinde_pair<K: FusionScalar>(
        &self,
        s_tilde: &BasicMatrix<K>,
        weights: &[K],
        d_inverse: &K,
        a: usize,
        b: usize,
        defects: &mut Vec<[usize; 3]>,
    ) -> Result<(), FusionError> {
        for c in 0..self.rank() {
            let value = self.verlinde_value(s_tilde, weights, d_inverse, a, b, c)?;
            let expected = omega_number_theory::scalar::from_i64::<K>(
                i64::try_from(self.table.at(a, b, c)).map_err(|_| FusionError::Overflow {
                    context: "embedding a fusion coefficient",
                })?,
            );
            if value != expected {
                defects.push([a, b, c]);
            }
        }
        Ok(())
    }

    pub fn z_n(n: usize) -> Result<Self, FusionError> {
        Self::pointed(&[n], None)
    }

    pub fn pointed(moduli: &[usize], names: Option<Vec<String>>) -> Result<Self, FusionError> {
        let group = AbelianGroup::new(moduli)?;
        let order = group.order();
        let mut n = vec![0u64; order * order * order];
        for a in 0..order {
            for b in 0..order {
                let c = group.add(a, b)?;
                if let Some(slot) = n.get_mut((a * order + b) * order + c) {
                    *slot = 1;
                }
            }
        }
        let names = names.unwrap_or_else(|| (0..order).map(|k| k.to_string()).collect());
        Self::try_new(FusionTable::with_names(order, names, n)?)
    }

    pub fn ising() -> Result<Self, FusionError> {
        Self::try_new(FusionTable::ising())
    }

    pub fn fibonacci() -> Result<Self, FusionError> {
        let n = [[[1, 0], [0, 1]], [[0, 1], [1, 1]]];
        let names = ["1", "tau"].map(String::from).to_vec();
        let flat = n
            .iter()
            .flat_map(|plane| plane.iter().flat_map(|row| row.iter().copied()))
            .collect();
        Self::try_new(FusionTable::with_names(2, names, flat)?)
    }

    pub fn semion() -> Result<Self, FusionError> {
        Self::pointed(&[2], Some(["1", "s"].map(String::from).to_vec()))
    }

    pub fn toric_code() -> Result<Self, FusionError> {
        Self::pointed(
            &[2, 2],
            Some(["1", "e", "m", "eps"].map(String::from).to_vec()),
        )
    }

    pub fn three_fermion() -> Result<Self, FusionError> {
        Self::pointed(
            &[2, 2],
            Some(["1", "f1", "f2", "f3"].map(String::from).to_vec()),
        )
    }

    pub fn su2_level(k: usize) -> Result<Self, FusionError> {
        let rank = k.checked_add(1).ok_or(FusionError::Overflow {
            context: "sizing an SU(2) fusion ring",
        })?;
        if k == 0 || rank > MAX_RANK {
            return Err(FusionError::RankOutOfRange {
                rank,
                max: MAX_RANK,
            });
        }
        let mut n = vec![0u64; rank * rank * rank];
        for i in 0..rank {
            for j in 0..rank {
                Self::fill_su2_product(&mut n, rank, k, i, j);
            }
        }
        let names = (0..rank).map(|i| format!("j={i}/2")).collect();
        Self::try_new(FusionTable::with_names(rank, names, n)?)
    }

    fn fill_su2_product(n: &mut [u64], rank: usize, k: usize, i: usize, j: usize) {
        let low = i.abs_diff(j);
        let high = (i + j).min((2 * k) - (i + j));
        for l in low..=high {
            if (i + j + l) % 2 == 0 {
                if let Some(slot) = n.get_mut((i * rank + j) * rank + l) {
                    *slot = 1;
                }
            }
        }
    }

    pub fn rep_s3() -> Result<Self, FusionError> {
        let n = [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
            [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
        ];
        let flat = n
            .iter()
            .flat_map(|plane| plane.iter().flat_map(|row| row.iter().copied()))
            .collect();
        Self::try_new(FusionTable::with_names(
            3,
            ["1", "sgn", "std"].map(String::from).to_vec(),
            flat,
        )?)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::rational::rq;

    fn ising_array() -> [[[u64; 3]; 3]; 3] {
        [
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
            [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
        ]
    }

    #[test]
    fn the_declared_ising_table_satisfies_every_ring_law() {
        let table = FusionTable::ising();
        assert_eq!(table.first_defect(), None);
        assert_eq!(table.multiplicity(1, 1, 0), Ok(1));
        assert_eq!(table.multiplicity(1, 1, 2), Ok(1));
        assert_eq!(table.multiplicity(1, 1, 1), Ok(0));
        let ring = table.validate().unwrap();
        assert_eq!(ring.rank(), 3);
        assert_eq!(ring.dual(1), Ok(1));
        assert!(ring.is_commutative());
        assert!(ring.is_multiplicity_free());
        assert!(!ring.is_pointed());
        assert_eq!(FusionTable::from_array(ising_array()).unwrap(), {
            let mut named = FusionTable::ising();
            named.names = (0..3).map(|k| k.to_string()).collect();
            named
        });
    }

    #[test]
    fn mutated_tables_are_refused_by_exactly_the_law_they_break() {
        let base = ising_array();

        let mut unit = base;
        unit[0][1] = [0, 0, 1];
        assert_eq!(
            FusionTable::from_array(unit).unwrap().first_defect(),
            Some(RingDefect::Unit { label: 1 })
        );

        let mut lopsided = base;
        lopsided[2][1] = [1, 0, 0];
        assert_eq!(
            FusionTable::from_array(lopsided).unwrap().first_defect(),
            Some(RingDefect::Commutativity { left: 1, right: 2 })
        );

        let mut psi_absorbs = base;
        psi_absorbs[1][2] = [0, 0, 1];
        psi_absorbs[2][1] = [0, 0, 1];
        assert_eq!(
            FusionTable::from_array(psi_absorbs).unwrap().first_defect(),
            Some(RingDefect::Associativity {
                labels: (1, 1, 2),
                outcome: 0,
                left: 1,
                right: 0
            })
        );

        let doubled = FusionTable::from_array([[[1, 0], [0, 1]], [[0, 1], [2, 0]]]).unwrap();
        assert_eq!(
            doubled.first_defect(),
            Some(RingDefect::Duality { label: 1 })
        );
        assert_eq!(
            doubled.validate(),
            Err(FusionError::Ring(RingDefect::Duality { label: 1 }))
        );
    }

    #[test]
    fn frobenius_reciprocity_is_a_separate_law_with_its_own_defect() {
        let mut psi_absorbs = ising_array();
        psi_absorbs[1][2] = [0, 0, 1];
        psi_absorbs[2][1] = [0, 0, 1];
        let table = FusionTable::from_array(psi_absorbs).unwrap();
        assert_eq!(
            table.first_reciprocity_defect(&[0, 1, 2]),
            Some(RingDefect::Reciprocity { labels: (1, 1, 2) })
        );
        assert_eq!(
            FusionTable::ising().first_reciprocity_defect(&[0, 1, 2]),
            None
        );
        assert!(FusionTable::ising()
            .first_reciprocity_defect(&[0, 2, 1])
            .is_some());
    }

    #[test]
    fn shapes_and_labels_are_refused_with_typed_errors() {
        assert_eq!(
            FusionTable::new(0, vec![]),
            Err(FusionError::RankOutOfRange {
                rank: 0,
                max: MAX_RANK
            })
        );
        assert_eq!(
            FusionTable::new(3, vec![0; 26]),
            Err(FusionError::TableShape {
                rank: 3,
                expected: 27,
                got: 26
            })
        );
        assert_eq!(
            FusionTable::new(MAX_RANK + 1, vec![]),
            Err(FusionError::RankOutOfRange {
                rank: MAX_RANK + 1,
                max: MAX_RANK
            })
        );
        let ising = FusionTable::ising();
        assert_eq!(
            ising.multiplicity(3, 0, 0),
            Err(FusionError::Label { label: 3, rank: 3 })
        );
        assert_eq!(
            ising.charge_counts(3, 2),
            Err(FusionError::Label { label: 3, rank: 3 })
        );
        assert!(matches!(
            ising.charge_counts(1, MAX_FUSION_WORD + 1),
            Err(FusionError::Budget { .. })
        ));
        assert_eq!(
            FusionTable::with_names(2, vec!["only".into()], vec![0; 8]),
            Err(FusionError::ListLength {
                what: "label names",
                expected: 2,
                got: 1
            })
        );
    }

    #[test]
    fn sigma_paths_count_the_parity_sectors_with_exact_arithmetic() {
        let ising = FusionTable::ising();
        for l in 1..=10u32 {
            let half = BigUint::from(2u32).pow(l - 1);
            let even = ising.charge_counts(1, 2 * l as usize).unwrap();
            assert_eq!(even, vec![half.clone(), BigUint::zero(), half.clone()]);
            let odd = ising.charge_counts(1, 2 * l as usize - 1).unwrap();
            assert_eq!(odd, vec![BigUint::zero(), half, BigUint::zero()]);
        }
        assert_eq!(
            ising.charge_counts(1, 0).unwrap(),
            vec![BigUint::one(), BigUint::zero(), BigUint::zero()]
        );
        assert_eq!(
            ising.charge_counts_u64(2, 3).unwrap(),
            vec![0, 0, 1],
            "psi x psi x psi = psi"
        );
        let big = ising.charge_counts(1, 400).unwrap();
        assert_eq!(big[0], BigUint::from(2u32).pow(199));
        assert_eq!(
            ising.charge_counts_u64(1, 400),
            Err(FusionError::Overflow {
                context: "narrowing a fusion-path count to u64"
            })
        );
    }

    #[test]
    fn fusion_paths_of_mixed_words_and_targets() {
        let ring = FusionRing::ising().unwrap();
        assert_eq!(
            ring.fusion_paths(&[1, 1, 1, 1], 0).unwrap(),
            BigUint::from(2u32)
        );
        assert_eq!(ring.fusion_paths(&[1, 2, 1], 2).unwrap(), BigUint::one());
        assert_eq!(ring.fusion_paths(&[1, 2, 1], 0).unwrap(), BigUint::one());
        assert_eq!(ring.fusion_paths(&[], 0).unwrap(), BigUint::one());
        assert_eq!(ring.fusion_paths(&[1], 0).unwrap(), BigUint::zero());
        assert!(ring.fusion_paths(&[1, 7], 0).is_err());
        assert!(ring.fusion_paths(&[1], 9).is_err());
    }

    #[test]
    fn the_catalog_rings_have_their_known_shape() {
        let fib = FusionRing::fibonacci().unwrap();
        assert_eq!(fib.fuse(1, 1).unwrap(), vec![0, 1]);
        assert_eq!(fib.dual(1), Ok(1));

        let toric = FusionRing::toric_code().unwrap();
        assert!(toric.is_pointed());
        assert_eq!(toric.fuse(1, 2).unwrap(), vec![3], "e x m = eps");
        assert_eq!(toric.dual(3), Ok(3));

        let z5 = FusionRing::z_n(5).unwrap();
        assert!(z5.is_pointed());
        assert_eq!(z5.dual(2), Ok(3));
        assert_eq!(z5.fuse(2, 4).unwrap(), vec![1]);

        let semion = FusionRing::semion().unwrap();
        let su2_1 = FusionRing::su2_level(1).unwrap();
        assert_eq!(semion.table().n, su2_1.table().n);
        let su2_2 = FusionRing::su2_level(2).unwrap();
        assert_eq!(su2_2.table().n, FusionTable::ising().n);

        let su2_3 = FusionRing::su2_level(3).unwrap();
        assert_eq!(su2_3.fuse(3, 3).unwrap(), vec![0]);
        assert_eq!(su2_3.fuse(1, 1).unwrap(), vec![0, 2]);
        assert_eq!(
            su2_3.fuse(2, 2).unwrap(),
            vec![0, 2],
            "truncation at level 3"
        );

        let s3 = FusionRing::rep_s3().unwrap();
        assert_eq!(s3.fuse(2, 2).unwrap(), vec![0, 1, 2]);
        assert_eq!(s3.fuse(1, 2).unwrap(), vec![2]);
        assert!(s3.is_commutative());

        assert!(matches!(
            FusionRing::su2_level(0),
            Err(FusionError::RankOutOfRange { .. })
        ));
        assert!(matches!(
            FusionRing::su2_level(MAX_RANK),
            Err(FusionError::RankOutOfRange { .. })
        ));
    }

    #[test]
    fn the_abelian_group_labels_are_mixed_radix_and_refuse_bad_input() {
        let group = AbelianGroup::new(&[2, 3]).unwrap();
        assert_eq!(group.order(), 6);
        assert_eq!(group.digits(5).unwrap(), vec![1, 2]);
        assert_eq!(group.label(&[1, 2]).unwrap(), 5);
        assert_eq!(group.add(5, 3), Ok(0));
        assert_eq!(group.negate(5), Ok(3));
        assert!(group.digits(6).is_err());
        assert!(group.label(&[2, 0]).is_err());
        assert!(group.label(&[0]).is_err());
        assert!(AbelianGroup::new(&[1]).is_err());
        assert!(
            AbelianGroup::new(&[7, 7]).is_err(),
            "49 exceeds the maximum rank"
        );
    }

    #[test]
    fn frobenius_perron_dimensions_are_exact() {
        let ising = FusionRing::ising().unwrap();
        assert_eq!(
            ising.frobenius_perron_dimension(0).unwrap(),
            RealAlgebraic::Rational(rq(1, 1))
        );
        let sigma = ising.frobenius_perron_dimension(1).unwrap();
        let surd = sigma.as_quadratic().unwrap();
        assert_eq!(surd.radicand(), &BigInt::from(2));
        assert_eq!(surd.sqrt_part(), &rq(1, 1));
        assert_eq!(
            ising.frobenius_perron_dimension(2).unwrap(),
            RealAlgebraic::Rational(rq(1, 1))
        );
        assert_eq!(
            ising.global_dimension_squared().unwrap(),
            RealAlgebraic::Rational(rq(4, 1))
        );

        let fib = FusionRing::fibonacci().unwrap();
        let phi = fib.frobenius_perron_dimension(1).unwrap();
        let surd = phi.as_quadratic().unwrap();
        assert_eq!(surd.rational_part(), &rq(1, 2));
        assert_eq!(surd.radicand(), &BigInt::from(5));
        let d2 = fib.global_dimension_squared().unwrap();
        let surd = d2.as_quadratic().unwrap();
        assert_eq!(surd.rational_part(), &rq(5, 2));
        assert_eq!(surd.sqrt_part(), &rq(1, 2));
        assert_eq!(surd.radicand(), &BigInt::from(5));

        let toric = FusionRing::toric_code().unwrap();
        assert_eq!(
            toric.global_dimension_squared().unwrap(),
            RealAlgebraic::Rational(rq(4, 1))
        );
        let s3 = FusionRing::rep_s3().unwrap();
        assert_eq!(
            s3.frobenius_perron_dimension(2).unwrap(),
            RealAlgebraic::Rational(rq(2, 1))
        );
        assert_eq!(
            s3.global_dimension_squared().unwrap(),
            RealAlgebraic::Rational(rq(6, 1))
        );
        let su2_4 = FusionRing::su2_level(4).unwrap();
        let d1 = su2_4.frobenius_perron_dimension(1).unwrap();
        assert_eq!(d1.as_quadratic().unwrap().radicand(), &BigInt::from(3));
        assert_eq!(
            su2_4.frobenius_perron_dimension(2).unwrap(),
            RealAlgebraic::Rational(rq(2, 1))
        );
        assert_eq!(
            su2_4.global_dimension_squared().unwrap(),
            RealAlgebraic::Rational(rq(12, 1))
        );
        let su2_5 = FusionRing::su2_level(5).unwrap();
        let d1 = su2_5.frobenius_perron_dimension(1).unwrap();
        assert!(
            !d1.is_closed_form(),
            "2cos(pi/7) is not a quadratic surd: {d1}"
        );
        let enclosure = d1.enclosure(&rq(1, 1_000_000)).unwrap();
        assert!(enclosure.lo() > &rq(18_019, 10_000) && enclosure.hi() < &rq(18_020, 10_000));
    }

    #[test]
    fn the_characteristic_polynomials_match_the_minimal_equations() {
        let fib = FusionRing::fibonacci().unwrap();
        assert_eq!(
            fib.characteristic_polynomial(1).unwrap(),
            vec![BigInt::from(-1), BigInt::from(-1), BigInt::from(1)]
        );
        let ising = FusionRing::ising().unwrap();
        assert_eq!(
            ising.characteristic_polynomial(1).unwrap(),
            vec![
                BigInt::from(0),
                BigInt::from(-2),
                BigInt::from(0),
                BigInt::from(1)
            ]
        );
    }
}
