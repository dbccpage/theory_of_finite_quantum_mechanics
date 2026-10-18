//! Recursive 5D rational interval partitioner and tree representation over `num_rational::BigRational`.
//!
//! STRICT ZERO-FLOAT DISCIPLINE: f32 and f64 are strictly forbidden in this module.
//! All coordinates, cuts, margins, and volumes are computed in exact rational arithmetic.
//!
//! AuthorityEffect: None.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub const DIM_5D: usize = 5;

/// Errors arising during 5D box partition and cover verification.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, thiserror::Error, Serialize, Deserialize)]
pub enum CoverTreeError {
    #[error("Invalid dimension {0}: must be strictly less than 5")]
    InvalidDimension(usize),

    #[error("Invalid interval for dimension {dim}: lo ({lo}) >= hi ({hi})")]
    InvalidInterval {
        dim: usize,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Cut out of bounds for dimension {dim}: cut ({cut}) is not strictly interior to ({lo}, {hi})")]
    CutOutOfBounds {
        dim: usize,
        cut: BigRational,
        lo: BigRational,
        hi: BigRational,
    },

    #[error("Box geometry mismatch: expected {expected:?}, got {actual:?}")]
    BoxMismatch {
        expected: Box<RationalBox5D>,
        actual: Box<RationalBox5D>,
    },

    #[error("Domain mismatch: expected domain {expected:?}, actual cover domain {actual:?}")]
    DomainMismatch {
        expected: Box<RationalBox5D>,
        actual: Box<RationalBox5D>,
    },

    #[error("Volume conservation mismatch: expected domain volume {expected}, total leaf volume {actual}")]
    VolumeMismatch {
        expected: BigRational,
        actual: BigRational,
    },

    #[error("Overlap detected between leaf {leaf_a} and leaf {leaf_b}")]
    OverlapDetected { leaf_a: usize, leaf_b: usize },

    #[error("Leaf box is missing an obstruction certificate: {0:?}")]
    MissingCertificate(RationalBox5D),

    #[error("Leaf box is missing an obstruction margin: {0:?}")]
    MissingMargin(RationalBox5D),

    #[error("Leaf box margin is non-positive ({margin} <= 0) for box {box_5d:?}")]
    NonPositiveMargin {
        box_5d: RationalBox5D,
        margin: BigRational,
    },

    #[error("Empty tree: partition tree has 0 leaves")]
    EmptyTree,

    #[error("Leaf index {index} out of bounds: tree has {total_leaves} leaves")]
    LeafIndexOutOfBounds { index: usize, total_leaves: usize },

    #[error("Serialization / format error: {0}")]
    SerializationError(String),
}

/// A 5-dimensional axis-aligned hyper-rectangle with exact rational interval bounds:
/// `[u_0, v_0] x [u_1, v_1] x [u_2, v_2] x [u_3, v_3] x [u_4, v_4]`.
///
/// Invariant: For all j in 0..5, `bounds[j].0 < bounds[j].1`.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct RationalBox5D {
    pub bounds: [(BigRational, BigRational); DIM_5D],
}

impl RationalBox5D {
    /// Constructs the standard 5D unit cube `[0, 1]^5`.
    pub fn unit_cube() -> Self {
        let zero = BigRational::zero();
        let one = BigRational::one();
        Self {
            bounds: std::array::from_fn(|_| (zero.clone(), one.clone())),
        }
    }

    /// Constructs a new 5D rational box with strict non-degeneracy check:
    /// `bounds[j].0 < bounds[j].1` for all j in 0..5.
    pub fn new(bounds: [(BigRational, BigRational); DIM_5D]) -> Result<Self, CoverTreeError> {
        for j in 0..DIM_5D {
            if bounds[j].0 >= bounds[j].1 {
                return Err(CoverTreeError::InvalidInterval {
                    dim: j,
                    lo: bounds[j].0.clone(),
                    hi: bounds[j].1.clone(),
                });
            }
        }
        Ok(Self { bounds })
    }

