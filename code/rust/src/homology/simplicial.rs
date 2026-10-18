
use crate::errors::HomologicalError;
use crate::linear_algebra::scalars::{q, Q};
use crate::linear_algebra::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::ExactRowReduction;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub struct Simplex {
    vertices: Vec<usize>,
}

impl Simplex {
    pub fn new(vertices: Vec<usize>) -> Result<Self, HomologicalError> {
        validate_strict_vertices(&vertices)?;
        Ok(Self { vertices })
    }

    pub fn from_unordered(vertices: Vec<usize>) -> Result<Self, HomologicalError> {
        let canonical = canonicalize_vertices(vertices)?;
        Ok(Self {
            vertices: canonical,
        })
    }

    pub fn dimension(&self) -> usize {
        self.vertices.len() - 1
    }

    pub fn vertices(&self) -> &[usize] {
        &self.vertices
    }

    pub fn num_vertices(&self) -> usize {
        self.vertices.len()
    }

    pub fn face(&self, removed_index: usize) -> Result<(Self, i8), HomologicalError> {
        if removed_index >= self.vertices.len() {
            return Err(HomologicalError::InvalidDegree(removed_index as i32));
        }
        if self.vertices.len() == 1 {
            return Err(HomologicalError::InvalidDegree(0));
        }

        let mut vertices = self.vertices.clone();
        vertices.remove(removed_index);
        let sign = if removed_index.is_multiple_of(2) {
            1
        } else {
            -1
        };
        Ok((Self { vertices }, sign))
    }

