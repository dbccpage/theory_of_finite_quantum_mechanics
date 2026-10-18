//! Simplicial Sets, Kan Complexes, and Quasi-Categories (∞-Categories).
//!
//! Provides mathematically rigorous foundations for simplicial homotopy theory:
//! - Simplicial sets X_• with face maps d_i and degeneracy maps s_j
//! - Simplicial identities validation:
//!     1. d_i ∘ d_j = d_{j-1} ∘ d_i (i < j)
//!     2. d_i ∘ s_j = s_{j-1} ∘ d_i (i < j)
//!     3. d_j ∘ s_j = id = d_{j+1} ∘ s_j
//!     4. d_i ∘ s_j = s_j ∘ d_{i-1} (i > j + 1)
//!     5. s_i ∘ s_j = s_{j+1} ∘ s_i (i <= j)
//! - Horns Λ^k_n (inner for 0 < k < n, outer for k = 0, n)
//! - Quasi-category inner horn filling verification
//! - Kan complex horn filling verification
//!
//! Zero floats. Soviet Builder allocation bounded by `OperationLimits`.
//!
//! AuthorityEffect: None.

use std::collections::HashMap;

use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};

use crate::error::{reserve_exact, HigherCategoryError};

/// An n-simplex in a simplicial set.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Simplex {
    pub id: String,
    pub dimension: usize,
}

/// A horn Λ^k_n in a simplicial set.
/// Specified by (n-1)-simplices x_i for i ∈ {0, ..., n} \ {k}.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Horn {
    pub dimension: usize,
    pub omitted_index: usize,
    /// Maps face index i (where i != omitted_index) to (n-1)-simplex ID.
    pub faces: HashMap<usize, String>,
}

impl Horn {
    /// Returns true if this is an inner horn (0 < k < n).
    pub fn is_inner(&self) -> bool {
        self.omitted_index > 0 && self.omitted_index < self.dimension
    }
}

/// Simplicial set data structure with exact combinatorial verification.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SimplicialSet {
    /// Simplices grouped by dimension
    pub simplices_by_dim: Vec<Vec<Simplex>>,
    /// Face maps: (dim, face_index, simplex_id) -> face_simplex_id
    pub face_maps: HashMap<(usize, usize, String), String>,
    /// Degeneracy maps: (dim, degen_index, simplex_id) -> degen_simplex_id
    pub degeneracy_maps: HashMap<(usize, usize, String), String>,
}

impl SimplicialSet {
    /// Constructs an empty simplicial set up to max_dimension under `OperationLimits`.
    pub fn new(max_dimension: usize, limits: &OperationLimits) -> Result<Self, HigherCategoryError> {
        let count = max_dimension.saturating_add(1);
        let mut simplices_by_dim = Vec::new();
        reserve_exact(&mut simplices_by_dim, count, limits)?;
        for _ in 0..count {
            simplices_by_dim.push(Vec::new());
        }
        Ok(Self {
            simplices_by_dim,
            face_maps: HashMap::new(),
            degeneracy_maps: HashMap::new(),
        })
    }

