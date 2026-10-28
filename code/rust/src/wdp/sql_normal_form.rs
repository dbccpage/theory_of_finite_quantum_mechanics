use tfqm_category_theory::finite_functional_dependencies::{
    natural_join, project, BinaryDecompositionReport, FdSchema, FunctionalDependency,
};
use std::collections::BTreeSet;
use thiserror::Error;

pub const ORIGIN: &str =
    "Origin: code/rust/src/wdp/sql_normal_form.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: a binary attribute split reconstructs the original finite instance exactly when the intersection closure determines one component";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const RECONSTRUCTION_TARGET: &str = "original_source_value";
pub const MUTATION_KILLS: u32 = 0;

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum DecompositionError {
    #[error("reconstruction target {target} is not {RECONSTRUCTION_TARGET}")]
    UnsupportedReconstructionTarget { target: String },
    #[error("components {left} and {right} are not a lossless binary split")]
    NonLosslessBinarySplit { left: u16, right: u16 },
    #[error("schema or instance refused: {detail}")]
    Schema { detail: String },
    #[error("join rebuilt {joined} tuples from {source_len} source tuples")]
    ReconstructionFailure { joined: usize, source_len: usize },
    #[error("binary float token refused")]
    BinaryFloatRefused,
    #[error("boolean is not an exact integer budget")]
    BooleanAsNumber,
    #[error("budget token is not an exact integer")]
    InexactToken,
    #[error("budget token overflows u64")]
    Overflow,
}

pub struct DeclaredSetDecomposition {
    pub schema: FdSchema,
    pub components: [u16; 2],
    pub reconstruction_target: String,
    pub rows: Vec<Vec<String>>,
}

pub fn admit_exact_budget(token: &str) -> Result<u64, DecompositionError> {
    if token.eq_ignore_ascii_case("true") || token.eq_ignore_ascii_case("false") {
        return Err(DecompositionError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E' | b'+' | b'-')) {
        return Err(DecompositionError::BinaryFloatRefused);
    }
    if token.is_empty() || !token.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(DecompositionError::InexactToken);
    }
    let mut value = 0u64;
    for byte in token.bytes() {
        let digit = u64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(DecompositionError::Overflow)?;
    }
    Ok(value)
}

fn schema_error(error: impl ToString) -> DecompositionError {
    DecompositionError::Schema {
        detail: error.to_string(),
    }
}

impl DeclaredSetDecomposition {
    pub fn authority_effect(&self) -> &'static str {
        AUTHORITY_EFFECT
    }

    pub fn evaluate_budget_token(
        &self,
        token: &str,
    ) -> Result<BinaryDecompositionReport, DecompositionError> {
        let budget = admit_exact_budget(token)?;
        self.evaluate(budget)
    }

    pub fn evaluate(&self, budget: u64) -> Result<BinaryDecompositionReport, DecompositionError> {
        self.schema_report(budget)
            .and_then(|report| self.finish_report(report))
    }

    fn schema_report(&self, budget: u64) -> Result<BinaryDecompositionReport, DecompositionError> {
        self.require_target()?;
        let report = self
            .schema
            .binary_decomposition(self.components, budget)
            .map_err(schema_error)?;
        self.require_lossless(&report)?;
        Ok(report)
    }

    fn finish_report(
        &self,
        report: BinaryDecompositionReport,
    ) -> Result<BinaryDecompositionReport, DecompositionError> {
        self.schema
            .check_instance(&self.rows)
            .map_err(schema_error)?;
        self.require_reconstruction()?;
        Ok(report)
    }

    fn require_target(&self) -> Result<(), DecompositionError> {
        if self.reconstruction_target != RECONSTRUCTION_TARGET {
            return Err(DecompositionError::UnsupportedReconstructionTarget {
                target: self.reconstruction_target.clone(),
            });
        }
        Ok(())
    }

    fn require_lossless(&self, report: &BinaryDecompositionReport) -> Result<(), DecompositionError> {
        if report.determined_component.is_none() {
            return Err(DecompositionError::NonLosslessBinarySplit {
                left: self.components[0],
                right: self.components[1],
            });
        }
        Ok(())
    }

    fn require_reconstruction(&self) -> Result<(), DecompositionError> {
        let [p0, p1] = self.components.map(|component| {
            project(&self.rows, self.schema.arity, component).map_err(schema_error)
        });
        let joined = natural_join(
            &p0?,
            &p1?,
            self.schema.arity,
            self.components,
        )
        .map_err(schema_error)?;
        let source = self.rows.iter().cloned().collect::<BTreeSet<_>>();
        if joined != source {
            return Err(DecompositionError::ReconstructionFailure {
                joined: joined.len(),
                source_len: source.len(),
            });
        }
        Ok(())
    }
}