    /// Tests whether an exact rational 5D point is contained in the closed box.
    pub fn contains_point(&self, pt: &[BigRational; DIM_5D]) -> bool {
        for j in 0..DIM_5D {
            let (ref lo, ref hi) = self.bounds[j];
            if &pt[j] < lo || &pt[j] > hi {
                return false;
            }
        }
        true
    }

    /// Exact 5D hyper-volume: product of interval lengths `(v_j - u_j)`.
    pub fn volume(&self) -> BigRational {
        let mut vol = BigRational::one();
        for (lo, hi) in &self.bounds {
            vol = vol * (hi - lo);
        }
        vol
    }

    /// Subdivides the box along dimension `dim` at `cut`, returning `(left, right)`.
    /// Requires `cut` to be strictly interior: `lo < cut < hi`.
    pub fn subdivide(&self, dim: usize, cut: &BigRational) -> Result<(Self, Self), CoverTreeError> {
        if dim >= DIM_5D {
            return Err(CoverTreeError::InvalidDimension(dim));
        }
        let (ref lo, ref hi) = self.bounds[dim];
        if cut <= lo || cut >= hi {
            return Err(CoverTreeError::CutOutOfBounds {
                dim,
                cut: cut.clone(),
                lo: lo.clone(),
                hi: hi.clone(),
            });
        }
        let mut left_bounds = self.bounds.clone();
        left_bounds[dim].1 = cut.clone();

        let mut right_bounds = self.bounds.clone();
        right_bounds[dim].0 = cut.clone();

        Ok((Self::new(left_bounds)?, Self::new(right_bounds)?))
    }

    /// Returns the exact rational midpoint along coordinate `dim`.
    pub fn midpoint(&self, dim: usize) -> Result<BigRational, CoverTreeError> {
        if dim >= DIM_5D {
            return Err(CoverTreeError::InvalidDimension(dim));
        }
        let two = BigRational::from_integer(BigInt::from(2));
        let (ref lo, ref hi) = self.bounds[dim];
        Ok((lo + hi) / two)
    }

    /// Bisects the box at the exact rational midpoint along coordinate `dim`.
    pub fn bisect(&self, dim: usize) -> Result<(Self, Self), CoverTreeError> {
        let mid = self.midpoint(dim)?;
        self.subdivide(dim, &mid)
    }

    /// Returns the interval width along coordinate `dim`.
    pub fn width(&self, dim: usize) -> Result<BigRational, CoverTreeError> {
        if dim >= DIM_5D {
            return Err(CoverTreeError::InvalidDimension(dim));
        }
        let (ref lo, ref hi) = self.bounds[dim];
        Ok(hi - lo)
    }

    /// Returns the dimension with the strictly maximal interval width (first index in case of tie).
    pub fn max_dim(&self) -> usize {
        let mut best_dim = 0;
        let mut best_width = &self.bounds[0].1 - &self.bounds[0].0;
        for j in 1..DIM_5D {
            let w = &self.bounds[j].1 - &self.bounds[j].0;
            if w > best_width {
                best_width = w;
                best_dim = j;
            }
        }
        best_dim
    }

    /// Checks whether the open interiors of `self` and `other` overlap.
    /// Two boxes have disjoint interiors iff along at least one dimension `d`,
    /// `self.hi <= other.lo` or `other.hi <= self.lo`.
    pub fn overlaps_interior(&self, other: &Self) -> bool {
        for j in 0..DIM_5D {
            let (ref a_lo, ref a_hi) = self.bounds[j];
            let (ref b_lo, ref b_hi) = other.bounds[j];
            if a_hi <= b_lo || b_hi <= a_lo {
                return false;
            }
        }
        true
    }

    /// Serializes to JSON string.
    pub fn to_json(&self) -> Result<String, CoverTreeError> {
        serde_json::to_string_pretty(self)
            .map_err(|e| CoverTreeError::SerializationError(e.to_string()))
    }

    /// Deserializes from JSON string.
    pub fn from_json(s: &str) -> Result<Self, CoverTreeError> {
        serde_json::from_str(s).map_err(|e| CoverTreeError::SerializationError(e.to_string()))
    }
}

