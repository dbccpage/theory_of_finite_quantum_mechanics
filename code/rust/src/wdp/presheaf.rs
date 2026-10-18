
use crate::error::WdpError;
use crate::types::AuthorityEffect;
use omega_category_theory::finite_report_descent::{
    DescentError, DescentOutcome, FiniteReportPresheaf,
};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CoveringSieve {
    pub carrier: BTreeSet<String>,
    pub contexts: BTreeMap<String, BTreeSet<String>>,
}

impl CoveringSieve {
    pub fn new(
        carrier: BTreeSet<String>,
        contexts: BTreeMap<String, BTreeSet<String>>,
    ) -> Result<Self, WdpError> {
        let mut covered: BTreeSet<String> = BTreeSet::new();
        for (cid, pts) in &contexts {
            for pt in pts {
                if !carrier.contains(pt) {
                    return Err(WdpError::InvalidInput {
                        detail: format!("context {cid} contains element {pt} outside carrier"),
                    });
                }
                covered.insert(pt.clone());
            }
        }
        if covered != carrier {
            let missing: Vec<String> = carrier.difference(&covered).cloned().collect();
            return Err(WdpError::IncompleteCoverage { missing });
        }
        Ok(Self { carrier, contexts })
    }

    pub fn overlap(&self, cid_i: &str, cid_j: &str) -> BTreeSet<String> {
        let empty = BTreeSet::new();
        let pts_i = self.contexts.get(cid_i).unwrap_or(&empty);
        let pts_j = self.contexts.get(cid_j).unwrap_or(&empty);
        pts_i.intersection(pts_j).cloned().collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct LocalReportSection {
    pub context_id: String,
    pub assignments: BTreeMap<String, String>,
}

impl LocalReportSection {
    pub fn new(context_id: String, assignments: BTreeMap<String, String>) -> Self {
        Self {
            context_id,
            assignments,
        }
    }

    pub fn get_value(&self, point: &str) -> Option<&str> {
        self.assignments.get(point).map(|s| s.as_str())
    }

    pub fn domain(&self) -> BTreeSet<String> {
        self.assignments.keys().cloned().collect()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SheafGluingObstruction {
    pub context_i: String,
    pub context_j: String,
    pub point: String,
    pub value_i: String,
    pub value_j: String,
    pub reason: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DescentReceipt {
    pub sieve: CoveringSieve,
    pub local_sections: Vec<LocalReportSection>,
    pub is_compatible: bool,
    pub global_section: Option<BTreeMap<String, String>>,
    pub obstruction: Option<SheafGluingObstruction>,
    pub authority_effect: AuthorityEffect,
}

pub fn solve_observer_descent(
    sieve: &CoveringSieve,
    local_sections: &[LocalReportSection],
) -> Result<DescentReceipt, WdpError> {
    CoveringSieve::new(sieve.carrier.clone(), sieve.contexts.clone())?;
    let mut sec_map: BTreeMap<String, &LocalReportSection> = BTreeMap::new();
    for sec in local_sections {
        if !sieve.contexts.contains_key(&sec.context_id) {
            return Err(WdpError::InvalidInput {
                detail: format!("unknown section context {}", sec.context_id),
            });
        }
        if sec_map.contains_key(&sec.context_id) {
            return Err(WdpError::InvalidInput {
                detail: format!("duplicate section for context {}", sec.context_id),
            });
        }
        sec_map.insert(sec.context_id.clone(), sec);
    }

    for (cid, pts) in &sieve.contexts {
        let sec = sec_map.get(cid).ok_or_else(|| WdpError::InvalidInput {
            detail: format!("missing section for context {cid}"),
        })?;
        if &sec.domain() != pts {
            return Err(WdpError::SectionDomainMismatch {
                context: cid.clone(),
                expected: pts.iter().cloned().collect(),
                found: sec.domain().into_iter().collect(),
            });
        }
    }

    let contexts: Vec<String> = sieve.contexts.keys().cloned().collect();
    for i in 0..contexts.len() {
        for j in (i + 1)..contexts.len() {
            let cid_i = &contexts[i];
            let cid_j = &contexts[j];
            let overlap_pts = sieve.overlap(cid_i, cid_j);
            let sec_i = sec_map[cid_i];
            let sec_j = sec_map[cid_j];
            for pt in &overlap_pts {
                let v_i = sec_i.get_value(pt).unwrap_or("");
                let v_j = sec_j.get_value(pt).unwrap_or("");
                if v_i != v_j {
                    let obstruction = SheafGluingObstruction {
                        context_i: cid_i.clone(),
                        context_j: cid_j.clone(),
                        point: pt.clone(),
                        value_i: v_i.to_string(),
                        value_j: v_j.to_string(),
                        reason: format!(
                            "local report mismatch at overlap point {pt}: {v_i} != {v_j}"
                        ),
                    };
                    return Ok(DescentReceipt {
                        sieve: sieve.clone(),
                        local_sections: local_sections.to_vec(),
                        is_compatible: false,
                        global_section: None,
                        obstruction: Some(obstruction),
                        authority_effect: AuthorityEffect::None,
                    });
                }
            }
        }
    }

    let mut global_dict: BTreeMap<String, String> = BTreeMap::new();
    for (cid, _) in &sieve.contexts {
        let sec = sec_map[cid];
        for (pt, val) in &sec.assignments {
            global_dict.insert(pt.clone(), val.clone());
        }
    }

    Ok(DescentReceipt {
        sieve: sieve.clone(),
        local_sections: local_sections.to_vec(),
        is_compatible: true,
        global_section: Some(global_dict),
        obstruction: None,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn restrict_report(
    report: &BTreeMap<String, String>,
    subset: &BTreeSet<String>,
) -> Result<BTreeMap<String, String>, WdpError> {
    subset
        .iter()
        .map(|point| {
            report
                .get(point)
                .cloned()
                .map(|value| (point.clone(), value))
                .ok_or_else(|| WdpError::ElementNotFound {
                    element: point.clone(),
                })
        })
        .collect()
}

pub fn verify_global_report(
    sieve: &CoveringSieve,
    local_sections: &[LocalReportSection],
    candidate: &BTreeMap<String, String>,
) -> Result<bool, WdpError> {
    let checked = solve_observer_descent(sieve, local_sections)?;
    if !checked.is_compatible || candidate.keys().cloned().collect::<BTreeSet<_>>() != sieve.carrier
    {
        return Ok(false);
    }
    for section in local_sections {
        let subset = &sieve.contexts[&section.context_id];
        if restrict_report(candidate, subset)? != section.assignments {
            return Ok(false);
        }
    }
    Ok(true)
}

pub fn verify_descent_receipt(receipt: &DescentReceipt) -> Result<bool, WdpError> {
    let checked = solve_observer_descent(&receipt.sieve, &receipt.local_sections)?;
    Ok(receipt.authority_effect == AuthorityEffect::None
        && receipt.is_compatible == checked.is_compatible
        && receipt.global_section == checked.global_section
        && receipt.obstruction == checked.obstruction)
}

pub fn general_presheaf_descent(
    presheaf: &FiniteReportPresheaf,
    target: u64,
    cover: &[u64],
    locals: &[usize],
) -> Result<DescentOutcome, DescentError> {
    presheaf
        .descent_fiber(target, cover, locals)
        .map(|fiber| fiber.outcome())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sheaf_descent_gluing_success() {
        let carrier = BTreeSet::from(["x0".to_string(), "x1".to_string(), "x2".to_string()]);
        let mut contexts = BTreeMap::new();
        contexts.insert(
            "U0".to_string(),
            BTreeSet::from(["x0".to_string(), "x1".to_string()]),
        );
        contexts.insert(
            "U1".to_string(),
            BTreeSet::from(["x1".to_string(), "x2".to_string()]),
        );
        let sieve = CoveringSieve::new(carrier, contexts).unwrap();

        let s0 = LocalReportSection::new(
            "U0".to_string(),
            BTreeMap::from([
                ("x0".to_string(), "val0".to_string()),
                ("x1".to_string(), "val1".to_string()),
            ]),
        );
        let s1 = LocalReportSection::new(
            "U1".to_string(),
            BTreeMap::from([
                ("x1".to_string(), "val1".to_string()),
                ("x2".to_string(), "val2".to_string()),
            ]),
        );

        let receipt = solve_observer_descent(&sieve, &[s0, s1]).unwrap();
        assert!(receipt.is_compatible);
        assert!(receipt.obstruction.is_none());
        let global = receipt.global_section.unwrap();
        assert_eq!(global.get("x0").unwrap(), "val0");
        assert_eq!(global.get("x1").unwrap(), "val1");
        assert_eq!(global.get("x2").unwrap(), "val2");
    }

    #[test]
    fn test_sheaf_descent_obstruction_detected() {
        let carrier = BTreeSet::from(["x0".to_string(), "x1".to_string(), "x2".to_string()]);
        let mut contexts = BTreeMap::new();
        contexts.insert(
            "U0".to_string(),
            BTreeSet::from(["x0".to_string(), "x1".to_string()]),
        );
        contexts.insert(
            "U1".to_string(),
            BTreeSet::from(["x1".to_string(), "x2".to_string()]),
        );
        let sieve = CoveringSieve::new(carrier, contexts).unwrap();

        let s0 = LocalReportSection::new(
            "U0".to_string(),
            BTreeMap::from([
                ("x0".to_string(), "val0".to_string()),
                ("x1".to_string(), "A".to_string()),
            ]),
        );
        let s1 = LocalReportSection::new(
            "U1".to_string(),
            BTreeMap::from([
                ("x1".to_string(), "B".to_string()),
                ("x2".to_string(), "val2".to_string()),
            ]),
        );

        let receipt = solve_observer_descent(&sieve, &[s0, s1]).unwrap();
        assert!(!receipt.is_compatible);
        let obs = receipt.obstruction.unwrap();
        assert_eq!(obs.point, "x1");
        assert_eq!(obs.value_i, "A");
        assert_eq!(obs.value_j, "B");
    }
    fn singleton_cover() -> (CoveringSieve, Vec<LocalReportSection>) {
        let sieve = CoveringSieve::new(
            BTreeSet::from(["x".to_string()]),
            BTreeMap::from([("U".to_string(), BTreeSet::from(["x".to_string()]))]),
        )
        .unwrap();
        let sections = vec![LocalReportSection::new(
            "U".to_string(),
            BTreeMap::from([("x".to_string(), "A".to_string())]),
        )];
        (sieve, sections)
    }

    #[test]
    fn rejects_unchecked_covers_and_unknown_sections() {
        let (mut sieve, mut sections) = singleton_cover();
        sections.push(LocalReportSection::new(
            "ghost".to_string(),
            BTreeMap::new(),
        ));
        assert!(solve_observer_descent(&sieve, &sections).is_err());
        sections.pop();
        sieve.carrier.insert("uncovered".to_string());
        assert!(matches!(
            solve_observer_descent(&sieve, &sections),
            Err(WdpError::IncompleteCoverage { .. })
        ));
    }

    #[test]
    fn restrictions_compose_and_detect_missing_data() {
        let report = BTreeMap::from([
            ("x".to_string(), "A".to_string()),
            ("y".to_string(), "B".to_string()),
            ("z".to_string(), "C".to_string()),
        ]);
        let all = report.keys().cloned().collect();
        let middle = BTreeSet::from(["x".to_string(), "y".to_string()]);
        let subset = BTreeSet::from(["x".to_string()]);
        assert_eq!(restrict_report(&report, &all).unwrap(), report);
        assert_eq!(
            restrict_report(&restrict_report(&report, &middle).unwrap(), &subset).unwrap(),
            restrict_report(&report, &subset).unwrap()
        );
        assert!(restrict_report(&report, &BTreeSet::from(["missing".to_string()])).is_err());
        assert!(restrict_report(&report, &BTreeSet::new())
            .unwrap()
            .is_empty());
    }

    #[test]
    fn gluing_verifier_binds_domain_values_and_receipt() {
        let (sieve, sections) = singleton_cover();
        let mut receipt = solve_observer_descent(&sieve, &sections).unwrap();
        assert!(verify_descent_receipt(&receipt).unwrap());
        let mut global = receipt.global_section.clone().unwrap();
        assert!(verify_global_report(&sieve, &sections, &global).unwrap());
        global.insert("x".to_string(), "forged".to_string());
        assert!(!verify_global_report(&sieve, &sections, &global).unwrap());
        receipt.global_section = Some(global);
        assert!(!verify_descent_receipt(&receipt).unwrap());
        let mut extra = sections[0].assignments.clone();
        extra.insert("outside".to_string(), "A".to_string());
        assert!(!verify_global_report(&sieve, &sections, &extra).unwrap());
    }

    #[test]
    fn empty_cover_glues_to_unique_empty_function() {
        let sieve = CoveringSieve::new(BTreeSet::new(), BTreeMap::new()).unwrap();
        let receipt = solve_observer_descent(&sieve, &[]).unwrap();
        assert_eq!(receipt.global_section, Some(BTreeMap::new()));
        assert!(verify_global_report(&sieve, &[], &BTreeMap::new()).unwrap());
        assert!(verify_descent_receipt(&receipt).unwrap());
    }
}
