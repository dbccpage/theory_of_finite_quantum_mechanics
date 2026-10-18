//! WDP retains declared headings, targets and instances; FD mathematics has its owner.
use omega_category_theory::finite_functional_dependencies::{
    natural_join, project, BinaryDecompositionReport, FdRefusal, FdSchema,
};
use std::collections::BTreeSet;

pub struct DeclaredSetDecomposition {
    pub schema: FdSchema,
    pub components: [u16; 2],
    pub reconstruction_target: String,
    pub rows: Vec<Vec<String>>,
}

impl DeclaredSetDecomposition {
    pub fn evaluate(&self, budget: u64) -> Result<BinaryDecompositionReport, String> {
        if self.reconstruction_target != "original_source_value" {
            return Err("UnsupportedReconstructionTarget".into());
        }
        let report = self
            .schema
            .binary_decomposition(self.components, budget)
            .map_err(|e| e.to_string())?;
        if report.determined_component.is_none() {
            return Err("NonLosslessBinarySplit".into());
        }
        self.schema
            .check_instance(&self.rows)
            .map_err(|e| e.to_string())?;
        let [p0, p1] = self
            .components
            .map(|c| project(&self.rows, self.schema.arity, c));
        let joined = natural_join(
            &p0.map_err(|e: FdRefusal| e.to_string())?,
            &p1.map_err(|e| e.to_string())?,
            self.schema.arity,
            self.components,
        )
        .map_err(|e| e.to_string())?;
        if joined != self.rows.iter().cloned().collect::<BTreeSet<_>>() {
            return Err("ReconstructionFailure".into());
        }
        Ok(report)
    }
}
