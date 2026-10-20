use std::collections::BTreeMap;

use linear_algebra::backend::basic_matrix::{BasicMatrix, OperationLimits};
use thiserror::Error;

use crate::error::FusionError;
use crate::fusion_ring::FusionRing;
use crate::scalar::FusionScalar;
use linear_algebra::exact_field::{elimination, involution};

pub const DEFAULT_CATEGORY_LIMITS: OperationLimits = OperationLimits {
    max_elements: 1 << 20,
    max_scalar_ops: 1 << 28,
};

// All callers hold a sealed FusionRing: 1<=rank<=32 and multiplicities are0/1.
fn label_pairs(rank: usize) -> impl Iterator<Item = [usize; 2]> {
    (0..rank).flat_map(move |a| (0..rank).map(move |b| [a, b]))
}

fn label_triples(rank: usize) -> impl Iterator<Item = [usize; 3]> {
    label_pairs(rank).flat_map(move |[a, b]| (0..rank).map(move |c| [a, b, c]))
}

fn label_quadruples(rank: usize) -> impl Iterator<Item = [usize; 4]> {
    label_triples(rank).flat_map(move |[a, b, c]| (0..rank).map(move |d| [a, b, c, d]))
}

type FusionSupport = Vec<Vec<Vec<usize>>>;

fn fusion_support(ring: &FusionRing) -> FusionSupport {
    (0..ring.rank())
        .map(|a| {
            (0..ring.rank())
                .map(|b| (0..ring.rank()).filter(|&c| ring.n(a, b, c) > 0).collect())
                .collect()
        })
        .collect()
}

fn charge_category(what: &'static str, requested: u128, limit: usize) -> Result<(), FusionError> {
    if requested > limit as u128 {
        return Err(FusionError::Budget {
            what,
            requested,
            limit: limit as u128,
        });
    }
    Ok(())
}

fn triple_path_counts(fuse: &FusionSupport, [a, b, c]: [usize; 3], counts: &mut [usize]) {
    counts.fill(0);
    for &e in &fuse[a][b] {
        for &total in &fuse[e][c] {
            counts[total] += 1;
        }
    }
}

fn extend_path_counts(fuse: &FusionSupport, counts: &[usize], label: usize, output: &mut [usize]) {
    output.fill(0);
    for (g, &count) in counts.iter().enumerate().filter(|(_, count)| **count != 0) {
        for &total in &fuse[g][label] {
            output[total] += count;
        }
    }
}

fn block_resource_totals(dimensions: &[usize]) -> (u128, u128) {
    dimensions
        .iter()
        .filter(|&&d| d != 0)
        .fold((0, 0), |(entries, work), &dimension| {
            let d = dimension as u128;
            (
                entries + 2 * (d * d + 2 * d + 4),
                work + 4 * d.pow(3) + 2 * d * d + d,
            )
        })
}

fn admit_category_resources(ring: &FusionRing, limits: OperationLimits) -> Result<(), FusionError> {
    let rank = ring.rank();
    let n = rank as u128;
    let fuse = fusion_support(ring);
    let width = fuse.iter().flatten().map(Vec::len).max().unwrap_or(0) as u128;
    let metadata = 4 * n.pow(5);
    let traversal = n.pow(4) * (2 * width.pow(6) + 2 * width.pow(3));
    charge_category(
        "fusion category label traversal",
        metadata + traversal,
        limits.max_scalar_ops,
    )?;
    let (mut entries, mut inverse_work, mut equations) = (0u128, 0u128, 0u128);
    // Two rank-sized buffers are reused for every label tuple.
    let mut three = vec![0usize; rank];
    let mut four = vec![0usize; rank];
    for labels in label_triples(rank) {
        triple_path_counts(&fuse, labels, &mut three);
        let (storage, inverse) = block_resource_totals(&three);
        entries += storage;
        inverse_work += inverse;
        for d in 0..rank {
            extend_path_counts(&fuse, &three, d, &mut four);
            equations += four
                .iter()
                .map(|&count| (count as u128).pow(2))
                .sum::<u128>();
        }
    }
    charge_category(
        "fusion category symbol storage",
        entries,
        limits.max_elements,
    )?;
    charge_category("pentagon defect records", equations, limits.max_elements)?;
    let pentagon_work = equations * (1 + 3 * width);
    let hexagon_work = 2 * n.pow(4) * width.pow(2) * (1 + 4 * width);
    charge_category(
        "fusion category aggregate replay work",
        metadata + traversal + inverse_work + pentagon_work + hexagon_work,
        limits.max_scalar_ops,
    )
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum CategoryDefect {
    #[error("the ring has multiplicity {multiplicity} at {labels:?}; only multiplicity-free categories are supported")]
    NotMultiplicityFree {
        labels: [usize; 3],
        multiplicity: u64,
    },
    #[error("missing F-block for {labels:?}")]
    BlockMissing { labels: [usize; 4] },
    #[error("unexpected F-block for {labels:?}")]
    BlockUnexpected { labels: [usize; 4] },
    #[error("F-block {labels:?} is {rows}x{cols}, expected {expected}x{expected}")]
    BlockShape {
        labels: [usize; 4],
        rows: usize,
        cols: usize,
        expected: usize,
    },
    #[error("F-block {labels:?} has the wrong intermediate labels")]
    BlockLabels { labels: [usize; 4] },
    #[error("F-block {labels:?} is singular")]
    BlockSingular { labels: [usize; 4] },
    #[error("pentagon equation violated at {labels:?}")]
    Pentagon { labels: [usize; 9] },
    #[error("F-symbol with a unit leg is not 1 at {labels:?}")]
    UnitLaw { labels: [usize; 4] },
    #[error("the gauge has no entry for the vertex {labels:?}")]
    GaugeMissing { labels: [usize; 3] },
    #[error("the gauge entry at {labels:?} is zero")]
    GaugeZero { labels: [usize; 3] },
    #[error("no gauge normalises the unit F-symbols (obstruction at {labels:?})")]
    UnitNormalizationImpossible { labels: [usize; 3] },
    #[error("dimension data: {0}")]
    Dimensions(DimensionDefect),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Error)]
