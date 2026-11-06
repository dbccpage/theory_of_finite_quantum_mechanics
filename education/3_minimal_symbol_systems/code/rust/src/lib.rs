//! MSS-N Stage 024: Topos Subobject Monic Factorization and Classifier Pullback Verifier.
//!
//! AuthorityEffect: None. GenesisEffect: None.
//!
//! Verifies whether a candidate subobject morphism m: S -> X and characteristic
//! morphism chi: X -> Omega form an exact pullback square with true: 1 -> Omega
//! over pure boundary packets.
//!
//! Fail-closed defect taxonomy:
//! - `ERR_SUBOBJECT_MONO_DEFECT`: if m fails monicity (non-injective fibers or lands outside X).
//! - `R024_LABEL_MISMATCH`: if chi(m(s)) != true or chi lands outside Omega.
//! - `R024_NOT_PULLBACK`: if {x in X | chi(x) = true} != im(m).
//! - `MALFORMED_PACKET`: if boundary packet fails syntax, balance, or schema rules.

use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub mod simplicial_gauge_gravity;
pub mod smith_normal_form;
pub mod quantum_state_transfer;
pub mod obstruction_detector;
pub mod exact_linear_algebra;
pub mod finite_algebra;



#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Stage024Error {
    ErrSubobjectMonoDefect(String),
    R024LabelMismatch(String),
    R024NotPullback(String),
    MalformedPacket(String),
}

impl std::fmt::Display for Stage024Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Stage024Error::ErrSubobjectMonoDefect(msg) => {
                write!(f, "ERR_SUBOBJECT_MONO_DEFECT: {}", msg)
            }
            Stage024Error::R024LabelMismatch(msg) => write!(f, "R024_LABEL_MISMATCH: {}", msg),
            Stage024Error::R024NotPullback(msg) => write!(f, "R024_NOT_PULLBACK: {}", msg),
            Stage024Error::MalformedPacket(msg) => write!(f, "MALFORMED_PACKET: {}", msg),
        }
    }
}

impl std::error::Error for Stage024Error {}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Stage024Receipt {
    pub stage: u32,
    pub status: String, // "PASS"
    pub monic_certified: bool,
    pub commutativity_certified: bool,
    pub pullback_certified: bool,
    pub subobject_size: usize,
    pub ambient_size: usize,
    pub truth_values_count: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Stage024Candidate {
    pub subobject_elements: BTreeSet<String>,
    pub ambient_elements: BTreeSet<String>,
    /// Monomorphism m: S -> X
    pub monic_map: BTreeMap<String, String>,
    pub truth_values: BTreeSet<String>,
    pub true_value: String,
    /// Characteristic morphism chi: X -> Omega
    pub char_map: BTreeMap<String, String>,
}

impl Stage024Candidate {
    pub fn new(
        subobject: Vec<&str>,
        ambient: Vec<&str>,
        monic: Vec<(&str, &str)>,
        truth_values: Vec<&str>,
        true_val: &str,
        char_map: Vec<(&str, &str)>,
    ) -> Self {
        Self {
            subobject_elements: subobject.into_iter().map(String::from).collect(),
            ambient_elements: ambient.into_iter().map(String::from).collect(),
            monic_map: monic
                .into_iter()
                .map(|(s, x)| (s.to_string(), x.to_string()))
                .collect(),
            truth_values: truth_values.into_iter().map(String::from).collect(),
            true_value: true_val.to_string(),
            char_map: char_map
                .into_iter()
                .map(|(x, t)| (x.to_string(), t.to_string()))
                .collect(),
        }
    }

