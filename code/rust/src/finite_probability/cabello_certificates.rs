use linear_algebra::backend::basic_matrix::BasicMatrix;
use super::frame_polytope::{
    eigenvalues_above, eigenvalues_at_least, FramePolytopeError, FrameSystem,
};
use super::pfp_exact::{self as mx, Matrix};
use num_bigint::BigInt;
use num_integer::Integer;
use num_rational::BigRational as Q;
use num_traits::{One, Signed, Zero};
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VertexCertificate {
    pub weights: Vec<Q>,
    pub representative: Matrix,
    pub negative_vector: [i64; 4],
    pub quadratic_value: Q,
    pub spectral_class: &'static str,
    pub half_shift_determinant: Q,
    pub quarter_shift_leading_minors: Vec<Q>,
    pub denominator: BigInt,
    pub matrix_numerators: Vec<BigInt>,
    pub weights_twice: Vec<BigInt>,
    pub negative_value_numerator: BigInt,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Census {
    pub basis_supports_examined: usize,
    pub incidence_rank: usize,
    pub projector_span_rank: usize,
    pub vertices: Vec<VertexCertificate>,
    pub at_minus_half: usize,
    pub above_minus_quarter: usize,
}
fn q(n: i64, d: i64) -> Q {
    Q::new(n.into(), d.into())
}
pub fn quadratic(a: &Matrix, v: &[i64; 4]) -> Q {
    (0..4)
        .flat_map(|i| {
            (0..4).map(move |j| {
                Q::from_integer(v[i].into()) * &a[i][j] * Q::from_integer(v[j].into())
            })
        })
        .sum()
}
fn shift(a: &Matrix, t: &Q) -> Matrix {
    a.iter()
        .enumerate()
        .map(|(i, r)| {
            r.iter()
                .enumerate()
                .map(|(j, x)| if i == j { x + t } else { x.clone() })
                .collect()
        })
        .collect()
}

fn find_witness_at_radius(rho: &Matrix, r: i64) -> Option<([i64; 4], Q)> {
    let side = 2 * r + 1;
    let total = side * side * side * side;
    for idx in 0..total {
        let mut rem = idx;
        let d = (rem % side) - r;
        rem /= side;
        let c = (rem % side) - r;
        rem /= side;
        let b = (rem % side) - r;
        rem /= side;
        let a = rem - r;
        let v = [a, b, c, d];
        let value = quadratic(rho, &v);
        if value.is_negative() {
            return Some((v, value));
        }
    }
    None
}

fn find_negative_witness(rho: &Matrix, radius: i64) -> Option<([i64; 4], Q)> {
    for r in 1..=radius {
        if let Some(res) = find_witness_at_radius(rho, r) {
            return Some(res);
        }
    }
    None
}

fn compute_spectral_class(
    basic: &BasicMatrix<Q>,
    rho: &Matrix,
) -> Result<(&'static str, Q, Vec<Q>), FramePolytopeError> {
    let half = shift(rho, &q(1, 2));
    let quarter = shift(rho, &q(1, 4));
    let half_det = mx::determinant(&half).map_err(|_| FramePolytopeError::InvalidSolution)?;
    let leading: Vec<Q> = (1..=4)
        .map(|k| {
            mx::determinant(&quarter[..k].iter().map(|r| r[..k].to_vec()).collect())
                .map_err(|_| FramePolytopeError::InvalidSolution)
        })
        .collect::<Result<_, _>>()?;
    let spectral_class = if eigenvalues_at_least(basic, &q(-1, 2))? && half_det.is_zero() {
        "at_minus_half"
    } else if eigenvalues_above(basic, &q(-1, 4))? {
        "above_minus_quarter"
    } else {
        return Err(FramePolytopeError::InvalidSolution);
    };
    Ok((spectral_class, half_det, leading))
}

fn build_vertex_certificate(
    weights: Vec<Q>,
    rho: Matrix,
    negative_vector: [i64; 4],
    quadratic_value: Q,
    spectral_class: &'static str,
    half_shift_determinant: Q,
    quarter_shift_leading_minors: Vec<Q>,
) -> Result<VertexCertificate, FramePolytopeError> {
    let denominator = rho
        .iter()
        .flatten()
        .fold(BigInt::one(), |d, x| d.lcm(x.denom()));
    let scaled: Vec<Q> = rho
        .iter()
        .flatten()
        .map(|x| x * Q::from_integer(denominator.clone()))
        .collect();
    let twice: Vec<Q> = weights.iter().map(|x| x * q(2, 1)).collect();
    let neg = &quadratic_value * Q::from_integer(denominator.clone());
    if scaled.iter().chain(&twice).any(|x| !x.denom().is_one()) || !neg.denom().is_one() {
        return Err(FramePolytopeError::InvalidSolution);
    }
    Ok(VertexCertificate {
        weights,
        representative: rho,
        negative_vector,
        quadratic_value,
        spectral_class,
        half_shift_determinant,
        quarter_shift_leading_minors,
        denominator,
        matrix_numerators: scaled.iter().map(|x| x.numer().clone()).collect(),
        weights_twice: twice.iter().map(|x| x.numer().clone()).collect(),
        negative_value_numerator: neg.numer().clone(),
    })
}

fn certify_vertex(
    system: &FrameSystem,
    weights: Vec<Q>,
    radius: i64,
) -> Result<VertexCertificate, FramePolytopeError> {
    if !system.is_vertex(&weights)? {
        return Err(FramePolytopeError::InvalidSolution);
    }
    let basic = system.state_of(&weights)?;
    let rho: Matrix = (0..4)
        .map(|i| {
            (0..4)
                .map(|j| basic.as_slice()[4 * i + j].clone())
                .collect()
        })
        .collect();
    let (spectral_class, half_det, leading) = compute_spectral_class(&basic, &rho)?;
    let (negative_vector, quadratic_value) = find_negative_witness(&rho, radius)
        .ok_or(FramePolytopeError::InvalidSolution)?;
    build_vertex_certificate(
        weights,
        rho,
        negative_vector,
        quadratic_value,
        spectral_class,
        half_det,
        leading,
    )
}

fn validate_system_and_radius(dim: usize, radius: i64) -> Result<(), FramePolytopeError> {
    if dim != 4 || !(1..=8).contains(&radius) {
        return Err(FramePolytopeError::CarrierBudget);
    }
    Ok(())
}

pub fn certify(
    rays: Vec<Vec<i64>>,
    frames: Vec<Vec<usize>>,
    budget: usize,
    radius: i64,
) -> Result<Census, FramePolytopeError> {
    let system = FrameSystem::new(rays, frames)?;
    validate_system_and_radius(system.dimension(), radius)?;
    let (points, examined) = system.vertices_with_statistics(budget)?;
    let mut vertices = Vec::new();
    let mut at_half = 0;
    let mut above_quarter = 0;
    for weights in points {
        let cert = certify_vertex(&system, weights, radius)?;
        match cert.spectral_class {
            "at_minus_half" => at_half += 1,
            "above_minus_quarter" => above_quarter += 1,
            _ => {}
        }
        vertices.push(cert);
    }
    Ok(Census {
        basis_supports_examined: examined,
        incidence_rank: system.incidence_rank()?,
        projector_span_rank: system.projector_span_rank()?,
        vertices,
        at_minus_half: at_half,
        above_minus_quarter: above_quarter,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    fn small() -> (Vec<Vec<i64>>, Vec<Vec<usize>>) {
        (vec![vec![1, 0], vec![0, 1]], vec![vec![0, 1]])
    }
    #[test]
    fn invalid_frame_and_degree_are_refused() {
        let (r, f) = small();
        let s = FrameSystem::new(r.clone(), f).unwrap();
        assert!(s.vertices_with_statistics(100).is_err());
        assert!(FrameSystem::new(r, vec![vec![0, 0]]).is_err());
    }
    #[test]
    fn exact_negative_quadratic_is_not_inferred_from_diagonals() {
        let a = vec![
            vec![q(1, 1), q(2, 1), q(0, 1), q(0, 1)],
            vec![q(2, 1), q(1, 1), q(0, 1), q(0, 1)],
            vec![q(0, 1), q(0, 1), q(1, 1), q(0, 1)],
            vec![q(0, 1), q(0, 1), q(0, 1), q(1, 1)],
        ];
        assert_eq!(quadratic(&a, &[1, -1, 0, 0]), q(-2, 1));
        assert!(!mx::is_psd(&a).unwrap());
    }
    #[test]
    fn negative_vector_search_bound_is_a_refusal() {
        let (r, f) = small();
        assert_eq!(certify(r, f, 0, 0), Err(FramePolytopeError::CarrierBudget));
    }
}