pub enum DimensionDefect {
    #[error("expected {expected} dimensions, got {got}")]
    Count { expected: usize, got: usize },
    #[error("the unit has dimension other than 1")]
    UnitNotOne,
    #[error("label {label} has dimension zero")]
    Zero { label: usize },
    #[error("label {label} and its dual have different dimensions")]
    NotSpherical { label: usize },
    #[error("dimensions are not a character of the fusion ring at ({a}, {b})")]
    NotCharacter { a: usize, b: usize },
    #[error("dimension of label {label} disagrees with the F-symbols")]
    DisagreesWithF { label: usize },
    #[error("Frobenius-Schur value of label {label} is not a sign")]
    FrobeniusSchurNotSign { label: usize },
}

fn dimension_error(defect: DimensionDefect) -> FusionError {
    FusionError::Category(CategoryDefect::Dimensions(defect))
}

#[derive(Debug, Clone, PartialEq)]
pub struct FBlock<K> {
    rows: Vec<usize>,
    cols: Vec<usize>,
    matrix: BasicMatrix<K>,
}

impl<K: FusionScalar> FBlock<K> {
    pub fn rows(&self) -> &[usize] {
        &self.rows
    }

    pub fn cols(&self) -> &[usize] {
        &self.cols
    }

    pub fn matrix(&self) -> &BasicMatrix<K> {
        &self.matrix
    }

    pub fn entry(&self, e: usize, f: usize) -> Option<&K> {
        let i = self.rows.binary_search(&e).ok()?;
        let j = self.cols.binary_search(&f).ok()?;
        self.matrix.get_ref(i, j).ok()
    }

