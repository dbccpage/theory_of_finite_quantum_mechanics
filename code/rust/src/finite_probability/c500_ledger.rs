//! Count actual preserved original-target and reviewed-clause records, not proofs.
use std::collections::BTreeSet;
pub struct Summary {
    pub targets: usize,
    pub source_satisfied: usize,
    pub scoped_clauses: usize,
    pub open_clauses: usize,
    pub invalid_clauses: usize,
    pub open_ids: Vec<String>,
}
pub fn summarize(
    targets: &[(usize, bool)],
    clauses: &[(String, u8)],
) -> Result<Summary, &'static str> {
    if targets.is_empty()
        || targets.iter().map(|t| t.0).collect::<BTreeSet<_>>().len() != targets.len()
        || clauses.iter().map(|c| &c.0).collect::<BTreeSet<_>>().len() != clauses.len()
        || clauses.iter().any(|c| c.1 > 2)
    {
        return Err("distinct typed target and clause records required");
    }
    Ok(Summary {
        targets: targets.len(),
        source_satisfied: targets.iter().filter(|t| t.1).count(),
        scoped_clauses: clauses.iter().filter(|c| c.1 == 0).count(),
        open_clauses: clauses.iter().filter(|c| c.1 == 1).count(),
        invalid_clauses: clauses.iter().filter(|c| c.1 == 2).count(),
        open_ids: clauses
            .iter()
            .filter(|c| c.1 != 0)
            .map(|c| c.0.clone())
            .collect(),
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn scoped_clauses_do_not_erase_original_targets() {
        let s = summarize(
            &[(301, false), (302, false)],
            &[("M1".into(), 0), ("M2".into(), 1)],
        )
        .unwrap();
        assert_eq!(
            (
                s.targets,
                s.source_satisfied,
                s.scoped_clauses,
                s.open_clauses
            ),
            (2, 0, 1, 1)
        );
    }
    #[test]
    fn source_satisfied_is_only_counted_not_proved() {
        let s = summarize(&[(301, true)], &[("M1".into(), 0)]).unwrap();
        assert_eq!(s.source_satisfied, 1);
    }
    #[test]
    fn duplicate_and_untyped_status_refused() {
        assert!(summarize(&[(301, false), (301, false)], &[]).is_err());
        assert!(summarize(&[(301, false)], &[("M1".into(), 3)]).is_err());
    }
}