/// Recursive 5D bisection tree over `BigRational`.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum BisectionTree {
    Leaf {
        box_5d: RationalBox5D,
        cert_id: Option<String>,
        margin: Option<BigRational>,
    },
    Split {
        dim: usize,
        cut: BigRational,
        left: Box<BisectionTree>,
        right: Box<BisectionTree>,
    },
}

impl BisectionTree {
    /// Constructs a leaf node.
    pub fn leaf(
        box_5d: RationalBox5D,
        cert_id: Option<String>,
        margin: Option<BigRational>,
    ) -> Self {
        BisectionTree::Leaf {
            box_5d,
            cert_id,
            margin,
        }
    }

    /// Constructs a split node.
    pub fn split(dim: usize, cut: BigRational, left: BisectionTree, right: BisectionTree) -> Self {
        BisectionTree::Split {
            dim,
            cut,
            left: Box::new(left),
            right: Box::new(right),
        }
    }

    /// Collects references to all 5D boxes in the tree leaves in left-to-right DFS order.
    pub fn leaves(&self) -> Vec<&RationalBox5D> {
        fn collect<'a>(node: &'a BisectionTree, acc: &mut Vec<&'a RationalBox5D>) {
            match node {
                BisectionTree::Leaf { box_5d, .. } => acc.push(box_5d),
                BisectionTree::Split { left, right, .. } => {
                    collect(left, acc);
                    collect(right, acc);
                }
            }
        }
        let mut out = Vec::new();
        collect(self, &mut out);
        out
    }

    /// Returns the total number of leaves in the tree.
    pub fn leaf_count(&self) -> usize {
        match self {
            BisectionTree::Leaf { .. } => 1,
            BisectionTree::Split { left, right, .. } => left.leaf_count() + right.leaf_count(),
        }
    }

    /// Computes the exact total volume across all leaves.
    pub fn total_volume(&self) -> BigRational {
        match self {
            BisectionTree::Leaf { box_5d, .. } => box_5d.volume(),
            BisectionTree::Split { left, right, .. } => left.total_volume() + right.total_volume(),
        }
    }

    /// Maximum depth of the bisection tree (leaf has depth 0).
    pub fn depth(&self) -> usize {
        match self {
            BisectionTree::Leaf { .. } => 0,
            BisectionTree::Split { left, right, .. } => {
                1 + std::cmp::max(left.depth(), right.depth())
            }
        }
    }

    /// Mutable references to all leaf records: `(&mut RationalBox5D, &mut Option<String>, &mut Option<BigRational>)`.
    pub fn leaves_mut(
        &mut self,
    ) -> Vec<(
        &mut RationalBox5D,
        &mut Option<String>,
        &mut Option<BigRational>,
    )> {
        fn collect<'a>(
            node: &'a mut BisectionTree,
            acc: &mut Vec<(
                &'a mut RationalBox5D,
                &'a mut Option<String>,
                &'a mut Option<BigRational>,
            )>,
        ) {
            match node {
                BisectionTree::Leaf {
                    box_5d,
                    cert_id,
                    margin,
                } => acc.push((box_5d, cert_id, margin)),
                BisectionTree::Split { left, right, .. } => {
                    collect(left, acc);
                    collect(right, acc);
                }
            }
        }
        let mut out = Vec::new();
        collect(self, &mut out);
        out
    }

    /// Serializes the tree to exact rational JSON format.
    pub fn to_json(&self) -> Result<String, CoverTreeError> {
        serde_json::to_string_pretty(self)
            .map_err(|e| CoverTreeError::SerializationError(e.to_string()))
    }

    /// Deserializes the tree from exact rational JSON format.
    pub fn from_json(s: &str) -> Result<Self, CoverTreeError> {
        serde_json::from_str(s).map_err(|e| CoverTreeError::SerializationError(e.to_string()))
    }

    /// Serializes the tree into a structured Lean 4 / Python DTO representation
    /// where rational numbers are represented by explicit numerator and denominator strings.
    pub fn to_lean_dto(&self) -> BisectionTreeDto {
        match self {
            BisectionTree::Leaf {
                box_5d,
                cert_id,
                margin,
            } => BisectionTreeDto::Leaf {
                box_5d: RationalBox5DDto::from_box(box_5d),
                cert_id: cert_id.clone(),
                margin_num: margin.as_ref().map(|m| m.numer().to_string()),
                margin_den: margin.as_ref().map(|m| m.denom().to_string()),
            },
            BisectionTree::Split {
                dim,
                cut,
                left,
                right,
            } => BisectionTreeDto::Split {
                dim: *dim,
                cut_num: cut.numer().to_string(),
                cut_den: cut.denom().to_string(),
                left: Box::new(left.to_lean_dto()),
                right: Box::new(right.to_lean_dto()),
            },
        }
    }

    /// Serializes to a Lean 4 / Python friendly JSON string with explicit `{num, den}` fields.
    pub fn to_lean_json(&self) -> Result<String, CoverTreeError> {
        let dto = self.to_lean_dto();
        serde_json::to_string_pretty(&dto)
            .map_err(|e| CoverTreeError::SerializationError(e.to_string()))
    }

    /// Reconstructs tree from Lean 4 / Python DTO format.
    pub fn from_lean_dto(dto: &BisectionTreeDto) -> Result<Self, CoverTreeError> {
        match dto {
            BisectionTreeDto::Leaf {
                box_5d,
                cert_id,
                margin_num,
                margin_den,
            } => {
                let rbox = box_5d.to_box()?;
                let margin = match (margin_num, margin_den) {
                    (Some(n_str), Some(d_str)) => {
                        let n: BigInt = n_str.parse().map_err(|e| {
                            CoverTreeError::SerializationError(format!("Invalid margin_num: {}", e))
                        })?;
                        let d: BigInt = d_str.parse().map_err(|e| {
                            CoverTreeError::SerializationError(format!("Invalid margin_den: {}", e))
                        })?;
                        if d.is_zero() {
                            return Err(CoverTreeError::SerializationError(
                                "Zero denominator in margin".to_string(),
                            ));
                        }
                        Some(BigRational::new(n, d))
                    }
                    _ => None,
                };
                Ok(BisectionTree::Leaf {
                    box_5d: rbox,
                    cert_id: cert_id.clone(),
                    margin,
                })
            }
            BisectionTreeDto::Split {
                dim,
                cut_num,
                cut_den,
                left,
                right,
            } => {
                let n: BigInt = cut_num.parse().map_err(|e| {
                    CoverTreeError::SerializationError(format!("Invalid cut_num: {}", e))
                })?;
                let d: BigInt = cut_den.parse().map_err(|e| {
                    CoverTreeError::SerializationError(format!("Invalid cut_den: {}", e))
                })?;
                if d.is_zero() {
                    return Err(CoverTreeError::SerializationError(
                        "Zero denominator in cut".to_string(),
                    ));
                }
                let cut = BigRational::new(n, d);
                let l_tree = Self::from_lean_dto(left)?;
                let r_tree = Self::from_lean_dto(right)?;
                Ok(BisectionTree::Split {
                    dim: *dim,
                    cut,
                    left: Box::new(l_tree),
                    right: Box::new(r_tree),
                })
            }
        }
    }

    /// Deserializes from Lean 4 / Python friendly JSON string.
    pub fn from_lean_json(s: &str) -> Result<Self, CoverTreeError> {
        let dto: BisectionTreeDto = serde_json::from_str(s)
            .map_err(|e| CoverTreeError::SerializationError(e.to_string()))?;
        Self::from_lean_dto(&dto)
    }
}

