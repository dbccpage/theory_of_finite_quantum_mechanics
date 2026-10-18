//! Target 18 — Born/Gleason conditional uniqueness with exposed assumptions.
//!
//! Conditional uniqueness: under dimension, continuity/noncontextuality, and
//! scalar assumptions, frame functions on rays coincide with the Born rule.
//! Hypotheses are **exposed** — unpaid assumptions refuse the uniqueness claim.
//!
//! The assumptions other than the dimension are declared booleans, not
//! computed properties. In particular non-contextuality is declared: a
//! `FrameFunction` here assigns values to the projectors of one basis only, so
//! there is no second context in which a ray's value could differ, and nothing
//! here can test context independence. Every report of these assumptions
//! (`GleasonAssumptions::unpaid`, the refusal `AssumptionsUnpaid`, and the
//! callers in `sealed_finite_matrix_recovery` and `engine_bridge`) reports
//! declarations.
//!
//! AuthorityEffect: None. Not PROVED continuum Gleason. Finite toy certificates only.

use num_traits::{One, Zero};

/// Fence.
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; conditional Born/Gleason face; assumptions exposed.";

/// Exact rationals (`BigRational`); frame values cannot overflow.
pub type Q = omega_number_theory::rational::Rational;

/// Exposed assumptions for conditional uniqueness. `dimension` is data; every
/// boolean is a declaration that nothing here computes.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GleasonAssumptions {
    /// Hilbert dimension n ≥ 3 for classical Gleason; n=2 is special (OPEN residual).
    pub dimension: usize,
    /// Declared, not computed: the frame function's value depends only on the
    /// ray. A frame function on one basis has no second context to compare.
    pub noncontextual: bool,
    /// Declared: continuity / countable additivity stand-in (finite additivity on orthogonal families).
    pub finite_additivity: bool,
    /// Declared: scalar field complex (true) vs real (false — rebit residual).
    pub complex_scalars: bool,
    /// Declared: explicit “no continuum uniqueness without these” fence.
    pub no_silent_continuum: bool,
}

impl GleasonAssumptions {
    /// The assumptions not paid. Apart from `dimension_ge_3`, each entry names
    /// a declaration that was declared false, not a property found to fail.
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

/// Finite frame function on computational-basis projectors (diagonal face).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrameFunction {
    pub dim: usize,
    /// f(|i⟩⟨i|) for i in 0..dim
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

    /// Born frame from state populations |c_i|².
    pub fn born_from_populations(pops: &[Q]) -> Result<Self, BornGleasonError> {
        Self::try_new(pops.to_vec())
    }
}

/// Conditional uniqueness theorem face: if assumptions paid and frame equals
/// Born populations of some density, accept diagnostic uniqueness on basis.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConditionalUniqueness {
    pub assumptions: GleasonAssumptions,
    pub frame: FrameFunction,
    pub born_reference: FrameFunction,
    pub unique_on_basis: bool,
}

impl ConditionalUniqueness {
    /// Refuse unless assumptions paid; then check frame == born_reference.
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

/// Dimension-2 residual: uniqueness not claimed (Gleason needs n≥3).
pub const OPEN_RESIDUAL_DIM2: &str =
    "OPEN residual: dim=2 frame-function uniqueness is not discharged by this face \
     (classical Gleason requires dim ≥ 3). AuthorityEffect None.";

#[cfg(test)]
mod tests {
    use super::*;
    use omega_number_theory::rational::rq;
    use omega_quantum_physics::busch_effects::{
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

    // --- Lean parity: BornSelectionImport / dim_two_forces_busch_route ------
    //
    // These mirror, by name, the theorems in qm_wave7_completion.lean. If either
    // side changes its fence the pair stops agreeing, which is the point.

    /// Parity with Lean `gleason_dim3plus_fails_at_dim_two`: the projection
    /// route is absent at the estate's working dimension.
    #[test]
    fn parity_gleason_route_absent_at_dim_two() {
        assert!(!available_born_routes(2).contains(&BornSelectionRoute::GleasonDim3Plus));
    }

    /// Parity with Lean `dim_two_forces_busch_route`.
    #[test]
    fn parity_dim_two_forces_busch_route() {
        assert!(dim_two_forces_busch_route());
        assert_eq!(
            available_born_routes(2),
            vec![BornSelectionRoute::BuschPovm]
        );
    }

    /// Parity with Lean `gleason_dim3plus_bound_reachable`: the fence
    /// discriminates rather than refusing everywhere.
    #[test]
    fn parity_gleason_route_available_from_dim_three() {
        let r = available_born_routes(3);
        assert!(r.contains(&BornSelectionRoute::GleasonDim3Plus));
        assert!(r.contains(&BornSelectionRoute::BuschPovm));
    }

    /// The Rust assumption gate and the route table agree at every small
    /// dimension. Guards against the two fences drifting apart inside Rust.
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

    /// Weights with denominators near 10^12 used to overflow the `Ratio<i64>`
    /// sum (a panic in debug builds, a false refusal in release); the sum is
    /// now exact.
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