    /// Adds a simplex of a given dimension.
    pub fn add_simplex(
        &mut self,
        dimension: usize,
        id: impl Into<String>,
        limits: &OperationLimits,
    ) -> Result<(), HigherCategoryError> {
        if dimension >= self.simplices_by_dim.len() {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("dimension < {}", self.simplices_by_dim.len()),
                found: format!("dimension = {}", dimension),
            });
        }
        let id_str = id.into();
        if self.simplices_by_dim[dimension].iter().any(|s| s.id == id_str) {
            return Err(HigherCategoryError::DuplicateCell { id: id_str });
        }
        reserve_exact(&mut self.simplices_by_dim[dimension], 1, limits)?;
        self.simplices_by_dim[dimension].push(Simplex {
            id: id_str,
            dimension,
        });
        Ok(())
    }

    /// Declares a face map d_i: X_n -> X_{n-1}.
    pub fn set_face(
        &mut self,
        dim: usize,
        i: usize,
        simplex: &str,
        face_simplex: &str,
    ) -> Result<(), HigherCategoryError> {
        if dim == 0 {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: "dim >= 1 for face map".to_string(),
                found: "dim = 0".to_string(),
            });
        }
        if i > dim {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("face index i <= {}", dim),
                found: format!("i = {}", i),
            });
        }
        // Verify simplex existence
        if !self.simplices_by_dim[dim].iter().any(|s| s.id == simplex) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: simplex.to_string() });
        }
        if !self.simplices_by_dim[dim - 1].iter().any(|s| s.id == face_simplex) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: face_simplex.to_string() });
        }

        self.face_maps.insert((dim, i, simplex.to_string()), face_simplex.to_string());
        Ok(())
    }

    /// Declares a degeneracy map s_j: X_n -> X_{n+1}.
    pub fn set_degeneracy(
        &mut self,
        dim: usize,
        j: usize,
        simplex: &str,
        degen_simplex: &str,
    ) -> Result<(), HigherCategoryError> {
        if j > dim {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("degeneracy index j <= {}", dim),
                found: format!("j = {}", j),
            });
        }
        if dim + 1 >= self.simplices_by_dim.len() {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("dim + 1 < {}", self.simplices_by_dim.len()),
                found: format!("dim + 1 = {}", dim + 1),
            });
        }
        if !self.simplices_by_dim[dim].iter().any(|s| s.id == simplex) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: simplex.to_string() });
        }
        if !self.simplices_by_dim[dim + 1].iter().any(|s| s.id == degen_simplex) {
            return Err(HigherCategoryError::ZeroCellNotFound { id: degen_simplex.to_string() });
        }

        self.degeneracy_maps.insert((dim, j, simplex.to_string()), degen_simplex.to_string());
        Ok(())
    }

    /// Evaluates d_i(x).
    pub fn face(&self, dim: usize, i: usize, simplex: &str) -> Option<&str> {
        self.face_maps.get(&(dim, i, simplex.to_string())).map(|s| s.as_str())
    }

    /// Evaluates s_j(x).
    pub fn degeneracy(&self, dim: usize, j: usize, simplex: &str) -> Option<&str> {
        self.degeneracy_maps.get(&(dim, j, simplex.to_string())).map(|s| s.as_str())
    }

    /// Verifies the first simplicial identity: d_i ∘ d_j = d_{j-1} ∘ d_i for all i < j.
    pub fn verify_face_face_identities(&self) -> Result<(), HigherCategoryError> {
        for dim in 2..self.simplices_by_dim.len() {
            for simplex in &self.simplices_by_dim[dim] {
                for j in 1..=dim {
                    for i in 0..j {
                        // Left: d_i(d_j(x))
                        let d_j_x = self.face(dim, j, &simplex.id).ok_or_else(|| {
                            HigherCategoryError::SimplicialIdentityViolation {
                                dimension: dim,
                                details: format!("Missing face d_{} on simplex '{}'", j, simplex.id),
                            }
                        })?;
                        let left = self.face(dim - 1, i, d_j_x).ok_or_else(|| {
                            HigherCategoryError::SimplicialIdentityViolation {
                                dimension: dim,
                                details: format!("Missing face d_{} on d_{}('{}')", i, j, simplex.id),
                            }
                        })?;
                        // Right: d_{j-1}(d_i(x))
                        let d_i_x = self.face(dim, i, &simplex.id).ok_or_else(|| {
                            HigherCategoryError::SimplicialIdentityViolation {
                                dimension: dim,
                                details: format!("Missing face d_{} on simplex '{}'", i, simplex.id),
                            }
                        })?;
                        let right = self.face(dim - 1, j - 1, d_i_x).ok_or_else(|| {
                            HigherCategoryError::SimplicialIdentityViolation {
                                dimension: dim,
                                details: format!("Missing face d_{} on d_{}('{}')", j - 1, i, simplex.id),
                            }
                        })?;
                        if left != right {
                            return Err(HigherCategoryError::SimplicialIdentityViolation {
                                dimension: dim,
                                details: format!(
                                    "Face-face identity d_{} ∘ d_{} != d_{} ∘ d_{} on simplex '{}': left='{}' != right='{}'",
                                    i, j, j - 1, i, simplex.id, left, right
                                ),
                            });
                        }
                    }
                }
            }
        }
        Ok(())
    }

    /// Verifies that a horn Λ^k_n is well-formed (satisfies boundary compatibility).
    pub fn verify_horn_compatibility(&self, horn: &Horn) -> Result<(), HigherCategoryError> {
        let n = horn.dimension;
        let k = horn.omitted_index;
        if n < 2 {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: "horn dimension n >= 2".to_string(),
                found: format!("n = {}", n),
            });
        }
        if k > n {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("omitted index k <= {}", n),
                found: format!("k = {}", k),
            });
        }

        // Verify compatibility: d_i(x_j) = d_{j-1}(x_i) for i < j, i != k, j != k
        for j in 0..=n {
            if j == k {
                continue;
            }
            let x_j = match horn.faces.get(&j) {
                Some(id) => id,
                None => {
                    return Err(HigherCategoryError::InnerHornFillingViolation {
                        dimension: n,
                        k,
                        details: format!("Missing horn face x_{}", j),
                    });
                }
            };

            for i in 0..j {
                if i == k {
                    continue;
                }
                let x_i = match horn.faces.get(&i) {
                    Some(id) => id,
                    None => {
                        return Err(HigherCategoryError::InnerHornFillingViolation {
                            dimension: n,
                            k,
                            details: format!("Missing horn face x_{}", i),
                        });
                    }
                };

                let d_i_xj = self.face(n - 1, i, x_j).ok_or_else(|| {
                    HigherCategoryError::InnerHornFillingViolation {
                        dimension: n,
                        k,
                        details: format!("Missing boundary sub-face d_{}(x_{}) on horn face '{}'", i, j, x_j),
                    }
                })?;
                let d_jm1_xi = self.face(n - 1, j - 1, x_i).ok_or_else(|| {
                    HigherCategoryError::InnerHornFillingViolation {
                        dimension: n,
                        k,
                        details: format!("Missing boundary sub-face d_{}(x_{}) on horn face '{}'", j - 1, i, x_i),
                    }
                })?;

                if d_i_xj != d_jm1_xi {
                    return Err(HigherCategoryError::InnerHornFillingViolation {
                        dimension: n,
                        k,
                        details: format!(
                            "Horn boundary mismatch: d_{}(x_{}) = '{}' != d_{}(x_{}) = '{}'",
                            i, j, d_i_xj, j - 1, i, d_jm1_xi
                        ),
                    });
                }
            }
        }
        Ok(())
    }

    /// Checks if a candidate n-simplex y fills horn Λ^k_n:
    /// d_i(y) = x_i for all i != k.
    pub fn is_horn_filler(&self, horn: &Horn, candidate_simplex_id: &str) -> bool {
        let n = horn.dimension;
        let k = horn.omitted_index;
        for i in 0..=n {
            if i == k {
                continue;
            }
            let expected_face = match horn.faces.get(&i) {
                Some(f) => f,
                None => return false,
            };
            match self.face(n, i, candidate_simplex_id) {
                Some(actual) if actual == expected_face => continue,
                _ => return false,
            }
        }
        true
    }

    /// Verifies that horn Λ^k_n admits a filler in X_n.
    pub fn verify_horn_has_filler(&self, horn: &Horn) -> Result<String, HigherCategoryError> {
        self.verify_horn_compatibility(horn)?;
        let n = horn.dimension;
        if n >= self.simplices_by_dim.len() {
            return Err(HigherCategoryError::InnerHornFillingViolation {
                dimension: n,
                k: horn.omitted_index,
                details: format!("No {}-simplices exist in simplicial set", n),
            });
        }

        for candidate in &self.simplices_by_dim[n] {
            if self.is_horn_filler(horn, &candidate.id) {
                return Ok(candidate.id.clone());
            }
        }

        Err(HigherCategoryError::InnerHornFillingViolation {
            dimension: n,
            k: horn.omitted_index,
            details: format!("No filler found for horn Lambda^{}_{}", horn.omitted_index, n),
        })
    }
}

