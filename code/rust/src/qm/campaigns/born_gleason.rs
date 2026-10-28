
use num_traits::{One, Zero};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; conditional Born/Gleason face; assumptions exposed.";

pub type Q = engine_number_theory::rational::Rational;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GleasonAssumptions {
    pub dimension: usize,
    pub noncontextual: bool,
    pub finite_additivity: bool,
    pub complex_scalars: bool,
    pub no_silent_continuum: bool,
}

impl GleasonAssumptions {
    pub fn unpaid(&self) -> Vec<&'static str> {
        let mut u = Vec::new();
        if self.dimension < 3 {
            u.push("dimension_ge_3");
        }
        if !self.noncontextual {
            u.push("noncontextual");
        }
        if !self.finite_additivity {
            u.push("finite_additivity");
        }
        if !self.complex_scalars {
            u.push("complex_scalars");
        }
        if !self.no_silent_continuum {
            u.push("no_silent_continuum");
        }
        u
    }

    pub fn all_paid(&self) -> bool {
        self.unpaid().is_empty()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BornGleasonError {
    AssumptionsUnpaid { unpaid: Vec<&'static str> },
    NotNormalized,
    FrameNotBorn,
    Empty,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrameFunction {
    pub dim: usize,
    pub on_basis: Vec<Q>,
}

impl FrameFunction {
    pub fn try_new(on_basis: Vec<Q>) -> Result<Self, BornGleasonError> {
        if on_basis.is_empty() {
            return Err(BornGleasonError::Empty);
        }
        if on_basis.iter().any(|x| *x < Zero::zero()) {
            return Err(BornGleasonError::NotNormalized);
        }
        let s: Q = on_basis.iter().sum();
        if s != Q::one() {
            return Err(BornGleasonError::NotNormalized);
        }
        Ok(Self {
            dim: on_basis.len(),
            on_basis,
        })
    }

    pub fn born_from_populations(pops: &[Q]) -> Result<Self, BornGleasonError> {
        Self::try_new(pops.to_vec())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConditionalUniqueness {
    pub assumptions: GleasonAssumptions,
    pub frame: FrameFunction,
    pub born_reference: FrameFunction,
    pub unique_on_basis: bool,
}

impl ConditionalUniqueness {
    pub fn try_prove(
        assumptions: GleasonAssumptions,
        frame: FrameFunction,
        born_reference: FrameFunction,
    ) -> Result<Self, BornGleasonError> {
        let unpaid = assumptions.unpaid();
        if !unpaid.is_empty() {
            return Err(BornGleasonError::AssumptionsUnpaid { unpaid });
        }
        if frame.dim != born_reference.dim {
            return Err(BornGleasonError::FrameNotBorn);
        }
        if frame.on_basis != born_reference.on_basis {
            return Err(BornGleasonError::FrameNotBorn);
        }
        Ok(Self {
            assumptions,
            frame,
            born_reference,
            unique_on_basis: true,
        })
    }
}

pub const OPEN_RESIDUAL_DIM2: &str =
    "OPEN residual: dim=2 frame-function uniqueness is not discharged by this face \
     (classical Gleason requires dim ≥ 3). AuthorityEffect None.";

#[cfg(test)]
mod tests {
    use super::*;
    use engine_number_theory::rational::rq;
    use engine_quantum_physics::busch_effects::{
        available_born_routes, dim_two_forces_busch_route, BornSelectionRoute,
    };

    fn paid_assumptions(dim: usize) -> GleasonAssumptions {
        GleasonAssumptions {
            dimension: dim,
            noncontextual: true,
            finite_additivity: true,
            complex_scalars: true,
            no_silent_continuum: true,
        }
    }


    #[test]
    fn parity_gleason_route_absent_at_dim_two() {
        assert!(!available_born_routes(2).contains(&BornSelectionRoute::GleasonDim3Plus));
    }

    #[test]
    fn parity_dim_two_forces_busch_route() {
        assert!(dim_two_forces_busch_route());
        assert_eq!(
            available_born_routes(2),
            vec![BornSelectionRoute::BuschPovm]
        );
    }

    #[test]
    fn parity_gleason_route_available_from_dim_three() {
        let r = available_born_routes(3);
        assert!(r.contains(&BornSelectionRoute::GleasonDim3Plus));
        assert!(r.contains(&BornSelectionRoute::BuschPovm));
    }

    #[test]
    fn assumption_gate_and_route_table_agree() {
        for dim in 0..6usize {
            let gleason_paid = paid_assumptions(dim).all_paid();
            let gleason_route =
                available_born_routes(dim).contains(&BornSelectionRoute::GleasonDim3Plus);
            assert_eq!(
                gleason_paid, gleason_route,
                "assumption gate and route table disagree at dim={dim}"
            );
        }
    }

    #[test]
    fn born_gleason_refuses_dim2() {
        let a = paid_assumptions(2);
        assert!(!a.all_paid());
        let frame = FrameFunction::born_from_populations(&[Q::one(), Q::zero()]).unwrap();
        let err = ConditionalUniqueness::try_prove(a, frame.clone(), frame);
        assert!(matches!(
            err,
            Err(BornGleasonError::AssumptionsUnpaid { .. })
        ));
    }

    #[test]
    fn born_gleason_refuses_real_scalars() {
        let mut a = paid_assumptions(3);
        a.complex_scalars = false;
        let p = [rq(1, 2), rq(1, 3), rq(1, 6)];
        let frame = FrameFunction::born_from_populations(&p).unwrap();
        let err = ConditionalUniqueness::try_prove(a, frame.clone(), frame);
        assert!(matches!(
            err,
            Err(BornGleasonError::AssumptionsUnpaid { .. })
        ));
    }

    #[test]
    fn born_gleason_accepts_matching_frame_dim3() {
        let a = paid_assumptions(3);
        let p = [rq(1, 2), rq(1, 3), rq(1, 6)];
        let frame = FrameFunction::born_from_populations(&p).unwrap();
        let u = ConditionalUniqueness::try_prove(a, frame.clone(), frame).unwrap();
        assert!(u.unique_on_basis);
    }

    #[test]
    fn born_gleason_mismatch_refused() {
        let a = paid_assumptions(3);
        let f = FrameFunction::born_from_populations(&[rq(1, 2), rq(1, 2), rq(0, 1)]).unwrap();
        let b = FrameFunction::born_from_populations(&[rq(1, 3), rq(1, 3), rq(1, 3)]).unwrap();
        let err = ConditionalUniqueness::try_prove(a, f, b);
        assert_eq!(err, Err(BornGleasonError::FrameNotBorn));
    }

    #[test]
    fn born_gleason_authority_none() {
        assert!(AUTHORITY_FENCE.contains("AuthorityEffect None"));
        assert!(OPEN_RESIDUAL_DIM2.contains("dim=2"));
        assert!(One::is_one(&Q::one()));
    }

    #[test]
    fn large_denominators_sum_exactly() {
        let (p, q) = (1_000_000_000_039i64, 999_999_999_989i64);
        let weights = vec![
            rq(1, 2 * p),
            rq(1, 2 * q),
            rq(p - 1, 2 * p),
            rq(q - 1, 2 * q),
        ];
        assert!(FrameFunction::try_new(weights).is_ok());
        assert_eq!(
            FrameFunction::try_new(vec![rq(1, 2 * p), rq(1, 2 * q)]),
            Err(BornGleasonError::NotNormalized)
        );
    }
}
