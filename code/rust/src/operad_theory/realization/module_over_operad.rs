
use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use crate::foundation::{Operation, OperationId, OperadSignature, PlanarColoredOperad};
use super::algebra_over_operad::OperadAlgebra;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OperadicModule {
    pub operad: PlanarColoredOperad,
    pub name: String,
    elements: HashMap<String, Operation>,
}

impl OperadicModule {
    pub fn new(operad: PlanarColoredOperad, name: impl Into<String>) -> Self {
        Self {
            operad,
            name: name.into(),
            elements: HashMap::new(),
        }
    }

    pub fn add_element(&mut self, elem: Operation) {
        self.elements.insert(elem.op_id.as_str().to_string(), elem);
    }

    pub fn right_action(&self, m: &Operation, f: &Operation, i: usize) -> Result<Operation, String> {
        if i >= m.arity() {
            return Err(format!("Insertion index i={} out of range for module element of arity {}", i, m.arity()));
        }

        if f.output() != &m.inputs()[i] {
            return Err(format!(
                "Module action ill-typed: {} expects {} at slot {}, but {} outputs {}",
                m.op_id.as_str(),
                m.inputs()[i].as_str(),
                i,
                f.op_id.as_str(),
                f.output().as_str()
            ));
        }

        let mut new_inputs = m.inputs()[..i].to_vec();
        new_inputs.extend_from_slice(f.inputs());
        new_inputs.extend_from_slice(&m.inputs()[i + 1..]);

        let new_id = OperationId::new(format!("({}_mod_o_{}_{})", m.op_id.as_str(), i, f.op_id.as_str()))?;

        Ok(Operation {
            op_id: new_id,
            signature: OperadSignature::new(new_inputs, m.output().clone()),
            kind: crate::foundation::OperationKind::generator(),
            is_equivariant: m.is_equivariant && f.is_equivariant,
            description: format!("Right operadic module action of {} on {} at slot {}", f.op_id.as_str(), m.op_id.as_str(), i),
        })
    }
}

#[derive(Clone)]
pub struct AlgebraModule {
    pub algebra: OperadAlgebra,
    pub name: String,
}

impl AlgebraModule {
    pub fn new(algebra: OperadAlgebra, name: impl Into<String>) -> Self {
        Self {
            algebra,
            name: name.into(),
        }
    }
}