/// DTO for exact rational intervals `[lo, hi]` with string numerators and denominators.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct RationalIntervalDto {
    pub lo_num: String,
    pub lo_den: String,
    pub hi_num: String,
    pub hi_den: String,
}

impl RationalIntervalDto {
    pub fn from_interval(lo: &BigRational, hi: &BigRational) -> Self {
        Self {
            lo_num: lo.numer().to_string(),
            lo_den: lo.denom().to_string(),
            hi_num: hi.numer().to_string(),
            hi_den: hi.denom().to_string(),
        }
    }

    pub fn to_interval(&self) -> Result<(BigRational, BigRational), CoverTreeError> {
        let lo_n: BigInt = self
            .lo_num
            .parse()
            .map_err(|e| CoverTreeError::SerializationError(format!("Invalid lo_num: {}", e)))?;
        let lo_d: BigInt = self
            .lo_den
            .parse()
            .map_err(|e| CoverTreeError::SerializationError(format!("Invalid lo_den: {}", e)))?;
        let hi_n: BigInt = self
            .hi_num
            .parse()
            .map_err(|e| CoverTreeError::SerializationError(format!("Invalid hi_num: {}", e)))?;
        let hi_d: BigInt = self
            .hi_den
            .parse()
            .map_err(|e| CoverTreeError::SerializationError(format!("Invalid hi_den: {}", e)))?;
        if lo_d.is_zero() || hi_d.is_zero() {
            return Err(CoverTreeError::SerializationError(
                "Zero denominator in interval".to_string(),
            ));
        }
        Ok((BigRational::new(lo_n, lo_d), BigRational::new(hi_n, hi_d)))
    }
}

