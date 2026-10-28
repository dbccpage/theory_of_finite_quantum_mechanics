use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde_json::json;

use crate::coda::types::{DualWitness, LayerExecutionRecord, LayerId, ProblemInstance};
use tfqm_functional::gamma2::{
    DegreeOneResidualQ, ExactCochainComplexQ, ExactGamma2Error, Gamma2Functional,
};
use omega_solvers::solver_cohomology_simplicial_l1::{
    solve_l1_curved_constrained, solve_l1_quotient, VerifiedCurvedConstrainedPhi1,
};

pub struct Layer1Foc;

impl Layer1Foc {
    pub fn evaluate(
        problem: &ProblemInstance,
    ) -> Result<
        (
            LayerExecutionRecord,
            BigRational,
            BigRational,
            Option<DualWitness>,
            Vec<BigRational>,
        ),
        LayerExecutionRecord,
    > {
        Self::evaluate_with_closure_guard(problem, &BigRational::zero())
    }

    pub fn evaluate_with_closure_guard(
        problem: &ProblemInstance,
        tau: &BigRational,
    ) -> Result<
        (
            LayerExecutionRecord,
            BigRational,
            BigRational,
            Option<DualWitness>,
            Vec<BigRational>,
        ),
        LayerExecutionRecord,
    > {
        let failure = |reason: String| {
            Err(
                LayerExecutionRecord::new(LayerId::FOC, false, reason, BigRational::zero())
                    .with_metadata("certificate_verified", json!(false)),
            )
        };
        if tau.denom().is_zero() || tau.is_negative() {
            return failure("closure slack tau must be a valid non-negative rational".into());
        }
        if problem
            .d1
            .iter()
            .any(|row| row.len() != problem.defect_cochain.len())
        {
            return failure("d1 width differs from the cochain".into());
        }
        let cols = problem.d0.first().map_or(0, Vec::len);
        match ExactCochainComplexQ::try_new(
            cols,
            problem.defect_cochain.len(),
            problem.d1.len(),
            problem.d0.clone(),
            problem.d1.clone(),
        ) {
            Ok(complex) => {
                let cert = match solve_l1_quotient(&problem.d0, &problem.defect_cochain) {
                    Ok(cert) => cert,
                    Err(error) => return failure(error),
                };
                let residual = match DegreeOneResidualQ::try_new(&complex, cert.residual.clone()) {
                    Ok(residual) => residual,
                    Err(error) => return failure(error.to_string()),
                };
                let gamma2_evidence = match Gamma2Functional::try_compute_exact_quotient(&residual)
                {
                    Ok(evidence) => evidence,
                    Err(error) => return failure(error.to_string()),
                };
                let gamma2 = gamma2_evidence.value().clone();
                let phi1 = cert.distance.clone();

                let witness = if phi1 > BigRational::zero() {
                    Some(DualWitness::new(cert.witness, phi1.clone()))
                } else {
                    None
                };

                let msg = if phi1.is_zero() {
                    "Cochain is in im(d0): exact zero quotient defect with an exact repair"
                        .to_string()
                } else {
                    format!(
                        "Non-trivial quotient obstruction Phi_1={} (primal repair and dual witness agree)",
                        phi1
                    )
                };

                let record =
                    LayerExecutionRecord::new(LayerId::FOC, gamma2.is_zero(), msg, phi1.clone())
                        .with_metadata("locus", json!("flat_quotient"))
                        .with_metadata("quotient_invariant", json!(true))
                        .with_metadata("phi1", json!(phi1.to_string()))
                        .with_metadata("gamma2", json!(gamma2.to_string()))
                        .with_metadata("is_coherent", json!(gamma2.is_zero()))
                        .with_metadata("solver", json!(cert.method))
                        .with_metadata("certificate_verified", json!(true));

                Ok((record, phi1, gamma2, witness, cert.repair))
            }
            Err(ExactGamma2Error::CochainIdentityViolation { .. }) => {
                let verified = Self::evaluate_curved_constrained(problem, tau)?;
                let phi1 = verified.value().clone();
                let baseline_raw_gamma2 = verified.baseline_raw_gamma2().value().clone();
                let repaired_raw_gamma2 = verified.repaired_raw_gamma2().value().clone();
                let gamma2 = repaired_raw_gamma2.clone();

                let witness = if phi1 > BigRational::zero() {
                    Some(DualWitness::new(verified.dual_y().to_vec(), phi1.clone()))
                } else {
                    None
                };

                let msg = format!(
                    "Curved descent (K = d1*d0 != 0): constrained repair norm={}, raw Gamma_2={} (baseline={}, tau={})",
                    phi1, repaired_raw_gamma2, baseline_raw_gamma2, tau
                );

                let record =
                    LayerExecutionRecord::new(LayerId::FOC, gamma2.is_zero(), msg, phi1.clone())
                        .with_metadata("locus", json!("curved_representative_constrained"))
                        .with_metadata("quotient_invariant", json!(false))
                        .with_metadata("phi1", json!(phi1.to_string()))
                        .with_metadata("gamma2", json!(gamma2.to_string()))
                        .with_metadata("baseline_raw_gamma2", json!(baseline_raw_gamma2.to_string()))
                        .with_metadata("repaired_raw_gamma2", json!(repaired_raw_gamma2.to_string()))
                        .with_metadata("closure_slack_tau", json!(tau.to_string()))
                        .with_metadata("is_coherent", json!(gamma2.is_zero()))
                        .with_metadata(
                            "solver",
                            json!("exact_curved_constrained_primal_dual_simplex"),
                        )
                        .with_metadata("certificate_verified", json!(true));

                Ok((
                    record,
                    phi1,
                    gamma2,
                    witness,
                    verified.alpha().to_vec(),
                ))
            }
            Err(error) => failure(error.to_string()),
        }
    }

    pub fn evaluate_curved_constrained(
        problem: &ProblemInstance,
        tau: &BigRational,
    ) -> Result<VerifiedCurvedConstrainedPhi1, LayerExecutionRecord> {
        let failure_record = |reason: String| {
            LayerExecutionRecord::new(LayerId::FOC, false, reason, BigRational::zero())
                .with_metadata("certificate_verified", json!(false))
        };
        if problem
            .d1
            .iter()
            .any(|row| row.len() != problem.defect_cochain.len())
        {
            return Err(failure_record("d1 width differs from the cochain".into()));
        }
        solve_l1_curved_constrained(&problem.d0, &problem.d1, &problem.defect_cochain, tau)
            .map_err(failure_record)
    }
}

