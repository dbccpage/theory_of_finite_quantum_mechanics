
use serde::{Deserialize, Serialize};
use super::colour::{OperadColour, OperadSignature};
use super::colored_operad::PlanarColoredOperad;
use super::operation::{Operation, OperationId};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MonoidalOperad {
    pub base: PlanarColoredOperad,
}

impl MonoidalOperad {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            base: PlanarColoredOperad::new(name, false),
        }
    }

    pub fn tensor_colours(&mut self, c1: &OperadColour, c2: &OperadColour) -> Result<OperadColour, String> {
        let tensor_name = format!("({}_x_{})", c1.as_str(), c2.as_str());
        let c = OperadColour::new(tensor_name)?;
        Ok(self.base.add_colour(c))
    }

    pub fn parallel_tensor_operations(&mut self, f: &Operation, g: &Operation) -> Result<Operation, String> {
        let mut combined_inputs = f.inputs().to_vec();
        combined_inputs.extend_from_slice(g.inputs());

        let combined_output = self.tensor_colours(f.output(), g.output())?;
        let tensor_id = OperationId::new(format!("({}_tensor_{})", f.op_id.as_str(), g.op_id.as_str()))?;

        let op = Operation {
            op_id: tensor_id,
            signature: OperadSignature::new(combined_inputs, combined_output),
            kind: super::operation::OperationKind::generator(),
            is_equivariant: f.is_equivariant && g.is_equivariant,
            description: format!("Parallel monoidal tensor of {} and {}", f.op_id.as_str(), g.op_id.as_str()),
        };
        self.base.add_operation(op.clone())?;
        Ok(op)
    }
}
