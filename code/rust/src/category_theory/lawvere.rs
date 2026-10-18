//! Lawvere Theory — Spec Section 25.
//!
//! A Lawvere theory is a Cauchy-complete monoid in Prof.
//! Operations are profunctor elements, substitution is composition,
//! and equations are 2-cells.

use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OperationDecl {
    pub name: String,
    pub input_sorts: Vec<String>,
    pub output_sorts: Vec<String>,
}

impl OperationDecl {
    pub fn new(name: &str, input_sorts: Vec<String>, output_sorts: Vec<String>) -> Self {
        Self {
            name: name.into(),
            input_sorts,
            output_sorts,
        }
    }

    pub fn arity(&self) -> usize {
        self.input_sorts.len()
    }

    pub fn coarity(&self) -> usize {
        self.output_sorts.len()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EquationDecl {
    pub name: String,
    pub lhs: String,
    pub rhs: String,
}

impl EquationDecl {
    pub fn new(name: &str, lhs: &str, rhs: &str) -> Self {
        Self {
            name: name.into(),
            lhs: lhs.into(),
            rhs: rhs.into(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TheoryCauchyStatus {
    Complete,
    Incomplete { unsplit_operations: Vec<String> },
}

#[derive(Debug, Clone)]
pub struct LawvereTheory {
    pub name: String,
    pub sorts: Vec<String>,
    pub operations: Vec<OperationDecl>,
    pub equations: Vec<EquationDecl>,
    pub substitution_table: BTreeMap<(String, usize, String), String>,
    pub identities: BTreeMap<String, String>, // sort -> identity operation
    pub cauchy_status: TheoryCauchyStatus,
}

impl LawvereTheory {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.into(),
            sorts: Vec::new(),
            operations: Vec::new(),
            equations: Vec::new(),
            substitution_table: BTreeMap::new(),
            identities: BTreeMap::new(),
            cauchy_status: TheoryCauchyStatus::Complete,
        }
    }

    pub fn add_sort(&mut self, sort: &str) {
        self.sorts.push(sort.into());
    }
    pub fn add_operation(&mut self, op: OperationDecl) {
        self.operations.push(op);
    }
    pub fn add_equation(&mut self, eq: EquationDecl) {
        self.equations.push(eq);
    }

    pub fn add_substitution(&mut self, outer: &str, slot: usize, inner: &str, result: &str) {
        self.substitution_table
            .insert((outer.into(), slot, inner.into()), result.into());
    }

    pub fn substitute(&self, outer: &str, slot: usize, inner: &str) -> Option<&str> {
        self.substitution_table
            .get(&(outer.into(), slot, inner.into()))
            .map(|s| s.as_str())
    }

    pub fn operations_of_arity(&self, arity: usize) -> Vec<&OperationDecl> {
        self.operations
            .iter()
            .filter(|op| op.arity() == arity)
            .collect()
    }
}

pub fn check_substitution_associativity(
    theory: &LawvereTheory,
    cases: &[(&str, usize, &str, usize, &str)],
) -> Vec<String> {
    let mut violations = Vec::new();
    for &(f, i, g, j, h) in cases {
        let left = theory
            .substitute(g, j, h)
            .and_then(|gh| theory.substitute(f, i, gh));
        let right = theory
            .substitute(f, i, g)
            .and_then(|fg| theory.substitute(fg, i + j, h));
        match (left, right) {
            (Some(l), Some(r)) if l == r => {}
            (Some(l), Some(r)) => violations.push(format!(
                "Substitution not associative: f={}, g={}, h={}: {}≠{}",
                f, g, h, l, r
            )),
            _ => violations.push(format!(
                "Substitution not defined for f={}, g={}, h={}",
                f, g, h
            )),
        }
    }
    violations
}

pub fn check_theory_cauchy(theory: &LawvereTheory) -> TheoryCauchyStatus {
    let mut unsplit = Vec::new();
    for op in &theory.operations {
        if op.arity() != 1 || op.coarity() != 1 {
            continue;
        }
        let is_idempotent = theory
            .substitute(&op.name, 0, &op.name)
            .map(|r| r == op.name)
            .unwrap_or(false);
        if !is_idempotent {
            continue;
        }
        // Search for splitting pair
        let splits = theory.operations.iter().any(|r_op| {
            theory.operations.iter().any(|s_op| {
                let sr_is_e = theory
                    .substitute(&s_op.name, 0, &r_op.name)
                    .map(|v| v == op.name)
                    .unwrap_or(false);

                let rs_is_id = theory
                    .substitute(&r_op.name, 0, &s_op.name)
                    .map(|v| {
                        r_op.output_sorts
                            .first()
                            .and_then(|sort| theory.identities.get(sort))
                            .map(|id| id == v)
                            .unwrap_or(false)
                    })
                    .unwrap_or(false);

                sr_is_e && rs_is_id
            })
        });
        if !splits {
            unsplit.push(op.name.clone());
        }
    }
    if unsplit.is_empty() {
        TheoryCauchyStatus::Complete
    } else {
        TheoryCauchyStatus::Incomplete {
            unsplit_operations: unsplit,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn monoid_theory() {
        let mut t = LawvereTheory::new("Monoid");
        t.add_sort("M");
        t.add_operation(OperationDecl::new(
            "mul",
            vec!["M".into(), "M".into()],
            vec!["M".into()],
        ));
        t.add_operation(OperationDecl::new("unit", vec![], vec!["M".into()]));
        t.add_equation(EquationDecl::new(
            "assoc",
            "mul(mul(x,y),z)",
            "mul(x,mul(y,z))",
        ));
        assert_eq!(t.operations.len(), 2);
        assert_eq!(t.equations.len(), 1);
    }

    #[test]
    fn trivial_theory_cauchy() {
        let t = LawvereTheory::new("Empty");
        assert_eq!(check_theory_cauchy(&t), TheoryCauchyStatus::Complete);
    }
}
