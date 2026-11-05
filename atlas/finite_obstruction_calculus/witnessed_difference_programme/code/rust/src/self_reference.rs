// Executable finite evidence; AuthorityEffect: None.
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct SelfReferenceWitness {
    pub index: usize,
    pub fixed_point: bool,
    pub authority_effect: String,
}

pub fn evaluate_diagonal_fixed_point(
    table: &[Vec<bool>],
) -> Option<SelfReferenceWitness> {
    for (i, row) in table.iter().enumerate() {
        if i < row.len() && row[i] {
            return Some(SelfReferenceWitness {
                index: i,
                fixed_point: true,
                authority_effect: "None".into(),
            });
        }
    }
    None
}
