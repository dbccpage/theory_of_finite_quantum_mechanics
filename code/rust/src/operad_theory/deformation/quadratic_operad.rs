//! Deformation: Quadratic Operads and Relations.
//!
//! AuthorityEffect: None.

use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use crate::foundation::Operation;

/// A weight-two relation in Free(E)(2) expressing an algebraic identity.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuadraticRelation {
    pub relation_id: String,
    pub generating_terms: Vec<String>,
    pub coefficients: Vec<i64>,
    pub description: String,
}

/// A quadratic operad P presented by generators E and quadratic relations R.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuadraticOperad {
    pub name: String,
    pub generators: HashMap<String, Operation>,
    pub relations: Vec<QuadraticRelation>,
}

impl QuadraticOperad {
    pub fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            generators: HashMap::new(),
            relations: Vec::new(),
        }
    }

    pub fn add_generator(&mut self, op: Operation) {
        self.generators.insert(op.op_id.as_str().to_string(), op);
    }

    pub fn add_relation(&mut self, rel: QuadraticRelation) {
        self.relations.push(rel);
    }
}