    /// Parse a boundary packet representation of a Stage 024 candidate.
    ///
    /// Pure boundary packet grammar:
    /// `<stage024<sub<s0><s1>><amb<x0><x1><x2>><m<<s0><x0>><<s1><x1>>><truth<true><false>><true<true>><chi<<x0><true>><<x1><true>><<x2><false>>>>`
    pub fn parse_boundary_packet(packet: &str) -> Result<Self, Stage024Error> {
        let p = packet.trim();
        if !p.starts_with("<stage024") || !p.ends_with('>') {
            return Err(Stage024Error::MalformedPacket(format!(
                "Packet must start with '<stage024' and end with '>': {}",
                p
            )));
        }

        let inner = &p[9..p.len() - 1].trim(); // strip <stage024 and >

        let blocks = split_top_level_blocks(inner)?;
        let mut sub_elems = None;
        let mut amb_elems = None;
        let mut m_pairs = None;
        let mut truth_vals = None;
        let mut true_val = None;
        let mut chi_pairs = None;

        for (tag, body) in blocks {
            match tag.as_str() {
                "sub" => {
                    sub_elems = Some(extract_leaf_tokens(&body));
                }
                "amb" => {
                    amb_elems = Some(extract_leaf_tokens(&body));
                }
                "m" => {
                    m_pairs = Some(extract_pair_tokens(&body)?);
                }
                "truth" => {
                    truth_vals = Some(extract_leaf_tokens(&body));
                }
                "true" => {
                    let tokens = extract_leaf_tokens(&body);
                    if tokens.len() != 1 {
                        return Err(Stage024Error::MalformedPacket(
                            "Must declare exactly one item inside <true<val>>".into(),
                        ));
                    }
                    true_val = Some(tokens[0].clone());
                }
                "chi" => {
                    chi_pairs = Some(extract_pair_tokens(&body)?);
                }
                unknown => {
                    return Err(Stage024Error::MalformedPacket(format!(
                        "Unrecognized stage024 section: <{}",
                        unknown
                    )));
                }
            }
        }

        let sub_list = sub_elems
            .ok_or_else(|| Stage024Error::MalformedPacket("Missing <sub...> section".into()))?;
        let amb_list = amb_elems
            .ok_or_else(|| Stage024Error::MalformedPacket("Missing <amb...> section".into()))?;
        let m_list = m_pairs
            .ok_or_else(|| Stage024Error::MalformedPacket("Missing <m...> section".into()))?;
        let truth_list = truth_vals
            .ok_or_else(|| Stage024Error::MalformedPacket("Missing <truth...> section".into()))?;
        let true_element = true_val
            .ok_or_else(|| Stage024Error::MalformedPacket("Missing <true...> section".into()))?;
        let chi_list = chi_pairs
            .ok_or_else(|| Stage024Error::MalformedPacket("Missing <chi...> section".into()))?;

        let mut sub_set = BTreeSet::new();
        for s in sub_list {
            sub_set.insert(s);
        }

        let mut amb_set = BTreeSet::new();
        for a in amb_list {
            amb_set.insert(a);
        }

        let mut monic_map = BTreeMap::new();
        for (s, x) in m_list {
            monic_map.insert(s, x);
        }

        let mut truth_set = BTreeSet::new();
        for t in truth_list {
            truth_set.insert(t);
        }

        let mut char_map = BTreeMap::new();
        for (x, t) in chi_list {
            char_map.insert(x, t);
        }

        Ok(Self {
            subobject_elements: sub_set,
            ambient_elements: amb_set,
            monic_map,
            truth_values: truth_set,
            true_value: true_element,
            char_map,
        })
    }

