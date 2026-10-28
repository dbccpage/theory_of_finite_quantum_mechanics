use crate::types::AuthorityEffect;
use tfqm_combinatorics::color_constraints::{
    minimum_color_violations, ColorConstraintError, MinimumColorViolations,
};
use std::collections::{BTreeMap, BTreeSet};

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/wdp_lggr_chromatic.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: a triangle with two colors and monochrome edges forbidden has minimum violation count 1";
pub const AUTHORITY_EFFECT_TEXT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum ChromaticPresentationError {
    #[error("duplicate vertex name")]
    DuplicateVertex,
    #[error("unknown edge endpoint: {0}")]
    Endpoint(String),
    #[error(transparent)]
    Search(#[from] ColorConstraintError),
    #[error("binary float token refused")]
    BinaryFloatRefused,
    #[error("boolean is not an exact integer")]
    BooleanAsNumber,
    #[error("token is not an exact integer")]
    InexactToken,
    #[error("integer token overflow")]
    Overflow,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChromaticConstraintSystem {
    pub vertices: Vec<String>,
    pub edges: Vec<(String, String)>,
    pub num_colors: usize,
    pub forbidden_color_pairs: BTreeSet<(usize, usize)>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChromaticCertificate {
    pub presentation: ChromaticConstraintSystem,
    pub minimum: MinimumColorViolations,
    pub authority_effect: AuthorityEffect,
}

pub fn admit_exact_integer(token: &str) -> Result<i64, ChromaticPresentationError> {
    if token == "true" || token == "false" {
        return Err(ChromaticPresentationError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(ChromaticPresentationError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, ChromaticPresentationError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(ChromaticPresentationError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(ChromaticPresentationError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(ChromaticPresentationError::Overflow)?;
    }
    Ok(value)
}

fn vertex_index(
    indices: &BTreeMap<&String, usize>,
    name: &String,
) -> Result<usize, ChromaticPresentationError> {
    indices
        .get(name)
        .copied()
        .ok_or_else(|| ChromaticPresentationError::Endpoint(name.clone()))
}

impl ChromaticConstraintSystem {
    pub fn evaluate(
        &self,
        max_colorings: usize,
        max_edge_checks: usize,
    ) -> Result<ChromaticCertificate, ChromaticPresentationError> {
        let indices = self.vertex_indices()?;
        let edges = self.indexed_edges(&indices)?;
        let minimum = minimum_color_violations(
            self.vertices.len(),
            &edges,
            self.num_colors,
            &self.forbidden_color_pairs,
            max_colorings,
            max_edge_checks,
        )?;
        Ok(ChromaticCertificate {
            presentation: self.clone(),
            minimum,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn evaluate_color_token(
        &self,
        token: &str,
        max_colorings: usize,
        max_edge_checks: usize,
    ) -> Result<ChromaticCertificate, ChromaticPresentationError> {
        let colors = admit_exact_integer(token)?;
        if colors < 0 {
            return Err(ChromaticPresentationError::InexactToken);
        }
        let mut problem = self.clone();
        problem.num_colors = colors as usize;
        problem.evaluate(max_colorings, max_edge_checks)
    }

    pub fn verify(
        &self,
        candidate: &ChromaticCertificate,
        max_colorings: usize,
        max_edge_checks: usize,
    ) -> Result<bool, ChromaticPresentationError> {
        Ok(*candidate == self.evaluate(max_colorings, max_edge_checks)?)
    }

    fn vertex_indices(&self) -> Result<BTreeMap<&String, usize>, ChromaticPresentationError> {
        let indices: BTreeMap<_, _> = self
            .vertices
            .iter()
            .enumerate()
            .map(|(index, name)| (name, index))
            .collect();
        if indices.len() != self.vertices.len() {
            return Err(ChromaticPresentationError::DuplicateVertex);
        }
        Ok(indices)
    }

    fn indexed_edges(
        &self,
        indices: &BTreeMap<&String, usize>,
    ) -> Result<Vec<(usize, usize)>, ChromaticPresentationError> {
        let mut edges = Vec::new();
        for (tail, head) in &self.edges {
            edges.push((vertex_index(indices, tail)?, vertex_index(indices, head)?));
        }
        Ok(edges)
    }
}

pub fn triangle_two_color() -> ChromaticConstraintSystem {
    ChromaticConstraintSystem {
        vertices: vec!["0".to_string(), "1".to_string(), "2".to_string()],
        edges: vec![
            ("0".to_string(), "1".to_string()),
            ("1".to_string(), "2".to_string()),
            ("2".to_string(), "0".to_string()),
        ],
        num_colors: 2,
        forbidden_color_pairs: BTreeSet::from([(0, 0), (1, 1)]),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    fn show(error: impl std::fmt::Debug) -> String {
        format!("{error:?}")
    }

    #[test]
    fn unit_triangle_needs_one_monochrome_edge() -> Result<(), String> {
        unit_certificate().and_then(|(system, certificate)| unit_claims(system, certificate))
    }

    fn unit_certificate() -> Result<(ChromaticConstraintSystem, ChromaticCertificate), String> {
        let system = triangle_two_color();
        let certificate = system.evaluate(8, 24).map_err(show)?;
        Ok((system, certificate))
    }

    fn unit_claims(
        system: ChromaticConstraintSystem,
        certificate: ChromaticCertificate,
    ) -> Result<(), String> {
        need(certificate.minimum.violated_edges.len() == 1, "violations")?;
        need(certificate.authority_effect == AuthorityEffect::None, "authority")?;
        need(system.verify(&certificate, 8, 24).map_err(show)?, "verify")
    }

    #[test]
    fn integration_color_token_matches_direct_evaluation() -> Result<(), String> {
        let system = triangle_two_color();
        let direct = system.evaluate(8, 24).map_err(|error| format!("{error:?}"))?;
        let token = system
            .evaluate_color_token("2", 8, 24)
            .map_err(|error| format!("{error:?}"))?;
        need(
            direct.minimum.violated_edges.len() == token.minimum.violated_edges.len(),
            "token",
        )?;
        Ok(())
    }

    #[test]
    fn e2e_three_colors_can_avoid_monochrome_edges() -> Result<(), String> {
        e2e_certificate().and_then(e2e_claims)
    }

    fn e2e_certificate() -> Result<ChromaticCertificate, String> {
        let mut system = triangle_two_color();
        system.num_colors = 3;
        system.forbidden_color_pairs = BTreeSet::from([(0, 0), (1, 1), (2, 2)]);
        system.evaluate(27, 81).map_err(show)
    }

    fn e2e_claims(certificate: ChromaticCertificate) -> Result<(), String> {
        need(certificate.minimum.violated_edges.is_empty(), "proper")?;
        need(ORIGIN.contains("wdp_lggr_chromatic.rs"), "origin")?;
        e2e_text()
    }

    fn e2e_text() -> Result<(), String> {
        need(CLAIM.contains("minimum violation count 1"), "claim")?;
        need(AUTHORITY_EFFECT_TEXT.ends_with("None"), "text")
    }

    #[test]
    fn negative_refuses_duplicate_endpoint_and_float() -> Result<(), String> {
        negative_vertices().and_then(|_| negative_tokens())
    }

    fn negative_vertices() -> Result<(), String> {
        let mut system = triangle_two_color();
        system.vertices = vec!["0".to_string(), "0".to_string(), "1".to_string()];
        need(
            matches!(system.evaluate(8, 24), Err(ChromaticPresentationError::DuplicateVertex)),
            "duplicate",
        )?;
        let mut missing = triangle_two_color();
        missing.edges.push(("0".to_string(), "missing".to_string()));
        need(
            matches!(missing.evaluate(8, 24), Err(ChromaticPresentationError::Endpoint(_))),
            "endpoint",
        )
    }

    fn negative_tokens() -> Result<(), String> {
        need(
            admit_exact_integer("2.0") == Err(ChromaticPresentationError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_integer("true") == Err(ChromaticPresentationError::BooleanAsNumber),
            "bool",
        )
    }
}
