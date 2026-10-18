//! Fixtures: one orthogonal pentatope, and the Kuhn triangulation of the
//! boundary of the 5-cube (a closed combinatorial 4-sphere) with a `Q^4` chart
//! on every facet.
//!
//! Charts are piecewise-flat and rational. The construction does not evaluate
//! the Einstein-Hilbert action of the round metric. The Euler characteristic
//! of this closed combinatorial 4-sphere is computed elsewhere.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use super::manifold::{ManifoldError, PentatopeChart, SimplicialManifold4D};
use super::permute::lex_permutations_4;
use linear_algebra::regge_exact::q_i64;
use num_rational::BigRational;

/// Orthogonal corner pentatope on
/// `(0,0,0,0), (1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)`.
pub fn orthogonal_pentatope() -> Result<SimplicialManifold4D, ManifoldError> {
    let pentatope = [
        rational_point([0, 0, 0, 0]),
        rational_point([1, 0, 0, 0]),
        rational_point([0, 1, 0, 0]),
        rational_point([0, 0, 1, 0]),
        rational_point([0, 0, 0, 1]),
    ];
    SimplicialManifold4D::from_ambient_pentatopes(&[pentatope])
}

/// Combinatorial boundary of the 5-cube `{0,1}^5`.
///
/// Each of the 10 facets is Kuhn-triangulated into `4! = 24` pentatopes:
/// 32 global vertices and 240 pentatopes. The id of a point is `Σ point[i] << i`
/// and stays in `0..=31`; vertices are not renumbered.
///
/// Chart slot `j` is the value of the `j`-th free axis in ascending index order,
/// not the order of the permutation. Values are `0` or `1`.
///
/// Charts are piecewise-flat and rational. This construction does not evaluate
/// the Einstein-Hilbert action of the round metric.
pub fn closed_s4_cube_boundary() -> Result<SimplicialManifold4D, ManifoldError> {
    let mut charts = Vec::with_capacity(240);
    for axis in 0..5 {
        let free = free_axes(axis);
        for bit in [0_u32, 1_u32] {
            for permutation in lex_permutations_4(free) {
                charts.push(kuhn_chart(axis, bit, &free, &permutation));
            }
        }
    }
    SimplicialManifold4D::from_charts(charts)
}

fn rational_point(coords: [i64; 4]) -> [BigRational; 4] {
    std::array::from_fn(|coordinate| q_i64(coords[coordinate]))
}

fn free_axes(frozen: usize) -> [usize; 4] {
    let mut free = [0; 4];
    let mut slot = 0;
    for coordinate in 0..5 {
        if coordinate != frozen {
            free[slot] = coordinate;
            slot += 1;
        }
    }
    free
}

fn kuhn_chart(
    axis: usize,
    bit: u32,
    free: &[usize; 4],
    permutation: &[usize; 4],
) -> PentatopeChart {
    let mut point = [0_u32; 5];
    point[axis] = bit;
    let mut vertices = [0_u32; 5];
    let mut coords: [[BigRational; 4]; 5] =
        std::array::from_fn(|_| std::array::from_fn(|_| q_i64(0)));
    vertices[0] = cube5_vertex_id(&point);
    coords[0] = chart_coords(&point, free);
    for step in 0..4 {
        point[permutation[step]] = 1;
        vertices[step + 1] = cube5_vertex_id(&point);
        coords[step + 1] = chart_coords(&point, free);
    }
    PentatopeChart { vertices, coords }
}

fn cube5_vertex_id(point: &[u32; 5]) -> u32 {
    point[0] + (point[1] << 1) + (point[2] << 2) + (point[3] << 3) + (point[4] << 4)
}

fn chart_coords(point: &[u32; 5], free: &[usize; 4]) -> [BigRational; 4] {
    std::array::from_fn(|slot| q_i64(i64::from(point[free[slot]])))
}
