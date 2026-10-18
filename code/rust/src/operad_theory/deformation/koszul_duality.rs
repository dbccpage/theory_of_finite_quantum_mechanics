
use serde::{Deserialize, Serialize};
use crate::foundation::{Operation, OperationId, OperadSignature};
use super::quadratic_operad::QuadraticOperad;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProposedQuadraticDual {
    pub original_name: String,
    pub dual_operad: QuadraticOperad,
    pub is_pairing_computed: bool,
    pub notes: String,
}

pub struct KoszulDualBuilder;

impl KoszulDualBuilder {
    pub fn build_koszul_dual_skeleton(quad_op: &QuadraticOperad) -> Result<ProposedQuadraticDual, String> {
        let dual_name = format!("{}_KoszulDual", quad_op.name);
        let mut dual_op = QuadraticOperad::new(dual_name);

        for (gen_id, gen) in &quad_op.generators {
            let dual_id = OperationId::new(format!("{}_dual", gen_id))?;
            let dual_sig = OperadSignature::new(gen.inputs().to_vec(), gen.output().clone());
            let dual_gen = Operation {
                op_id: dual_id,
                signature: dual_sig,
                kind: crate::foundation::OperationKind::generator(),
                is_equivariant: gen.is_equivariant,
                description: format!("Koszul dual generator for {}", gen_id),
            };
            dual_op.add_generator(dual_gen);
        }

        Ok(ProposedQuadraticDual {
            original_name: quad_op.name.clone(),
            dual_operad: dual_op,
            is_pairing_computed: false,
            notes: "Dual generator skeleton constructed; full R_perp orthogonal complement not yet computed.".to_string(),
        })
    }
}