/// DTO for 5D rational boxes compatible with Lean 4 and Python.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub struct RationalBox5DDto {
    pub intervals: [RationalIntervalDto; DIM_5D],
}

impl RationalBox5DDto {
    pub fn from_box(box_5d: &RationalBox5D) -> Self {
        let intervals = std::array::from_fn(|j| {
            RationalIntervalDto::from_interval(&box_5d.bounds[j].0, &box_5d.bounds[j].1)
        });
        Self { intervals }
    }

    pub fn to_box(&self) -> Result<RationalBox5D, CoverTreeError> {
        let mut bounds = Vec::with_capacity(DIM_5D);
        for iv in &self.intervals {
            bounds.push(iv.to_interval()?);
        }
        let arr: [(BigRational, BigRational); DIM_5D] = bounds
            .try_into()
            .map_err(|_| CoverTreeError::InvalidDimension(DIM_5D))?;
        RationalBox5D::new(arr)
    }
}

/// DTO for recursive bisection trees compatible with Lean 4 and Python.
#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum BisectionTreeDto {
    Leaf {
        box_5d: RationalBox5DDto,
        cert_id: Option<String>,
        margin_num: Option<String>,
        margin_den: Option<String>,
    },
    Split {
        dim: usize,
        cut_num: String,
        cut_den: String,
        left: Box<BisectionTreeDto>,
        right: Box<BisectionTreeDto>,
    },
}

/// Verifies that `tree` constitutes an exact, gap-free, overlap-free partition cover of `domain`.
///
/// Specifically verifies:
/// 1. The root bisection matches the specified domain box.
/// 2. Every recursive split along coordinate `dim` cuts strictly in the interior `lo < cut < hi`.
/// 3. The left child exactly matches `[lo, cut]` and the right child exactly matches `[cut, hi]`,
///    guaranteeing zero boundary leakage and zero gap.
/// 4. Every leaf box matches the propagated boundary interval.
/// 5. Exact volume conservation holds: `total_leaf_volume == domain_volume`.
/// 6. Pairwise open interiors of all leaves are mutually disjoint.
pub fn check_partition_cover(
    tree: &BisectionTree,
    domain: &RationalBox5D,
) -> Result<(), CoverTreeError> {
    if tree.leaf_count() == 0 {
        return Err(CoverTreeError::EmptyTree);
    }

    // Step 1 & 2 & 3 & 4: Recursive geometric propagation check
    fn verify_node(
        node: &BisectionTree,
        expected_box: &RationalBox5D,
    ) -> Result<(), CoverTreeError> {
        match node {
            BisectionTree::Leaf { box_5d, .. } => {
                if box_5d != expected_box {
                    return Err(CoverTreeError::BoxMismatch {
                        expected: Box::new(expected_box.clone()),
                        actual: Box::new(box_5d.clone()),
                    });
                }
                Ok(())
            }
            BisectionTree::Split {
                dim,
                cut,
                left,
                right,
            } => {
                if *dim >= DIM_5D {
                    return Err(CoverTreeError::InvalidDimension(*dim));
                }
                let (ref lo, ref hi) = expected_box.bounds[*dim];
                if cut <= lo || cut >= hi {
                    return Err(CoverTreeError::CutOutOfBounds {
                        dim: *dim,
                        cut: cut.clone(),
                        lo: lo.clone(),
                        hi: hi.clone(),
                    });
                }
                let (left_box, right_box) = expected_box.subdivide(*dim, cut)?;
                verify_node(left, &left_box)?;
                verify_node(right, &right_box)?;
                Ok(())
            }
        }
    }

    verify_node(tree, domain)?;

    // Step 5: Exact volume conservation
    let total_leaf_vol = tree.total_volume();
    let domain_vol = domain.volume();
    if total_leaf_vol != domain_vol {
        return Err(CoverTreeError::VolumeMismatch {
            expected: domain_vol,
            actual: total_leaf_vol,
        });
    }

    // Step 6: Pairwise disjoint leaf interiors
    let leaves = tree.leaves();
    let n = leaves.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if leaves[i].overlaps_interior(leaves[j]) {
                return Err(CoverTreeError::OverlapDetected {
                    leaf_a: i,
                    leaf_b: j,
                });
            }
        }
    }

    Ok(())
}

