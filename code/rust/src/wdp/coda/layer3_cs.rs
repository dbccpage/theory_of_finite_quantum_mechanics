use num_rational::BigRational;
use omega_category_theory::finite_report_query::{
    ReportQueryDecision, ReportQueryProblem, ReportQueryRefusal,
};
use serde_json::json;
use std::collections::BTreeSet;
use std::fmt;

use crate::coda::types::{LayerExecutionRecord, LayerId, ProblemInstance};

pub struct Layer3Cs;

impl Layer3Cs {
    pub fn evaluate(problem: &ProblemInstance) -> (LayerExecutionRecord, bool) {
        let fine: BTreeSet<i64> = problem.fine_profile.iter().copied().collect();
        let coarse: BTreeSet<i64> = problem.coarse_profile.iter().copied().collect();
        let duplicate_fine = fine.len() != problem.fine_profile.len();
        let duplicate_coarse = coarse.len() != problem.coarse_profile.len();
        let keys: BTreeSet<i64> = problem.projection_map.keys().copied().collect();
        let missing: Vec<i64> = fine.difference(&keys).copied().collect();
        let extraneous: Vec<i64> = keys.difference(&fine).copied().collect();
        let outside: Vec<i64> = problem
            .projection_map
            .iter()
            .filter(|(k, v)| fine.contains(k) && !coarse.contains(v))
            .map(|(k, _)| *k)
            .collect();

        let defects =
            missing.len() + extraneous.len() + outside.len() + duplicate_fine as usize
                + duplicate_coarse as usize;
        let consistent = defects == 0 && !fine.is_empty();
        let msg = if consistent {
            "Projection table is total on the fine profile tokens with images in the coarse \
             profile; no factorization question was decided"
                .to_string()
        } else if fine.is_empty() {
            "Refinement failure: empty fine profile".to_string()
        } else {
            format!(
                "Refinement failure: missing rows {:?}, extraneous rows {:?}, images outside \
                 the coarse profile {:?}, repeated fine tokens {}, repeated coarse tokens {}",
                missing, extraneous, outside, duplicate_fine, duplicate_coarse
            )
        };

        let record = LayerExecutionRecord::new(
            LayerId::CS,
            consistent,
            msg,
            BigRational::from_integer((defects as i64).into()),
        )
        .with_metadata("coarse_profile", json!(problem.coarse_profile))
        .with_metadata("fine_profile", json!(problem.fine_profile))
        .with_metadata("missing_rows", json!(missing))
        .with_metadata("extraneous_rows", json!(extraneous))
        .with_metadata("images_outside_coarse", json!(outside))
        .with_metadata("inconsistent_fibers", json!(defects));

        (record, consistent)
    }

    pub fn evaluate_report_query<X, A, B>(
        source: &[X],
        report_codomain: &[A],
        query_codomain: &[B],
        report_rows: &[(X, A)],
        query_rows: &[(X, B)],
    ) -> (
        LayerExecutionRecord,
        Result<ReportQueryDecision<X, A, B>, ReportQueryRefusal<X>>,
    )
    where
        X: Ord + Clone + fmt::Debug,
        A: Ord + Clone + fmt::Debug,
        B: Ord + Clone + fmt::Debug,
    {
        let outcome = ReportQueryProblem::new(
            source,
            report_codomain,
            query_codomain,
            report_rows,
            query_rows,
        )
        .map(|problem| problem.decide());
        let (succeeded, msg, residual) = match &outcome {
            Ok(ReportQueryDecision::Factorable(cert)) => (
                true,
                format!(
                    "Query factors through the report on the realized image ({} values)",
                    cert.realized_image.len()
                ),
                0,
            ),
            Ok(ReportQueryDecision::Collision(c)) => (
                false,
                format!(
                    "Report collision: {:?} and {:?} share report {:?} with queries {:?} and {:?}",
                    c.first, c.second, c.report, c.first_query, c.second_query
                ),
                1,
            ),
            Err(refusal) => (false, format!("Report/query input refused: {refusal:?}"), 1),
        };
        let record = LayerExecutionRecord::new(
            LayerId::CS,
            succeeded,
            msg,
            BigRational::from_integer(residual.into()),
        )
        .with_metadata("contract", json!("finite_report_query"));
        (record, outcome)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeMap;

    fn base() -> ProblemInstance {
        let mut p = ProblemInstance::new("layer3_unit");
        p.coarse_profile = vec![0, 1];
        p.fine_profile = vec![0, 1];
        p.projection_map = BTreeMap::from([(0, 0), (1, 1)]);
        p
    }

    #[test]
    fn total_table_is_accepted() {
        let (rec, ok) = Layer3Cs::evaluate(&base());
        assert!(ok && rec.succeeded);
    }

    #[test]
    fn extraneous_row_is_refused() {
        let mut p = base();
        p.projection_map.insert(99, 0);
        let (rec, ok) = Layer3Cs::evaluate(&p);
        assert!(!ok && !rec.succeeded);
        assert!(rec.diagnostic_message.contains("extraneous rows [99]"));
    }

    #[test]
    fn missing_row_is_refused() {
        let mut p = base();
        p.projection_map.remove(&1);
        let (_, ok) = Layer3Cs::evaluate(&p);
        assert!(!ok);
    }

    #[test]
    fn repeated_tokens_and_empty_profiles_are_refused() {
        let mut p = base();
        p.fine_profile = vec![0, 1, 1];
        assert!(!Layer3Cs::evaluate(&p).1);
        let mut p = base();
        p.coarse_profile = vec![0, 0, 1];
        assert!(!Layer3Cs::evaluate(&p).1);
        let mut p = base();
        p.fine_profile.clear();
        p.projection_map.clear();
        assert!(!Layer3Cs::evaluate(&p).1);
    }

    #[test]
    fn image_outside_coarse_profile_is_refused() {
        let mut p = base();
        p.projection_map.insert(0, 999);
        assert!(!Layer3Cs::evaluate(&p).1);
    }

    #[test]
    fn report_query_contract_factors_collides_and_refuses() {
        let (rec, out) = Layer3Cs::evaluate_report_query(
            &[0, 1, 2],
            &["p", "q"],
            &[10, 20],
            &[(0, "p"), (1, "p"), (2, "q")],
            &[(0, 10), (1, 10), (2, 20)],
        );
        assert!(rec.succeeded);
        assert!(matches!(out, Ok(ReportQueryDecision::Factorable(_))));

        let (rec, out) = Layer3Cs::evaluate_report_query(
            &[0, 1],
            &["p"],
            &[10, 20],
            &[(0, "p"), (1, "p")],
            &[(0, 10), (1, 20)],
        );
        assert!(!rec.succeeded);
        assert!(matches!(out, Ok(ReportQueryDecision::Collision(_))));

        let (rec, out) = Layer3Cs::evaluate_report_query(
            &[0, 1],
            &["p"],
            &[10],
            &[(0, "p"), (1, "p"), (99, "p")],
            &[(0, 10), (1, 10)],
        );
        assert!(!rec.succeeded);
        assert!(matches!(
            out,
            Err(ReportQueryRefusal::ExtraneousAssignment { .. })
        ));
    }
}