    pub fn inverse(&self) -> Result<FBlock<K>, FusionError> {
        Ok(FBlock {
            rows: self.cols.clone(),
            cols: self.rows.clone(),
            matrix: elimination::inverse(&self.matrix).map_err(FusionError::from)?,
        })
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct FSymbols<K> {
    rank: usize,
    blocks: BTreeMap<[usize; 4], FBlock<K>>,
}

impl<K: FusionScalar> FSymbols<K> {
    pub fn from_fn(
        ring: &FusionRing,
        mut entry: impl FnMut([usize; 4], usize, usize) -> K,
    ) -> Result<Self, FusionError> {
        Self::try_from_fn(ring, |labels, e, f| Ok(entry(labels, e, f)))
    }

    pub fn from_fn_with_limits(
        ring: &FusionRing,
        limits: OperationLimits,
        mut entry: impl FnMut([usize; 4], usize, usize) -> K,
    ) -> Result<Self, FusionError> {
        Self::try_from_fn_with_limits(ring, limits, |labels, e, f| Ok(entry(labels, e, f)))
    }

    pub fn try_from_fn(
        ring: &FusionRing,
        entry: impl FnMut([usize; 4], usize, usize) -> Result<K, FusionError>,
    ) -> Result<Self, FusionError> {
        Self::try_from_fn_with_limits(ring, DEFAULT_CATEGORY_LIMITS, entry)
    }

    pub fn try_from_fn_with_limits(
        ring: &FusionRing,
        limits: OperationLimits,
        mut entry: impl FnMut([usize; 4], usize, usize) -> Result<K, FusionError>,
    ) -> Result<Self, FusionError> {
        require_multiplicity_free(ring)?;
        admit_category_resources(ring, limits)?;
        let mut blocks = BTreeMap::new();
        for labels in label_quadruples(ring.rank()) {
            if let Some(block) = build_f_block(ring, labels, limits.max_elements, &mut entry)? {
                blocks.insert(labels, block);
            }
        }
        Ok(Self {
            rank: ring.rank(),
            blocks,
        })
    }

    pub fn trivial(ring: &FusionRing) -> Result<Self, FusionError> {
        if !ring.is_pointed() {
            return Err(FusionError::NotInSubfield {
                what: "a fusion ring with non-invertible objects",
                expected: "pointed (every F-block 1x1)",
            });
        }
        Self::from_fn(ring, |_, _, _| K::one())
    }

    pub fn rank(&self) -> usize {
        self.rank
    }

    pub fn block(&self, labels: [usize; 4]) -> Option<&FBlock<K>> {
        self.blocks.get(&labels)
    }

    pub fn entry(&self, labels: [usize; 4], e: usize, f: usize) -> Option<&K> {
        self.block(labels)?.entry(e, f)
    }

    pub fn blocks(&self) -> impl Iterator<Item = (&[usize; 4], &FBlock<K>)> {
        self.blocks.iter()
    }

    pub fn with_entry(
        &self,
        labels: [usize; 4],
        e: usize,
        f: usize,
        value: K,
    ) -> Result<Self, FusionError> {
        let mut blocks = self.blocks.clone();
        let block =
            blocks
                .get_mut(&labels)
                .ok_or(FusionError::Category(CategoryDefect::BlockMissing {
                    labels,
                }))?;
        let i = block
            .rows
            .binary_search(&e)
            .map_err(|_| FusionError::Category(CategoryDefect::BlockLabels { labels }))?;
        let j = block
            .cols
            .binary_search(&f)
            .map_err(|_| FusionError::Category(CategoryDefect::BlockLabels { labels }))?;
        block.matrix.set(i, j, value)?;
        Ok(Self {
            rank: self.rank,
            blocks,
        })
    }
}

fn build_f_block<K: FusionScalar>(
    ring: &FusionRing,
    labels: [usize; 4],
    max_elements: usize,
    entry: &mut impl FnMut([usize; 4], usize, usize) -> Result<K, FusionError>,
) -> Result<Option<FBlock<K>>, FusionError> {
    let (rows, cols) = intermediate_labels(ring, labels);
    if rows.is_empty() && cols.is_empty() {
        return Ok(None);
    }
    if rows.len() != cols.len() {
        return Err(FusionError::Category(CategoryDefect::BlockShape {
            labels,
            rows: rows.len(),
            cols: cols.len(),
            expected: rows.len(),
        }));
    }
    // Matrix callbacks supply indices within the admitted row/column shape.
    let matrix = BasicMatrix::try_from_fn_result_with_limit(
        rows.len(),
        cols.len(),
        max_elements,
        |i, j| entry(labels, rows[i], cols[j]),
    )?;
    Ok(Some(FBlock { rows, cols, matrix }))
}

fn require_multiplicity_free(ring: &FusionRing) -> Result<(), FusionError> {
    for labels in label_triples(ring.rank()) {
        let [a, b, c] = labels;
        let multiplicity = ring.n(a, b, c);
        if multiplicity > 1 {
            return Err(FusionError::Category(CategoryDefect::NotMultiplicityFree {
                labels,
                multiplicity,
            }));
        }
    }
    Ok(())
}

fn intermediate_labels(ring: &FusionRing, [a, b, c, d]: [usize; 4]) -> (Vec<usize>, Vec<usize>) {
    let r = ring.rank();
    let rows = (0..r)
        .filter(|&e| ring.n(a, b, e) > 0 && ring.n(e, c, d) > 0)
        .collect();
    let cols = (0..r)
        .filter(|&f| ring.n(b, c, f) > 0 && ring.n(a, f, d) > 0)
        .collect();
    (rows, cols)
}

struct PentagonPaths {
    left: Vec<[usize; 3]>,
    right: Vec<Vec<[usize; 2]>>,
}

impl PentagonPaths {
    fn new(rank: usize) -> Self {
        Self {
            left: Vec::new(),
            right: vec![Vec::new(); rank],
        }
    }

    fn fill_left(&mut self, fuse: &FusionSupport, [a, b, c, d]: [usize; 4]) {
        self.left.clear();
        for &f in &fuse[a][b] {
            for &g in &fuse[f][c] {
                for &e in &fuse[g][d] {
                    self.left.push([e, f, g]);
                }
            }
        }
        self.left.sort_unstable();
    }

    fn fill_right(&mut self, fuse: &FusionSupport, [a, b, c, d]: [usize; 4]) {
        for group in &mut self.right {
            group.clear();
        }
        for &l in &fuse[c][d] {
            for &k in &fuse[b][l] {
                for &e in &fuse[a][k] {
                    self.right[e].push([k, l]);
                }
            }
        }
        for group in &mut self.right {
            group.sort_unstable();
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct PentagonDefect<K> {
    pub labels: [usize; 9],
    pub lhs: K,
    pub rhs: K,
}

impl<K> PentagonDefect<K> {
    pub fn involves(&self, [a2, b2, c2, d2]: [usize; 4], e2: usize, f2: usize) -> bool {
        let [a, b, c, d, e, f, g, k, l] = self.labels;
        let left = ([a2, b2, c2, d2] == [f, c, d, e] && (e2, f2) == (g, l))
            || ([a2, b2, c2, d2] == [a, b, l, e] && (e2, f2) == (f, k));
        let right = ([a2, b2, c2, d2] == [a, b, c, g] && e2 == f)
            || ([a2, c2, d2] == [a, d, e] && (e2, f2) == (g, k))
            || ([a2, b2, c2, d2] == [b, c, d, k] && f2 == l);
        left || right
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Gauge<K> {
    u: BTreeMap<[usize; 3], K>,
}

impl<K: FusionScalar> Gauge<K> {
    pub fn trivial(ring: &FusionRing) -> Self {
        Self::build(ring, |_| K::one())
    }

    fn build(ring: &FusionRing, mut value: impl FnMut([usize; 3]) -> K) -> Self {
        let mut u = BTreeMap::new();
        for labels in label_triples(ring.rank()) {
            if ring.n(labels[0], labels[1], labels[2]) > 0 {
                u.insert(labels, value(labels));
            }
        }
        Self { u }
    }

    pub fn from_fn(
        ring: &FusionRing,
        value: impl FnMut([usize; 3]) -> K,
    ) -> Result<Self, FusionError> {
        let gauge = Self::build(ring, value);
        if let Some((labels, _)) = gauge.u.iter().find(|(_, v)| v.is_zero()) {
            return Err(FusionError::Category(CategoryDefect::GaugeZero {
                labels: *labels,
            }));
        }
        Ok(gauge)
    }

    pub fn get(&self, labels: [usize; 3]) -> Option<&K> {
        self.u.get(&labels)
    }

    fn require(&self, labels: [usize; 3]) -> Result<&K, FusionError> {
        self.u
            .get(&labels)
            .ok_or(FusionError::Category(CategoryDefect::GaugeMissing {
                labels,
            }))
    }

    fn validate_entry(&self, labels: [usize; 3], value: &K) -> Result<(), FusionError> {
        if value.is_zero() {
            return Err(FusionError::Category(CategoryDefect::GaugeZero { labels }));
        }
        self.require(labels)?;
        Ok(())
    }

    fn replace(&mut self, labels: [usize; 3], value: K) -> Result<(), FusionError> {
        self.validate_entry(labels, &value)?;
        self.u.insert(labels, value);
        Ok(())
    }

    pub fn with(&self, labels: [usize; 3], value: K) -> Result<Self, FusionError> {
        self.validate_entry(labels, &value)?;
        let mut result = self.clone();
        result.u.insert(labels, value);
        Ok(result)
    }

    pub fn inverse(&self) -> Result<Self, FusionError> {
        let mut u = BTreeMap::new();
        for (labels, value) in &self.u {
            u.insert(
                *labels,
                omega_number_theory::scalar::inverse(value).map_err(FusionError::from)?,
            );
        }
        Ok(Self { u })
    }
}

enum InverseBlock<K> {
    Vacant,
    Invertible(FBlock<K>),
    Singular,
}

fn classify_f_block<K: FusionScalar>(
    ring: &FusionRing,
    f: &FSymbols<K>,
    labels: [usize; 4],
) -> Result<InverseBlock<K>, FusionError> {
    let (rows, cols) = intermediate_labels(ring, labels);
    let admissible = !rows.is_empty() || !cols.is_empty();
    let block = match (f.block(labels), admissible) {
        (None, false) => return Ok(InverseBlock::Vacant),
        (None, true) => {
            return Err(FusionError::Category(CategoryDefect::BlockMissing {
                labels,
            }))
        }
        (Some(_), false) => {
            return Err(FusionError::Category(CategoryDefect::BlockUnexpected {
                labels,
            }))
        }
        (Some(block), true) => block,
    };
    if block.rows != rows || block.cols != cols {
        return Err(FusionError::Category(CategoryDefect::BlockLabels {
            labels,
        }));
    }
    if block.matrix.shape() != (rows.len(), cols.len()) {
        return Err(FusionError::Category(CategoryDefect::BlockShape {
            labels,
            rows: block.matrix.shape().0,
            cols: block.matrix.shape().1,
            expected: rows.len(),
        }));
    }
    invert_f_block(block)
}

fn invert_f_block<K: FusionScalar>(block: &FBlock<K>) -> Result<InverseBlock<K>, FusionError> {
    match block.inverse() {
        Ok(inverse) => Ok(InverseBlock::Invertible(inverse)),
        Err(
            FusionError::Singular { .. }
            | FusionError::NoInverse { .. }
            | FusionError::ExactField(linear_algebra::exact_field::ExactFieldError::Singular {
                ..
            }),
        ) => Ok(InverseBlock::Singular),
        Err(other) => Err(other),
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct FusionCategory<K> {
    ring: FusionRing,
    f: FSymbols<K>,
    f_inverse: BTreeMap<[usize; 4], FBlock<K>>,
    singular: Vec<[usize; 4]>,
}

impl<K: FusionScalar> FusionCategory<K> {
    pub fn new(ring: FusionRing, f: FSymbols<K>) -> Result<Self, FusionError> {
        Self::new_with_limits(ring, f, DEFAULT_CATEGORY_LIMITS)
    }

    pub fn new_with_limits(
        ring: FusionRing,
        f: FSymbols<K>,
        limits: OperationLimits,
    ) -> Result<Self, FusionError> {
        require_multiplicity_free(&ring)?;
        admit_category_resources(&ring, limits)?;
        let r = ring.rank();
        if f.rank != r {
            return Err(FusionError::ListLength {
                what: "F-symbol labels",
                expected: r,
                got: f.rank,
            });
        }
        let mut f_inverse = BTreeMap::new();
        let mut singular = Vec::new();
        for labels in label_quadruples(r) {
            match classify_f_block(&ring, &f, labels)? {
                InverseBlock::Vacant => {}
                InverseBlock::Invertible(inverse) => {
                    f_inverse.insert(labels, inverse);
                }
                InverseBlock::Singular => singular.push(labels),
            }
        }
        Ok(Self {
            ring,
            f,
            f_inverse,
            singular,
        })
    }

    pub fn singular_blocks(&self) -> &[[usize; 4]] {
        &self.singular
    }

    pub fn validated(ring: FusionRing, f: FSymbols<K>) -> Result<Self, FusionError> {
        let category = Self::new(ring, f)?;
        category.validate()?;
        Ok(category)
    }

    pub fn ring(&self) -> &FusionRing {
        &self.ring
    }

    pub fn f_symbols(&self) -> &FSymbols<K> {
        &self.f
    }

    pub fn f_entry(&self, labels: [usize; 4], e: usize, f: usize) -> K {
        self.f.entry(labels, e, f).cloned().unwrap_or_else(K::zero)
    }

    pub fn f_inverse_block(&self, labels: [usize; 4]) -> Option<&FBlock<K>> {
        self.f_inverse.get(&labels)
    }

    pub fn f_inverse_entry(&self, labels: [usize; 4], f: usize, e: usize) -> K {
        self.f_inverse
            .get(&labels)
            .and_then(|block| block.entry(f, e))
            .cloned()
            .unwrap_or_else(K::zero)
    }

    fn fuse_table(&self) -> FusionSupport {
        fusion_support(&self.ring)
    }

    pub fn pentagon_defects(&self) -> Vec<PentagonDefect<K>> {
        self.pentagon_scan(false)
    }

    pub fn first_pentagon_defect(&self) -> Option<PentagonDefect<K>> {
        self.pentagon_scan(true).into_iter().next()
    }

    fn pentagon_scan(&self, stop_at_first: bool) -> Vec<PentagonDefect<K>> {
        let fuse = self.fuse_table();
        let mut defects = Vec::new();
        let mut paths = PentagonPaths::new(self.ring.rank());
        for labels in label_quadruples(self.ring.rank()) {
            if self.pentagon_quad_scan(labels, &fuse, &mut paths, stop_at_first, &mut defects) {
                break;
            }
        }
        defects
    }

    fn pentagon_quad_scan(
        &self,
        [a, b, c, d]: [usize; 4],
        fuse: &FusionSupport,
        paths: &mut PentagonPaths,
        stop_at_first: bool,
        defects: &mut Vec<PentagonDefect<K>>,
    ) -> bool {
        paths.fill_left(fuse, [a, b, c, d]);
        paths.fill_right(fuse, [a, b, c, d]);
        for &[e, f, g] in &paths.left {
            for &[k, l] in &paths.right[e] {
                let labels = [a, b, c, d, e, f, g, k, l];
                let lhs = self.pentagon_lhs(labels);
                let rhs = self.pentagon_rhs(labels, &fuse[b][c]);
                if lhs == rhs {
                    continue;
                }
                defects.push(PentagonDefect { labels, lhs, rhs });
                if stop_at_first {
                    return true;
                }
            }
        }
        false
    }

    fn pentagon_lhs(&self, [a, b, c, d, e, f, g, k, l]: [usize; 9]) -> K {
        match (
            self.f.entry([f, c, d, e], g, l),
            self.f.entry([a, b, l, e], f, k),
        ) {
            (Some(x), Some(y)) => x.mul(y),
            _ => K::zero(),
        }
    }

    fn pentagon_rhs(&self, [a, b, c, d, e, f, g, k, l]: [usize; 9], h_labels: &[usize]) -> K {
        let mut total = K::zero();
        for &h in h_labels {
            if let (Some(x), Some(y), Some(z)) = (
                self.f.entry([a, b, c, g], f, h),
                self.f.entry([a, h, d, e], g, k),
                self.f.entry([b, c, d, k], h, l),
            ) {
                total = total.add(&x.mul(y).mul(z));
            }
        }
        total
    }

    fn unit_defect_labels(&self) -> impl Iterator<Item = [usize; 4]> + '_ {
        let unit = self.ring.unit();
        self.f
            .blocks
            .iter()
            .filter(move |([a, b, c, _], _)| *a == unit || *b == unit || *c == unit)
            .filter(|(_, block)| {
                !(block.matrix.shape() == (1, 1)
                    && block.matrix.get_ref(0, 0).is_ok_and(|x| *x == K::one()))
            })
            .map(|(labels, _)| *labels)
    }

    pub fn unit_defects(&self) -> Vec<[usize; 4]> {
        self.unit_defect_labels().collect()
    }

    pub fn validate(&self) -> Result<(), FusionError> {
        if let Some(labels) = self.singular.first() {
            return Err(FusionError::Category(CategoryDefect::BlockSingular {
                labels: *labels,
            }));
        }
        if let Some(labels) = self.unit_defect_labels().next() {
            return Err(FusionError::Category(CategoryDefect::UnitLaw { labels }));
        }
        if let Some(defect) = self.first_pentagon_defect() {
            return Err(FusionError::Category(CategoryDefect::Pentagon {
                labels: defect.labels,
            }));
        }
        Ok(())
    }

    pub fn is_unitary(&self) -> Result<bool, FusionError> {
        for block in self.f.blocks.values() {
            if !involution::is_unitary(&block.matrix).map_err(FusionError::from)? {
                return Ok(false);
            }
        }
        Ok(true)
    }

    pub fn gauge_transform(&self, gauge: &Gauge<K>) -> Result<Self, FusionError> {
        let mut blocks = BTreeMap::new();
        for (&[a, b, c, d], block) in &self.f.blocks {
            let matrix = BasicMatrix::try_from_fn_result(
                block.rows.len(),
                block.cols.len(),
                |i, j| -> Result<K, FusionError> {
                    let e = block.rows[i];
                    let f = block.cols[j];
                    let numerator = gauge.require([a, b, e])?.mul(gauge.require([e, c, d])?);
                    let denominator = gauge.require([b, c, f])?.mul(gauge.require([a, f, d])?);
                    let factor = omega_number_theory::scalar::divide(&numerator, &denominator)
                        .map_err(FusionError::from)?;
                    Ok(factor.mul(block.matrix.get_ref(i, j)?))
                },
            )?;
            blocks.insert(
                [a, b, c, d],
                FBlock {
                    rows: block.rows.clone(),
                    cols: block.cols.clone(),
                    matrix,
                },
            );
        }
        Self::new(
            self.ring.clone(),
            FSymbols {
                rank: self.f.rank,
                blocks,
            },
        )
    }

    fn unit_constraint(&self, labels: [usize; 4], e: usize, f: usize) -> Result<&K, FusionError> {
        self.f.entry(labels, e, f).ok_or(FusionError::Category(
            CategoryDefect::UnitNormalizationImpossible {
                labels: [labels[0], labels[1], labels[2]],
            },
        ))
    }

    fn unit_gauge_pair(&self, b: usize) -> Result<(K, K), FusionError> {
        let unit = self.ring.unit();
        let b_star = self.ring.dual(b)?;
        let right = self.unit_constraint([b_star, b, unit, unit], unit, b)?;
        let left_inverse = self.unit_constraint([unit, b, b_star, unit], b, unit)?;
        let left = omega_number_theory::scalar::inverse(left_inverse).map_err(FusionError::from)?;
        Ok((right.clone(), left))
    }

    pub fn unit_normalizing_gauge(&self) -> Result<Gauge<K>, FusionError> {
        let unit = self.ring.unit();
        let mut gauge = Gauge::trivial(&self.ring);
        for b in (0..self.ring.rank()).filter(|&b| b != unit) {
            let (right, left) = self.unit_gauge_pair(b)?;
            gauge.replace([b, unit, b], right)?;
            gauge.replace([unit, b, b], left)?;
        }
        let normalized = self.gauge_transform(&gauge)?;
        if let Some(labels) = normalized.unit_defect_labels().next() {
            return Err(FusionError::Category(
                CategoryDefect::UnitNormalizationImpossible {
                    labels: [labels[0], labels[1], labels[2]],
                },
            ));
        }
        Ok(gauge)
    }

    pub fn normalize_units(&self) -> Result<Self, FusionError> {
        self.gauge_transform(&self.unit_normalizing_gauge()?)
    }

    pub fn dimension_invariant(&self, a: usize) -> Result<K, FusionError> {
        let unit = self.ring.unit();
        let a_star = self.ring.dual(a)?;
        let first = self.f.entry([a, a_star, a, a], unit, unit);
        let second = self.f.entry([a_star, a, a_star, a_star], unit, unit);
        match (first, second) {
            (Some(x), Some(y)) => Ok(x.mul(y)),
            _ => Err(FusionError::Category(CategoryDefect::BlockMissing {
                labels: [a, a_star, a, a],
            })),
        }
    }

    fn verify_dimension_entry(&self, a: usize, dims: &[K]) -> Result<(), FusionError> {
        if dims[a].is_zero() {
            return Err(dimension_error(DimensionDefect::Zero { label: a }));
        }
        if dims[a] != dims[self.ring.dual(a)?] {
            return Err(dimension_error(DimensionDefect::NotSpherical { label: a }));
        }
        Ok(())
    }

    fn verify_character_pair(&self, [a, b]: [usize; 2], dims: &[K]) -> Result<(), FusionError> {
        let mut total = K::zero();
        for (c, dimension) in dims.iter().enumerate() {
            let multiplicity = self.ring.n(a, b, c);
            if multiplicity == 0 {
                continue;
            }
            let n = omega_number_theory::scalar::from_i64::<K>(
                i64::try_from(multiplicity).map_err(|_| FusionError::Overflow {
                    context: "embedding a fusion coefficient",
                })?,
            );
            total = total.add(&n.mul(dimension));
        }
        if dims[a].mul(&dims[b]) != total {
            return Err(dimension_error(DimensionDefect::NotCharacter { a, b }));
        }
        Ok(())
    }

    fn verify_dimension_invariant(&self, a: usize, dims: &[K]) -> Result<(), FusionError> {
        let product = dims[a]
            .mul(&dims[self.ring.dual(a)?])
            .mul(&self.dimension_invariant(a)?);
        if product != K::one() {
            return Err(dimension_error(DimensionDefect::DisagreesWithF {
                label: a,
            }));
        }
        Ok(())
    }

    pub fn verify_dimensions(&self, dims: &[K]) -> Result<(), FusionError> {
        let rank = self.ring.rank();
        if dims.len() != rank {
            return Err(dimension_error(DimensionDefect::Count {
                expected: rank,
                got: dims.len(),
            }));
        }
        if dims[self.ring.unit()] != K::one() {
            return Err(dimension_error(DimensionDefect::UnitNotOne));
        }
        for a in 0..rank {
            self.verify_dimension_entry(a, dims)?;
        }
        for labels in label_pairs(rank) {
            self.verify_character_pair(labels, dims)?;
        }
        for a in 0..rank {
            self.verify_dimension_invariant(a, dims)?;
        }
        Ok(())
    }

    pub fn frobenius_schur_indicator(
        &self,
        a: usize,
        dims: &[K],
    ) -> Result<Option<i8>, FusionError> {
        if self.ring.dual(a)? != a {
            return Ok(None);
        }
        let unit = self.ring.unit();
        let entry = self
            .f
            .entry([a, a, a, a], unit, unit)
            .ok_or(FusionError::Category(CategoryDefect::BlockMissing {
                labels: [a, a, a, a],
            }))?;
        let d = dims.get(a).ok_or(FusionError::Label {
            label: a,
            rank: dims.len(),
        })?;
        let value = d.mul(entry);
        if value == K::one() {
            Ok(Some(1))
        } else if value == K::one().neg() {
            Ok(Some(-1))
        } else {
            Err(FusionError::Category(CategoryDefect::Dimensions(
                DimensionDefect::FrobeniusSchurNotSign { label: a },
            )))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::rational::{rq, Rational};

    #[test]
    fn generic_category_admission_bounds_storage_and_law_work_before_coefficients() {
        let ring = FusionRing::pointed(&[8], None).unwrap();
        let calls = std::cell::Cell::new(0usize);
        let tight = OperationLimits {
            max_elements: 1 << 20,
            max_scalar_ops: 1,
        };
        assert!(matches!(
            FSymbols::<Rational>::from_fn_with_limits(&ring, tight, |_, _, _| {
                calls.set(calls.get() + 1);
                rq(1, 1)
            }),
            Err(FusionError::Budget { .. })
        ));
        assert_eq!(calls.get(), 0);
        let tight = OperationLimits {
            max_elements: 1,
            max_scalar_ops: 1 << 28,
        };
        assert!(matches!(
            FSymbols::<Rational>::from_fn_with_limits(&ring, tight, |_, _, _| {
                calls.set(calls.get() + 1);
                rq(1, 1)
            }),
            Err(FusionError::Budget {
                what: "fusion category symbol storage",
                ..
            })
        ));
        assert_eq!(calls.get(), 0);
        let symbols = FSymbols::<Rational>::trivial(&ring).unwrap();
        assert!(matches!(
            FusionCategory::new_with_limits(ring.clone(), symbols.clone(), tight),
            Err(FusionError::Budget { .. })
        ));
        let category = FusionCategory::new(ring, symbols).unwrap();
        assert!(category.validate().is_ok());
        assert!(category.pentagon_defects().is_empty());
    }

    #[test]
    fn pointed_rank32_replays_every_pentagon_without_dense_label_products() {
        let ring = FusionRing::pointed(&[32], None).unwrap();
        let category =
            FusionCategory::<Rational>::validated(ring.clone(), FSymbols::trivial(&ring).unwrap())
                .unwrap();
        assert_eq!(category.ring().rank(), 32);
        assert!(category.first_pentagon_defect().is_none());
    }

    fn z2_category(omega: i64) -> Result<FusionCategory<Rational>, FusionError> {
        let ring = FusionRing::z_n(2)?;
        let f = FSymbols::from_fn(&ring, |labels, _, _| {
            if labels == [1, 1, 1, 1] {
                rq(omega, 1)
            } else {
                rq(1, 1)
            }
        })?;
        FusionCategory::new(ring, f)
    }

    #[test]
    fn the_two_associators_of_z2_satisfy_the_pentagon_and_nothing_else_does() {
        for omega in [1, -1] {
            let category = z2_category(omega).unwrap();
            assert_eq!(category.pentagon_defects(), vec![], "omega = {omega}");
            assert!(category.validate().is_ok());
        }
        let bad = z2_category(2).unwrap();
        let defects = bad.pentagon_defects();
        assert!(!defects.is_empty());
        assert!(matches!(
            bad.validate(),
            Err(FusionError::Category(CategoryDefect::Pentagon { .. }))
        ));
        let zero_entry = z2_category(0).unwrap();
        assert_eq!(zero_entry.singular_blocks(), &[[1, 1, 1, 1]]);
        assert!(
            matches!(
                zero_entry.validate(),
                Err(FusionError::Category(CategoryDefect::BlockSingular {
                    labels: [1, 1, 1, 1]
                }))
            ),
            "a singular F-block is refused by validation"
        );
    }

    #[test]
    fn the_pentagon_defect_reports_the_first_tuple_and_both_sides() {
        let bad = z2_category(3).unwrap();
        let defects = bad.pentagon_defects();
        assert_eq!(defects.len(), 1);
        let first = bad.first_pentagon_defect().unwrap();
        assert_eq!(defects[0], first);
        assert_eq!(first.labels, [1, 1, 1, 1, 0, 0, 1, 1, 0]);
        assert_eq!(first.lhs, rq(1, 1));
        assert_eq!(first.rhs, rq(9, 1));
        assert!(first.involves([1, 1, 1, 1], 0, 0));
        assert!(!first.involves([0, 0, 0, 0], 0, 0));
    }

    #[test]
    fn unit_laws_are_checked_and_repaired_by_the_canonical_gauge() {
        let category = z2_category(-1).unwrap();
        assert_eq!(category.unit_defects(), Vec::<[usize; 4]>::new());
        let gauge = Gauge::trivial(category.ring())
            .with([1, 0, 1], rq(2, 1))
            .unwrap()
            .with([0, 1, 1], rq(3, 1))
            .unwrap();
        let scaled = category.gauge_transform(&gauge).unwrap();
        assert!(!scaled.unit_defects().is_empty());
        assert_eq!(scaled.pentagon_defects(), vec![]);
        let repaired = scaled.normalize_units().unwrap();
        assert_eq!(repaired.unit_defects(), Vec::<[usize; 4]>::new());
        assert_eq!(repaired.pentagon_defects(), vec![]);
        assert_eq!(
            repaired, category,
            "the normalised gauge is the original one"
        );
    }

    #[test]
    fn the_gauge_transform_follows_its_defining_formula_entrywise() {
        let category = z2_category(-1).unwrap();
        let gauge = Gauge::from_fn(category.ring(), |[a, b, c]| {
            rq(1 + 2 * a as i64 + 5 * b as i64 + 7 * c as i64, 3)
        })
        .unwrap();
        let transformed = category.gauge_transform(&gauge).unwrap();
        let g = |a, b, c| gauge.get([a, b, c]).unwrap().clone();
        let expected = (g(1, 1, 0) * g(0, 1, 1)) / (g(1, 1, 0) * g(1, 0, 1)) * rq(-1, 1);
        assert_eq!(transformed.f_entry([1, 1, 1, 1], 0, 0), expected);
        let back = transformed
            .gauge_transform(&gauge.inverse().unwrap())
            .unwrap();
        assert_eq!(back, category);
    }

    #[test]
    fn structural_defects_in_f_data_are_refused_with_typed_errors() {
        let ring = FusionRing::z_n(2).unwrap();
        let s3 = FusionRing::rep_s3().unwrap();
        assert!(FSymbols::<Rational>::trivial(&s3).is_err());
        let fusion = FSymbols::from_fn(&ring, |_, _, _| rq(1, 1)).unwrap();
        let other = FusionRing::z_n(3).unwrap();
        assert!(matches!(
            FusionCategory::new(other, fusion.clone()),
            Err(FusionError::ListLength { .. })
        ));
        assert!(fusion.with_entry([0, 0, 0, 1], 0, 0, rq(1, 1)).is_err());
        assert!(fusion.with_entry([1, 1, 1, 1], 1, 1, rq(1, 1)).is_err());
        let replaced = fusion.with_entry([1, 1, 1, 1], 0, 0, rq(-1, 1)).unwrap();
        assert_eq!(replaced.entry([1, 1, 1, 1], 0, 0), Some(&rq(-1, 1)));
        assert_eq!(replaced.entry([1, 1, 1, 1], 1, 0), None);
    }

    #[test]
    fn dimensions_are_checked_against_the_ring_and_the_f_symbols() {
        let semion = z2_category(-1).unwrap();
        let ones = vec![rq(1, 1), rq(1, 1)];
        assert_eq!(semion.verify_dimensions(&ones), Ok(()));
        assert_eq!(semion.frobenius_schur_indicator(1, &ones), Ok(Some(-1)));
        assert_eq!(semion.frobenius_schur_indicator(0, &ones), Ok(Some(1)));
        let trivial = z2_category(1).unwrap();
        assert_eq!(trivial.frobenius_schur_indicator(1, &ones), Ok(Some(1)));
        let defect = |dims: Vec<Rational>| match semion.verify_dimensions(&dims) {
            Err(FusionError::Category(CategoryDefect::Dimensions(defect))) => defect,
            other => panic!("expected a dimension defect, got {other:?}"),
        };
        assert_eq!(
            defect(vec![rq(1, 1)]),
            DimensionDefect::Count {
                expected: 2,
                got: 1
            }
        );
        assert_eq!(
            defect(vec![rq(2, 1), rq(1, 1)]),
            DimensionDefect::UnitNotOne
        );
        assert_eq!(
            defect(vec![rq(1, 1), rq(0, 1)]),
            DimensionDefect::Zero { label: 1 }
        );
        assert_eq!(
            defect(vec![rq(1, 1), rq(2, 1)]),
            DimensionDefect::NotCharacter { a: 1, b: 1 }
        );
        let flipped = vec![rq(1, 1), rq(-1, 1)];
        assert_eq!(semion.verify_dimensions(&flipped), Ok(()));
        assert_eq!(semion.frobenius_schur_indicator(1, &flipped), Ok(Some(1)));
        let scaled = z2_category(2).unwrap();
        match scaled.verify_dimensions(&ones) {
            Err(FusionError::Category(CategoryDefect::Dimensions(defect))) => {
                assert_eq!(defect, DimensionDefect::DisagreesWithF { label: 1 });
            }
            other => panic!("expected a disagreement with the F-symbols, got {other:?}"),
        }
        assert_eq!(
            scaled.frobenius_schur_indicator(1, &ones),
            Err(FusionError::Category(CategoryDefect::Dimensions(
                DimensionDefect::FrobeniusSchurNotSign { label: 1 }
            )))
        );
    }
}