/// Sealed receipt of a verified exact cover obstruction over a stated 5D rational domain.
///
/// Contains proof data that every leaf in the partition cover has a verified positive obstruction margin.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CoverObstructionReceipt {
    pub schema_version: String,
    pub domain: RationalBox5D,
    pub leaf_count: usize,
    pub total_volume: BigRational,
    pub min_margin: BigRational,
    pub certified_leaves: usize,
    pub verified_sound: bool,
    pub firewall: String,
    pub authority_effect: String,
    pub sha256_digest: Option<String>,
}

impl CoverObstructionReceipt {
    /// Computes canonical SHA256 hex digest of the receipt.
    pub fn compute_digest(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.schema_version.as_bytes());
        hasher.update(self.leaf_count.to_string().as_bytes());
        hasher.update(self.total_volume.to_string().as_bytes());
        hasher.update(self.min_margin.to_string().as_bytes());
        hasher.update(self.certified_leaves.to_string().as_bytes());
        hasher.update(self.firewall.as_bytes());
        hasher.update(self.authority_effect.as_bytes());
        for (lo, hi) in &self.domain.bounds {
            hasher.update(lo.to_string().as_bytes());
            hasher.update(hi.to_string().as_bytes());
        }
        format!("{:x}", hasher.finalize())
    }

    /// Serializes receipt to JSON.
    pub fn to_json(&self) -> Result<String, CoverTreeError> {
        serde_json::to_string_pretty(self)
            .map_err(|e| CoverTreeError::SerializationError(e.to_string()))
    }

    /// Deserializes receipt from JSON.
    pub fn from_json(s: &str) -> Result<Self, CoverTreeError> {
        serde_json::from_str(s).map_err(|e| CoverTreeError::SerializationError(e.to_string()))
    }
}

/// Verifies that `tree` is a valid partition cover of `domain` AND that every leaf has a
/// valid obstruction certificate with strictly positive margin `margin > 0`.
///
/// Returns a sealed `CoverObstructionReceipt`.
pub fn verify_cover_obstruction(
    tree: &BisectionTree,
    domain: &RationalBox5D,
) -> Result<CoverObstructionReceipt, CoverTreeError> {
    // 1. Check partition geometry and volume conservation
    check_partition_cover(tree, domain)?;

    // 2. Audit all leaves for positive obstruction certificates
    fn check_leaves<'a>(
        node: &'a BisectionTree,
        min_margin: &mut Option<BigRational>,
        count: &mut usize,
    ) -> Result<(), CoverTreeError> {
        match node {
            BisectionTree::Leaf {
                box_5d,
                cert_id,
                margin,
            } => {
                if cert_id.is_none() {
                    return Err(CoverTreeError::MissingCertificate(box_5d.clone()));
                }
                let m = margin
                    .as_ref()
                    .ok_or_else(|| CoverTreeError::MissingMargin(box_5d.clone()))?;
                if m <= &BigRational::zero() {
                    return Err(CoverTreeError::NonPositiveMargin {
                        box_5d: box_5d.clone(),
                        margin: m.clone(),
                    });
                }
                *count += 1;
                if let Some(ref current_min) = min_margin {
                    if m < current_min {
                        *min_margin = Some(m.clone());
                    }
                } else {
                    *min_margin = Some(m.clone());
                }
                Ok(())
            }
            BisectionTree::Split { left, right, .. } => {
                check_leaves(left, min_margin, count)?;
                check_leaves(right, min_margin, count)?;
                Ok(())
            }
        }
    }

    let mut min_margin = None;
    let mut certified_count = 0;
    check_leaves(tree, &mut min_margin, &mut certified_count)?;

    let min_margin = min_margin.expect("non-empty tree must produce min_margin");
    let total_volume = tree.total_volume();

    let mut receipt = CoverObstructionReceipt {
        schema_version: "omega.mub6.cover-obstruction.v1".to_string(),
        domain: domain.clone(),
        leaf_count: tree.leaf_count(),
        total_volume,
        min_margin,
        certified_leaves: certified_count,
        verified_sound: true,
        firewall: FIREWALL.to_string(),
        authority_effect: AUTHORITY_EFFECT.to_string(),
        sha256_digest: None,
    };

    receipt.sha256_digest = Some(receipt.compute_digest());
    Ok(receipt)
}

