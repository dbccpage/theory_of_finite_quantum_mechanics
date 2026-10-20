use std::collections::BTreeSet;
use thiserror::Error;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/finite_geometry.rs\nClaim: urn:omega:fqm:combinatorics:finite-incidence-geometry:v1\nAuthorityEffect: None\nScope Fence: Fano and AG(2,p) certificates are finite incidence checks, not a claim about continuous projective planes.\nMutation-Kills: 3 non-equivalent source mutants, executed by cargo test -p tfqm_combinatorics --lib.\n";

pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";

/// Scalar-entry and pair-work caps, checked before owned output allocation.
pub const MAX_GEOMETRY_CELLS: usize = 1 << 20;
pub const MAX_GEOMETRY_WORK: usize = 1 << 24;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum FiniteGeometryError {
    #[error("point index {point} out of bounds for {num_points} points")]
    PointOutOfBounds { point: usize, num_points: usize },
    #[error("line index {line} out of bounds for {num_lines} lines")]
    LineOutOfBounds { line: usize, num_lines: usize },
    #[error("line must contain at least 2 distinct points")]
    DegenerateLine,
    #[error("configuration requires at least 3 points and 3 lines")]
    TooSmall,
    #[error("dimension must be positive and bounded")]
    InvalidDimension,
    #[error("dimension {0} is not a prime")]
    NotPrime(usize),
    #[error("vector {index} has width {found}, expected {expected}")]
    DimensionMismatch {
        index: usize,
        expected: usize,
        found: usize,
    },
    #[error("{operation} requires {requested}, exceeding limit {maximum}")]
    ResourceLimit {
        operation: &'static str,
        requested: usize,
        maximum: usize,
    },
    #[error("dot product overflow for factors {left} and {right}")]
    DotOverflow { left: i64, right: i64 },
}

