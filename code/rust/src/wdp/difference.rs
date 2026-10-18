// Executable finite evidence; AuthorityEffect: None.
//! Root W: Genesis Primitive Difference, Carrier Symmetries & Presentation Blind Spots.
//! Formalizes Chapter 1 & Chapter 3 foundations.

use crate::error::WdpError;
use crate::types::AuthorityEffect;
use omega_category_theory::finite_report_query::{
    ReportQueryDecision, ReportQueryProblem, ReportQueryRefusal,
};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

/// A finite carrier set of discrete named states.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct Carrier {
    pub states: BTreeSet<String>,
}

impl Carrier {
    pub fn new<I, S>(iter: I) -> Result<Self, WdpError>
    where
        I: IntoIterator<Item = S>,
        S: Into<String>,
    {
        let states: BTreeSet<String> = iter.into_iter().map(Into::into).collect();
        if states.is_empty() {
            return Err(WdpError::InvalidInput {
                detail: "carrier cannot be empty".to_string(),
            });
        }
        Ok(Self { states })
    }

    pub fn size(&self) -> usize {
        self.states.len()
    }

    pub fn contains(&self, state: &str) -> bool {
        self.states.contains(state)
    }
}

/// Primitive difference outcome comparing two elements on a carrier.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum DifferenceOutcome {
    Same,
    Different,
}

/// Computes primitive difference delta_0(x, y) on a carrier.
pub fn primitive_difference(x: &str, y: &str) -> DifferenceOutcome {
    if x == y {
        DifferenceOutcome::Same
    } else {
        DifferenceOutcome::Different
    }
}

/// A presentation map q: X -> P mapping carrier states to presented tokens.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PresentationMap {
    pub carrier: Carrier,
    pub mapping: BTreeMap<String, String>,
    pub authority_effect: AuthorityEffect,
}

impl PresentationMap {
    pub fn new(carrier: Carrier, mapping: BTreeMap<String, String>) -> Result<Self, WdpError> {
        for s in &carrier.states {
            if !mapping.contains_key(s) {
                return Err(WdpError::InvalidInput {
                    detail: format!("presentation map missing assignment for carrier state {s}"),
                });
            }
        }
        if let Some(extra) = mapping.keys().find(|k| !carrier.states.contains(*k)) {
            return Err(WdpError::InvalidInput {
                detail: format!("presentation map assigns a state outside the carrier: {extra}"),
            });
        }
        Ok(Self {
            carrier,
            mapping,
            authority_effect: AuthorityEffect::None,
        })
    }

    /// Decides whether a query on the carrier can be read from this
    /// presentation, through the DP-1 owner
    /// `omega_category_theory::finite_report_query`. The presentation is the
    /// report with the declared `report_codomain` (every presented token must
    /// lie in it); the query table must be total on the carrier with values
    /// in `query_codomain`. The result is a decoder on the realized image or a
    /// collision witness; unrealized codomain tokens play no part.
    pub fn decide_query(
        &self,
        report_codomain: &[String],
        query_codomain: &[String],
        query_rows: &[(String, String)],
    ) -> Result<ReportQueryDecision<String, String, String>, ReportQueryRefusal<String>> {
        let source: Vec<String> = self.carrier.states.iter().cloned().collect();
        let report_rows: Vec<(String, String)> = self
            .mapping
            .iter()
            .map(|(k, v)| (k.clone(), v.clone()))
            .collect();
        let problem = ReportQueryProblem::new(
            &source,
            report_codomain,
            query_codomain,
            &report_rows,
            query_rows,
        )?;
        Ok(problem.decide())
    }

    pub fn present(&self, state: &str) -> Result<&str, WdpError> {
        self.mapping
            .get(state)
            .map(|s| s.as_str())
            .ok_or_else(|| WdpError::ElementNotFound {
                element: state.to_string(),
            })
    }

    /// Computes presentation fibers q^-1(p) for every presented token p in P.
    pub fn fibers(&self) -> BTreeMap<String, BTreeSet<String>> {
        let mut fibers: BTreeMap<String, BTreeSet<String>> = BTreeMap::new();
        for (state, token) in &self.mapping {
            fibers
                .entry(token.clone())
                .or_default()
                .insert(state.clone());
        }
        fibers
    }

    /// Identifies presentation blind spots: fibers containing >= 2 distinct states.
    pub fn blind_spots(&self) -> BTreeMap<String, BTreeSet<String>> {
        self.fibers()
            .into_iter()
            .filter(|(_, states)| states.len() >= 2)
            .collect()
    }

    /// Evaluates whether two distinct states x != y are separable by this presentation.
    pub fn is_separable(&self, x: &str, y: &str) -> Result<bool, WdpError> {
        let px = self.present(x)?;
        let py = self.present(y)?;
        Ok(px != py)
    }
}

impl omega_homotopy_type_theory::primitive_difference::PrimitiveDifference for Carrier {
    type Carrier = String;
    type Diff = DifferenceOutcome;

    fn delta(&self, x: &Self::Carrier, y: &Self::Carrier) -> Self::Diff {
        primitive_difference(x, y)
    }

    fn zero(&self, d: &Self::Diff) -> bool {
        *d == DifferenceOutcome::Same
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use omega_homotopy_type_theory::primitive_difference::PrimitiveDifference;

    #[test]
    fn test_primitive_difference() {
        assert_eq!(primitive_difference("a", "a"), DifferenceOutcome::Same);
        assert_eq!(primitive_difference("a", "b"), DifferenceOutcome::Different);
    }

    #[test]
    fn test_carrier_primitive_difference_trait() {
        let carrier = Carrier::new(vec!["x", "y"]).unwrap();
        let x = "x".to_string();
        let y = "y".to_string();
        assert_eq!(carrier.delta(&x, &x), DifferenceOutcome::Same);
        assert_eq!(carrier.delta(&x, &y), DifferenceOutcome::Different);
        assert!(carrier.zero_rel(&x, &x));
        assert!(!carrier.zero_rel(&x, &y));
    }

    #[test]
    fn test_presentation_fibers_and_blind_spots() {
        let carrier = Carrier::new(vec!["s0", "s1", "s2", "s3"]).unwrap();
        let mut mapping = BTreeMap::new();
        mapping.insert("s0".to_string(), "p0".to_string());
        mapping.insert("s1".to_string(), "p0".to_string()); // s0, s1 in blind spot
        mapping.insert("s2".to_string(), "p1".to_string());
        mapping.insert("s3".to_string(), "p2".to_string());

        let pres = PresentationMap::new(carrier, mapping).unwrap();
        let blind_spots = pres.blind_spots();
        assert_eq!(blind_spots.len(), 1);
        assert!(blind_spots.contains_key("p0"));
        assert_eq!(
            blind_spots.get("p0").unwrap(),
            &BTreeSet::from(["s0".to_string(), "s1".to_string()])
        );

        assert_eq!(pres.is_separable("s0", "s1").unwrap(), false);
        assert_eq!(pres.is_separable("s0", "s2").unwrap(), true);
    }
}
