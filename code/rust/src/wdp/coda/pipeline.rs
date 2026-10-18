use sha2::{Digest, Sha256};

use crate::coda::layer1_foc::Layer1Foc;
use crate::coda::layer2_mur::Layer2Mur;
use crate::coda::layer3_cs::Layer3Cs;
use crate::coda::layer4_cs_q::Layer4CsQ;
use crate::coda::layer5_q::Layer5Q;
use crate::coda::layer6_a::Layer6A;
use crate::coda::layer7_or::Layer7Or;
use crate::coda::layer8_fda::Layer8Fda;
use crate::coda::layer9_coda_gtla::Layer9CodaGtla;
use crate::coda::types::{ExternalAuthorityGrant, MasterNormalFormOutcome, ProblemInstance};

pub fn evaluate_coda_pipeline(problem: &ProblemInstance) -> MasterNormalFormOutcome {
    evaluate_coda_pipeline_with_grant(problem, None)
}

pub fn evaluate_coda_pipeline_with_grant(
    problem: &ProblemInstance,
    external_grant: Option<&ExternalAuthorityGrant>,
) -> MasterNormalFormOutcome {
    let mut records = Vec::with_capacity(9);

    let (rec1, phi1, gamma2, witness, primal_repair) = match Layer1Foc::evaluate(problem) {
        Ok(measured) => measured,
        Err(record) => {
            records.push(record);
            let digest = evidence_digest(problem, external_grant, &records);
            return Layer9CodaGtla::terminalize(
                problem,
                None,
                None,
                None,
                crate::coda::types::FirewallDecision::RouteRefused,
                None,
                records,
                Some("Invalid cochain complex or unverified quotient certificate".into()),
                None,
                digest,
            );
        }
    };
    records.push(rec1);

    let (rec2, _loss) = Layer2Mur::evaluate(problem);
    records.push(rec2);

    let (rec3, _consistent) = Layer3Cs::evaluate(problem);
    records.push(rec3);

    let (rec4, _min_sep) = Layer4CsQ::evaluate(problem);
    records.push(rec4);

    let (rec5, _diam) = Layer5Q::evaluate(problem);
    records.push(rec5);

    let (rec6, _has_residual) = Layer6A::evaluate(problem, &phi1, &gamma2);
    records.push(rec6);

    let (rec7, is_refused) = Layer7Or::evaluate(problem, &gamma2);
    records.push(rec7);
    let is_refused = is_refused || records.iter().any(|record| !record.succeeded);

    let (rec8, decision, token) =
        Layer8Fda::evaluate_with_grant(problem, &phi1, &gamma2, is_refused, external_grant);
    records.push(rec8);

    let evidence_digest = evidence_digest(problem, external_grant, &records);

    Layer9CodaGtla::terminalize(
        problem,
        Some(phi1),
        Some(gamma2),
        witness,
        decision,
        token,
        records,
        None,
        Some(primal_repair),
        evidence_digest,
    )
}

fn evidence_digest(
    problem: &ProblemInstance,
    external_grant: Option<&ExternalAuthorityGrant>,
    records: &[crate::coda::types::LayerExecutionRecord],
) -> String {
    let evidence = serde_json::json!({
        "schema": "omega.coda.pipeline.evidence.v1",
        "problem_id": problem.problem_id,
        "raw_data": problem.raw_data,
        "candidate_sieve": problem.candidate_sieve,
        "coarse_profile": problem.coarse_profile,
        "fine_profile": problem.fine_profile,
        "projection_map": problem.projection_map,
        "local_sections": problem.local_sections,
        "overlaps": problem.overlaps.iter().collect::<Vec<_>>(),
        "d0": problem.d0,
        "d1": problem.d1,
        "defect_cochain": problem.defect_cochain,
        "fda_license_granted": problem.fda_license_granted,
        "enclosure_interval": problem.enclosure_interval,
        "external_grant": external_grant,
        "records": records,
    });
    format!(
        "{:x}",
        Sha256::digest(
            serde_json::to_vec(&evidence).expect("canonical evidence consists of JSON values")
        )
    )
}
