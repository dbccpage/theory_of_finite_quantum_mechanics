
use std::collections::{BTreeMap, BTreeSet};

use num_rational::BigRational;
use num_traits::{One, Zero};
use tfqm_category_theory::finite_relational::FinitePreorder;
use tfqm_functional::gamma2::{
    DegreeOneResidualQ, ExactCochainComplexQ, ExactGamma2Result, Gamma2Functional,
};
use tfqm_functional::l1_seminorm::L1Seminorm;
use tfqm_functional::phi1::VerifiedExactPhi1;
use omega_homology::carrier::Carrier;
use omega_policy::trichotomy::{
    classify_exact, CertifiedExactTrichotomy, ObstructionDiagnosticClass, TrichotomyOutcome,
};
use omega_solvers::solver_lp_phi1_quotient::solve_exact_phi1;
use serde::{Deserialize, Serialize};

use crate::cochains::{coboundary_rows, named_graph_carrier};
use crate::error::WdpError;
use crate::types::AuthorityEffect;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum PrimitiveDifferenceAxiom {
    A01NonIdentification,
    A02UnentailedAdmission,
    A03EvaluationRelation,
    A04DirectedEvaluationCarrier,
    A05NilpotentCoboundary,
    A06QuotientDefectPurity,
    A07DescendedClosureMap,
    A08TriadTrichotomy,
    A09ObserverSelectedMetric,
    A10AntiReificationFirewall,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct GenesisAdmissionKernel {
    pub carrier_items: BTreeSet<String>,
    pub admitted_differences: Vec<(String, String, String)>,
    pub authority_effect: AuthorityEffect,
}

impl GenesisAdmissionKernel {
    pub fn new(items: BTreeSet<String>) -> Self {
        Self {
            carrier_items: items,
            admitted_differences: Vec::new(),
            authority_effect: AuthorityEffect::None,
        }
    }

    pub fn admit_difference(&mut self, a: &str, b: &str, token: &str) -> Result<(), &'static str> {
        if a == b {
            return Err(
                "Axiom A1 violation: cannot admit non-identification between identical items",
            );
        }
        if !self.carrier_items.contains(a) || !self.carrier_items.contains(b) {
            return Err("Carrier violation: items must belong to the declared carrier set");
        }
        self.admitted_differences
            .push((a.to_string(), b.to_string(), token.to_string()));
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EvaluationPreorder {
    domain: Vec<String>,
    preorder: FinitePreorder,
}

impl EvaluationPreorder {
    pub fn from_relation(
        domain: Vec<String>,
        base_pairs: &[(String, String)],
    ) -> Result<Self, WdpError> {
        if domain.iter().any(String::is_empty)
            || domain.iter().collect::<BTreeSet<_>>().len() != domain.len()
        {
            return Err(WdpError::InvalidInput {
                detail: "preorder requires nonempty, distinct labels".into(),
            });
        }
        let name_to_idx: BTreeMap<&str, usize> = domain
            .iter()
            .enumerate()
            .map(|(i, s)| (s.as_str(), i))
            .collect();
        let edges = base_pairs
            .iter()
            .map(|(u, v)| {
                let resolve = |name: &str| {
                    name_to_idx
                        .get(name)
                        .copied()
                        .ok_or_else(|| WdpError::ElementNotFound {
                            element: name.into(),
                        })
                };
                Ok((resolve(u)?, resolve(v)?))
            })
            .collect::<Result<Vec<_>, WdpError>>()?;
        let preorder = FinitePreorder::from_edges(domain.len(), &edges)?;
        Ok(Self { domain, preorder })
    }

    pub fn domain(&self) -> &[String] {
        &self.domain
    }

    pub fn relation_matrix(&self) -> &[Vec<bool>] {
        self.preorder.relation()
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }

    pub fn leq(&self, u: &str, v: &str) -> Result<bool, WdpError> {
        let resolve = |name: &str| {
            self.domain
                .iter()
                .position(|s| s == name)
                .ok_or_else(|| WdpError::ElementNotFound {
                    element: name.into(),
                })
        };
        Ok(self.preorder.leq(resolve(u)?, resolve(v)?)?)
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TriadSignature {
    phi1: VerifiedExactPhi1,
    gamma2: ExactGamma2Result,
    trichotomy: CertifiedExactTrichotomy,
    authority_effect: AuthorityEffect,
}

impl TriadSignature {
    pub fn phi1(&self) -> &VerifiedExactPhi1 {
        &self.phi1
    }

    pub fn gamma2(&self) -> &ExactGamma2Result {
        &self.gamma2
    }

    pub fn trichotomy(&self) -> &CertifiedExactTrichotomy {
        &self.trichotomy
    }

    pub fn classification(&self) -> ObstructionDiagnosticClass {
        self.trichotomy.diagnostic_class()
    }

    pub fn r_cl(&self) -> Option<BigRational> {
        let (phi_1, gamma_2) = (self.trichotomy.phi1_value(), self.trichotomy.gamma2_value());
        if !phi_1.is_zero() {
            Some(gamma_2 / phi_1)
        } else if gamma_2.is_zero() {
            Some(BigRational::zero())
        } else {
            None
        }
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        self.authority_effect
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct EvaluationCarrier {
    pub vertices: Vec<String>,
    pub edges: Vec<(String, String)>,
    pub faces: Vec<(String, String, String)>,
    pub authority_effect: AuthorityEffect,
}

impl EvaluationCarrier {
    pub fn new(
        vertices: Vec<String>,
        edges: Vec<(String, String)>,
        faces: Vec<(String, String, String)>,
    ) -> Self {
        Self {
            vertices,
            edges,
            faces,
            authority_effect: AuthorityEffect::None,
        }
    }

    pub fn carrier(&self) -> Result<Carrier, WdpError> {
        named_graph_carrier(
            &self.vertices,
            &self.edges,
            &self.faces,
            vec![BigRational::one(); self.edges.len()],
            "omega_wdp::EvaluationCarrier",
        )
    }

    pub fn compute_triad_signature(&self, h: &[BigRational]) -> Result<TriadSignature, WdpError> {
        let carrier = self.carrier()?;
        let d0 = coboundary_rows(carrier.d0());
        let space = L1Seminorm::new(d0.clone(), carrier.weights().to_vec())?;
        let phi1 = solve_exact_phi1(&space, h)?;

        let complex = ExactCochainComplexQ::try_new(
            carrier.c0_dim(),
            carrier.c1_dim(),
            carrier.c2_dim(),
            d0,
            coboundary_rows(carrier.d1()),
        )?;
        let residual = DegreeOneResidualQ::try_new(&complex, phi1.primal_residual().to_vec())?;
        let gamma2 = Gamma2Functional::try_compute_exact_quotient(&residual)?;

        let trichotomy = match classify_exact(&phi1, &gamma2) {
            TrichotomyOutcome::Classified(trichotomy) => trichotomy,
            TrichotomyOutcome::TriRefused(refusal) => return Err(WdpError::Trichotomy(refusal)),
        };

        Ok(TriadSignature {
            phi1,
            gamma2,
            trichotomy,
            authority_effect: AuthorityEffect::None,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tfqm_functional::phi1::Phi1Functional;
    use omega_homology::scalar::{q, qr};

    fn triangle(faces: Vec<(String, String, String)>) -> EvaluationCarrier {
        let vertices = vec!["0".to_string(), "1".to_string(), "2".to_string()];
        let edges = vec![
            ("0".to_string(), "1".to_string()),
            ("1".to_string(), "2".to_string()),
            ("0".to_string(), "2".to_string()),
        ];
        EvaluationCarrier::new(vertices, edges, faces)
    }

    fn filled_triangle() -> EvaluationCarrier {
        triangle(vec![("0".to_string(), "1".to_string(), "2".to_string())])
    }

    #[test]
    fn test_primitive_axiomatics_genesis_admission() {
        let items = BTreeSet::from(["alpha".to_string(), "beta".to_string(), "gamma".to_string()]);
        let mut kernel = GenesisAdmissionKernel::new(items);
        assert!(kernel.admit_difference("alpha", "beta", "token_ab").is_ok());
        assert!(kernel
            .admit_difference("alpha", "alpha", "token_aa")
            .is_err());
        assert_eq!(kernel.authority_effect, AuthorityEffect::None);
    }

    #[test]
    fn test_evaluation_preorder_transitivity() {
        let domain = vec!["x0".to_string(), "x1".to_string(), "x2".to_string()];
        let base_rel = vec![
            ("x0".to_string(), "x1".to_string()),
            ("x1".to_string(), "x2".to_string()),
        ];
        let preorder = EvaluationPreorder::from_relation(domain, &base_rel).unwrap();

        assert!(preorder.leq("x0", "x0").unwrap());
        assert!(preorder.leq("x0", "x1").unwrap());
        assert!(preorder.leq("x1", "x2").unwrap());
        assert!(preorder.leq("x0", "x2").unwrap());
        assert!(!preorder.leq("x2", "x0").unwrap());
    }

    #[test]
    fn test_nilpotence_d1_d0_is_zero() {
        let carrier = filled_triangle().carrier().unwrap();
        let test_phi = vec![qr(1, 2), qr(3, 4), qr(-1, 3)];
        let d0_phi = carrier.d0().mul_vec(&test_phi).unwrap();
        let d1_d0_phi = carrier.d1().mul_vec(&d0_phi).unwrap();
        assert!(d1_d0_phi.iter().all(Zero::is_zero));
    }

    #[test]
    fn test_triad_three_way_classification() {
        let carrier = filled_triangle();

        let exact_h = carrier
            .carrier()
            .unwrap()
            .d0()
            .mul_vec(&[q(1), q(3), q(7)])
            .unwrap();
        let sig1 = carrier.compute_triad_signature(&exact_h).unwrap();
        assert_eq!(
            sig1.classification(),
            ObstructionDiagnosticClass::ExactRepair
        );
        assert!(sig1.phi1().value().is_zero());
        assert!(sig1.gamma2().value().is_zero());
        assert_eq!(sig1.r_cl(), Some(q(0)));

        let rupture_h = vec![q(1), q(1), q(0)];
        let sig2 = carrier.compute_triad_signature(&rupture_h).unwrap();
        assert_eq!(
            sig2.classification(),
            ObstructionDiagnosticClass::ActiveClosureFailure
        );
        assert_eq!(sig2.gamma2().coboundary(), &[q(2)]);
        assert!(!sig2.gamma2().value().is_zero());

        let sig3 = triangle(vec![])
            .compute_triad_signature(&rupture_h)
            .unwrap();
        assert_eq!(
            sig3.classification(),
            ObstructionDiagnosticClass::ClosedResidual
        );
        assert_eq!(sig3.phi1().value(), &q(2));
        assert_eq!(sig3.r_cl(), Some(q(0)));

        for sig in [sig1, sig2, sig3] {
            Phi1Functional::verify_exact_certificate(sig.phi1().certificate().clone()).unwrap();
            assert_eq!(sig.authority_effect(), AuthorityEffect::None);
        }
    }

    #[test]
    fn test_triad_refuses_malformed_input() {
        let carrier = filled_triangle();
        assert!(matches!(
            carrier.compute_triad_signature(&[q(1)]),
            Err(WdpError::Phi1(_))
        ));
        let missing_edge = EvaluationCarrier::new(
            vec!["0".to_string(), "1".to_string(), "2".to_string()],
            vec![("0".to_string(), "1".to_string())],
            vec![("0".to_string(), "1".to_string(), "2".to_string())],
        );
        assert!(matches!(
            missing_edge.compute_triad_signature(&[q(1)]),
            Err(WdpError::Homology(_))
        ));
    }
}
