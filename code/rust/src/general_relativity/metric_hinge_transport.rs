
use crate::certified_dihedral::{
    deficit_enclosure, DeficitEnclosure, GeometryError, MetricHingeStar,
};
use linear_algebra::regge_exact::So4;
use num_rational::BigRational as Q;
use num_traits::{One, Zero};
use tfqm_number_theory::{certified_angles::validate_rational, rational::sqrt_exact};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum TransportError {
    #[error(transparent)]
    Geometry(#[from] GeometryError),
    #[error("normal rotation is outside the exact rational class")]
    AlgebraicRotation,
    #[error("invalid basepoint, frame count, rational profile or SO(4) frame")]
    Frame,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Orientation {
    Forward,
    Reverse,
}

#[derive(Debug, Clone)]
pub struct MetricHingeTransport {
    deficit: DeficitEnclosure,
    normal_rotations: Vec<(Q, Q)>,
    links: Vec<So4>,
}

fn checked_frame(m: &So4) -> Result<So4, TransportError> {
    for q in m.m.iter().flatten() {
        validate_rational(q).map_err(|_| TransportError::Frame)?;
    }
    So4::try_new(m.m.clone()).map_err(|_| TransportError::Frame)
}

fn loop_product(links: &[So4], base: usize) -> Result<So4, TransportError> {
    if base >= links.len() {
        return Err(TransportError::Frame);
    }
    let mut out = So4::identity();
    for i in 0..links.len() {
        out = links[(base + i) % links.len()].mul(&out);
    }
    Ok(out)
}

impl MetricHingeTransport {
    pub fn new(star: &MetricHingeStar, eps: &Q) -> Result<Self, TransportError> {
        let deficit = deficit_enclosure(star, eps)?;
        let mut normal_rotations = Vec::new();
        let mut links = Vec::new();
        for a in deficit.angles() {
            let [aa, bb, ab] = a.normal_gram();
            let square_norm = aa * bb;
            let cosine_square = ab * ab / &square_norm;
            let cosine_abs = sqrt_exact(&cosine_square).ok_or(TransportError::AlgebraicRotation)?;
            let cosine = if ab < &Q::zero() {
                -cosine_abs
            } else {
                cosine_abs
            };
            let sine =
                sqrt_exact(&(Q::one() - cosine_square)).ok_or(TransportError::AlgebraicRotation)?;
            if sine <= Q::zero() || &cosine * &cosine + &sine * &sine != Q::one() {
                return Err(TransportError::AlgebraicRotation);
            }
            let mut m = So4::identity().m;
            m[2][2] = cosine.clone();
            m[3][3] = cosine.clone();
            m[2][3] = sine.clone();
            m[3][2] = -&sine;
            links.push(So4::try_new(m).map_err(|_| TransportError::Frame)?);
            normal_rotations.push((cosine, sine));
        }
        Ok(Self {
            deficit,
            normal_rotations,
            links,
        })
    }
    pub fn deficit(&self) -> &DeficitEnclosure {
        &self.deficit
    }
    pub fn normal_rotations(&self) -> &[(Q, Q)] {
        &self.normal_rotations
    }
    pub fn links(&self) -> &[So4] {
        &self.links
    }
    pub fn holonomy(&self, base: usize, orientation: Orientation) -> Result<So4, TransportError> {
        let w = loop_product(&self.links, base)?;
        Ok(match orientation {
            Orientation::Forward => w,
            Orientation::Reverse => w.transpose(),
        })
    }
    pub fn gauged_links(&self, frames: &[So4]) -> Result<Vec<So4>, TransportError> {
        if frames.len() != self.links.len() {
            return Err(TransportError::Frame);
        }
        let frames: Vec<_> = frames.iter().map(checked_frame).collect::<Result<_, _>>()?;
        Ok((0..self.links.len())
            .map(|i| {
                frames[(i + 1) % frames.len()]
                    .mul(&self.links[i])
                    .mul(&frames[i].transpose())
            })
            .collect())
    }
    pub fn gauged_holonomy(&self, base: usize, frames: &[So4]) -> Result<So4, TransportError> {
        let links = self.gauged_links(frames)?;
        let w = loop_product(&links, base)?;
        let frame = frames.get(base).ok_or(TransportError::Frame)?;
        let expected = frame
            .mul(&self.holonomy(base, Orientation::Forward)?)
            .mul(&frame.transpose());
        if w != expected {
            return Err(TransportError::Frame);
        }
        Ok(w)
    }
    pub fn observed_defect(&self, base: usize) -> Result<[[Q; 4]; 4], TransportError> {
        let w = self.holonomy(base, Orientation::Forward)?;
        Ok(std::array::from_fn(|i| {
            std::array::from_fn(|j| &w.m[i][j] - if i == j { Q::one() } else { Q::zero() })
        }))
    }
}