// ---------------------------------------------------------------------------
// Integration with Target A4 Dual SDP Certifier and L1 Network Simplex
// ---------------------------------------------------------------------------

use omega_solvers::solver_flow_network_simplex::NetworkSimplexSolution;

use crate::omega_native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};
use crate::omega_native::exact::mub6_quad_sdp::MubQuadSdpCertificate;
use omega_certifiers::phi1_certifier::Phi1Certificate;
use omega_solvers::solver_lp_phi1_boundary::Phi1Solution;

/// Attaches a Target A4 SDP Dual Certificate to leaf at `leaf_index`.
/// Verifies that the SDP certificate successfully certified non-PSD obstruction
/// and attaches its strict regularized margin.
pub fn certify_leaf_with_sdp(
    tree: &mut BisectionTree,
    leaf_index: usize,
    sdp_cert: &MubQuadSdpCertificate,
) -> Result<(), CoverTreeError> {
    let mut leaves = tree.leaves_mut();
    let total = leaves.len();
    if leaf_index >= total {
        return Err(CoverTreeError::LeafIndexOutOfBounds {
            index: leaf_index,
            total_leaves: total,
        });
    }

    if !sdp_cert.dual_certificate_psd_certified || !sdp_cert.constructed_matrix_not_psd {
        return Err(CoverTreeError::SerializationError(
            "SDP certificate is not certified sound".to_string(),
        ));
    }

    // In Target A4, strict_inner_product < 0 indicates contradiction: Tr(W * G) < 0 with W >= eps I.
    // The margin is the magnitude of the negative trace: -Tr(W * G) > 0.
    let num: BigInt = sdp_cert
        .strict_inner_product_num
        .parse()
        .map_err(|e| CoverTreeError::SerializationError(format!("SDP numerator error: {}", e)))?;
    let den: BigInt = sdp_cert
        .strict_inner_product_den
        .parse()
        .map_err(|e| CoverTreeError::SerializationError(format!("SDP denominator error: {}", e)))?;
    let tr_val = BigRational::new(num, den);
    if tr_val >= BigRational::zero() {
        return Err(CoverTreeError::SerializationError(
            "SDP strict inner product is not strictly negative".to_string(),
        ));
    }
    let margin = -tr_val;

    let (_, ref mut cert_id, ref mut leaf_margin) = leaves[leaf_index];
    **cert_id = Some(format!("target_a4_sdp:{}", sdp_cert.schema_version));
    **leaf_margin = Some(margin);
    Ok(())
}

