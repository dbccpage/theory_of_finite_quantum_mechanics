//! Phase-fiber boundary (Target 11).
//!
//! # Discrete toy fence (retained)
//!
//! The only **constructed** phase fiber in this module is
//! [`CyclicPhaseGroup`]: the finite cyclic group \(\mathbb{Z}/n\) as a
//! discrete stand-in for \(U(1)\). Exact arithmetic uses residues mod \(n\)
//! and optional circle fractions \(k/n \in \mathbb{Q}/\mathbb{Z}\).
//!
//! # General-E interface
//!
//! [`U1PhaseFiberE`] holds a general-E claim about a \(U(1)\) phase fiber
//! together with an explicit evidence tag ([`U1PhaseFiberEvidence`]):
//!
//! - `ConstructedDiscrete { n }` — built here as \(\mathbb{Z}/n\)
//! - `ImportRegistered { import_id, source_ref }` — formal import, **not**
//!   a construction (does not mint continuum structure)
//! - `OpenResidual { reason }` — honest open residual (e.g. continuum \(U(1)\))
//!
//! Continuum \(U(1)\) is **never** constructed. Claiming continuum without
//! import/residual evidence **fails closed**.
//!
//! # Cohomology-ish diagnostic
//!
//! A 1-cochain assigns discrete phases to directed edges of a small graph.
//! Coboundary of a 0-cochain \(\alpha\) is
//! \((\delta\alpha)(u \to v) = \alpha(v) - \alpha(u) \pmod n\).
//! Exactness (trivial class) is decided by consistent gauge-fixing.
//!
//! **AuthorityEffect:** None. Not PROVED. Not GlobalGreen. No continuum promotion.

use omega_homology::cyclic_phase::{CyclicPhaseError, CyclicPhaseGroup};

/// Fence string — never mints PROVED / GlobalGreen / continuum \(U(1)\).
pub const AUTHORITY_FENCE: &str = "AuthorityEffect None; not PROVED; not GlobalGreen; \
     discrete Z/n toy fence retained; continuum U(1) not constructed; no continuum promotion.";

/// Errors for phase-fiber boundary operations (fail-closed).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PhaseFiberError {
    Cyclic(CyclicPhaseError),
    /// Continuum \(U(1)\) claimed without import or residual evidence.
    ContinuumU1WithoutEvidence,
    /// Import registration requires nonempty import_id and source_ref.
    EmptyImportRegistration,
    /// Open residual requires a nonempty reason.
    EmptyOpenResidualReason,
}

/// Evidence tag for a general-E \(U(1)\) phase-fiber claim.
///
/// Distinguishes actual discrete construction from formal import and from
/// honest open residuals. Import registration **must not** be treated as
/// construction of continuum \(U(1)\).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum U1PhaseFiberEvidence {
    /// Constructed in-crate as discrete \(\mathbb{Z}/n\).
    ConstructedDiscrete { n: usize },
    /// Formally registered import — **not** a construction.
    ImportRegistered {
        import_id: String,
        source_ref: String,
    },
    /// Honest open residual (e.g. continuum \(U(1)\) exactness OPEN).
    OpenResidual { reason: String },
}

impl U1PhaseFiberEvidence {
    /// True only for the discrete construction path.
    pub fn is_constructed(&self) -> bool {
        matches!(self, Self::ConstructedDiscrete { .. })
    }

    /// True only for formal import (never pretends construction).
    pub fn is_import_registered(&self) -> bool {
        matches!(self, Self::ImportRegistered { .. })
    }

    /// True only for open residual packaging.
    pub fn is_open_residual(&self) -> bool {
        matches!(self, Self::OpenResidual { .. })
    }

    /// Continuum \(U(1)\) is never evidenced as constructed here.
    pub fn claims_continuum_construction(&self) -> bool {
        false
    }
}

/// General-E carrier for \(U(1)\) phase fibers with associated evidence.
///
/// Does **not** store continuum manifold data. Continuum claims route only
/// through `ImportRegistered` or `OpenResidual`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct U1PhaseFiberE {
    /// Evidence for the fiber status.
    pub evidence: U1PhaseFiberEvidence,
    /// Stable label / claim id.
    pub label: String,
}

impl U1PhaseFiberE {
    /// Construct discrete \(\mathbb{Z}/n\) evidence (\(n \ge 2\)).
    pub fn construct_discrete(n: usize, label: impl Into<String>) -> Result<Self, PhaseFiberError> {
        let fiber = CyclicPhaseGroup::try_new(n).map_err(PhaseFiberError::Cyclic)?;
        Ok(Self {
            evidence: U1PhaseFiberEvidence::ConstructedDiscrete { n: fiber.order() },
            label: label.into(),
        })
    }

    /// Register a formal import of continuum / external \(U(1)\) structure.
    ///
    /// This does **not** construct \(U(1)\); it only records import linkage.
    pub fn register_import(
        import_id: impl Into<String>,
        source_ref: impl Into<String>,
        label: impl Into<String>,
    ) -> Result<Self, PhaseFiberError> {
        let import_id = import_id.into();
        let source_ref = source_ref.into();
        if import_id.trim().is_empty() || source_ref.trim().is_empty() {
            return Err(PhaseFiberError::EmptyImportRegistration);
        }
        Ok(Self {
            evidence: U1PhaseFiberEvidence::ImportRegistered {
                import_id,
                source_ref,
            },
            label: label.into(),
        })
    }

