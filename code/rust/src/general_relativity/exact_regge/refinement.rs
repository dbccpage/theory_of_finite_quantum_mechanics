
#![forbid(unsafe_code)]

use super::manifold::ManifoldError;
use super::permute::lex_permutations_4;
use linear_algebra::regge_exact::{q_i64, signed_volume_4};
use num_rational::BigRational;
use num_traits::{Signed, Zero};

pub fn freudenthal_refine_16(
    parent: &[[BigRational; 4]; 5],
) -> Result<Vec<[[BigRational; 4]; 5]>, ManifoldError> {
    let parent_volume = signed_volume_4(parent).map_err(|_| degenerate_pentatope())?;
    if parent_volume.is_zero() {
        return Err(degenerate_pentatope());
    }
    let paths = reference_paths();
    if paths.len() != 16 {
        return Err(degenerate_pentatope());
    }
    let mut children = Vec::with_capacity(16);
    for path in paths {
        let child = [
            barycentric_image(parent, path[0]),
            barycentric_image(parent, path[1]),
            barycentric_image(parent, path[2]),
            barycentric_image(parent, path[3]),
            barycentric_image(parent, path[4]),
        ];
        children.push(orient_with_parent(&parent_volume, child)?);
    }
    Ok(children)
}

fn degenerate_pentatope() -> ManifoldError {
    ManifoldError::Degenerate {
        cell: "pentatope",
        index: 0,
    }
}

fn reference_paths() -> Vec<[[i64; 4]; 5]> {
    let permutations = lex_permutations_4([0, 1, 2, 3]);
    let mut paths = Vec::with_capacity(16);
    for x0 in 0_i64..=2 {
        for x1 in 0_i64..=2 {
            for x2 in 0_i64..=2 {
                for x3 in 0_i64..=2 {
                    let start = [x0, x1, x2, x3];
                    for permutation in &permutations {
                        if let Some(path) = admissible_path(start, permutation) {
                            paths.push(path);
                        }
                    }
                }
            }
        }
    }
    paths
}

fn admissible_path(start: [i64; 4], permutation: &[usize; 4]) -> Option<[[i64; 4]; 5]> {
    let mut current = start;
    let mut path = [start; 5];
    if !in_reference_simplex(current) {
        return None;
    }
    for step in 0..4 {
        current[permutation[step]] += 1;
        if !in_reference_simplex(current) {
            return None;
        }
        path[step + 1] = current;
    }
    Some(path)
}

fn in_reference_simplex(point: [i64; 4]) -> bool {
    point[3] >= 0
        && point[2] >= point[3]
        && point[1] >= point[2]
        && point[0] >= point[1]
        && point[0] <= 2
}

fn barycentric_image(parent: &[[BigRational; 4]; 5], point: [i64; 4]) -> [BigRational; 4] {
    let two = q_i64(2);
    let p = [
        q_i64(point[0]),
        q_i64(point[1]),
        q_i64(point[2]),
        q_i64(point[3]),
    ];
    let lambda = [
        q_i64(1) - (&p[0] / &two),
        (&p[0] - &p[1]) / &two,
        (&p[1] - &p[2]) / &two,
        (&p[2] - &p[3]) / &two,
        &p[3] / &two,
    ];
    std::array::from_fn(|coordinate| {
        let mut sum = q_i64(0);
        for vertex in 0..5 {
            sum += &lambda[vertex] * &parent[vertex][coordinate];
        }
        sum
    })
}

fn orient_with_parent(
    parent_volume: &BigRational,
    mut child: [[BigRational; 4]; 5],
) -> Result<[[BigRational; 4]; 5], ManifoldError> {
    let child_volume = signed_volume_4(&child).map_err(|_| degenerate_pentatope())?;
    if child_volume.is_zero() {
        return Err(degenerate_pentatope());
    }
    if (&child_volume * parent_volume).is_negative() {
        child.swap(0, 1);
    }
    Ok(child)
}
