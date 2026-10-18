//! Deformation: Cooperads and cocomposition.
//!
//! AuthorityEffect: None.

use std::collections::{HashMap, HashSet};
use serde::{Deserialize, Serialize};
use crate::foundation::{OperadColour, Operation};

/// A multi-coloured cooperad C with cocomposition maps.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ColouredCooperad {
    pub name: String,
    colours: HashSet<OperadColour>,
    cognerators: HashMap<String, Operation>,
}

impl ColouredCooperad {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            colours: HashSet::new(),
            cognerators: HashMap::new(),
        }
    }

    pub fn add_cognerator(&mut self, op: Operation) {
        self.cognerators.insert(op.op_id.as_str().to_string(), op);
    }
}
