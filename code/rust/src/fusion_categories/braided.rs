use std::cmp::Ordering;
use std::collections::BTreeMap;

use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_traits::Signed;
use thiserror::Error;

use crate::braid_group::{BraidRelationDefect, DEFAULT_BRAID_LIMITS};
use crate::error::FusionError;
use crate::fusion_category::{CategoryDefect, FSymbols, FusionCategory, Gauge};
use crate::fusion_ring::FusionRing;
use crate::scalar::{sign_of, FusionScalar};
use linear_algebra::backend::basic_matrix::OperationLimits;
use linear_algebra::exact_field::matrix;
use omega_number_theory::algebraic_real::RealAlgebraic;

pub const MAX_FUSION_SPACE: usize = 1 << 16;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FusionSpaceLimits {
    pub max_strands: usize,
    pub max_paths: usize,
    pub max_path_labels: usize,
    pub max_extension_work: usize,
}

impl Default for FusionSpaceLimits {
    fn default() -> Self {
        Self {
            max_strands: 1024,
            max_paths: MAX_FUSION_SPACE,
            max_path_labels: 1 << 20,
            max_extension_work: 1 << 26,
        }
    }
}

fn charge_braid(what: &'static str, requested: u128, limit: usize) -> Result<(), FusionError> {
    if requested > limit as u128 {
        return Err(FusionError::Budget {
            what,
            requested,
            limit: limit as u128,
        });
    }
    Ok(())
}

fn braid_product_work(
    dimension: usize,
    products: usize,
    limits: OperationLimits,
) -> Result<(), FusionError> {
    let work = (dimension as u128)
        .checked_pow(3)
        .and_then(|work| work.checked_mul(2 * products as u128))
        .ok_or(FusionError::Overflow {
            context: "braid product work",
        })?;
    charge_braid("braid product scalar work", work, limits.max_scalar_ops)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Error)]
pub enum BraidedDefect {
    #[error("labels {left} and {right} do not fuse commutatively")]
    NotCommutative { left: usize, right: usize },
    #[error("missing R-symbol at {labels:?}")]
    RMissing { labels: [usize; 3] },
    #[error("unexpected R-symbol at {labels:?}")]
    RUnexpected { labels: [usize; 3] },
    #[error("R-symbol at {labels:?} is zero")]
    RZero { labels: [usize; 3] },
    #[error("hexagon equation (mirror form: {mirror}) violated at {labels:?}")]
    Hexagon { mirror: bool, labels: [usize; 6] },
    #[error("balancing relation fails at {labels:?}")]
    Ribbon { labels: [usize; 3] },
    #[error("the twist of label {label} differs from the twist of its dual")]
    TwistNotDualInvariant { label: usize },
    #[error("the twist of the unit is not 1")]
    TwistOfUnit,
    #[error("the twist of label {label} is zero")]
    TwistZero { label: usize },
}

#[derive(Debug, Clone, PartialEq)]
pub struct RSymbols<K> {
    rank: usize,
    r: BTreeMap<[usize; 3], K>,
}

impl<K: FusionScalar> RSymbols<K> {
    pub fn from_fn(
        ring: &FusionRing,
        mut value: impl FnMut([usize; 3]) -> K,
    ) -> Result<Self, FusionError> {
        let n = ring.rank();
        let mut r = BTreeMap::new();
        for a in 0..n {
            for b in 0..n {
                for c in 0..n {
                    if ring.n(a, b, c) > 0 {
                        let entry = value([a, b, c]);
                        if entry.is_zero() {
                            return Err(FusionError::Braided(BraidedDefect::RZero {
                                labels: [a, b, c],
                            }));
                        }
                        r.insert([a, b, c], entry);
                    }
                }
            }
        }
        Ok(Self { rank: n, r })
    }

    pub fn get(&self, labels: [usize; 3]) -> Option<&K> {
        self.r.get(&labels)
    }

    pub fn entries(&self) -> impl Iterator<Item = (&[usize; 3], &K)> {
        self.r.iter()
    }

