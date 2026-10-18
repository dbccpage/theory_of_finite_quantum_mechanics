#[path = "../../../tests/omega_wdp/common/genesis_bell_cases.rs"]
mod cases;
use omega_solvers::solver_convex_farkas_feasibility::FeasibilityVerdict;
use omega_wdp::genesis_bell::PassageBellExperiment;
fn main() -> Result<(), String> {
    for (name, request) in [
        (
            "interaction_exposes_hidden_token",
            cases::expose_hidden_token(),
        ),
        ("shared_preparation", cases::token_response_experiment()),
        (
            "setting_dependent_preparation",
            cases::setting_dependent_experiment(),
        ),
    ] {
        let p = PassageBellExperiment::build(&request).map_err(|e| format!("{e:?}"))?;
        let c = p.certify(10000).map_err(|e| format!("{e:?}"))?;
        PassageBellExperiment::verify(&request, &c).map_err(|e| format!("{e:?}"))?;
        let (verdict, witness) = match &c.experiment.extension {
            FeasibilityVerdict::Feasible { point } => ("positive_local_extension", point),
            FeasibilityVerdict::Infeasible { multipliers } => {
                ("no_positive_local_extension", multipliers)
            }
        };
        println!(
            "{}",
            serde_json::json!({
                "case":name,"native_replay_verified":true,
                "rows":c.experiment.rows.iter().map(|r| r.iter().map(ToString::to_string).collect::<Vec<_>>()).collect::<Vec<_>>(),
                "verdict":verdict,"witness":witness.iter().map(ToString::to_string).collect::<Vec<_>>(),
                "shared_prior":c.experiment.prior_difference.is_none(),
                "prior_difference":c.experiment.prior_difference.as_ref().map(|d| serde_json::json!({"context":d.context,
                    "preparation":d.preparation,"first":d.first_weight.to_string(),"other":d.other_weight.to_string()})),
                "joint_collision":c.joint_analysis.collision.as_ref().map(|w| serde_json::json!({
                    "rows":[w.left,w.right],"word":w.word,"answers":[w.left_answer,w.right_answer]})),
                "supported_assignments":p.probability().bell().supported_assignments().len(),
                "scope":"Declared finite protocols and supplied preparation laws; no quantum-realization claim."
            })
        );
    }
    Ok(())
}