    /// Package an open residual (e.g. continuum exactness OPEN).
    pub fn open_residual(
        reason: impl Into<String>,
        label: impl Into<String>,
    ) -> Result<Self, PhaseFiberError> {
        let reason = reason.into();
        if reason.trim().is_empty() {
            return Err(PhaseFiberError::EmptyOpenResidualReason);
        }
        Ok(Self {
            evidence: U1PhaseFiberEvidence::OpenResidual { reason },
            label: label.into(),
        })
    }

    /// Fail-closed gate for continuum \(U(1)\) claims.
    ///
    /// Without explicit import or residual evidence, continuum \(U(1)\) is
    /// refused. Providing an import or residual is allowed and does **not**
    /// promote the claim to constructed continuum structure.
    pub fn claim_continuum_u1(
        evidence: ContinuumU1ClaimEvidence,
        label: impl Into<String>,
    ) -> Result<Self, PhaseFiberError> {
        match evidence {
            ContinuumU1ClaimEvidence::None => Err(PhaseFiberError::ContinuumU1WithoutEvidence),
            ContinuumU1ClaimEvidence::Import {
                import_id,
                source_ref,
            } => Self::register_import(import_id, source_ref, label),
            ContinuumU1ClaimEvidence::OpenResidual { reason } => Self::open_residual(reason, label),
        }
    }

    /// Whether this carrier was constructed as discrete \(\mathbb{Z}/n\).
    pub fn is_constructed(&self) -> bool {
        self.evidence.is_constructed()
    }

    /// Whether this is a formal import only (never construction).
    pub fn is_import_only(&self) -> bool {
        self.evidence.is_import_registered()
    }

    /// Authority fence (never mints PROVED/GlobalGreen/continuum).
    pub fn authority_fence() -> &'static str {
        AUTHORITY_FENCE
    }
}