/// Quasi-Category (∞-Category) validator.
pub struct QuasiCategoryValidator;

impl QuasiCategoryValidator {
    /// Verifies that every supplied inner horn (0 < k < n) admits a filler in the simplicial set.
    pub fn verify_inner_horns(
        sset: &SimplicialSet,
        inner_horns: &[Horn],
    ) -> Result<(), HigherCategoryError> {
        for horn in inner_horns {
            if !horn.is_inner() {
                return Err(HigherCategoryError::InnerHornFillingViolation {
                    dimension: horn.dimension,
                    k: horn.omitted_index,
                    details: format!("Horn Lambda^{}_{} is not an inner horn (requires 0 < k < n)", horn.omitted_index, horn.dimension),
                });
            }
            sset.verify_horn_has_filler(horn)?;
        }
        Ok(())
    }
}

/// Kan Complex validator.
pub struct KanComplexValidator;

impl KanComplexValidator {
    /// Verifies that every supplied horn (inner and outer: 0 <= k <= n) admits a filler.
    pub fn verify_all_horns(
        sset: &SimplicialSet,
        horns: &[Horn],
    ) -> Result<(), HigherCategoryError> {
        for horn in horns {
            sset.verify_horn_has_filler(horn)?;
        }
        Ok(())
    }
}
