//! Exact finite Cabello census, tomography, spectral margins and negative vectors.
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
pub fn certify(
    rays: Vec<Vec<i64>>,
    frames: Vec<Vec<usize>>,
    budget: usize,
    radius: i64,
) -> Result<Census, FramePolytopeError> {
    let system = FrameSystem::new(rays, frames)?;
    if system.dimension() != 4 || radius < 1 || radius > 8 {
        return Err(FramePolytopeError::CarrierBudget);
    }
    let (points, examined) = system.vertices_with_statistics(budget)?;
    let mut vertices = Vec::new();
    let mut at_half = 0;
    let mut above_quarter = 0;
    for weights in points {
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
        let half = shift(&rho, &q(1, 2));
        let quarter = shift(&rho, &q(1, 4));
        let half_det = mx::determinant(&half).map_err(|_| FramePolytopeError::InvalidSolution)?;
        let leading: Vec<Q> = (1..=4)
            .map(|k| {
                mx::determinant(&quarter[..k].iter().map(|r| r[..k].to_vec()).collect())
                    .map_err(|_| FramePolytopeError::InvalidSolution)
            })
            .collect::<Result<_, _>>()?;
        let spectral_class = if eigenvalues_at_least(&basic, &q(-1, 2))? && half_det.is_zero() {
            at_half += 1;
            "at_minus_half"
        } else if eigenvalues_above(&basic, &q(-1, 4))? {
            above_quarter += 1;
            "above_minus_quarter"
        } else {
            return Err(FramePolytopeError::InvalidSolution);
        };
        let mut witness = None;
        'search: for r in 1..=radius {
            for a in -r..=r {
                for b in -r..=r {
                    for c in -r..=r {
                        for d in -r..=r {
                            let v = [a, b, c, d];
                            let value = quadratic(&rho, &v);
                            if value.is_negative() {
                                witness = Some((v, value));
                                break 'search;
                            }
                        }
                    }
                }
            }
        }
        let Some((negative_vector, quadratic_value)) = witness else {
            return Err(FramePolytopeError::InvalidSolution);
        };
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
        vertices.push(VertexCertificate {
            weights,
            representative: rho,
            negative_vector,
            quadratic_value,
            spectral_class,
            half_shift_determinant: half_det,
            quarter_shift_leading_minors: leading,
            denominator,
            matrix_numerators: scaled.iter().map(|x| x.numer().clone()).collect(),
            weights_twice: twice.iter().map(|x| x.numer().clone()).collect(),
            negative_value_numerator: neg.numer().clone(),
        });
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