/// Attaches an L1 Phi1 certificate to leaf at `leaf_index`.
/// Uses the certified objective as the obstruction margin.
pub fn certify_leaf_with_phi1(
    tree: &mut BisectionTree,
    leaf_index: usize,
    phi1_cert: &Phi1Certificate,
) -> Result<(), CoverTreeError> {
    let mut leaves = tree.leaves_mut();
    let total = leaves.len();
    if leaf_index >= total {
        return Err(CoverTreeError::LeafIndexOutOfBounds {
            index: leaf_index,
            total_leaves: total,
        });
    }

    let margin = phi1_cert.dual_objective().clone();
    if margin <= BigRational::zero() {
        return Err(CoverTreeError::NonPositiveMargin {
            box_5d: leaves[leaf_index].0.clone(),
            margin,
        });
    }

    let (_, ref mut cert_id, ref mut leaf_margin) = leaves[leaf_index];
    **cert_id = Some(format!(
        "l1_phi1:{}",
        phi1_cert.metadata().lean_phi1_specification()
    ));
    **leaf_margin = Some(margin);
    Ok(())
}

/// Attaches an L1 Network Simplex solution to leaf at `leaf_index`.
pub fn certify_leaf_with_simplex_solution(
    tree: &mut BisectionTree,
    leaf_index: usize,
    sol: &NetworkSimplexSolution,
) -> Result<(), CoverTreeError> {
    let mut leaves = tree.leaves_mut();
    let total = leaves.len();
    if leaf_index >= total {
        return Err(CoverTreeError::LeafIndexOutOfBounds {
            index: leaf_index,
            total_leaves: total,
        });
    }

    let margin = BigRational::from_integer(BigInt::from(sol.objective));
    if margin <= BigRational::zero() {
        return Err(CoverTreeError::NonPositiveMargin {
            box_5d: leaves[leaf_index].0.clone(),
            margin,
        });
    }

    let (_, ref mut cert_id, ref mut leaf_margin) = leaves[leaf_index];
    **cert_id = Some("l1_network_simplex:v1".to_string());
    **leaf_margin = Some(margin);
    Ok(())
}

/// Attaches an L1 Phi1 solution from `solve_l1_boundary` to leaf at `leaf_index`.
pub fn certify_leaf_with_phi1_solution(
    tree: &mut BisectionTree,
    leaf_index: usize,
    sol: &Phi1Solution,
) -> Result<(), CoverTreeError> {
    let mut leaves = tree.leaves_mut();
    let total = leaves.len();
    if leaf_index >= total {
        return Err(CoverTreeError::LeafIndexOutOfBounds {
            index: leaf_index,
            total_leaves: total,
        });
    }

    let margin = BigRational::from_integer(BigInt::from(sol.objective));
    if margin <= BigRational::zero() {
        return Err(CoverTreeError::NonPositiveMargin {
            box_5d: leaves[leaf_index].0.clone(),
            margin,
        });
    }

    let (_, ref mut cert_id, ref mut leaf_margin) = leaves[leaf_index];
    **cert_id = Some("l1_phi1_boundary:v1".to_string());
    **leaf_margin = Some(margin);
    Ok(())
}

/// Attaches a custom obstruction certificate and margin to leaf at `leaf_index`.
pub fn certify_leaf_with_margin(
    tree: &mut BisectionTree,
    leaf_index: usize,
    cert_id_val: impl Into<String>,
    margin_val: BigRational,
) -> Result<(), CoverTreeError> {
    let mut leaves = tree.leaves_mut();
    let total = leaves.len();
    if leaf_index >= total {
        return Err(CoverTreeError::LeafIndexOutOfBounds {
            index: leaf_index,
            total_leaves: total,
        });
    }

    let (_, ref mut cert_id, ref mut leaf_margin) = leaves[leaf_index];
    **cert_id = Some(cert_id_val.into());
    **leaf_margin = Some(margin_val);
    Ok(())
}

/// Attaches the same certified margin and certificate prefix across all leaves in the tree.
pub fn certify_all_leaves_with_margin(
    tree: &mut BisectionTree,
    cert_id_prefix: &str,
    margin_val: BigRational,
) -> Result<(), CoverTreeError> {
    let mut leaves = tree.leaves_mut();
    for (idx, (_, cert_id, leaf_margin)) in leaves.iter_mut().enumerate() {
        **cert_id = Some(format!("{}:leaf_{}", cert_id_prefix, idx));
        **leaf_margin = Some(margin_val.clone());
    }
    Ok(())
}