    pub fn faces(&self) -> Vec<(Self, i8)> {
        if self.vertices.len() <= 1 {
            return Vec::new();
        }

        (0..self.vertices.len())
            .map(|i| {
                let mut vertices = self.vertices.clone();
                vertices.remove(i);
                let sign = if i % 2 == 0 { 1 } else { -1 };
                (Self { vertices }, sign)
            })
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub struct OrientedSimplex {
    simplex: Simplex,
    orientation: i8,
}

impl OrientedSimplex {
    pub fn new(vertices: Vec<usize>) -> Result<Self, HomologicalError> {
        Ok(Self {
            simplex: Simplex::new(vertices)?,
            orientation: 1,
        })
    }

    pub fn from_ordered(vertices: Vec<usize>) -> Result<Self, HomologicalError> {
        let orientation = permutation_orientation(&vertices)?;
        Ok(Self {
            simplex: Simplex::from_unordered(vertices)?,
            orientation,
        })
    }

    pub fn from_unordered(vertices: Vec<usize>) -> Result<Self, HomologicalError> {
        Ok(Self {
            simplex: Simplex::from_unordered(vertices)?,
            orientation: 1,
        })
    }

    pub fn simplex(&self) -> &Simplex {
        &self.simplex
    }

    pub fn orientation(&self) -> i8 {
        self.orientation
    }

    pub fn dimension(&self) -> usize {
        self.simplex.dimension()
    }

    pub fn vertices(&self) -> &[usize] {
        self.simplex.vertices()
    }

    pub fn num_vertices(&self) -> usize {
        self.simplex.num_vertices()
    }

    pub fn faces(&self) -> Vec<(OrientedSimplex, i8)> {
        self.simplex
            .faces()
            .into_iter()
            .map(|(face, sign)| {
                (
                    OrientedSimplex {
                        simplex: face,
                        orientation: 1,
                    },
                    sign * self.orientation,
                )
            })
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SimplicialComplex {
    simplices_by_dim: Vec<Vec<Simplex>>,
    indices_by_dim: Vec<BTreeMap<Simplex, usize>>,
    num_vertices: usize,
}

impl SimplicialComplex {
    pub fn from_maximal_simplices(maximal: Vec<OrientedSimplex>) -> Result<Self, HomologicalError> {
        Self::from_canonical_simplices(maximal.into_iter().map(|s| s.simplex).collect())
    }

    pub fn from_simplices(simplices: Vec<Simplex>) -> Result<Self, HomologicalError> {
        Self::from_canonical_simplices(simplices)
    }

    pub fn standard_n_simplex(n: usize) -> Result<Self, HomologicalError> {
        Self::from_simplices(vec![Simplex::new((0..=n).collect())?])
    }

    fn from_canonical_simplices(simplices: Vec<Simplex>) -> Result<Self, HomologicalError> {
        let mut all: BTreeSet<Simplex> = BTreeSet::new();
        let mut stack = simplices;

        while let Some(simplex) = stack.pop() {
            if all.insert(simplex.clone()) {
                for (face, _) in simplex.faces() {
                    stack.push(face);
                }
            }
        }

        let max_dim = all.iter().map(Simplex::dimension).max().unwrap_or(0);
        let mut simplices_by_dim = vec![Vec::new(); max_dim + 1];
        let mut max_vertex = None::<usize>;

        for simplex in all {
            if let Some(&v) = simplex.vertices().last() {
                max_vertex = Some(max_vertex.map_or(v, |m| m.max(v)));
            }
            simplices_by_dim[simplex.dimension()].push(simplex);
        }

        let indices_by_dim = simplices_by_dim
            .iter()
            .map(|simplices| {
                simplices
                    .iter()
                    .cloned()
                    .enumerate()
                    .map(|(index, simplex)| (simplex, index))
                    .collect()
            })
            .collect();

        Ok(Self {
            simplices_by_dim,
            indices_by_dim,
            num_vertices: max_vertex.map_or(0, |v| v + 1),
        })
    }

    pub fn max_dimension(&self) -> usize {
        self.simplices_by_dim.len().saturating_sub(1)
    }

    pub fn simplices(&self, dim: usize) -> &[Simplex] {
        self.simplices_by_dim
            .get(dim)
            .map(Vec::as_slice)
            .unwrap_or(&[])
    }

    pub fn simplices_by_dim(&self) -> &[Vec<Simplex>] {
        &self.simplices_by_dim
    }

    pub fn count(&self, dim: usize) -> usize {
        self.simplices(dim).len()
    }

    pub fn num_vertices(&self) -> usize {
        self.num_vertices
    }

    pub fn total_simplices(&self) -> usize {
        self.simplices_by_dim.iter().map(Vec::len).sum()
    }

    pub fn contains(&self, simplex: &Simplex) -> bool {
        self.indices_by_dim
            .get(simplex.dimension())
            .is_some_and(|indices| indices.contains_key(simplex))
    }

    pub fn euler_characteristic(&self) -> i64 {
        self.simplices_by_dim
            .iter()
            .enumerate()
            .map(|(k, simplices)| {
                if k % 2 == 0 {
                    simplices.len() as i64
                } else {
                    -(simplices.len() as i64)
                }
            })
            .sum()
    }

    pub fn boundary_matrix(&self, k: usize) -> Result<BasicMatrix<Q>, HomologicalError> {
        if k == 0 {
            return BasicMatrix::zero(0, self.count(0)).map_err(HomologicalError::MatrixError);
        }

        let rows = self.count(k - 1);
        let cols = self.count(k);
        if cols == 0 {
            return BasicMatrix::zero(rows, 0).map_err(HomologicalError::MatrixError);
        }

        let face_indices = self
            .indices_by_dim
            .get(k - 1)
            .ok_or(HomologicalError::InvalidDegree(k as i32))?;
        let mut matrix = BasicMatrix::<Q>::zero(rows, cols)?;

        for (col, simplex) in self.simplices(k).iter().enumerate() {
            for (face, sign) in simplex.faces() {
                let row = face_indices.get(&face).ok_or_else(|| {
                    HomologicalError::UnsupportedOperation(format!(
                        "simplicial closure missing face {:?}",
                        face.vertices()
                    ))
                })?;
                matrix.set(*row, col, q(sign as i64))?;
            }
        }

        Ok(matrix)
    }

    pub fn coboundary_matrix(&self, k: usize) -> Result<BasicMatrix<Q>, HomologicalError> {
        let boundary = self.boundary_matrix(k + 1)?;
        let mut matrix = BasicMatrix::<Q>::zero(boundary.cols(), boundary.rows())?;

        for row in 0..boundary.rows() {
            for col in 0..boundary.cols() {
                matrix.set(col, row, boundary.get(row, col)?)?;
            }
        }

        Ok(matrix)
    }

    pub fn boundary_composition(&self, k: usize) -> Result<BasicMatrix<Q>, HomologicalError> {
        if k < 2 {
            return Err(HomologicalError::InvalidDegree(k as i32));
        }
        let lower = self.boundary_matrix(k - 1)?;
        let upper = self.boundary_matrix(k)?;
        lower.mul(&upper).map_err(HomologicalError::MatrixError)
    }

    pub fn verify_boundary_law_at(&self, k: usize) -> Result<bool, HomologicalError> {
        let composed = self.boundary_composition(k)?;
        let is_zero = composed.as_slice().iter().all(|x| *x == q(0));
        if is_zero {
            Ok(true)
        } else {
            Err(HomologicalError::BoundaryLawViolation {
                degree: (k - 1) as i32,
            })
        }
    }

    pub fn verify_boundary_law(&self) -> Result<bool, HomologicalError> {
        let max_dim = self.max_dimension();
        if max_dim < 2 {
            return Ok(true);
        }
        for k in 2..=max_dim {
            self.verify_boundary_law_at(k)?;
        }
        Ok(true)
    }

    pub fn coboundary_composition(&self, k: usize) -> Result<BasicMatrix<Q>, HomologicalError> {
        if k < 1 {
            return Err(HomologicalError::InvalidDegree(k as i32));
        }
        let lower = self.coboundary_matrix(k - 1)?;
        let upper = self.coboundary_matrix(k)?;
        upper.mul(&lower).map_err(HomologicalError::MatrixError)
    }

    pub fn verify_coboundary_law_at(&self, k: usize) -> Result<bool, HomologicalError> {
        let composed = self.coboundary_composition(k)?;
        let is_zero = composed.as_slice().iter().all(|x| *x == q(0));
        if is_zero {
            Ok(true)
        } else {
            Err(HomologicalError::CoboundaryLawViolation { degree: k as i32 })
        }
    }

    pub fn verify_coboundary_law(&self) -> Result<bool, HomologicalError> {
        let max_dim = self.max_dimension();
        if max_dim < 2 {
            return Ok(true);
        }
        for k in 1..max_dim {
            self.verify_coboundary_law_at(k)?;
        }
        Ok(true)
    }

    pub fn rational_betti_numbers(&self) -> Result<Vec<usize>, HomologicalError> {
        let max_dim = self.max_dimension();
        let rank = |k: usize| -> Result<usize, HomologicalError> {
            self.boundary_matrix(k)?
                .rank()
                .map_err(|e| HomologicalError::UnsupportedOperation(format!("{}", e)))
        };
        let mut betti = Vec::with_capacity(max_dim + 1);

        for k in 0..=max_dim {
            let ck_dim = self.count(k);
            if ck_dim == 0 {
                betti.push(0);
                continue;
            }

            let rank_dk = if k == 0 { 0 } else { rank(k)? };
            let ker_dk =
                ck_dim
                    .checked_sub(rank_dk)
                    .ok_or(HomologicalError::BettiRankInconsistency {
                        dimension: ck_dim,
                        rank_sum: rank_dk,
                        degree: k,
                    })?;

            let rank_dk_plus_1 = if k == max_dim { 0 } else { rank(k + 1)? };
            let bk = ker_dk.checked_sub(rank_dk_plus_1).ok_or(
                HomologicalError::BettiRankInconsistency {
                    dimension: ker_dk,
                    rank_sum: rank_dk_plus_1,
                    degree: k,
                },
            )?;

            betti.push(bk);
        }

        Ok(betti)
    }
}

fn validate_strict_vertices(vertices: &[usize]) -> Result<(), HomologicalError> {
    if vertices.is_empty() {
        return Err(HomologicalError::EmptyBasis);
    }

    for index in 1..vertices.len() {
        if vertices[index] <= vertices[index - 1] {
            return Err(HomologicalError::BasisMismatch {
                description: format!(
                    "simplex vertices must be strictly ascending; violation at index {}",
                    index
                ),
            });
        }
    }

    Ok(())
}

fn canonicalize_vertices(mut vertices: Vec<usize>) -> Result<Vec<usize>, HomologicalError> {
    if vertices.is_empty() {
        return Err(HomologicalError::EmptyBasis);
    }

    vertices.sort_unstable();
    for index in 1..vertices.len() {
        if vertices[index] == vertices[index - 1] {
            return Err(HomologicalError::BasisMismatch {
                description: "simplex vertices must be distinct".to_string(),
            });
        }
    }

    Ok(vertices)
}

fn permutation_orientation(vertices: &[usize]) -> Result<i8, HomologicalError> {
    if vertices.is_empty() {
        return Err(HomologicalError::EmptyBasis);
    }

    let mut seen = BTreeSet::new();
    for vertex in vertices {
        if !seen.insert(*vertex) {
            return Err(HomologicalError::BasisMismatch {
                description: "oriented simplex vertices must be distinct".to_string(),
            });
        }
    }

    let inversions = vertices
        .iter()
        .enumerate()
        .map(|(i, left)| {
            vertices
                .iter()
                .skip(i + 1)
                .filter(|right| left > *right)
                .count()
        })
        .sum::<usize>();

    Ok(if inversions % 2 == 0 { 1 } else { -1 })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn standard_n_simplex_has_all_dimensions() {
        let complex = SimplicialComplex::standard_n_simplex(4).unwrap();

        assert_eq!(complex.count(0), 5);
        assert_eq!(complex.count(1), 10);
        assert_eq!(complex.count(2), 10);
        assert_eq!(complex.count(3), 5);
        assert_eq!(complex.count(4), 1);
        assert_eq!(complex.total_simplices(), 31);
        assert_eq!(complex.euler_characteristic(), 1);
    }

    #[test]
    fn rational_betti_numbers_of_circle_disk_and_sphere() {
        let edge = |a, b| Simplex::from_unordered(vec![a, b]).unwrap();
        let hollow =
            SimplicialComplex::from_simplices(vec![edge(0, 1), edge(1, 2), edge(0, 2)]).unwrap();
        assert_eq!(hollow.rational_betti_numbers().unwrap(), vec![1, 1]);

        let disk = SimplicialComplex::standard_n_simplex(2).unwrap();
        assert_eq!(disk.rational_betti_numbers().unwrap(), vec![1, 0, 0]);

        let sphere = SimplicialComplex::from_simplices(
            [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
                .into_iter()
                .map(|face| Simplex::from_unordered(face.to_vec()).unwrap())
                .collect(),
        )
        .unwrap();
        assert_eq!(sphere.rational_betti_numbers().unwrap(), vec![1, 0, 1]);

        let ball = SimplicialComplex::standard_n_simplex(4).unwrap();
        assert_eq!(ball.rational_betti_numbers().unwrap(), vec![1, 0, 0, 0, 0]);
    }

    #[test]
    fn closes_under_faces_for_tetrahedron() {
        let tetrahedron = OrientedSimplex::new(vec![0, 1, 2, 3]).unwrap();
        let complex = SimplicialComplex::from_maximal_simplices(vec![tetrahedron]).unwrap();

        assert_eq!(complex.count(0), 4);
        assert_eq!(complex.count(1), 6);
        assert_eq!(complex.count(2), 4);
        assert_eq!(complex.count(3), 1);
    }

    #[test]
    fn oriented_simplex_tracks_parity() {
        let positive = OrientedSimplex::from_ordered(vec![0, 1, 2]).unwrap();
        let negative = OrientedSimplex::from_ordered(vec![1, 0, 2]).unwrap();

        assert_eq!(positive.vertices(), &[0, 1, 2]);
        assert_eq!(positive.orientation(), 1);
        assert_eq!(negative.vertices(), &[0, 1, 2]);
        assert_eq!(negative.orientation(), -1);
    }

    #[test]
    fn boundary_matrix_1_for_edge() {
        let complex = SimplicialComplex::standard_n_simplex(1).unwrap();
        let d1 = complex.boundary_matrix(1).unwrap();

        assert_eq!(d1.rows(), 2);
        assert_eq!(d1.cols(), 1);
        assert_eq!(d1.get(0, 0).unwrap(), q(-1));
        assert_eq!(d1.get(1, 0).unwrap(), q(1));
    }

    #[test]
    fn boundary_matrix_2_for_triangle() {
        let complex = SimplicialComplex::standard_n_simplex(2).unwrap();
        let d2 = complex.boundary_matrix(2).unwrap();

        assert_eq!(d2.rows(), 3);
        assert_eq!(d2.cols(), 1);
        assert_eq!(d2.get(0, 0).unwrap(), q(1));
        assert_eq!(d2.get(1, 0).unwrap(), q(-1));
        assert_eq!(d2.get(2, 0).unwrap(), q(1));
    }

    #[test]
    fn boundary_squared_is_zero_for_4_simplex() {
        let complex = SimplicialComplex::standard_n_simplex(4).unwrap();

        for k in 2..=4 {
            let lower = complex.boundary_matrix(k - 1).unwrap();
            let upper = complex.boundary_matrix(k).unwrap();
            let composed = lower.mul(&upper).unwrap();
            for row in 0..composed.rows() {
                for col in 0..composed.cols() {
                    assert_eq!(composed.get(row, col).unwrap(), q(0));
                }
            }
        }
    }

    #[test]
    fn rejects_degenerate_simplex() {
        let result = Simplex::from_unordered(vec![0, 1, 1]);
        assert!(matches!(
            result,
            Err(HomologicalError::BasisMismatch { .. })
        ));
    }

    #[test]
    fn boundary_and_coboundary_composition_multi_dimension() {
        let complex = SimplicialComplex::standard_n_simplex(5).unwrap();
        assert_eq!(complex.max_dimension(), 5);

        for k in 2..=5 {
            let composed = complex.boundary_composition(k).unwrap();
            let rows = complex.count(k - 2);
            let cols = complex.count(k);
            assert_eq!(composed.rows(), rows);
            assert_eq!(composed.cols(), cols);
            assert!(complex.verify_boundary_law_at(k).unwrap());
        }

        assert!(complex.verify_boundary_law().unwrap());

        assert!(complex.verify_coboundary_law().unwrap());
    }

    #[test]
    fn boundary_composition_invalid_degree() {
        let complex = SimplicialComplex::standard_n_simplex(3).unwrap();
        assert!(matches!(
            complex.boundary_composition(0),
            Err(HomologicalError::InvalidDegree(0))
        ));
        assert!(matches!(
            complex.boundary_composition(1),
            Err(HomologicalError::InvalidDegree(1))
        ));
    }
}