    /// Execute fail-closed Stage 024 pullback verification.
    pub fn verify(&self) -> Result<Stage024Receipt, Stage024Error> {
        // 1. Verify totality of monic map m: S -> X
        for s in &self.subobject_elements {
            match self.monic_map.get(s) {
                Some(x) => {
                    if !self.ambient_elements.contains(x) {
                        return Err(Stage024Error::ErrSubobjectMonoDefect(format!(
                            "Morphism m({}) = {} lands outside ambient set X",
                            s, x
                        )));
                    }
                }
                None => {
                    return Err(Stage024Error::ErrSubobjectMonoDefect(format!(
                        "Morphism m is not total on S: missing value for {}",
                        s
                    )));
                }
            }
        }

        // 2. Monic Property: m must be strictly injective
        let mut seen_targets = BTreeMap::new();
        for (s, x) in &self.monic_map {
            if let Some(prev_s) = seen_targets.insert(x, s) {
                return Err(Stage024Error::ErrSubobjectMonoDefect(format!(
                    "Morphism m is not monic: fibers collide m({}) = m({}) = {}",
                    prev_s, s, x
                )));
            }
        }

        // 3. Totality of characteristic morphism chi: X -> Omega
        for x in &self.ambient_elements {
            match self.char_map.get(x) {
                Some(t) => {
                    if !self.truth_values.contains(t) {
                        return Err(Stage024Error::R024LabelMismatch(format!(
                            "chi({}) = {} lands outside truth object Omega",
                            x, t
                        )));
                    }
                }
                None => {
                    return Err(Stage024Error::R024LabelMismatch(format!(
                        "Characteristic map chi is not total: missing value for {}",
                        x
                    )));
                }
            }
        }

        // 4. Commutativity: for all s in S, chi(m(s)) == true
        for s in &self.subobject_elements {
            let x = &self.monic_map[s];
            let t = &self.char_map[x];
            if t != &self.true_value {
                return Err(Stage024Error::R024LabelMismatch(format!(
                    "Diagram does not commute: chi(m({})) = chi({}) = {} != true ({})",
                    s, x, t, self.true_value
                )));
            }
        }

        // 5. Pullback Universal Property: {x in X | chi(x) = true} == im(m)
        let image_m: BTreeSet<&String> = self.monic_map.values().collect();
        for x in &self.ambient_elements {
            let t = &self.char_map[x];
            let is_true = t == &self.true_value;
            let in_image = image_m.contains(x);

            if is_true && !in_image {
                return Err(Stage024Error::R024NotPullback(format!(
                    "Pullback failure: chi({}) = true, but {} is not in the image of m",
                    x, x
                )));
            }
            if !is_true && in_image {
                return Err(Stage024Error::R024NotPullback(format!(
                    "Pullback failure: {} is in the image of m, but chi({}) = {} != true",
                    x, x, t
                )));
            }
        }

        Ok(Stage024Receipt {
            stage: 24,
            status: "PASS".to_string(),
            monic_certified: true,
            commutativity_certified: true,
            pullback_certified: true,
            subobject_size: self.subobject_elements.len(),
            ambient_size: self.ambient_elements.len(),
            truth_values_count: self.truth_values.len(),
        })
    }
}

// ---------------------------------------------------------------------------
// Pure Boundary Packet Block Parser
// ---------------------------------------------------------------------------

fn split_top_level_blocks(s: &str) -> Result<Vec<(String, String)>, Stage024Error> {
    let mut blocks = Vec::new();
    let mut depth = 0;
    let mut start_idx = 0;

    for (idx, c) in s.char_indices() {
        if c == '<' {
            if depth == 0 {
                start_idx = idx;
            }
            depth += 1;
        } else if c == '>' {
            depth -= 1;
            if depth == 0 {
                let full_block = &s[start_idx..=idx];
                // Strip outer < and >
                let inside = &full_block[1..full_block.len() - 1];
                // Find tag (up to first '<' or whitespace)
                let tag_end = inside
                    .find(|ch: char| ch == '<' || ch.is_whitespace())
                    .unwrap_or(inside.len());
                let tag = inside[..tag_end].trim().to_string();
                let body = inside[tag_end..].trim().to_string();
                blocks.push((tag, body));
            }
        }
    }

    if depth != 0 {
        return Err(Stage024Error::MalformedPacket(
            "Unbalanced angle brackets in packet".into(),
        ));
    }

    Ok(blocks)
}

fn extract_leaf_tokens(s: &str) -> Vec<String> {
    let mut tokens = Vec::new();
    let mut in_leaf = false;
    let mut current = String::new();

    for c in s.chars() {
        if c == '<' {
            in_leaf = true;
            current.clear();
        } else if c == '>' {
            if in_leaf && !current.is_empty() {
                tokens.push(current.trim().to_string());
            }
            in_leaf = false;
            current.clear();
        } else if in_leaf {
            current.push(c);
        }
    }
    tokens
}

fn extract_pair_tokens(s: &str) -> Result<Vec<(String, String)>, Stage024Error> {
    let mut pairs = Vec::new();
    let mut depth = 0;
    let mut pair_start = 0;

    for (idx, c) in s.char_indices() {
        if c == '<' {
            if depth == 0 {
                pair_start = idx;
            }
            depth += 1;
        } else if c == '>' {
            depth -= 1;
            if depth == 0 {
                let pair_block = &s[pair_start..=idx];
                let tokens = extract_leaf_tokens(pair_block);
                if tokens.len() == 2 {
                    pairs.push((tokens[0].clone(), tokens[1].clone()));
                } else {
                    return Err(Stage024Error::MalformedPacket(format!(
                        "Expected pair <<a<b>>, got: {}",
                        pair_block
                    )));
                }
            }
        }
    }

    if depth != 0 {
        return Err(Stage024Error::MalformedPacket(
            "Unbalanced brackets inside relation/pairs section".into(),
        ));
    }

    Ok(pairs)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_stage_024_pullback_receipt() {
        let candidate = Stage024Candidate::new(
            vec!["s0", "s1"],
            vec!["x0", "x1", "x2"],
            vec![("s0", "x0"), ("s1", "x1")],
            vec!["true", "false"],
            "true",
            vec![("x0", "true"), ("x1", "true"), ("x2", "false")],
        );

        let receipt = candidate.verify().expect("Valid candidate must PASS");
        assert_eq!(receipt.stage, 24);
        assert_eq!(receipt.status, "PASS");
        assert!(receipt.monic_certified);
        assert!(receipt.commutativity_certified);
        assert!(receipt.pullback_certified);
        assert_eq!(receipt.subobject_size, 2);
        assert_eq!(receipt.ambient_size, 3);
    }

    #[test]
    fn test_fail_closed_non_monic_defect() {
        // Non-injective: m(s0) = x0 and m(s1) = x0
        let candidate = Stage024Candidate::new(
            vec!["s0", "s1"],
            vec!["x0", "x1"],
            vec![("s0", "x0"), ("s1", "x0")],
            vec!["true", "false"],
            "true",
            vec![("x0", "true"), ("x1", "false")],
        );

        let err = candidate.verify().unwrap_err();
        match err {
            Stage024Error::ErrSubobjectMonoDefect(msg) => {
                assert!(msg.contains("fibers collide"));
            }
            other => panic!("Expected ErrSubobjectMonoDefect, got {:?}", other),
        }
    }

    #[test]
    fn test_fail_closed_label_mismatch_non_commuting() {
        // chi(m(s1)) = false != true
        let candidate = Stage024Candidate::new(
            vec!["s0", "s1"],
            vec!["x0", "x1"],
            vec![("s0", "x0"), ("s1", "x1")],
            vec!["true", "false"],
            "true",
            vec![("x0", "true"), ("x1", "false")],
        );

        let err = candidate.verify().unwrap_err();
        match err {
            Stage024Error::R024LabelMismatch(msg) => {
                assert!(msg.contains("Diagram does not commute"));
            }
            other => panic!("Expected R024LabelMismatch, got {:?}", other),
        }
    }

    #[test]
    fn test_fail_closed_not_pullback_defect() {
        // chi(x2) = true, but x2 is not in im(m)
        let candidate = Stage024Candidate::new(
            vec!["s0"],
            vec!["x0", "x2"],
            vec![("s0", "x0")],
            vec!["true", "false"],
            "true",
            vec![("x0", "true"), ("x2", "true")],
        );

        let err = candidate.verify().unwrap_err();
        match err {
            Stage024Error::R024NotPullback(msg) => {
                assert!(msg.contains("not in the image of m"));
            }
            other => panic!("Expected R024NotPullback, got {:?}", other),
        }
    }

    #[test]
    fn test_boundary_packet_round_trip_parse_and_verify() {
        let packet = "<stage024<sub<s0><s1>><amb<x0><x1><x2>><m<<s0><x0>><<s1><x1>>><truth<true><false>><true<true>><chi<<x0><true>><<x1><true>><<x2><false>>>>";
        let candidate = Stage024Candidate::parse_boundary_packet(packet)
            .expect("Valid packet must parse");
        let receipt = candidate.verify().expect("Parsed packet must verify");
        assert_eq!(receipt.status, "PASS");
        assert_eq!(receipt.ambient_size, 3);
        assert_eq!(receipt.subobject_size, 2);
    }
}