    pub fn with_entry(&self, labels: [usize; 3], value: K) -> Result<Self, FusionError> {
        if value.is_zero() {
            return Err(FusionError::Braided(BraidedDefect::RZero { labels }));
        }
        if !self.r.contains_key(&labels) {
            return Err(FusionError::Braided(BraidedDefect::RMissing { labels }));
        }
        let mut r = self.r.clone();
        r.insert(labels, value);
        Ok(Self { rank: self.rank, r })
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HexagonForm {
    Direct,
    Mirror,
}

#[derive(Debug, Clone, PartialEq)]
pub struct HexagonDefect<K> {
    pub form: HexagonForm,
    pub labels: [usize; 6],
    pub lhs: K,
    pub rhs: K,
}

impl<K> HexagonDefect<K> {
    pub fn reads_r(&self, [x, y, z]: [usize; 3]) -> bool {
        let [a, b, c, d, e, g] = self.labels;
        match self.form {
            HexagonForm::Direct => {
                [x, y, z] == [e, c, d] || [x, y] == [b, c] || [x, y, z] == [a, c, g]
            }
            HexagonForm::Mirror => {
                [x, y, z] == [c, e, d] || [x, y] == [c, b] || [x, y, z] == [c, a, g]
            }
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FusionSpace {
    word: Vec<usize>,
    total: usize,
    basis: Vec<Vec<usize>>,
    extension_work: usize,
}

impl FusionSpace {
    pub fn word(&self) -> &[usize] {
        &self.word
    }

    pub fn total(&self) -> usize {
        self.total
    }

    pub fn dimension(&self) -> usize {
        self.basis.len()
    }

    pub fn basis(&self) -> &[Vec<usize>] {
        &self.basis
    }

    pub fn index_of(&self, path: &[usize]) -> Option<usize> {
        self.basis.binary_search_by(|p| p.as_slice().cmp(path)).ok()
    }

    fn charge(&self, path: &[usize], j: usize) -> Option<usize> {
        let n = self.word.len();
        if j == 0 || j > n {
            None
        } else if j == 1 {
            self.word.first().copied()
        } else if j == n {
            Some(self.total)
        } else {
            path.get(j - 2).copied()
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct BraidedFusionCategory<K> {
    category: FusionCategory<K>,
    r: RSymbols<K>,
}

impl<K: FusionScalar> BraidedFusionCategory<K> {
    pub fn new(category: FusionCategory<K>, r: RSymbols<K>) -> Result<Self, FusionError> {
        let ring = category.ring();
        let n = ring.rank();
        for left in 0..n {
            for right in left + 1..n {
                if (0..n).any(|c| ring.n(left, right, c) != ring.n(right, left, c)) {
                    return Err(FusionError::Braided(BraidedDefect::NotCommutative {
                        left,
                        right,
                    }));
                }
            }
        }
        if let Some(labels) = category.singular_blocks().first() {
            return Err(FusionError::Category(CategoryDefect::BlockSingular {
                labels: *labels,
            }));
        }
        if r.rank != n {
            return Err(FusionError::ListLength {
                what: "R-symbol labels",
                expected: n,
                got: r.rank,
            });
        }
        for a in 0..n {
            for b in 0..n {
                for c in 0..n {
                    let labels = [a, b, c];
                    match (r.get(labels), ring.n(a, b, c) > 0) {
                        (None, true) => {
                            return Err(FusionError::Braided(BraidedDefect::RMissing { labels }));
                        }
                        (Some(_), false) => {
                            return Err(FusionError::Braided(BraidedDefect::RUnexpected {
                                labels,
                            }));
                        }
                        (Some(entry), true) if entry.is_zero() => {
                            return Err(FusionError::Braided(BraidedDefect::RZero { labels }));
                        }
                        _ => {}
                    }
                }
            }
        }
        Ok(Self { category, r })
    }

    pub fn validated(category: FusionCategory<K>, r: RSymbols<K>) -> Result<Self, FusionError> {
        let braided = Self::new(category, r)?;
        braided.validate()?;
        Ok(braided)
    }

    pub fn category(&self) -> &FusionCategory<K> {
        &self.category
    }

    pub fn ring(&self) -> &FusionRing {
        self.category.ring()
    }

    pub fn r_symbols(&self) -> &RSymbols<K> {
        &self.r
    }

    pub fn r_entry(&self, labels: [usize; 3]) -> K {
        self.r.get(labels).cloned().unwrap_or_else(K::zero)
    }

    fn r_in_form(&self, form: HexagonForm, [x, y, z]: [usize; 3]) -> Option<K> {
        match form {
            HexagonForm::Direct => self.r.get([x, y, z]).cloned(),
            HexagonForm::Mirror => self.r.get([y, x, z])?.try_inv(),
        }
    }

    pub fn hexagon_defects(&self, form: HexagonForm) -> Vec<HexagonDefect<K>> {
        self.hexagon_scan(form, false)
    }

    pub fn first_hexagon_defect(&self, form: HexagonForm) -> Option<HexagonDefect<K>> {
        self.hexagon_scan(form, true).into_iter().next()
    }

    fn hexagon_scan(&self, form: HexagonForm, stop_at_first: bool) -> Vec<HexagonDefect<K>> {
        let ring = self.ring();
        let n = ring.rank();
        let mut defects = Vec::new();
        for a in 0..n {
            for b in 0..n {
                for c in 0..n {
                    for d in 0..n {
                        let Some(block) = self.category.f_symbols().block([a, b, c, d]) else {
                            continue;
                        };
                        let targets: Vec<usize> = (0..n)
                            .filter(|&g| ring.n(a, c, g) > 0 && ring.n(g, b, d) > 0)
                            .collect();
                        for &e in block.rows() {
                            for &g in &targets {
                                let lhs = self.hexagon_lhs(form, [a, b, c, d], e, g);
                                let rhs = self.hexagon_rhs(form, [a, b, c, d], e, g, block.cols());
                                if lhs != rhs {
                                    defects.push(HexagonDefect {
                                        form,
                                        labels: [a, b, c, d, e, g],
                                        lhs,
                                        rhs,
                                    });
                                    if stop_at_first {
                                        return defects;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        defects
    }

    fn hexagon_lhs(&self, form: HexagonForm, [a, b, c, d]: [usize; 4], e: usize, g: usize) -> K {
        match self.r_in_form(form, [e, c, d]) {
            Some(r) => r.mul(&self.category.f_inverse_entry([c, a, b, d], e, g)),
            None => K::zero(),
        }
    }

    fn hexagon_rhs(
        &self,
        form: HexagonForm,
        [a, b, c, d]: [usize; 4],
        e: usize,
        g: usize,
        middle: &[usize],
    ) -> K {
        let Some(r_ac_g) = self.r_in_form(form, [a, c, g]) else {
            return K::zero();
        };
        let mut total = K::zero();
        for &f in middle {
            let Some(r_bc_f) = self.r_in_form(form, [b, c, f]) else {
                continue;
            };
            let term = self
                .category
                .f_entry([a, b, c, d], e, f)
                .mul(&r_bc_f)
                .mul(&self.category.f_inverse_entry([a, c, b, d], f, g))
                .mul(&r_ac_g);
            total = total.add(&term);
        }
        total
    }

    pub fn validate(&self) -> Result<(), FusionError> {
        self.category.validate()?;
        for (form, mirror) in [(HexagonForm::Direct, false), (HexagonForm::Mirror, true)] {
            if let Some(defect) = self.first_hexagon_defect(form) {
                return Err(FusionError::Braided(BraidedDefect::Hexagon {
                    mirror,
                    labels: defect.labels,
                }));
            }
        }
        Ok(())
    }

    pub fn monodromy(&self, [a, b, c]: [usize; 3]) -> Option<K> {
        Some(self.r.get([a, b, c])?.mul(self.r.get([b, a, c])?))
    }

    pub fn is_symmetric(&self) -> bool {
        self.r
            .entries()
            .all(|(&[a, b, c], _)| self.monodromy([a, b, c]).is_some_and(|m| m == K::one()))
    }

    pub fn gauge_transform(&self, gauge: &Gauge<K>) -> Result<Self, FusionError> {
        let category = self.category.gauge_transform(gauge)?;
        let mut entries = BTreeMap::new();
        for (&[a, b, c], value) in self.r.entries() {
            let forward = gauge.get([a, b, c]).ok_or(FusionError::Category(
                CategoryDefect::GaugeMissing { labels: [a, b, c] },
            ))?;
            let backward = gauge.get([b, a, c]).ok_or(FusionError::Category(
                CategoryDefect::GaugeMissing { labels: [b, a, c] },
            ))?;
            entries.insert(
                [a, b, c],
                omega_number_theory::scalar::divide(forward, backward)
                    .map_err(FusionError::from)?
                    .mul(value),
            );
        }
        Self::new(
            category,
            RSymbols {
                rank: self.r.rank,
                r: entries,
            },
        )
    }

    pub fn complex_conjugate(&self) -> Result<Self, FusionError> {
        let ring = self.ring().clone();
        let f = FSymbols::from_fn(&ring, |labels, e, f| {
            self.category.f_symbols().entry(labels, e, f).map_or_else(
                K::zero,
                linear_algebra::exact_field::involution::Involution::conjugate,
            )
        })?;
        let category = FusionCategory::new(ring.clone(), f)?;
        let r = RSymbols::from_fn(&ring, |labels| self.r_entry(labels).conjugate())?;
        Self::new(category, r)
    }

    pub fn reverse_braiding(&self) -> Result<Self, FusionError> {
        let ring = self.ring().clone();
        let mut entries = BTreeMap::new();
        for (&[a, b, c], _) in self.r.entries() {
            let opposite =
                self.r
                    .get([b, a, c])
                    .ok_or(FusionError::Braided(BraidedDefect::RMissing {
                        labels: [b, a, c],
                    }))?;
            entries.insert(
                [a, b, c],
                omega_number_theory::scalar::inverse(opposite).map_err(FusionError::from)?,
            );
        }
        Self::new(
            FusionCategory::new(ring, self.category.f_symbols().clone())?,
            RSymbols {
                rank: self.r.rank,
                r: entries,
            },
        )
    }

    pub fn fusion_space(&self, word: &[usize], total: usize) -> Result<FusionSpace, FusionError> {
        self.fusion_space_with_limits(word, total, FusionSpaceLimits::default())
    }

    pub fn fusion_space_with_limits(
        &self,
        word: &[usize],
        total: usize,
        limits: FusionSpaceLimits,
    ) -> Result<FusionSpace, FusionError> {
        charge_braid(
            "materialized fusion strands",
            word.len() as u128,
            limits.max_strands,
        )?;
        let ring = self.ring();
        let rank = ring.rank();
        for &label in word.iter().chain(std::iter::once(&total)) {
            if label >= rank {
                return Err(FusionError::Label { label, rank });
            }
        }
        let n = word.len();
        let mut basis: Vec<Vec<usize>> = Vec::new();
        let mut work = n as u128;
        charge_braid(
            "fusion path extension work",
            work,
            limits.max_extension_work,
        )?;
        match n {
            0 => {
                if total == ring.unit() {
                    basis.push(Vec::new());
                }
            }
            1 => {
                if word.first() == Some(&total) {
                    basis.push(Vec::new());
                }
            }
            _ => {
                let first = word.first().copied().unwrap_or(0);
                let mut partial: Vec<(Vec<usize>, usize)> = vec![(Vec::new(), first)];
                for step in 2..n {
                    let label = word.get(step - 1).copied().unwrap_or(0);
                    let mut next = Vec::new();
                    for (path, x) in &partial {
                        work = work
                            .checked_add(rank as u128)
                            .ok_or(FusionError::Overflow {
                                context: "fusion path extension work",
                            })?;
                        charge_braid(
                            "fusion path extension work",
                            work,
                            limits.max_extension_work,
                        )?;
                        for c in 0..rank {
                            if ring.n(*x, label, c) > 0 {
                                let count = next.len() as u128 + 1;
                                charge_braid("fusion space dimension", count, limits.max_paths)?;
                                charge_braid(
                                    "fusion path labels",
                                    count * (path.len() as u128 + 1),
                                    limits.max_path_labels,
                                )?;
                                work = work.checked_add(path.len() as u128 + 1).ok_or(
                                    FusionError::Overflow {
                                        context: "fusion path extension work",
                                    },
                                )?;
                                charge_braid(
                                    "fusion path extension work",
                                    work,
                                    limits.max_extension_work,
                                )?;
                                let mut extended = path.clone();
                                extended.push(c);
                                next.push((extended, c));
                            }
                        }
                    }
                    partial = next;
                }
                let last = word.get(n - 1).copied().unwrap_or(0);
                for (path, x) in partial {
                    if ring.n(x, last, total) > 0 {
                        basis.push(path);
                    }
                }
            }
        }
        charge_braid(
            "fusion space dimension",
            basis.len() as u128,
            limits.max_paths,
        )?;
        charge_braid(
            "fusion path labels",
            basis.len() as u128 * n.saturating_sub(2) as u128 + n as u128,
            limits.max_path_labels,
        )?;
        basis.sort();
        Ok(FusionSpace {
            word: word.to_vec(),
            total,
            basis,
            extension_work: usize::try_from(work).map_err(|_| FusionError::Overflow {
                context: "fusion path work",
            })?,
        })
    }

    pub fn braid_matrix(
        &self,
        space: &FusionSpace,
        i: usize,
    ) -> Result<(FusionSpace, BasicMatrix<K>), FusionError> {
        self.braid_matrix_with_limits(space, i, DEFAULT_BRAID_LIMITS)
    }

    pub fn braid_matrix_with_limits(
        &self,
        space: &FusionSpace,
        i: usize,
        limits: OperationLimits,
    ) -> Result<(FusionSpace, BasicMatrix<K>), FusionError> {
        let mut path_work = FusionSpaceLimits::default().max_extension_work;
        self.braid_matrix_using_path_budget(space, i, limits, &mut path_work)
    }

    fn braid_matrix_using_path_budget(
        &self,
        space: &FusionSpace,
        i: usize,
        limits: OperationLimits,
        path_work: &mut usize,
    ) -> Result<(FusionSpace, BasicMatrix<K>), FusionError> {
        let n = space.word.len();
        if i == 0 || i >= n {
            return Err(FusionError::Label {
                label: i,
                rank: n.saturating_sub(1),
            });
        }
        let source = self.fusion_space_with_limits(
            space.word(),
            space.total(),
            FusionSpaceLimits {
                max_extension_work: *path_work,
                ..FusionSpaceLimits::default()
            },
        )?;
        *path_work -= source.extension_work;
        if source != *space {
            return Err(FusionError::Inconsistent {
                context: "fusion space does not belong to this fusion ring",
            });
        }
        let mut swapped = space.word.clone();
        swapped.swap(i - 1, i);
        let target = self.fusion_space_with_limits(
            &swapped,
            space.total,
            FusionSpaceLimits {
                max_extension_work: *path_work,
                ..FusionSpaceLimits::default()
            },
        )?;
        *path_work -= target.extension_work;
        let a = space.word.get(i - 1).copied().unwrap_or(0);
        let b = space.word.get(i).copied().unwrap_or(0);
        let missing =
            |labels: [usize; 4]| FusionError::Category(CategoryDefect::BlockMissing { labels });
        charge_braid(
            "braid matrix entries",
            target.dimension() as u128 * space.dimension() as u128,
            limits.max_elements,
        )?;
        charge_braid(
            "braid coefficient scalar work",
            3 * space.dimension() as u128 * (self.ring().rank() as u128).pow(2),
            limits.max_scalar_ops,
        )?;
        let mut matrix =
            matrix::zeros_with_limits::<K>(target.dimension(), space.dimension(), limits)?;
        for (column, path) in space.basis.iter().enumerate() {
            if i == 1 {
                let x2 = space
                    .charge(path, 2)
                    .ok_or(FusionError::Label { label: 2, rank: n })?;
                let row = target.index_of(path).ok_or(FusionError::Inconsistent {
                    context: "a fusion path of the word is missing from the exchanged word",
                })?;
                let entry = self.r.get([a, b, x2]).ok_or(FusionError::Braided(
                    BraidedDefect::RMissing { labels: [a, b, x2] },
                ))?;
                matrix.set(row, column, entry.clone())?;
                continue;
            }
            let p = space.charge(path, i - 1).ok_or(FusionError::Label {
                label: i - 1,
                rank: n,
            })?;
            let e = space
                .charge(path, i)
                .ok_or(FusionError::Label { label: i, rank: n })?;
            let r = space.charge(path, i + 1).ok_or(FusionError::Label {
                label: i + 1,
                rank: n,
            })?;
            let source_block = self
                .category
                .f_symbols()
                .block([p, a, b, r])
                .ok_or_else(|| missing([p, a, b, r]))?;
            let target_inverse = self
                .category
                .f_inverse_block([p, b, a, r])
                .ok_or_else(|| missing([p, b, a, r]))?;
            for &e_prime in target_inverse.cols() {
                let mut entry = K::zero();
                for &f in source_block.cols() {
                    let Some(f_e_f) = source_block.entry(e, f) else {
                        continue;
                    };
                    let Some(r_f) = self.r.get([a, b, f]) else {
                        continue;
                    };
                    let Some(inv) = target_inverse.entry(f, e_prime) else {
                        continue;
                    };
                    entry = entry.add(&f_e_f.mul(r_f).mul(inv));
                }
                let mut new_path = path.clone();
                if let Some(slot) = new_path.get_mut(i - 2) {
                    *slot = e_prime;
                }
                let row = target
                    .index_of(&new_path)
                    .ok_or(FusionError::Inconsistent {
                        context: "an exchanged fusion path is missing from the exchanged word",
                    })?;
                matrix.set(row, column, entry)?;
            }
        }
        Ok((target, matrix))
    }

    pub fn braid_relation_defects_on_word(
        &self,
        word: &[usize],
        total: usize,
    ) -> Result<Vec<BraidRelationDefect>, FusionError> {
        let space = self.fusion_space(word, total)?;
        let n = word.len();
        let mut path_work = FusionSpaceLimits::default().max_extension_work - space.extension_work;
        let pairs = n
            .saturating_sub(1)
            .checked_pow(2)
            .ok_or(FusionError::Overflow {
                context: "braid relation count",
            })?;
        let products = pairs
            .checked_mul(2)
            .and_then(|count| count.checked_add(4 * n.saturating_sub(2)))
            .ok_or(FusionError::Overflow {
                context: "braid relation count",
            })?;
        braid_product_work(space.dimension(), products, DEFAULT_BRAID_LIMITS)?;
        let d = space.dimension() as u128;
        let coefficient_work =
            (6 * n as u128 + 2 * pairs as u128) * 3 * d * (self.ring().rank() as u128).pow(2);
        charge_braid(
            "braid relation aggregate scalar work",
            2 * products as u128 * d.pow(3) + coefficient_work,
            DEFAULT_BRAID_LIMITS.max_scalar_ops,
        )?;
        let mut defects = Vec::new();
        for i in 1..n.saturating_sub(1) {
            let (a1, m1) = self.braid_matrix_using_path_budget(
                &space,
                i,
                DEFAULT_BRAID_LIMITS,
                &mut path_work,
            )?;
            let (a2, m2) = self.braid_matrix_using_path_budget(
                &a1,
                i + 1,
                DEFAULT_BRAID_LIMITS,
                &mut path_work,
            )?;
            let (a3, m3) =
                self.braid_matrix_using_path_budget(&a2, i, DEFAULT_BRAID_LIMITS, &mut path_work)?;
            let (b1, n1) = self.braid_matrix_using_path_budget(
                &space,
                i + 1,
                DEFAULT_BRAID_LIMITS,
                &mut path_work,
            )?;
            let (b2, n2) =
                self.braid_matrix_using_path_budget(&b1, i, DEFAULT_BRAID_LIMITS, &mut path_work)?;
            let (b3, n3) = self.braid_matrix_using_path_budget(
                &b2,
                i + 1,
                DEFAULT_BRAID_LIMITS,
                &mut path_work,
            )?;
            if a3.word() != b3.word() {
                return Err(FusionError::Inconsistent {
                    context: "the two sides of a braid relation end in different words",
                });
            }
            let left = matrix::multiply_with_limits(
                &m3,
                &matrix::multiply_with_limits(&m2, &m1, DEFAULT_BRAID_LIMITS)?,
                DEFAULT_BRAID_LIMITS,
            )
            .map_err(FusionError::from)?;
            let right = matrix::multiply_with_limits(
                &n3,
                &matrix::multiply_with_limits(&n2, &n1, DEFAULT_BRAID_LIMITS)?,
                DEFAULT_BRAID_LIMITS,
            )
            .map_err(FusionError::from)?;
            if left != right {
                defects.push(BraidRelationDefect::Braid { i: i - 1 });
            }
        }
        for i in 1..n {
            for j in (i + 2)..n {
                let (x1, p1) = self.braid_matrix_using_path_budget(
                    &space,
                    i,
                    DEFAULT_BRAID_LIMITS,
                    &mut path_work,
                )?;
                let (x2, p2) = self.braid_matrix_using_path_budget(
                    &x1,
                    j,
                    DEFAULT_BRAID_LIMITS,
                    &mut path_work,
                )?;
                let (y1, q1) = self.braid_matrix_using_path_budget(
                    &space,
                    j,
                    DEFAULT_BRAID_LIMITS,
                    &mut path_work,
                )?;
                let (y2, q2) = self.braid_matrix_using_path_budget(
                    &y1,
                    i,
                    DEFAULT_BRAID_LIMITS,
                    &mut path_work,
                )?;
                if x2.word() != y2.word() {
                    return Err(FusionError::Inconsistent {
                        context: "the two sides of a commutation relation end in different words",
                    });
                }
                if matrix::multiply_with_limits(&p2, &p1, DEFAULT_BRAID_LIMITS)?
                    != matrix::multiply_with_limits(&q2, &q1, DEFAULT_BRAID_LIMITS)?
                {
                    defects.push(BraidRelationDefect::Far { i: i - 1, j: j - 1 });
                }
            }
        }
        Ok(defects)
    }

    pub fn braid_generators(
        &self,
        a: usize,
        n: usize,
        total: usize,
    ) -> Result<Vec<BasicMatrix<K>>, FusionError> {
        self.braid_generators_with_limits(a, n, total, DEFAULT_BRAID_LIMITS)
    }

    pub fn braid_generators_with_limits(
        &self,
        a: usize,
        n: usize,
        total: usize,
        limits: OperationLimits,
    ) -> Result<Vec<BasicMatrix<K>>, FusionError> {
        charge_braid(
            "materialized fusion strands",
            n as u128,
            FusionSpaceLimits::default().max_strands,
        )?;
        let word = vec![a; n];
        let space = self.fusion_space(&word, total)?;
        let mut path_work = FusionSpaceLimits::default().max_extension_work - space.extension_work;
        let generators = n.saturating_sub(1) as u128;
        let dimension = space.dimension() as u128;
        charge_braid(
            "braid generator entries",
            generators * dimension * dimension,
            limits.max_elements,
        )?;
        let assembly = generators
            * dimension
            * (3 * (self.ring().rank() as u128).pow(2) + 3 * (n as u128).pow(2));
        charge_braid(
            "braid generator assembly work",
            assembly,
            limits.max_scalar_ops,
        )?;
        (1..n)
            .map(|i| {
                self.braid_matrix_using_path_budget(&space, i, limits, &mut path_work)
                    .map(|(_, matrix)| matrix)
            })
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct RibbonFusionCategory<K> {
    braided: BraidedFusionCategory<K>,
    dimensions: Vec<K>,
    twists: Vec<K>,
}

impl<K: FusionScalar> RibbonFusionCategory<K> {
    pub fn compute_twists(
        braided: &BraidedFusionCategory<K>,
        dimensions: &[K],
    ) -> Result<Vec<K>, FusionError> {
        let ring = braided.ring();
        let n = ring.rank();
        if dimensions.len() != n {
            return Err(FusionError::ListLength {
                what: "dimensions",
                expected: n,
                got: dimensions.len(),
            });
        }
        let mut twists = Vec::with_capacity(n);
        for a in 0..n {
            let mut total = K::zero();
            for (c, d_c) in dimensions.iter().enumerate() {
                if ring.n(a, a, c) > 0 {
                    total = total.add(&d_c.mul(&braided.r_entry([a, a, c])));
                }
            }
            let d_a = dimensions
                .get(a)
                .ok_or(FusionError::Label { label: a, rank: n })?;
            twists
                .push(omega_number_theory::scalar::divide(&total, d_a).map_err(FusionError::from)?);
        }
        Ok(twists)
    }

    pub fn try_new(
        braided: BraidedFusionCategory<K>,
        dimensions: Vec<K>,
    ) -> Result<Self, FusionError> {
        braided.validate()?;
        braided.category.verify_dimensions(&dimensions)?;
        let twists = Self::compute_twists(&braided, &dimensions)?;
        let ring = braided.ring();
        let n = ring.rank();
        if twists.first() != Some(&K::one()) {
            return Err(FusionError::Braided(BraidedDefect::TwistOfUnit));
        }
        for a in 0..n {
            let twist = twists
                .get(a)
                .ok_or(FusionError::Label { label: a, rank: n })?;
            if twist.is_zero() {
                return Err(FusionError::Braided(BraidedDefect::TwistZero { label: a }));
            }
            let dual = ring.dual(a)?;
            if twists.get(dual) != Some(twist) {
                return Err(FusionError::Braided(BraidedDefect::TwistNotDualInvariant {
                    label: a,
                }));
            }
        }
        for (&[a, b, c], _) in braided.r.entries() {
            let (Some(ta), Some(tb), Some(tc)) = (twists.get(a), twists.get(b), twists.get(c))
            else {
                continue;
            };
            let expected =
                omega_number_theory::scalar::divide(tc, &ta.mul(tb)).map_err(FusionError::from)?;
            if braided.monodromy([a, b, c]) != Some(expected) {
                return Err(FusionError::Braided(BraidedDefect::Ribbon {
                    labels: [a, b, c],
                }));
            }
        }
        Ok(Self {
            braided,
            dimensions,
            twists,
        })
    }

    pub fn braided(&self) -> &BraidedFusionCategory<K> {
        &self.braided
    }

    pub fn category(&self) -> &FusionCategory<K> {
        self.braided.category()
    }

    pub fn ring(&self) -> &FusionRing {
        self.braided.ring()
    }

    pub fn dimensions(&self) -> &[K] {
        &self.dimensions
    }

    pub fn twists(&self) -> &[K] {
        &self.twists
    }

    pub fn dimension(&self, a: usize) -> Result<&K, FusionError> {
        self.dimensions.get(a).ok_or(FusionError::Label {
            label: a,
            rank: self.dimensions.len(),
        })
    }

    pub fn twist(&self, a: usize) -> Result<&K, FusionError> {
        self.twists.get(a).ok_or(FusionError::Label {
            label: a,
            rank: self.twists.len(),
        })
    }

    pub fn global_dimension_squared(&self) -> K {
        self.dimensions
            .iter()
            .fold(K::zero(), |acc, d| acc.add(&d.mul(d)))
    }

    pub fn gauss_sum(&self) -> K {
        self.dimensions
            .iter()
            .zip(&self.twists)
            .fold(K::zero(), |acc, (d, theta)| acc.add(&d.mul(d).mul(theta)))
    }

    pub fn dimensions_are_frobenius_perron(&self) -> Result<bool, FusionError> {
        let ring = self.ring();
        for a in 0..ring.rank() {
            let d = self.dimension(a)?;
            let agrees = match ring.frobenius_perron_dimension(a)? {
                RealAlgebraic::Rational(q) => *d == K::from_rational(&q),
                RealAlgebraic::Quadratic(surd) => {
                    let annihilates = omega_number_theory::scalar::evaluate_integer_polynomial(
                        &surd.minimal_polynomial(),
                        d,
                    )
                    .map_err(FusionError::from)?
                    .is_zero();
                    let offset = d.sub(&K::from_rational(surd.rational_part()));
                    let wanted = if surd.sqrt_part().is_positive() {
                        Ordering::Greater
                    } else {
                        Ordering::Less
                    };
                    annihilates && sign_of(&offset)? == wanted
                }
                RealAlgebraic::Root(root) => {
                    let interval = root.isolating_interval()?;
                    let annihilates = omega_number_theory::scalar::evaluate_integer_polynomial(
                        root.polynomial(),
                        d,
                    )
                    .map_err(FusionError::from)?
                    .is_zero();
                    let above_lower =
                        sign_of(&d.sub(&K::from_rational(interval.lo())))? == Ordering::Greater;
                    let at_most_upper =
                        sign_of(&K::from_rational(interval.hi()).sub(d))? != Ordering::Less;
                    annihilates && above_lower && at_most_upper
                }
            };
            if !agrees {
                return Ok(false);
            }
        }
        Ok(true)
    }

    pub fn complex_conjugate(&self) -> Result<Self, FusionError> {
        let dimensions = self
            .dimensions
            .iter()
            .map(linear_algebra::exact_field::involution::Involution::conjugate)
            .collect();
        Self::try_new(self.braided.complex_conjugate()?, dimensions)
    }

    pub fn braid_generators(
        &self,
        a: usize,
        n: usize,
        total: usize,
    ) -> Result<Vec<BasicMatrix<K>>, FusionError> {
        self.braided.braid_generators(a, n, total)
    }

    pub fn full_twist(
        &self,
        a: usize,
        n: usize,
        total: usize,
    ) -> Result<BasicMatrix<K>, FusionError> {
        charge_braid(
            "materialized fusion strands",
            n as u128,
            FusionSpaceLimits::default().max_strands,
        )?;
        let space = self.braided.fusion_space(&vec![a; n], total)?;
        let dimension = space.dimension();
        let power_products = 2 * (usize::BITS - n.leading_zeros()) as usize;
        braid_product_work(
            dimension,
            n.saturating_sub(1) + power_products,
            DEFAULT_BRAID_LIMITS,
        )?;
        let d = dimension as u128;
        charge_braid(
            "full twist aggregate scalar work",
            2 * (n.saturating_sub(1) + power_products) as u128 * d.pow(3)
                + 3 * n.saturating_sub(1) as u128 * d * (self.ring().rank() as u128).pow(2),
            DEFAULT_BRAID_LIMITS.max_scalar_ops,
        )?;
        let mut product = matrix::identity_with_limits::<K>(dimension, DEFAULT_BRAID_LIMITS)?;
        for generator in self.braided.braid_generators(a, n, total)? {
            product = matrix::multiply_with_limits(&product, &generator, DEFAULT_BRAID_LIMITS)?;
        }
        matrix::power_with_limits(
            &product,
            u64::try_from(n).map_err(|_| FusionError::Overflow {
                context: "the number of strands",
            })?,
            DEFAULT_BRAID_LIMITS,
        )
        .map_err(FusionError::from)
    }

    pub fn full_twist_scalar(&self, a: usize, n: usize, total: usize) -> Result<K, FusionError> {
        let theta_a = self.twist(a)?;
        let theta_total = self.twist(total)?;
        let power = omega_number_theory::scalar::power(
            theta_a,
            i64::try_from(n).map_err(|_| FusionError::Overflow {
                context: "the number of strands",
            })?,
        )
        .map_err(FusionError::from)?;
        omega_number_theory::scalar::divide(theta_total, &power).map_err(FusionError::from)
    }
}

#[cfg(test)]
mod resource_tests {
    use super::*;
    use omega_number_theory::cyclotomic_field::Cyclotomic;

    #[test]
    fn empty_sectors_charge_intermediate_paths_across_generator_materialization() {
        let model = crate::catalog::ising::<Cyclotomic<16>>().unwrap();
        let space = model.braided().fusion_space(&vec![1; 32], 1).unwrap();
        assert_eq!(space.dimension(), 0);
        assert!(matches!(
            model.braid_generators(1, 32, 1),
            Err(FusionError::Budget {
                what: "fusion path extension work",
                ..
            })
        ));
    }

    #[test]
    fn braid_materialization_refuses_oversized_dense_and_path_carriers() {
        let model = crate::catalog::ising::<Cyclotomic<16>>().unwrap();
        let braided = model.braided();
        let space = braided.fusion_space(&vec![1; 24], 0).unwrap();
        assert_eq!(space.dimension(), 2048);
        assert!(matches!(
            braided.braid_matrix(&space, 1),
            Err(FusionError::Budget {
                what: "braid matrix entries",
                ..
            })
        ));
        assert!(matches!(
            braided.braid_generators(1, 20, 0),
            Err(FusionError::Budget {
                what: "braid generator entries",
                ..
            })
        ));
        assert!(matches!(
            braided.fusion_space(&vec![1; 34], 0),
            Err(FusionError::Budget {
                what: "fusion path labels",
                ..
            })
        ));
        assert!(matches!(
            braided.braid_generators(1, usize::MAX, 0),
            Err(FusionError::Budget {
                what: "materialized fusion strands",
                ..
            })
        ));
        assert!(matches!(
            model.full_twist(1, usize::MAX, 0),
            Err(FusionError::Budget {
                what: "materialized fusion strands",
                ..
            })
        ));
        let tight = FusionSpaceLimits {
            max_extension_work: 1,
            ..FusionSpaceLimits::default()
        };
        assert!(matches!(
            braided.fusion_space_with_limits(&[1, 1, 1], 1, tight),
            Err(FusionError::Budget {
                what: "fusion path extension work",
                ..
            })
        ));
        assert_eq!(braided.fusion_space(&[], 0).unwrap().dimension(), 1);
        assert_eq!(braided.fusion_space(&[], 1).unwrap().dimension(), 0);
        let empty = braided.fusion_space(&[0, 0], 1).unwrap();
        assert_eq!(braided.braid_matrix(&empty, 1).unwrap().1.shape(), (0, 0));
    }
}