pub fn lossless_ab_ac(rows: Vec<Vec<String>>) -> DeclaredSetDecomposition {
    DeclaredSetDecomposition {
        schema: FdSchema {
            arity: 3,
            dependencies: vec![FunctionalDependency {
                determinant: 1,
                dependent: 2,
            }],
        },
        components: [0b011, 0b101],
        reconstruction_target: RECONSTRUCTION_TARGET.to_string(),
        rows,
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

    fn sample_rows() -> Vec<Vec<String>> {
        vec![
            vec!["a".to_string(), "b".to_string(), "c".to_string()],
            vec!["d".to_string(), "e".to_string(), "c".to_string()],
        ]
    }

    #[test]
    fn unit_ab_ac_split_is_lossless_on_a_to_b() -> Result<(), String> {
        let decomposition = lossless_ab_ac(sample_rows());
        let report = decomposition
            .evaluate(1000)
            .map_err(|error| format!("{error:?}"))?;
        need(report.determined_component == Some(0), "component")?;
        need(decomposition.authority_effect() == AUTHORITY_EFFECT, "authority")?;
        Ok(())
    }

    #[test]
    fn integration_budget_token_drives_the_same_split() -> Result<(), String> {
        let decomposition = lossless_ab_ac(sample_rows());
        let direct = decomposition
            .evaluate(1000)
            .map_err(|error| format!("{error:?}"))?;
        let token = decomposition
            .evaluate_budget_token("1000")
            .map_err(|error| format!("{error:?}"))?;
        need(
            direct.determined_component == token.determined_component,
            "token",
        )?;
        Ok(())
    }

    #[test]
    fn e2e_reconstructed_instance_matches_source_rows() -> Result<(), String> {
        let decomposition = lossless_ab_ac(sample_rows());
        decomposition
            .evaluate(1000)
            .map_err(|error| format!("{error:?}"))?;
        need(ORIGIN.contains("sql_normal_form.rs"), "origin")?;
        need(CLAIM.contains("intersection closure"), "claim")?;
        Ok(())
    }

    #[test]
    fn negative_refuses_target_lossy_split_instance_and_float_budget() -> Result<(), String> {
        let mut bad_target = lossless_ab_ac(sample_rows());
        bad_target.reconstruction_target = "shadow".to_string();
        need(
            matches!(
                bad_target.evaluate(1000),
                Err(DecompositionError::UnsupportedReconstructionTarget { .. })
            ),
            "target",
        )?;
        let lossy = DeclaredSetDecomposition {
            schema: bad_target.schema.clone(),
            components: [0b011, 0b110],
            reconstruction_target: RECONSTRUCTION_TARGET.to_string(),
            rows: sample_rows(),
        };
        need(
            matches!(
                lossy.evaluate(1000),
                Err(DecompositionError::NonLosslessBinarySplit { .. })
            ),
            "lossy",
        )?;
        let violating = lossless_ab_ac(vec![
            vec!["a".to_string(), "b".to_string(), "c".to_string()],
            vec!["a".to_string(), "z".to_string(), "c".to_string()],
        ]);
        need(
            matches!(violating.evaluate(1000), Err(DecompositionError::Schema { .. })),
            "instance",
        )?;
        need(
            admit_exact_budget("1.0") == Err(DecompositionError::BinaryFloatRefused),
            "float",
        )?;
        need(
            admit_exact_budget("true") == Err(DecompositionError::BooleanAsNumber),
            "bool",
        )?;
        Ok(())
    }
}