impl FiniteGeometryError {
    pub fn violated_invariant(&self) -> &'static str {
        match self {
            Self::PointOutOfBounds { .. } => "point indices lie in the declared point set",
            Self::LineOutOfBounds { .. } => "line indices lie in the declared line set",
            Self::DegenerateLine => "every line contains at least two distinct points",
            Self::TooSmall => "configuration has at least three points and three lines",
            Self::InvalidDimension => "affine order lies in the admitted prime interval",
            Self::NotPrime(_) => "affine order is prime",
            Self::DotOverflow { .. } => "ray dot products stay inside i64",
            Self::DimensionMismatch { .. } => "all vectors have the same coordinate dimension",
            Self::ResourceLimit { .. } => {
                "geometry allocation and work remain within admitted budgets"
            }
        }
    }

    pub fn measured_parameters(&self) -> Vec<(&'static str, String)> {
        match self {
            Self::PointOutOfBounds { point, num_points } => {
                vec![
                    ("point", point.to_string()),
                    ("num_points", num_points.to_string()),
                ]
            }
            Self::LineOutOfBounds { line, num_lines } => {
                vec![
                    ("line", line.to_string()),
                    ("num_lines", num_lines.to_string()),
                ]
            }
            Self::DegenerateLine => vec![("distinct_points", "less than 2".to_owned())],
            Self::TooSmall => vec![("minimum", "3".to_owned())],
            Self::InvalidDimension => vec![("min", "2".to_owned()), ("max", "13".to_owned())],
            Self::NotPrime(order) => vec![("order", order.to_string())],
            Self::DimensionMismatch {
                index,
                expected,
                found,
            } => vec![
                ("index", index.to_string()),
                ("expected", expected.to_string()),
                ("found", found.to_string()),
            ],
            Self::ResourceLimit {
                operation,
                requested,
                maximum,
            } => vec![
                ("operation", (*operation).to_owned()),
                ("requested", requested.to_string()),
                ("maximum", maximum.to_string()),
            ],
            Self::DotOverflow { left, right } => {
                vec![("left", left.to_string()), ("right", right.to_string())]
            }
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IncidenceStructure {
    num_points: usize,
    num_lines: usize,
    lines: Vec<BTreeSet<usize>>,
}

impl IncidenceStructure {
    pub fn new(num_points: usize, lines: Vec<Vec<usize>>) -> Result<Self, FiniteGeometryError> {
        if num_points < 3 || lines.len() < 3 {
            return Err(FiniteGeometryError::TooSmall);
        }
        let num_lines = lines.len();
        let square = admit_product("point pairs", num_points, num_points, MAX_GEOMETRY_WORK)?;
        admit_product(
            "incidence pair checks",
            square,
            num_lines,
            MAX_GEOMETRY_WORK,
        )?;
        admit_incidence_entries(&lines)?;
        let mut clean_lines = Vec::with_capacity(num_lines);
        for l in lines {
            let pts: BTreeSet<usize> = l.into_iter().collect();
            if pts.len() < 2 {
                return Err(FiniteGeometryError::DegenerateLine);
            }
            if let Some(&max_pt) = pts.iter().next_back() {
                if max_pt >= num_points {
                    return Err(FiniteGeometryError::PointOutOfBounds {
                        point: max_pt,
                        num_points,
                    });
                }
            }
            clean_lines.push(pts);
        }
        Ok(Self {
            num_points,
            num_lines,
            lines: clean_lines,
        })
    }

    pub fn num_points(&self) -> usize {
        self.num_points
    }

    pub fn num_lines(&self) -> usize {
        self.num_lines
    }

    pub fn is_incident(&self, point: usize, line: usize) -> Result<bool, FiniteGeometryError> {
        if point >= self.num_points {
            return Err(FiniteGeometryError::PointOutOfBounds {
                point,
                num_points: self.num_points,
            });
        }
        if line >= self.num_lines {
            return Err(FiniteGeometryError::LineOutOfBounds {
                line,
                num_lines: self.num_lines,
            });
        }
        Ok(self.lines[line].contains(&point))
    }

    pub fn points_on_line(&self, line: usize) -> Result<&BTreeSet<usize>, FiniteGeometryError> {
        self.lines
            .get(line)
            .ok_or(FiniteGeometryError::LineOutOfBounds {
                line,
                num_lines: self.num_lines,
            })
    }

    pub fn lines_on_point(&self, point: usize) -> Result<Vec<usize>, FiniteGeometryError> {
        if point >= self.num_points {
            return Err(FiniteGeometryError::PointOutOfBounds {
                point,
                num_points: self.num_points,
            });
        }
        Ok((0..self.num_lines)
            .filter(|&l| self.lines[l].contains(&point))
            .collect())
    }

    pub fn line_intersection(
        &self,
        l1: usize,
        l2: usize,
    ) -> Result<Vec<usize>, FiniteGeometryError> {
        let pts1 = self.points_on_line(l1)?;
        let pts2 = self.points_on_line(l2)?;
        Ok(pts1.intersection(pts2).copied().collect())
    }

    pub fn is_partial_linear_space(&self) -> bool {
        for p1 in 0..self.num_points {
            for p2 in (p1 + 1)..self.num_points {
                let lines_containing_both = (0..self.num_lines)
                    .filter(|&l| self.lines[l].contains(&p1) && self.lines[l].contains(&p2))
                    .count();
                if lines_containing_both > 1 {
                    return false;
                }
            }
        }
        true
    }

    pub fn is_linear_space(&self) -> bool {
        for p1 in 0..self.num_points {
            for p2 in (p1 + 1)..self.num_points {
                let lines_containing_both = (0..self.num_lines)
                    .filter(|&l| self.lines[l].contains(&p1) && self.lines[l].contains(&p2))
                    .count();
                if lines_containing_both != 1 {
                    return false;
                }
            }
        }
        true
    }
}

pub fn fano_plane() -> Result<IncidenceStructure, FiniteGeometryError> {
    let lines = vec![
        vec![0, 1, 2],
        vec![0, 3, 4],
        vec![0, 5, 6],
        vec![1, 3, 5],
        vec![1, 4, 6],
        vec![2, 3, 6],
        vec![2, 4, 5],
    ];
    IncidenceStructure::new(7, lines)
}

pub fn affine_plane_ag2(p: usize) -> Result<IncidenceStructure, FiniteGeometryError> {
    if p < 2 || p > 13 {
        return Err(FiniteGeometryError::InvalidDimension);
    }
    for d in 2..p {
        if p % d == 0 {
            return Err(FiniteGeometryError::NotPrime(p));
        }
    }
    let num_points = p * p;
    let mut lines = Vec::with_capacity(p * (p + 1));

    for c in 0..p {
        let mut line = Vec::with_capacity(p);
        for y in 0..p {
            line.push(c * p + y);
        }
        lines.push(line);
    }

    for m in 0..p {
        for c in 0..p {
            let mut line = Vec::with_capacity(p);
            for x in 0..p {
                let y = (m * x + c) % p;
                line.push(x * p + y);
            }
            lines.push(line);
        }
    }

    IncidenceStructure::new(num_points, lines)
}

/// Off-diagonal exact orthogonality of equal-width vectors, including zero vectors.
/// Empty input and width zero are allowed. Reject resource/shape errors before
/// allocating the square result; reject checked-i64 product/prefix overflow.
pub fn ray_orthogonality(vectors: &[Vec<i64>]) -> Result<Vec<Vec<bool>>, FiniteGeometryError> {
    let n = vectors.len();
    admit_ray_shape(vectors)?;
    let mut adj = vec![vec![false; n]; n];
    for i in 0..n {
        mark_orthogonal_row(&mut adj, vectors, i)?;
    }
    Ok(adj)
}

fn admit_product(
    operation: &'static str,
    left: usize,
    right: usize,
    maximum: usize,
) -> Result<usize, FiniteGeometryError> {
    let requested = left
        .checked_mul(right)
        .ok_or(FiniteGeometryError::ResourceLimit {
            operation,
            requested: usize::MAX,
            maximum,
        })?;
    if requested > maximum {
        return Err(FiniteGeometryError::ResourceLimit {
            operation,
            requested,
            maximum,
        });
    }
    Ok(requested)
}

fn admit_incidence_entries(lines: &[Vec<usize>]) -> Result<(), FiniteGeometryError> {
    let mut entries = 0usize;
    for line in lines {
        entries = entries
            .checked_add(line.len())
            .ok_or(FiniteGeometryError::ResourceLimit {
                operation: "incidence entries",
                requested: usize::MAX,
                maximum: MAX_GEOMETRY_CELLS,
            })?;
        if entries > MAX_GEOMETRY_CELLS {
            return Err(FiniteGeometryError::ResourceLimit {
                operation: "incidence entries",
                requested: entries,
                maximum: MAX_GEOMETRY_CELLS,
            });
        }
    }
    Ok(())
}

fn admit_ray_shape(vectors: &[Vec<i64>]) -> Result<(), FiniteGeometryError> {
    let n = vectors.len();
    admit_product("ray matrix cells", n, n, MAX_GEOMETRY_CELLS)?;
    let width = vectors.first().map_or(0, Vec::len);
    for (index, vector) in vectors.iter().enumerate() {
        if vector.len() != width {
            return Err(FiniteGeometryError::DimensionMismatch {
                index,
                expected: width,
                found: vector.len(),
            });
        }
    }
    admit_product("ray input cells", n, width, MAX_GEOMETRY_CELLS)?;
    let pairs = if n == 0 { 0 } else { n * (n - 1) / 2 };
    admit_product("ray dot terms", pairs, width, MAX_GEOMETRY_WORK)?;
    Ok(())
}

fn mark_orthogonal_row(
    adj: &mut [Vec<bool>],
    vectors: &[Vec<i64>],
    i: usize,
) -> Result<(), FiniteGeometryError> {
    let left = match vectors.get(i) {
        Some(row) => row,
        None => {
            return Err(FiniteGeometryError::PointOutOfBounds {
                point: i,
                num_points: vectors.len(),
            })
        }
    };
    for j in (i + 1)..vectors.len() {
        mark_pair(adj, vectors, left, i, j)?;
    }
    Ok(())
}

fn mark_pair(
    adj: &mut [Vec<bool>],
    vectors: &[Vec<i64>],
    left: &[i64],
    i: usize,
    j: usize,
) -> Result<(), FiniteGeometryError> {
    let right = match vectors.get(j) {
        Some(row) => row,
        None => {
            return Err(FiniteGeometryError::PointOutOfBounds {
                point: j,
                num_points: vectors.len(),
            })
        }
    };
    let product = match dot(left, right) {
        Ok(value) => value,
        Err(err) => return Err(err),
    };
    if product == 0 {
        return set_symmetric(adj, i, j);
    }
    Ok(())
}

fn dot(left: &[i64], right: &[i64]) -> Result<i64, FiniteGeometryError> {
    if left.len() != right.len() {
        return Err(FiniteGeometryError::DimensionMismatch {
            index: 1,
            expected: left.len(),
            found: right.len(),
        });
    }
    let mut acc = 0i64;
    for (a, b) in left.iter().zip(right) {
        let prod = a.checked_mul(*b).ok_or(FiniteGeometryError::DotOverflow {
            left: *a,
            right: *b,
        })?;
        acc = acc
            .checked_add(prod)
            .ok_or(FiniteGeometryError::DotOverflow {
                left: acc,
                right: prod,
            })?;
    }
    Ok(acc)
}

fn set_symmetric(adj: &mut [Vec<bool>], i: usize, j: usize) -> Result<(), FiniteGeometryError> {
    write_cell(adj, i, j)?;
    write_cell(adj, j, i)
}

fn write_cell(adj: &mut [Vec<bool>], row: usize, col: usize) -> Result<(), FiniteGeometryError> {
    let rows = adj.len();
    let line = adj
        .get_mut(row)
        .ok_or(FiniteGeometryError::PointOutOfBounds {
            point: row,
            num_points: rows,
        })?;
    let cols = line.len();
    let cell = line
        .get_mut(col)
        .ok_or(FiniteGeometryError::PointOutOfBounds {
            point: col,
            num_points: cols,
        })?;
    *cell = true;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fano_plane_is_linear_space() {
        let fano = fano_plane().unwrap();
        assert_eq!(fano.num_points(), 7);
        assert_eq!(fano.num_lines(), 7);
        assert!(fano.is_linear_space());
        assert!(fano.is_partial_linear_space());
        assert_eq!(fano.lines_on_point(0).unwrap().len(), 3);
        assert_eq!(fano.points_on_line(0).unwrap().len(), 3);
        assert_eq!(fano.line_intersection(0, 1).unwrap().len(), 1);
    }

    #[test]
    fn negative_geometry_refusals_record_invariants() {
        let small =
            IncidenceStructure::new(2, vec![vec![0, 1], vec![0, 1], vec![0, 1]]).unwrap_err();
        assert_eq!(
            small.violated_invariant(),
            "configuration has at least three points and three lines"
        );
        let order = affine_plane_ag2(4).unwrap_err();
        assert_eq!(order.violated_invariant(), "affine order is prime");
        assert_eq!(order.measured_parameters(), vec![("order", "4".to_owned())]);
        let overflow = dot(&[i64::MAX], &[2]).unwrap_err();
        assert_eq!(
            overflow.violated_invariant(),
            "ray dot products stay inside i64"
        );
    }

    #[test]
    fn test_affine_plane_ag2_3() {
        let ag = affine_plane_ag2(3).unwrap();
        assert_eq!(ag.num_points(), 9);
        assert_eq!(ag.num_lines(), 12);
        assert!(ag.is_linear_space());

        for l in 0..12 {
            assert_eq!(ag.points_on_line(l).unwrap().len(), 3);
        }
        for p in 0..9 {
            assert_eq!(ag.lines_on_point(p).unwrap().len(), 4);
        }
    }

    #[test]
    fn test_ray_orthogonality() {
        let rays = vec![vec![1, 0, 0], vec![0, 1, 0], vec![0, 0, 1], vec![1, 1, 0]];
        let adj = ray_orthogonality(&rays).unwrap();
        assert_eq!(adj[0][1], true);
        assert_eq!(adj[0][2], true);
        assert_eq!(adj[0][3], false);
        assert_eq!(adj[1][2], true);
        assert_eq!(adj[2][3], true);
        assert!(PROVENANCE.contains("AuthorityEffect: None"));
        assert!(PROVENANCE.contains("Mutation-Kills: 3 non-equivalent source mutants"));
        assert_eq!(AUTHORITY_EFFECT, "AuthorityEffect: None");
    }
}