/// Explicit evidence choices when claiming continuum \(U(1)\).
///
/// `None` fails closed. Import and residual are formal / residual only.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ContinuumU1ClaimEvidence {
    /// No evidence — must fail closed.
    None,
    /// Formal import registration (not construction).
    Import {
        import_id: String,
        source_ref: String,
    },
    /// Honest open residual.
    OpenResidual { reason: String },
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_homology::cyclic_phase::{check_coboundary_triviality, coboundary, PhaseOneCochain};
    use omega_homology::finite_directed_graph::{DirectedGraphBuilder, TheoremProvenance};
    use omega_number_theory::rational::rq;

    #[test]
    fn toy_n2_constructs_discrete_z2() {
        let fiber = CyclicPhaseGroup::try_new(2).unwrap();
        assert_eq!(fiber.order(), 2);
        assert_eq!(fiber.identity().residue(), 0);
        let p = fiber.phase(1).unwrap();
        assert_eq!(p.as_circle_rational(), rq(1, 2));
        // Z/2: 1+1 = 0
        assert_eq!(p.add(p).unwrap().residue(), 0);

        let e = U1PhaseFiberE::construct_discrete(2, "toy-n2").unwrap();
        assert!(e.is_constructed());
        assert!(!e.is_import_only());
        assert_eq!(
            e.evidence,
            U1PhaseFiberEvidence::ConstructedDiscrete { n: 2 }
        );
        assert!(U1PhaseFiberE::authority_fence().contains("AuthorityEffect None"));
        assert!(AUTHORITY_FENCE.contains("no continuum promotion"));
    }

    #[test]
    fn toy_n4_constructs_discrete_z4_and_circle_rationals() {
        let fiber = CyclicPhaseGroup::try_new(4).unwrap();
        assert_eq!(fiber.order(), 4);
        let p = fiber.phase(3).unwrap();
        assert_eq!(p.as_circle_rational(), rq(3, 4));
        assert_eq!(p.add(fiber.phase(1).unwrap()).unwrap().residue(), 0);
        assert_eq!(fiber.relative_phase_dim_shell(3), 2);

        let e = U1PhaseFiberE::construct_discrete(4, "toy-n4").unwrap();
        assert!(matches!(
            e.evidence,
            U1PhaseFiberEvidence::ConstructedDiscrete { n: 4 }
        ));
        assert!(!e.evidence.claims_continuum_construction());
    }

    #[test]
    fn invalid_modulus_rejected() {
        assert_eq!(
            CyclicPhaseGroup::try_new(1),
            Err(CyclicPhaseError::InvalidModulus { n: 1 })
        );
        assert_eq!(
            CyclicPhaseGroup::try_new(0),
            Err(CyclicPhaseError::InvalidModulus { n: 0 })
        );
    }

    #[test]
    fn import_registered_path_does_not_pretend_construction() {
        let e = U1PhaseFiberE::register_import(
            "imp:u1-holonomy",
            "qm_207_complex_phase_fiber_and_u1_transport_lift",
            "import-u1",
        )
        .unwrap();

        assert!(!e.is_constructed());
        assert!(e.is_import_only());
        assert!(e.evidence.is_import_registered());
        assert!(!e.evidence.claims_continuum_construction());
        match &e.evidence {
            U1PhaseFiberEvidence::ImportRegistered {
                import_id,
                source_ref,
            } => {
                assert_eq!(import_id, "imp:u1-holonomy");
                assert!(source_ref.contains("qm_207"));
            }
            other => panic!("expected ImportRegistered, got {other:?}"),
        }
        // Must not be ConstructedDiscrete
        assert!(!matches!(
            e.evidence,
            U1PhaseFiberEvidence::ConstructedDiscrete { .. }
        ));
    }

    #[test]
    fn continuum_u1_without_evidence_fails_closed() {
        let err =
            U1PhaseFiberE::claim_continuum_u1(ContinuumU1ClaimEvidence::None, "bad-continuum")
                .unwrap_err();
        assert_eq!(err, PhaseFiberError::ContinuumU1WithoutEvidence);
    }

    #[test]
    fn continuum_u1_with_import_is_import_only_not_construction() {
        let e = U1PhaseFiberE::claim_continuum_u1(
            ContinuumU1ClaimEvidence::Import {
                import_id: "imp:continuum-u1".into(),
                source_ref: "external:mathlib-U1".into(),
            },
            "claimed-u1",
        )
        .unwrap();
        assert!(!e.is_constructed());
        assert!(e.is_import_only());
        assert!(!e.evidence.claims_continuum_construction());
    }

    #[test]
    fn continuum_u1_with_open_residual_packages_honestly() {
        let e = U1PhaseFiberE::claim_continuum_u1(
            ContinuumU1ClaimEvidence::OpenResidual {
                reason: "continuous U(1)^{|E_w|-1} exactness OPEN".into(),
            },
            "open-u1",
        )
        .unwrap();
        assert!(!e.is_constructed());
        assert!(e.evidence.is_open_residual());
        assert!(!e.evidence.claims_continuum_construction());
    }

    #[test]
    fn coboundary_of_zero_cochain_is_exact_on_triangle_n2() {
        let fiber = CyclicPhaseGroup::try_new(2).unwrap();
        let g = DirectedGraphBuilder::cycle_graph(
            3,
            TheoremProvenance {
                verification_source: "exact phase regression".into(),
            },
        )
        .unwrap();
        // α = (0, 1, 0) on Z/2
        let alpha = vec![0usize, 1, 0];
        let theta = coboundary(&fiber, &g, &alpha).unwrap();
        // edges: 0→1: 1-0=1, 1→2: 0-1=1, 2→0: 0-0=0
        assert_eq!(theta.edge_phases, vec![1, 1, 0]);

        let check = check_coboundary_triviality(&fiber, &g, &theta).unwrap();
        assert!(check.is_exact);
        assert!(check.witness_zero_cochain.is_some());
        assert!(check.holonomy_obstruction.is_none());
    }

    #[test]
    fn nontrivial_holonomy_on_triangle_n4_is_not_exact() {
        let fiber = CyclicPhaseGroup::try_new(4).unwrap();
        let g = DirectedGraphBuilder::cycle_graph(
            3,
            TheoremProvenance {
                verification_source: "exact phase regression".into(),
            },
        )
        .unwrap();
        // Uniform phase 1 on each edge ⇒ holonomy 3 ≢ 0 mod 4
        let theta = PhaseOneCochain::try_new(&fiber, &g, vec![1, 1, 1]).unwrap();
        assert_eq!(
            theta.as_circle_rationals(),
            vec![rq(1, 4), rq(1, 4), rq(1, 4)]
        );

        let check = check_coboundary_triviality(&fiber, &g, &theta).unwrap();
        assert!(!check.is_exact);
        assert!(check.witness_zero_cochain.is_none());
        assert!(check.holonomy_obstruction.is_some());
        assert_ne!(check.holonomy_obstruction.unwrap() % 4, 0);
    }

    #[test]
    fn path_graph_all_one_cochains_exact_n4() {
        let fiber = CyclicPhaseGroup::try_new(4).unwrap();
        let g = DirectedGraphBuilder::chain(
            3,
            TheoremProvenance {
                verification_source: "exact phase regression".into(),
            },
        )
        .unwrap();
        let theta = PhaseOneCochain::try_new(&fiber, &g, vec![1, 2]).unwrap();
        let check = check_coboundary_triviality(&fiber, &g, &theta).unwrap();
        assert!(check.is_exact);
        let wit = check.witness_zero_cochain.unwrap();
        let rebuilt = coboundary(&fiber, &g, &wit).unwrap();
        assert_eq!(rebuilt.edge_phases, theta.edge_phases);
    }

    #[test]
    fn empty_import_registration_rejected() {
        assert_eq!(
            U1PhaseFiberE::register_import("", "src", "l"),
            Err(PhaseFiberError::EmptyImportRegistration)
        );
    }
}
